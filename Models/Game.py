import typing
from .Team import Team

class Game:

    @staticmethod
    def create_from_home_away(home_id, home_score, away_id, away_score, game_id=0):
        if home_score > away_score:
            new_game = Game(home_id, away_id, game_id)
            new_game.win_score = home_score
            new_game.lose_score = away_score
            return new_game
        else:
            new_game = Game(away_id, home_id, game_id)
            new_game.win_score = away_score
            new_game.lose_score = home_score
            new_game.home_win = False
            return new_game

    def __init__(self, winner_id: int, loser_id: int, id=0):  # where winner and loser are Team objects
        self.id = id
        self.winner: int = winner_id
        self.win_score = 0
        self.loser: int = loser_id
        self.lose_score = 0
        self.home_win = True
        self.year = 2000
        self.week = 0

    def get_margin(self) -> int:
        return self.win_score - self.lose_score

    def get_teams(self) -> typing.Tuple[int, int]:
        return (self.winner, self.loser)

    def __repr__(self):
        return f"Game({self.winner}, {self.loser})"

    def __str__(self):
        return f"{self.winner} {self.win_score} - {self.loser} {self.lose_score}"
