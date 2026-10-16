# Path: horse-racing-sim/simulation\mechanics\position_keep\position_keep.py
import math
import random

import simulation.mechanics.position_keep.speed_up as speed_up
from data_types import PositionKeepMode
from race.race import Runner, Race
from utils import section_boundaries


def update_position_keep(
        runner: Runner,
        race: Race,
        current_frame: int,
        fps: int
) -> None:
    if not position_keep_active(
            runner.state.position.distance,
            race.course.distance
    ):
        if runner.state.position_keep.mode is not PositionKeepMode.NORMAL:
            update_pos_keep_state(
                runner, PositionKeepMode.NORMAL,
                None,
                None
            )
        return

    current_mode = runner.state.position_keep.mode
    next_check_frame = runner.state.position_keep.next_check_frame

    # Check to enter non-normal modes
    if current_mode is PositionKeepMode.NORMAL:
        if next_check_frame is not None and current_frame < next_check_frame:
            return

        # Check entry conditions for all modes
        # Every mode's condition should be mutually exclusive except for
        # PACE_UP_EX
        entry_conditions = get_entry_conditions(runner, race)

        # Wit check
        check = wit_check(runner.entry.final_stats.wit)
        if any(entry_conditions) and check:
            # Prioritise PACE_UP_EX if entry condition is True
            # if entry_conditions[4]:
            #     update_runner_pos_keep_state(
            #         runner,
            #         PositionKeepMode.PACE_UP_EX,
            #         runner.state.position.distance,
            #         None
            #     )
            #     return

            # if entry_conditions[4]:
            #     new_mode = PositionKeepMode.PACE_UP_EX
            # else:
            #     new_mode = PositionKeepMode(entry_conditions.index(True) + 1)

            update_pos_keep_state(
                runner,
                PositionKeepMode(entry_conditions.index(True) + 1),
                runner.state.position.distance,
                None
            )
            return
        runner.state.position_keep.next_check_frame = current_frame + 2 * fps
        return

    # In non-normal mode
    start_distance = runner.state.position_keep.start_distance
    section_length = math.floor(race.course.distance / 24)

    # Runner fulfills mode's exit condition
    exit_conditions = get_exit_conditions(runner, race)
    if exit_conditions[current_mode.value - 1]:
        update_pos_keep_state(
            runner,
            PositionKeepMode.NORMAL,
            None,
            current_frame + 3 * fps
        )
        return

    # Runner has run in mode for length of one section
    if runner.state.position.distance - start_distance >= section_length:
        update_pos_keep_state(
            runner,
            PositionKeepMode.NORMAL,
            None,
            current_frame + 3 * fps
        )
        return


def position_keep_active(
        current_position: float,
        course_distance: int
) -> bool:
    sections = section_boundaries(course_distance)
    return current_position <= sections[9]


def update_pos_keep_state(
        runner: Runner,
        mode: PositionKeepMode | None,
        start_distance: float | None,
        next_check_frame: int | None
) -> None:
    runner.state.position_keep.mode = mode
    runner.state.position_keep.start_distance = start_distance
    runner.state.position_keep.next_check_frame = next_check_frame


def get_entry_conditions(runner: Runner, race: Race) -> list[bool]:
    return [
        speed_up.entry_condition(runner, race),
        # overtake.entry_condition(runner, race),
        # pace_up.entry_condition(runner, race),
        # pace_down.entry_condition(runner, race),
        # pace_up_ex.entry_condition(runner, race),
    ]


def get_exit_conditions(runner: Runner, race: Race) -> list[bool]:
    return [
        speed_up.exit_condition(runner, race),
        # overtake.exit_condition(runner, race),
        # pace_up.exit_condition(runner, race),
        # pace_down.exit_condition(runner, race),
        # pace_up_ex.exit_condition(runner, race),
    ]


def wit_check(wit_stat: float) -> bool:
    chance = 20 * math.log10(wit_stat * 0.1)
    return random.uniform(0, 100) < chance


# Testing
if __name__ == '__main__':
    max_value = 100000
    rolls = [wit_check(100) for _ in range(max_value)]

    print(sum(rolls))
    print(max_value - sum(rolls))
    print(f'Chance: {sum(rolls) / max_value * 100:.2f}%')
