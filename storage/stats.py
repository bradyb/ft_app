# Stat objects for tennis players.
from abc import ABC, abstractmethod
from enum import Enum

POSITION_KEY = "position"


class Position(Enum):
    SERVE = 1
    POWER = 2
    DEFENSE = 3
    RETURN = 4
    MIND = 5


class Stat(Enum):
    ACES = 1
    DOUBLE_FAULTS = 2
    WINNERS = 3
    UNFORCED_ERRORS = 4
    SECOND_SERVES_WON_PCT = 5
    RETURNING_POINTS_WON_PCT = 6
    BREAK_POINTS_WON = 7
    BREAK_POINTS_SAVED = 8
    BREAK_POINTS_LOST = 9


class MatchStat(ABC):
    def __init__(self, position: Position):
        self.position = position

    @abstractmethod
    def compute_score(self):
        pass


class ServeMatchStat(MatchStat):
    def __init__(self, aces: int, double_faults: int):
        super().__init__(Position.SERVE)
        self.aces = aces
        self.double_faults = double_faults

    def compute_score(self):
        return 3 * (self.aces - self.double_faults)

    def __iter__(self):
        yield (POSITION_KEY, Position.SERVE.name)
        yield (Stat.ACES.name, self.aces)
        yield (Stat.DOUBLE_FAULTS, self.double_faults)


class PowerMatchStat(MatchStat):
    def __init__(self, winners: int, unforced_errors: int):
        super().__init__(Position.POWER)
        self.winners = winners
        self.unforced_errors = unforced_errors

    def compute_score(self):
        return 2 * self.winners - self.unforced_errors

    def __iter__(self):
        yield (POSITION_KEY, Position.POWER.name)
        yield (Stat.WINNERS.name, self.winners)
        yield (Stat.UNFORCED_ERRORS, self.unforced_errors)


class DefenseMatchStat(MatchStat):
    def __init__(self, second_serves_won_pct: int):
        super().__init__(Position.DEFENSE)
        self.second_serves_won_pct = second_serves_won_pct

    def compute_score(self):
        return self.second_serves_won_pct

    def __iter__(self):
        yield (POSITION_KEY, Position.DEFENSE.name)
        yield (Stat.SECOND_SERVES_WON_PCT.name, self.second_serves_won_pct)


class ReturnMatchStat(MatchStat):
    def __init__(self, returning_points_won_pct: int):
        super().__init__(Position.RETURN)
        self.returning_points_won_pct = returning_points_won_pct

    def compute_score(self):
        return self.returning_points_won_pct

    def __iter__(self):
        yield (POSITION_KEY, Position.RETURN.name)
        yield (Stat.RETURNING_POINTS_WON_PCT.name, self.returning_points_won_pct)


class MindMatchStat(MatchStat):
    def __init__(
        self, break_points_won: int, break_points_saved: int, break_points_lost: int
    ):
        super().__init__(Position.MIND)
        self.break_points_won = break_points_won
        self.break_points_saved = break_points_saved
        self.break_points_lost = break_points_lost

    def compute_score(self):
        return (
            5 * (self.break_points_won + self.break_points_saved)
            - 3 * self.break_points_lost
        )

    def __iter__(self):
        yield (POSITION_KEY, Position.MIND.name)
        yield (Stat.BREAK_POINTS_WON.name, self.break_points_won)
        yield (Stat.BREAK_POINTS_SAVED, self.break_points_saved)
        yield (Stat.BREAK_POINTS_LOST, self.break_points_lost)
