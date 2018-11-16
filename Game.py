class Game:
    def __init__(self, win_team, lose_team):  # where winner and loser are Team objects
        self.winner = win_team
        self.win_score = 0
        self.loser = lose_team
        self.lose_score = 0
        self.home_win = True

    def get_margin(self):
        return self.win_score - self.lose_score

    def get_teams(self):
        return [self.winner, self.loser]
