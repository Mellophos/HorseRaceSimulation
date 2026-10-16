# Path: horse-racing-sim/simulation\mechanics\speed.py
import math

from data_types import Strategy, RacePhase, Grade, PositionKeepMode
from horse.state import HorseState
from lookups import STRATEGY_PHASE_MULTIPLIERS, GRADE_DISTANCE_MULTIPLIERS, \
    POSITION_KEEP_MODIFIERS
from race import Runner, Race
from utils import get_current_phase


def calculate_base_speed(distance: float) -> float:
    return 20 - (distance - 2000) / 1000


def calculate_minimum_speed(
        base_speed: float,
        guts_stat: float
) -> float:
    return 0.85 * base_speed + math.sqrt(200 * guts_stat) * 0.001


def calculate_base_target_speed(
        base_speed: float,
        strategy: Strategy,
        race_phase: RacePhase,
        speed_stat: float,
        distance_aptitude: Grade,
) -> float:
    strategy_phase_coef = STRATEGY_PHASE_MULTIPLIERS[strategy][
        race_phase.value]
    distance_prof_mod = GRADE_DISTANCE_MULTIPLIERS[distance_aptitude]

    if race_phase.value <= 1:
        return base_speed * strategy_phase_coef
    else:
        return (
                base_speed
                * strategy_phase_coef
                + math.sqrt(500 * speed_stat)
                * distance_prof_mod
                * 0.002
        )


def calculate_position_keep_coefficient(
        mode: PositionKeepMode,
        race_phase: RacePhase,
) -> float:
    position_keep_coef = POSITION_KEEP_MODIFIERS[mode]
    if mode is PositionKeepMode.PACE_DOWN:
        if race_phase is RacePhase.MID:
            return position_keep_coef[0]
        else:
            return position_keep_coef[1]
    return position_keep_coef


def calculate_target_speed(runner: Runner, race: Race) -> float:
    current_phase = get_current_phase(runner.state.position.distance,
                                      race.course.distance)
    base_speed = calculate_base_speed(race.course.distance)
    base_target_speed = calculate_base_target_speed(
        base_speed,
        runner.entry.strategy,
        current_phase,
        runner.entry.final_stats.speed,
        runner.entry.distance_aptitude
    )
    position_keep_coef = calculate_position_keep_coefficient(
        runner.state.position_keep.mode,
        current_phase
    )
    # [X] determine Phase
    # [X] calculate BaseSpeed
    # [X] calculate BaseTargetSpeed
    # [X] apply PositionKeepCoef
    # [ ] apply ForceInModifier
    # [ ] apply SlopeModifier
    # [ ] apply MoveLaneModifier
    # [ ] clamp result (MinimumSpeed <= TargetSpeed <= 30)
    pass


def calculate_acceleration():
    pass


def update_current_speed(horse_state: HorseState, acceleration: float,
                         duration: float):
    horse_state.movement.current_speed += acceleration * duration


if __name__ == "__main__":
    base_speed = calculate_base_speed(5000)
    minimum_speed = calculate_minimum_speed(base_speed, 100)
    base_target_speed = calculate_base_target_speed(
        base_speed,
        Strategy.END,
        RacePhase.LATE,
        1200,
        Grade.G
    )
    pos_keep_coef = calculate_position_keep_coefficient(
        PositionKeepMode.PACE_DOWN, RacePhase.MID)

    print(
        f'MinimumSpeed: {minimum_speed}\n'
        f'BaseSpeed: {base_speed}\n'
        f'BaseTargetSpeed: {base_target_speed}\n'
        f'PositionKeepCoef: {pos_keep_coef}\n'
    )
