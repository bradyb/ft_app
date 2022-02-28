# Tournament information.
from typing import List

from teams import Team


class Tournament:
    def __inti__(self, teams: List[Team]):
        self.teams = teams
