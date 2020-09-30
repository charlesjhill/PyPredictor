import pickle
import requests
import typing
from pathlib import Path

from .Game import Game
from .Team import Team

class Season:

    def __init__(self, year: str, max_week: str):
        self.teams: typing.Dict[int, Team] = {}
        self.matches: typing.Dict[int, Game] = {}
        self.year = year
        self.max_week = max_week
        self.process_data()

    @staticmethod
    def fetch_data(year='2019', week=None, seasonType='regular') -> typing.List[typing.Dict]:
        url = 'https://api.collegefootballdata.com/games'
        params = {'year': year, 'seasonType': seasonType}
        if week is not None:
            params['week'] = week

        response = requests.get(url=url, params=params)
        return response.json()

    def process_data(self):
        def get_file_paths(y, w) -> typing.Tuple[str, str]:
            return f'data/{y}-{w}-teams', f'data/{y}-{w}-matches'

        t_path, m_path = get_file_paths(self.year, self.max_week)
        if Path(t_path).is_file():
            with open(t_path, 'rb') as t_file:
                self.teams = pickle.load(t_file)
            with open(m_path, 'rb') as m_file:
                self.matches = pickle.load(m_file)
            return

        data = self.fetch_data(self.year)
        for match_obj in data:
            # First, extract the teams
            if (home_id := match_obj['home_id']) not in self.teams:
                self.add_team(home_id, match_obj['home_team'], match_obj['home_conference'])
            
            if (away_id := match_obj['away_id']) not in self.teams:
                self.add_team(away_id, match_obj['away_team'], match_obj['away_conference'])

            # Extract scores
            home_score = match_obj['home_points']
            away_score = match_obj['away_points']

            # Create a Game object
            game = Game.create_from_home_away(home_id, home_score, away_id, away_score, match_obj['id'])
            game.year = match_obj['season']
            game.week = match_obj['week']
            self.matches[game.id] = game

            # Record the Win/Loss for the teams
            self.teams[game.winner].add_win(game.id)
            self.teams[game.loser].add_loss(game.id)

        # Strip FBS-FCS games:
        self.teams = { k: v for (k, v) in self.teams.items() if v.conf is not None}
        self.matches = { k: v for (k, v) in self.matches.items() if all(t in self.teams for t in v.get_teams())}

        # Save our data
        m = self.get_matches()
        max_week = max(m, key=lambda g: g.week).week
        year = m[0].year

        new_t_path, new_m_path = get_file_paths(year, max_week)

        # TODO: Ensure data folder exists
        with open(new_t_path, 'wb') as out_t:
            pickle.dump(self.teams, out_t)
        
        with open(new_m_path, 'wb') as out_m:
            pickle.dump(self.matches, out_m)

    def add_team(self, id: int, name: str, conference: str):
        new_team = Team(name, id)
        new_team.conf = conference
        self.teams.setdefault(id, new_team)

    def get_teams(self, conference = None) -> typing.List[Team]:
        return list(self.teams.values()) if conference is None else \
            list(t for t in self.teams.values() if t.conf == conference)

    def get_team(self, id) -> Team:
        if id not in self.teams:
            raise KeyError('ID of team not found')
        return self.teams[id]

    def print_teams(self, conference = None) -> None:
        for idx, team in enumerate(sorted(self.get_teams(conference), key=lambda t: t.ELO, reverse=True)):
            print(f"{idx + 1}, {team}")
        print("")

    def get_matches(self, conference: str=None) -> typing.List[Game]:
        matches = list(self.matches.values())
        if conference is None:
            return matches
        else:
            return [m for m in matches if (conf := self.get_team(m.winner).conf) == self.get_team(m.loser).conf \
                and conf == conference]

    def get_match(self, id) -> Game:
        if id not in self.matches:
            raise KeyError('ID of match not found')
        return self.matches[id]

    def reset_team_elos(self) -> None:
        for t in self.teams.values():
            t.ELO = t.default_rating