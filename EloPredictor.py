from math import log
from Team import Team


class EloPredictor:
    hfa_adjustment =    3.5
    k_factor =          16
    mov_fact =          0.7  # TODO: Rename this to something else
    elo2pts_conv =      25
    bias_adjust =       6.62
    rating_scalar =     0
    regression_factor = 1.6

    def __init__(self, games):
        self.games = games

    def get_abs_error(self):
        g_list = self.games
        l = [abs(EloPredictor.get_exp_margin(g) - g.get_margin()) for g in g_list]
        return sum(l) / len(l)

    def get_mse(self):
        g_list = self.games
        l = [pow(EloPredictor.get_exp_margin(g) - g.get_margin(), 2) for g in g_list]
        return sum(l) / len(l)

    def get_bias(self):
        g_list = self.games
        l = [EloPredictor.get_exp_margin(g) - g.get_margin() for g in g_list]
        return sum(l) / len(l)

    def get_pct_games_right(self):
        g_list = self.games
        l = [1 for g in g_list if EloPredictor.get_exp_margin(g) > 0]
        return sum(l) / len(g_list)

    def get_performance_info(self):
        print(f"Abs Err: {self.get_abs_error()}")
        print(f"Bias: {self.get_bias()}")
        print(f"Pct. Correct: {self.get_pct_games_right()}")

    @staticmethod
    def update_teams_elo(g):
        mov_factor = log(g.get_margin() + 1)
        rating_adjustment = EloPredictor.mov_fact / ((g.winner.ELO - g.loser.ELO) * 0.001 + EloPredictor.mov_fact)
        k = EloPredictor.k_factor + EloPredictor.rating_scalar * ((g.winner.ELO + g.loser.ELO) / 2)

        adjustment = k * rating_adjustment * mov_factor
        g.winner.ELO = round(g.winner.ELO + adjustment)
        g.loser.ELO = round(g.loser.ELO - adjustment)

    @staticmethod
    def get_exp_margin(g):
        exp_margin = (g.winner.ELO - g.loser.ELO) / EloPredictor.elo2pts_conv
        if g.home_win:
            exp_margin += EloPredictor.hfa_adjustment
        else:
            exp_margin -= EloPredictor.hfa_adjustment
        return exp_margin + EloPredictor.bias_adjust

    @staticmethod
    def get_exp_prob_winning(g):
        return 1 / (pow(10, ((g.loser.ELO - g.winner.ELO) / 400)) + 1)

    @staticmethod
    def regress_elo(t):
        t.ELO =  (t.ELO - Team.default_rating) / EloPredictor.regression_factor + Team.default_rating

    @staticmethod
    def rank_regress_rank(games, teams):
        for g in games:
            EloPredictor.update_teams_elo(g)
        for t in teams.values():
            EloPredictor.regress_elo(t)
        for g in games:
            EloPredictor.update_teams_elo(g)