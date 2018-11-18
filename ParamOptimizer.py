from EloPredictor import EloPredictor as EP


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
    def minimize_abs_err_no_bias(g_list):
        min_err = 100
        min_e2p = 15
        min_hfa = 0

        # Iterate over the two parameters: e2p and hta
        EP.bias_adjust = 0
        for ep_fact in [x / 10.0 for x in range(100, 401, 1)]:  # 15 to 35 (larger values interprets
            EP.elo2pts_conv = ep_fact
            for hta_adj in [x / 10.0 for x in range(0, 101, 1)]:  # 0 to 10
                EP.hfa_adjustment = hta_adj
                calc_err = EP.get_abs_error(g_list)
                if calc_err < min_err:
                    min_err = calc_err
                    min_e2p = ep_fact
                    min_hfa = hta_adj

            print(f"Current best: {min_err} with {min_e2p} elo / pt, {min_hfa} hta")

        print(f"Lowest error: {min_err}")  # 11.3201 | 11.3202
        print(f"Elo2pts fact: {min_e2p}")  # 26.1    | 26.0
        print(f"HTA adjustmnet: {min_hfa}")  # 3.7   | 3.6
