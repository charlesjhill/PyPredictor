from math import pow, log
import re

# This is the adjustment factor as used by 538

# This should be "average." Good starting point
Default_Rating = 1500
# Home Team Advantage - S&P+ uses 2.5. 538 uses 2.6 for the NFL.
hta_adjustment = 2.5


class Team:
    def __init__(self, name):
        self.name = name
        self.conf = ""
        self.numWins = 0
        self.numLosses = 0
        self.ELO = Default_Rating

    def add_win(self):
        self.numWins += 1

    def add_loss(self):
        self.numLosses += 1

    def get_num_games(self):
        return self.numWins + self.numLosses


class Game:
    def __init__(self, winTeam, loseTeam):  # where winner and loser are Team objects
        self.winner = winTeam
        self.win_score = 0
        self.loser = loseTeam
        self.lose_score = 0
        self.home_win = True

    def get_margin(self):
        return self.win_score - self.lose_score

    def get_exp_margin(self):
        exp_margin = (self.winner.ELO - self.loser.ELO) / 25
        if home_win:
            exp_margin += hta_adjustment
        else:
            exp_margin -= hta_adjustment
        return exp_margin

    def get_exp_prob_winning(self):
        return 1 / (pow(10, ((self.loser.ELO - self.winner.ELO)/400)) + 1)

    def update_teams(self):
        def get_update_fact(elo_w, elo_l, marg, k_fact):
            init_fact = k_fact * log(marg + 1)
            mov_mult = 2.2 / ((elo_w - elo_l) * 0.001 + 2.2)
            return init_fact * mov_mult

        if self.winner.get_num_games() > 2:
            k = 20
        else:
            k = 32
        adjustment_factor = get_update_fact(self.winner.ELO, self.loser.ELO, self.get_margin(), k)
        self.winner.ELO += adjustment_factor
        self.loser.ELO -= adjustment_factor


def remove_rank(string):
    regex = r"\(\d*\)\s"
    return re.sub(regex, "", string, 0, re.MULTILINE)


# Load data from file into structure
f = open('data.txt')
dataLine = f.readline()
games = []
teams = {}
while dataLine != '':
    data = dataLine.split(',')
    # -- READ DATA --
    # Clear date, idk maybe we'll keep it
    data.pop(0)  # Clear number
    data.pop(0)  # Clear week
    data.pop(0)  # Clear date
    data.pop(0)  # Clear time
    data.pop(0)  # Clear Day of week

    # Extract info
    winner = remove_rank(data[0])
    win_score = int(data[1])
    home_win = "@" not in data[2]
    loser = remove_rank(data[3])
    lose_score = int(data[4])

    # -- STORE DATA -- #
    # Create team objects if they don't exist
    if winner not in teams.keys():
        teams[winner] = Team(winner)
    if loser not in teams.keys():
        teams[loser] = Team(loser)

    # Add wins and losses to the relevant teams
    teams[winner].add_win()
    teams[loser].add_loss()

    # Create a match object
    match = Game(winTeam=teams[winner], loseTeam=teams[loser])
    match.win_score = win_score
    match.lose_score = lose_score
    match.home_win = home_win
    games.append(match)

    dataLine = f.readline()
f.close()

# Begin processing every match-up
for game in games:
    game.update_teams()

for idx, team in enumerate(sorted(teams.values(), key=lambda t: t.ELO, reverse=True)):
    print(f"{idx + 1}. {team.name} - {team.ELO}")
