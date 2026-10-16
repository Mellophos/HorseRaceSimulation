# Path: horse-racing-sim/lookups\racing.py
# racing.py

from data_types import DistanceCategory, Surface, GroundCondition, \
    PositionKeepMode

# Used for categorising race distances
DISTANCE_CATEGORIES = {
    DistanceCategory.SPRINT: (1000, 1300),
    DistanceCategory.MILE: (1301, 1899),
    DistanceCategory.INTERMEDIATE: (1900, 2100),
    DistanceCategory.LONG: (2101, 2700),
    DistanceCategory.EXTENDED: (2701, 5000)
}

# Source: pg.6 [Ground modifier for speed]
# Flat value shifts applied to base speed based on the ground condition
SURFACE_SPEED_MODIFIERS = {
    Surface.TURF: {
        GroundCondition.FIRM: 0,
        GroundCondition.GOOD: 0,
        GroundCondition.SOFT: 0,
        GroundCondition.HEAVY: -50
    },
    Surface.DIRT: {
        GroundCondition.FIRM: 0,
        GroundCondition.GOOD: 0,
        GroundCondition.SOFT: 0,
        GroundCondition.HEAVY: -50
    }
}

# Source: pg.6 [Ground modifier for power]
# Flat value shifts applied to power based on the ground condition
SURFACE_POWER_MODIFIERS = {
    Surface.TURF: {
        GroundCondition.FIRM: 0,
        GroundCondition.GOOD: -50,
        GroundCondition.SOFT: -50,
        GroundCondition.HEAVY: -50
    },
    Surface.DIRT: {
        GroundCondition.FIRM: -100,
        GroundCondition.GOOD: -50,
        GroundCondition.SOFT: -100,
        GroundCondition.HEAVY: -100
    }
}

# Source: pg.25-27 [Position Keeping]
# Position Keeping modifiers applied to target speed calculation
POSITION_KEEP_MODIFIERS = {
    PositionKeepMode.NORMAL: 1.000,
    PositionKeepMode.SPEED_UP: 1.040,
    PositionKeepMode.OVERTAKE: 1.050,
    PositionKeepMode.PACE_UP: 1.040,
    PositionKeepMode.PACE_DOWN: (0.945, 0.915),
    PositionKeepMode.PACE_UP_EX: 2.000
}
