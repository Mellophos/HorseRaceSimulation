# Path: horse-racing-sim/lookups\stats.py

from data_types import Mood, Grade, Strategy

# Source: pg.5 [Base Stats]
# Float scalars applied to overall stats based on current mood
MOOD_MULTIPLIERS = {
    Mood.AWFUL: 0.96,
    Mood.BAD: 0.98,
    Mood.NORMAL: 1.0,
    Mood.GOOD: 1.02,
    Mood.GREAT: 1.04
}

# Source: pg.6 [Strategy Proficiency Modifier]
# Grade-based scaling multipliers applied to the Wit stat
GRADE_WIT_MULTIPLIERS = {
    Grade.S: 1.1,
    Grade.A: 1.0,
    Grade.B: 0.85,
    Grade.C: 0.75,
    Grade.D: 0.6,
    Grade.E: 0.4,
    Grade.F: 0.2,
    Grade.G: 0.1,
}

# Source: pg.8 [Distance Proficiency Modifier]
# Grade-based scaling multipliers for target speed calculations
GRADE_DISTANCE_MULTIPLIERS = {
    Grade.S: 1.05,
    Grade.A: 1.0,
    Grade.B: 0.9,
    Grade.C: 0.8,
    Grade.D: 0.6,
    Grade.E: 0.4,
    Grade.F: 0.2,
    Grade.G: 0.1,
}

# Source: pg.12 [Strategy Coefficient]
# Strategy-based scale modifiers applied to overall HP
STRATEGY_HP_MULTIPLIERS = {
    Strategy.FRONT: 0.95,
    Strategy.PACE: 0.89,
    Strategy.LATE: 1.0,
    Strategy.END: 0.995
}

# Source: pg.8 [Strategy Phase Modifier]
# Phase-by-phase scaling coefficients used for base target speed
STRATEGY_PHASE_MULTIPLIERS = {
    Strategy.FRONT: (1.000, 0.980, 0.962, 0.962),
    Strategy.PACE: (0.978, 0.991, 0.975, 0.975),
    Strategy.LATE: (0.938, 0.998, 0.994, 0.994),
    Strategy.END: (0.931, 1.000, 1.000, 1.000),
    # Strategy.RUNAWAY: (1.063, 0.962, 0.95, 0.95)
}
