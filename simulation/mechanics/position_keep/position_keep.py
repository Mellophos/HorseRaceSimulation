# Path: horse-racing-sim/simulation\mechanics\position_keep\position_keep.py
import math
import random

from data_types import PositionKeepMode
from race.race import Runner, Race
from simulation.mechanics.position_keep import (
    speed_up, overtake, pace_up_ex, pace_up, pace_down
)
from utils import section_boundaries


class PositionKeep:
    def __init__(self):
        self.active = True
        self.current_mode: PositionKeepMode = PositionKeepMode.NORMAL
        self.next_check_frame = 0
        self.start_distance = None

    def update(
            self,
            runner: Runner,
            race: Race,
            current_frame: int,
            fps: int
    ) -> PositionKeepMode | None:
        """Update a Runner's Position Keeping state"""
        if not self.active:
            return None

        distance = runner.state.position.distance
        course_distance = race.course.distance

        # Exit state machine if past section 10
        if not is_position_keep_active(distance, course_distance):
            self.active = False
            return None

        # Check to enter a non-NORMAL mode
        if self.current_mode is PositionKeepMode.NORMAL:
            return self._try_enter_mode(
                runner, race, distance, current_frame, fps
            )

        # Check to exit a non-NORMAL mode
        return self._try_exit_mode(
            runner, race, distance, course_distance, current_frame, fps
        )

    def _try_enter_mode(
            self,
            runner: Runner,
            race: Race,
            distance: float,
            current_frame: int,
            fps: int
    ) -> PositionKeepMode:
        """Check to enter a non-NORMAL mode, must pass a wit check."""
        if current_frame < self.next_check_frame:
            return PositionKeepMode.NORMAL

        # Check entry conditions for all modes
        entry_conditions = get_entry_conditions(runner, race)
        if not any(entry_conditions):
            # No entry conditions are fulfilled
            self.next_check_frame = current_frame + 2 * fps
            return PositionKeepMode.NORMAL

        # Priotitise PACE_UP_EX if entry condition is True
        if entry_conditions[-1]:
            new_mode = PositionKeepMode.PACE_UP_EX
        else:
            # Wit check
            if not wit_check(runner.entry.final_stats.wit):
                self.next_check_frame = current_frame + 2 * fps
                return PositionKeepMode.NORMAL
            else:
                new_mode = PositionKeepMode(entry_conditions.index(True) + 1)

        self.enter_mode(new_mode, distance)
        return new_mode

    def _try_exit_mode(
            self,
            runner: Runner,
            race: Race,
            distance: float,
            course_distance: int,
            current_frame: int,
            fps: int
    ) -> PositionKeepMode:
        """Check to exit a non-NORMAL mode."""
        section_length = math.floor(course_distance / 24)
        exit_condition = get_exit_condition(self.current_mode, runner, race)
        completed_section = distance - self.start_distance >= section_length

        if exit_condition or completed_section:
            self.exit_mode(current_frame + 3 * fps)
        return self.current_mode

    def enter_mode(self, mode: PositionKeepMode, distance: float) -> None:
        """Enter a non-NORMAL mode."""
        self.current_mode = mode
        self.start_distance = distance
        self.next_check_frame = None

    def exit_mode(self, next_check_frame: int) -> None:
        """Exit a non-NORMAL mode."""
        self.current_mode = PositionKeepMode.NORMAL
        self.start_distance = None
        self.next_check_frame = next_check_frame


def is_position_keep_active(
        current_position: float,
        course_distance: int
) -> bool:
    sections = section_boundaries(course_distance)
    return current_position <= sections[9]


def get_entry_conditions(runner: Runner, race: Race) -> list[bool]:
    # All entry conditions except for PACE_UP_EX should be mutually exclusive
    return [
        speed_up.entry_condition(runner, race),
        overtake.entry_condition(runner, race),
        pace_up.entry_condition(runner, race),
        pace_down.entry_condition(runner, race),
        pace_up_ex.entry_condition(runner, race),
    ]


EXIT_CONDITIONS = {
    PositionKeepMode.SPEED_UP: speed_up.exit_condition,
    PositionKeepMode.OVERTAKE: overtake.exit_condition,
    PositionKeepMode.PACE_UP: pace_up.exit_condition,
    PositionKeepMode.PACE_DOWN: pace_down.exit_condition,
    PositionKeepMode.PACE_UP_EX: pace_up_ex.exit_condition,
}


def get_exit_condition(
        current_mode: PositionKeepMode,
        runner: Runner,
        race: Race
) -> bool:
    condition = EXIT_CONDITIONS[current_mode]
    return condition(runner, race)


def wit_check(wit_stat: float) -> bool:
    chance = 20 * math.log10(wit_stat * 0.1)
    return random.uniform(0, 100) < chance
