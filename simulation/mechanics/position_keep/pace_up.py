# Path: pace_up.py
import random

from data_types import Strategy
from race import Runner, Race
from tests import test_race


def entry_condition(runner: Runner, race: Race) -> bool:
    if runner.entry.strategy is Strategy.FRONT:
        return False
    _, max_dist = calculate_course_factor(
        race.course.distance, runner.entry.strategy)
    pacemaker_pos = race.get_pacemaker().state.position.distance
    return runner.state.position.distance < pacemaker_pos - max_dist


def exit_condition(runner: Runner, race: Race) -> bool:
    if runner.entry.strategy is Strategy.FRONT:
        return False
    min_dist, max_dist = calculate_course_factor(
        race.course.distance, runner.entry.strategy)
    rand_value = random.uniform(min_dist, max_dist)
    pacemaker_pos = race.get_pacemaker().state.position.distance
    return runner.state.position.distance > pacemaker_pos - rand_value


def calculate_course_factor(course_distance: int, strategy: Strategy) -> tuple[
    float, float]:
    course_factor = 0.0008 * (course_distance - 1000) + 1.0
    if strategy is Strategy.PACE:
        return 3.0, 5.0 * course_factor
    if strategy is Strategy.LATE:
        return 6.5 * course_factor, 7.0 * course_factor
    if strategy is Strategy.END:
        return 7.5 * course_factor, 8.0 * course_factor
    raise ValueError(f"Strategy {strategy} has no course factor")


if __name__ == "__main__":
    test_race.runners[0].state.position.distance = 100
    test_race.runners[3].state.position.distance = 94
    print(test_race.get_pacemaker().entry.strategy)
    print(test_race.get_pacemaker().state.position.distance)

    print(calculate_course_factor(1000, Strategy.PACE))

    assert entry_condition(test_race.runners[3], test_race) is True
    assert exit_condition(test_race.runners[3], test_race) is False
