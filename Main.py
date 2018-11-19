import re
from EloPredictor import EloPredictor as EP
from Game import Game
from Team import Team


def remove_rank(string):
    regex = r"\(\d*\)\s"
    return re.sub(regex, "", string, 0, re.MULTILINE)


def print_teams(teams_list):
    for idx, team in enumerate(sorted(teams_list, key=lambda t: t.ELO, reverse=True)):
        print(f"{idx + 1}, {team}")
    print("")


def print_teams_csv(teams_list):
    for idx, team in enumerate(sorted(teams_list, key=lambda t: t.ELO, reverse=True)):
        print(f"{team.name},{team.ELO}")
    print("")


def load_data(file_name, game_list, team_dict):
    # Load data from file into structure
    f = open(file_name)
    data_line = f.readline()
    while data_line != '':
        data = data_line.split(',')
        # -- READ DATA --
        # Clear date, idk maybe we'll keep it eventually
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
        if winner not in team_dict.keys():
            team_dict[winner] = Team(winner)
        if loser not in team_dict.keys():
            team_dict[loser] = Team(loser)

        # Create a match object
        match = Game(team_dict[winner], team_dict[loser])
        match.win_score = win_score
        match.lose_score = lose_score
        match.home_win = home_win
        game_list.append(match)

        # Add wins and losses to the relevant teams
        team_dict[winner].add_win(match)
        team_dict[loser].add_loss(match)

        data_line = f.readline()
    f.close()


file_name = "data.txt"
teams = {}
games = []

# Load Data
load_data(file_name, team_dict=teams, game_list=games)

# Filter Data
teams = {k: v for k, v in teams.items() if v.get_num_games() > 8}
games = [g for g in games if
         g.get_teams()[0] in teams.values() and g.get_teams()[1] in teams.values()]

# Update ELO using every FBS v. FBS match-up
ep = EP(games)
ep.rank_regress_rank(games, teams)

print_teams_csv(teams.values())
ep.get_performance_info()

# from ParamOptimizer import ParamOptimizer as PO
# PO.optimize_regression_factor(games, teams)
