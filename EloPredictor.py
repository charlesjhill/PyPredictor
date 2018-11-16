from math import log


class EloPredictor:
    hta_adjustment = 2.5

    @staticmethod
    def update_teams_elo(g):
        def get_update_fact(elo_w, elo_l, marg, k_fact):
            init_fact = k_fact * log(marg + 1)
            mov_mult = 2.2 / ((elo_w - elo_l) * 0.001 + 2.2)
            return init_fact * mov_mult

        if g.winner.get_num_games() > 2:
            k = 20
        else:
            k = 32
        adjustment_factor = get_update_fact(g.winner.ELO, g.loser.ELO, g.get_margin(), k)
        g.winner.ELO += adjustment_factor
        g.loser.ELO -= adjustment_factor

    @staticmethod
    def get_exp_margin(g):
        exp_margin = (g.winner.ELO - g.loser.ELO) / 25
        if g.home_win:
            exp_margin += EloPredictor.hta_adjustment
        else:
            exp_margin -= EloPredictor.hta_adjustment
        return exp_margin

    @staticmethod
    def get_exp_prob_winning(g):
        return 1 / (pow(10, ((g.loser.ELO - g.winner.ELO) / 400)) + 1)
