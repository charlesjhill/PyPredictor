import typing
from math import log
from Models.Team import Team
from Models.Game import Game
from Models.Season import Season


class EloPredictor:
    hfa_adjustment =    3.7
    k_factor =          14
    mov_fact =          0.6  # TODO: Rename this to something else
    elo2pts_conv =      25
    bias_adjust =       5.94
    rating_scalar =     0.444
    regression_factor = 0.64

    def __init__(self, season: Season):
        self.season: Season = season

    def get_abs_error(self):
        g_list = self.season.get_matches()
        l = [abs(self.get_exp_margin(g) - g.get_margin()) for g in g_list]
        return sum(l) / len(l)

    def get_mse(self):
        g_list = self.season.get_matches()
        l = [pow(self.get_exp_margin(g) - g.get_margin(), 2) for g in g_list]
        return sum(l) / len(l)

    def get_bias(self):
        g_list = self.season.get_matches()
        l = [self.get_exp_margin(g) - g.get_margin() for g in g_list]
        return sum(l) / len(l)

    def get_pct_games_right(self):
        g_list = self.season.get_matches()
        l = [1 for g in g_list if self.get_exp_margin(g) > 0]
        return sum(l) / len(g_list)

    def get_performance_info(self):
        print(f"Abs Err: {self.get_abs_error()}")
        print(f"Bias: {self.get_bias()}")
        print(f"Pct. Correct: {self.get_pct_games_right()}")

    def update_teams_elo(self, conference):
        for g in self.season.get_matches(conference):
            winner = self.season.teams[g.winner]
            loser = self.season.teams[g.loser]

            mov_factor = log(g.get_margin() + 1)
            rating_adjustment = EloPredictor.mov_fact / ((winner.ELO - loser.ELO) * 0.001 + EloPredictor.mov_fact + 0.0001)
            k = EloPredictor.k_factor + EloPredictor.rating_scalar * log((abs(winner.ELO) + abs(loser.ELO)) / 2)

            adjustment = k * rating_adjustment * mov_factor
            winner.ELO = round(winner.ELO + adjustment)
            loser.ELO = round(loser.ELO - adjustment)

    def get_exp_margin(self, g: Game):
        winner = self.season.teams[g.winner]
        loser = self.season.teams[g.loser]

        exp_margin = float(winner.ELO - loser.ELO) / EloPredictor.elo2pts_conv
        if g.home_win:
            exp_margin += EloPredictor.hfa_adjustment
        else:
            exp_margin -= EloPredictor.hfa_adjustment
        return exp_margin + EloPredictor.bias_adjust

    @staticmethod
    def get_exp_prob_winning(g):
        return 1 / (pow(10, ((g.loser.ELO - g.winner.ELO) / 400)) + 1)

    def regress_elo(self):
        for t in self.season.get_teams():
            t.ELO = round((t.ELO - Team.default_rating) * EloPredictor.regression_factor + Team.default_rating)

    def rank_regress_rank(self, conference = None):
        self.update_teams_elo(conference)
        self.regress_elo()
        self.update_teams_elo(conference)