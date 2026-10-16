# Path: horse-racing-sim/simulation\mechanics\position_keep\speed_up.py
from data_types import Strategy
from race import Race, Runner
from tests import test_race


def entry_condition(runner: Runner, race: Race) -> bool:
    # Not front runner
    if runner.entry.strategy != Strategy.FRONT:
        return False
    order = race.get_race_order()
    position = order.index(runner)

    # Not first place
    if position != 0:
        return False

    # No runner behind; in last place or only runner in race
    try:
        second_runner = race.get_runner_behind(runner)
    except IndexError:
        return False

    gap = (runner.state.position.distance -
           second_runner.state.position.distance)
    front_runner_count = sum(
        r.entry.strategy == Strategy.FRONT for r in race.runners)

    # Gap threshold is 12.5 if only front runner in race, else 4.5
    if front_runner_count == 1:
        return gap < 12.5
    return gap < 4.5


def exit_condition(runner: Runner, race: Race) -> bool:
    # Protect against non-front runners just in case
    if runner.entry.strategy != Strategy.FRONT:
        return False
    order = race.get_race_order()
    position = order.index(runner)

    # Not first place
    if position != 0:
        return False

    # No runner behind; in last place or only runner in race
    try:
        second_runner = race.get_runner_behind(runner)
    except IndexError:
        return False

    gap = (runner.state.position.distance -
           second_runner.state.position.distance)
    front_runner_count = sum(
        r.entry.strategy == Strategy.FRONT for r in race.runners)

    # Gap threshold is 12.5 if only front runner in race, else 4.5
    if front_runner_count == 1:
        return gap >= 12.5
    return gap >= 4.5


if __name__ == '__main__':
    print(entry_condition(test_race, test_race.runners[0]))
