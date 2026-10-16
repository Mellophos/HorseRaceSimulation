# Path: overtake.py
from data_types import Strategy
from race import Runner, Race
from tests import test_race


def entry_condition(runner: Runner, race: Race) -> bool:
    # Not front runner
    if runner.entry.strategy is not Strategy.FRONT:
        return False

    # Not first place among runners of same strategy
    position = race.get_strategy_position(runner)
    return position > 0


def exit_condition(runner: Runner, race: Race) -> bool:
    # Not front runner
    if runner.entry.strategy is not Strategy.FRONT:
        return False

    # 10 metres ahead of 2nd place among runners of same strategy
    strat_order = race.get_strategy_order(runner.entry.strategy)
    position = race.get_strategy_position(runner)
    if position > 0:
        return False
    second_runner = strat_order[1]
    gap = (runner.state.position.distance -
           second_runner.state.position.distance)
    return gap >= 10


if __name__ == '__main__':
    test_race.runners[0].state.position.distance = 100
    test_race.runners[1].state.position.distance = 100

    print(exit_condition(test_race.runners[0], test_race))