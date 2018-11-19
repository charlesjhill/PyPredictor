from EloPredictor import EloPredictor as EP
from Team import Team


class ParamOptimizer:

    @staticmethod
    def minimize_abs_err(g_list, t_dict):
        ep = EP(g_list)
        min_err = 100

        # Iterate over the FOUR!! parameters: e2p, hfa, k, MoV
        for mov_fact in [x / 10.0 for x in range(7, 31, 1)]: # 23 choices on [0.7, 3]
            EP.mov_fact = mov_fact
            for k_fact in range(10, 41):  # 30 choices on [10, 40]
                EP.k_factor = k_fact

                # reset team rankings
                for v in t_dict.values():
                    v.ELO = Team.default_rating
                # RRR:
                EP.rank_regress_rank(g_list, t_dict)

                # Check different hfa-values to minimize error
                for e2p in [x / 10.0 for x in range(200, 300, 2)]: # 50 choices on [20, 30]
                    EP.elo2pts_conv = e2p
                    for hfa_adj in [x / 10.0 for x in range(0, 51, 1)]:  # 50 choices on [0, 5]
                        EP.hfa_adjustment = hfa_adj
                        calc_err = ep.get_abs_error()
                        if calc_err < min_err:
                            min_err = calc_err
                            min_mov = mov_fact
                            min_k = k_fact
                            min_e2p = e2p
                            min_hfa = hfa_adj

            print(f"Current best: {min_err} with {min_e2p} elo / pt, {min_hfa} hfa, {min_mov} MoV, and {min_k} K ")

        print(f"Lowest error: {min_err}")
        print(f"Elo2pts fact: {min_e2p}")
        print(f"HFA adjustmnet: {min_hfa}")
        print(f"K Factor: {min_k}")
        print(f"MoV Factor: {min_mov}")

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
                EP.rank_regress_rank(g_list, t_dict)

                # Check different hfa-values to minimize error
                for hfa_adj in [x / 10.0 for x in range(0, 51, 1)]:  # 0 to 50
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

    @staticmethod
    def optimize(g_list, t_dict):
        ep = EP(g_list)
        min_err = 100

        # Iterate over the four parameters: k_factor and hta
        for mov_fact in [x / 10.0 for x in range(7, 41, 1)]:  # 5 to 40
            EP.mov_fact = mov_fact
            for k_fact in range(10, 41):  # 10 to 40
                EP.k_factor = k_fact
                # reset team rankings
                for v in t_dict.values():
                    v.ELO = Team.default_rating

                # RRR:
                EP.rank_regress_rank(g_list, t_dict)

                # Check different hfa-values to minimize error
                for hfa_adj in [x / 10.0 for x in range(0, 51, 1)]:  # 0 to 50
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

    @staticmethod
    def optimize_rating_scalar(g_list, t_dict):
        ep = EP(g_list)
        min_err = 100

        for k in [x for x in range(10, 41)]:
            EP.k_factor = k

            for rs in [x / 10000.0 for x in range(-10000, 1, 1)]: # 10001 values on [-1, 1] in steps of 1/10000
                EP.rating_scalar = rs
                # Reset rankings
                for v in t_dict.values():
                    v.ELO = Team.default_rating

                # Rank
                for g in g_list:
                    EP.update_teams_elo(g)

                # Regress
                for t in t_dict.values():
                    EP.regress_elo(t)

                # Rank
                for g in g_list:
                    EP.update_teams_elo(g)

                err = ep.get_abs_error()
                if err < min_err:
                    min_err = err
                    min_rs = rs
                    min_k = k
            print(f"Current best: {min_err} w/ K = {min_k} & RS = {min_rs}")

        print("With fixed ELO2PTS, MoV, and HFA values...")
        print(f"Lowest error: {min_err}")
        print(f"RS value: {min_rs}")
        print(f"K value: {min_k}s")

    @staticmethod
    def optimize_regression_factor(g_list, t_dict):
        ep = EP(g_list)
        min_err = 100

        for rf in [x / 10.0 for x in range(10, 1001, 1)]:
            EP.regression_factor = rf
            # Reset rankings
            for v in t_dict.values():
                v.ELO = Team.default_rating

            # Rank
            for g in g_list:
                EP.update_teams_elo(g)

            # Regress
            for t in t_dict.values():
                EP.regress_elo(t)

            # Rank
            for g in g_list:
                EP.update_teams_elo(g)

            err = ep.get_abs_error()
            if err < min_err:
                min_err = err
                min_rf = rf

        print("With fixed everything but Regression amount...")
        print(f"Lowest error: {min_err}")
        print(f"RF value: {min_rf}")