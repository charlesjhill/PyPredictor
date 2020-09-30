import argparse
import sys

from EloPredictor import EloPredictor as EP
from ParamOptimizer import ParamOptimizer as PO
from Models.Game import Game
from Models.Team import Team
from Models.Season import Season

parser = argparse.ArgumentParser(description='Processing college football data')
parser.add_argument('-y', '--year', default='2019', help='The year of interest')
parser.add_argument('-m', '--max-week', default='15', help='The maximum week games should processed for')
parser.add_argument('-p', '--proportion', default=0.2, type=float, help='The proportion of matches which are for testing')
parser.add_argument('-c', '--conference', help='The conference to focus on')
arguments = parser.parse_args()

season = Season(arguments.year, arguments.max_week)

# Update ELO using every FBS v. FBS match-up
ep = EP(season)

ep.rank_regress_rank(arguments.conference)
season.print_teams(arguments.conference)
ep.get_performance_info()


# PO.minimize_abs_err_no_bias(season)
# PO.optimize_rating_scalar(season)
# PO.optimize_regression_factor(season)