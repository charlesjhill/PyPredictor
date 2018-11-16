import re
from EloPredictor import EloPredictor
from Game import Game
from Team import Team


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

# Begin processing every match-up

for game in games:
    EloPredictor.update_teams_elo(game)

for idx, team in enumerate(sorted(teams.values(), key=lambda t: t.ELO, reverse=True)):
    print(f"{idx + 1}. {team.name} - {team.ELO}")
