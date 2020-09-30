import typing

class Team:
    default_rating = 1500

    def __init__(self, name: str, id=0):
        self.name = name
        self.id = id
        self.conf = ""
        self.num_wins = 0
        self.num_losses = 0
        self.ELO = Team.default_rating  # Default ELO Rating
        self.matches: typing.List[int] = []  # Maybe make these sets?
        self.wins: typing.List[int] = []
        self.losses: typing.List[int] = []

    def __str__(self):
        return f"{self.name} ({self.num_wins}-{self.num_losses}) - {self.ELO}"

    def __repr__(self):
        return f"Team({self.name})"

    def add_win(self, match_id: int) -> None:
        self.num_wins += 1
        self.matches.append(match_id)
        self.wins.append(match_id)

    def add_loss(self, match_id: int) -> None:
        self.num_losses += 1
        self.matches.append(match_id)
        self.losses.append(match_id)

    def get_num_games(self) -> int:
        return self.num_wins + self.num_losses
