# Path: horse-racing-sim/simulation\mechanics\hp.py
# hp.py
from horse import RaceEntry
from lookups import STRATEGY_HP_MULTIPLIERS


def calculate_max_hp(race_entry: RaceEntry, distance: int):
    strat_coef = STRATEGY_HP_MULTIPLIERS[race_entry.strategy]
    return 0.8 * strat_coef * race_entry.horse.stats.stamina + distance
