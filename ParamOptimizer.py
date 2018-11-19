from EloPredictor import EloPredictor as EP
from Team import Team


class ParamOptimizer:

    @staticmethod
    def minimize_abs_err(g_list):
        min_err = 100
        min_e2p = 15
        min_hta = 0
        min_bias_adj = 0

        # Iterate over the three parameters:
        for ep_fact in [x / 10.0 for x in range(200, 401, 1)]:  # 15 to 35 (larger values interprets
            EP.elo2pts_conv = ep_fact
            for hta_adj in [x / 10.0 for x in range(0, 51, 1)]:  # 0 to 10
                EP.hfa_adjustment = hta_adj
                for bias_adj in [x / 10.0 for x in range(0, 71, 1)]:  # -10 to 10
                    EP.bias_adjust = bias_adj

                    calc_err = EP.get_abs_error(g_list)
                    if calc_err < min_err:
                        min_err = calc_err
                        min_e2p = ep_fact
                        min_hta = hta_adj
                        min_bias_adj = bias_adj
            print(f"Current best: {min_err} with {min_e2p} elo / pt, {min_hta} hta, and {min_bias_adj} flat adjust")

        print(f"Lowest error: {min_err}")  # 9.07843
        print(f"Elo2pts fact: {min_e2p}")  # 43.3
        print(f"HTA adjustmnet: {min_hta}")  # 1.7
        print(f"Bias adjustment: {min_bias_adj}")  # 10.6

    @staticmethod
    def minimize_abs_err_no_bias(g_list, t_dict):
        ep = EP(g_list)
        min_err = 100

        # Iterate over the two parameters: k_factor and hta
        for mov_fact in [x / 10.0 for x in range(7, 41, 1)]: # 5 to 40
            EP.mov_fact = mov_fact
            for k_fact in range(10, 41):  # 10 to 40
                EP.k_factor = k_fact
                # reset team rankings
                for v in t_dict.values():
                    v.ELO = Team.default_rating

                # RRR:
                for g in g_list:
                    EP.update_teams_elo(g)
                for t in t_dict.values():
                    EP.regress_elo(t)
                for g in g_list:
                    EP.update_teams_elo(g)

                # Check different hfa-values to minimize error
                for hfa_adj in [x / 10.0 for x in range(0, 51, 1)]:  # 0 to 10
                    EP.hfa_adjustment = hfa_adj
                    calc_err = ep.get_abs_error()
                    if calc_err < min_err:
                        min_err = calc_err
                        min_k = k_fact
                        min_hfa = hfa_adj
                        min_mov = mov_fact

            print(f"Current best: {min_err} with {min_k} k factor, {min_hfa} hfa, {min_mov} MoV")

        print(f"With fixed elo-conversion-factor: {EP.elo2pts_conv} and bias adjustment {EP.bias_adjust}")
        print(f"Lowest error: {min_err}")
        print(f"K factor: {min_k}")
        print(f"HFA value: {min_hfa}")
        print(f"MoV value: {min_mov}")
