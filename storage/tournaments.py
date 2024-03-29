# Tournament information.
from typing import List

from teams import Team


class Tournament:
    def __init__(self, teams: List[Team]):
        self.teams = teams

    def __iter__(self):
        for team in self.teams.items():
            yield (team.name, dict(team))
