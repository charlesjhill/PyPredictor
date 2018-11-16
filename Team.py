class Team:
    default_rating = 1500

    def __init__(self, name):
        self.name = name
        self.conf = ""
        self.num_wins = 0
        self.num_losses = 0
        self.ELO = Team.default_rating  # Default ELO Rating
        self.matches = []
        self.wins = []
        self.losses = []

    def add_win(self, match_obj):
        self.num_wins += 1
        self.matches.append(match_obj)
        self.wins.append(match_obj)

    def add_loss(self, match_obj):
        self.num_losses += 1
        self.matches.append(match_obj)
        self.losses.append(match_obj)

    def get_num_games(self):
        return self.num_wins + self.num_losses

    def get_opponents(self):
        def get_other_team(lst):
            if lst[0] == self:
                return lst[1]
            return lst[0]

        return [get_other_team(l) for l in [m.get_teams() for m in self.matches]]
