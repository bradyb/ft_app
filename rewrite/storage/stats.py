# Stat objects for tennis players.
from enum import Enum


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
