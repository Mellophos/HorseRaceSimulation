# Path: horse-racing-sim/data_types.py
"""Define shared enums and constants used throughout the simulation.

This module contains the common data types used to describe race conditions,
horse aptitudes, racing strategies, and other simulation concepts.
"""
from enum import Enum, auto

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASHIN = 2.5
COURSE_WIDTH = 11.25
HORSE_LANE = COURSE_WIDTH / 18


# ---------------------------------------------------------------------------
# Horse
# ---------------------------------------------------------------------------

class Grade(Enum):
    G = 1
    F = 2
    E = 3
    D = 4
    C = 5
    B = 6
    A = 7
    S = 8


class Strategy(Enum):
    # RUNAWAY = 0 # UNCOMMENT ONLY WHEN READY
    FRONT = 1
    PACE = 2
    LATE = 3
    END = 4


class Mood(Enum):
    AWFUL = auto()
    BAD = auto()
    NORMAL = auto()
    GOOD = auto()
    GREAT = auto()


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class Surface(Enum):
    TURF = auto()
    DIRT = auto()
    # ARTIFICIAL = auto() # UNCOMMENT ONLY WHEN READY


class GroundCondition(Enum):
    FIRM = auto()
    GOOD = auto()
    SOFT = auto()
    HEAVY = auto()


class DistanceCategory(Enum):
    SPRINT = auto()
    MILE = auto()
    INTERMEDIATE = auto()
    LONG = auto()
    EXTENDED = auto()


# ---------------------------------------------------------------------------
# Race
# ---------------------------------------------------------------------------

class RacePhase(Enum):
    EARLY = 0
    MID = 1
    LATE = 2
    FINAL = 3


class PositionKeepMode(Enum):
    NORMAL = 0
    SPEED_UP = 1
    OVERTAKE = 2
    PACE_UP = 3
    PACE_DOWN = 4
    PACE_UP_EX = 5
