# Defines the Team object to track the teams of the human players.
from datetime import date
from stats import Position, Stat
from typing import Dict

PlayerToPosition = Dict[str, Position]
StatToValue = Dict[Stat, int]


class Team:
    def __init__(
        self, name: str, lineup: PlayerToPosition, bench: PlayerToPosition
    ) -> None:
        self.name = name
        self.lineup = lineup
        self.bench = bench
        self.score = 0

    def has_player(self, name: str) -> None:
        return name in self.lineup or name in self.bench

    def update_player(self, match_date: date, name: str, match_stats: StatToValue):
        if not self.has_player(name):
            return
        # TODO: Add logic for adding a match to this team.

    def move_to_lineup(self, name: str):
        # TODO: Add logic for moving a player from the bench to the lineup.
