# Defines the Team object to track the teams of the human players.
from datetime import date
from stats import Position, MatchStat
from typing import Dict

PlayerToPosition = Dict[str, Position]
PositionToMatchStat = Dict[Position, MatchStat]


class Team:
    def __init__(
        self, name: str, lineup: PlayerToPosition, bench: PlayerToPosition
    ) -> None:
        self.name = name
        self.lineup = lineup
        self.bench = bench
        self.score = 0
        self._init_player_to_date_to_match_stat()

    def _init_player_to_date_to_match_stat(self):
        self.player_to_date_to_match_stat = {}
        for player_name, _ in self.lineup.items():
            self.player_to_date_to_match_stat[player_name] = {}
        for player_name, _ in self.bench.items():
            self.player_to_date_to_match_stat[player_name] = {}

    def _has_player(self, name: str) -> None:
        return name in self.lineup or name in self.bench

    def _get_player_position(self, name: str):
        if name in self.lineup:
            return self.lineup[name]
        else:
            return self.bench[name]

    def update_player(self, match_date: date, name: str, match_stats: PositionToMatchStat):
        if not self._has_player(name):
            return
        position = self._get_player_position(name)
        self.player_to_date_to_match_stat[name][match_date] = match_stats[position]

    def move_to_lineup(self, name: str):
        # TODO: Add logic for moving a player from the bench to the lineup.
        pass

    def get_current_score(self):
        # TODO: How this is computed is dependent on how we represent/store
        # when someone is benched.
        pass