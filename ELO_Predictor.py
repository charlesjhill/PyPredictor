import re
from EloPredictor import EloPredictor as EP
from Game import Game
from Team import Team
from ParamOptimizer import ParamOptimizer as PO


def remove_rank(string):
    regex = r"\(\d*\)\s"
    return re.sub(regex, "", string, 0, re.MULTILINE)


def print_teams(teams_list):
    for idx, team in enumerate(sorted(teams_list, key=lambda t: t.ELO, reverse=True)):
        print(f"{idx + 1}. {team}")


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

    # Create a match object
    match = Game(teams[winner], teams[loser])
    match.win_score = win_score
    match.lose_score = lose_score
    match.home_win = home_win
    games.append(match)

    # Add wins and losses to the relevant teams
    teams[winner].add_win(match)
    teams[loser].add_loss(match)

    dataLine = f.readline()
f.close()

# Filter list to remove teams with 1 or 2 games (FCS schools)
teams = {k: v for k, v in teams.items() if v.get_num_games() > 8}
games = [g for g in games if
         g.get_teams()[0] in teams.values() and g.get_teams()[1] in teams.values()]

# Update ELO using every FBS v. FBS match-up

ep = EP(games)
for game in games:
    ep.update_teams_elo(game)

print_teams(teams.values())

ep.get_performance_info()
