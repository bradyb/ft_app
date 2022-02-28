# Defines the Team object to track the teams of the human players.
from stats import Stat
from typing import Dict

StatToPlayer = Dict[Stat, str]


class Team:
    def __init__(self, name: str, lineup: StatToPlayer, bench: StatToPlayer):
        self.name = name
        self.lineup = lineup
        self.bench = bench
        self.score = 0
