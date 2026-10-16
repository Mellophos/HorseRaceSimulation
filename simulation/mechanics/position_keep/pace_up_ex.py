# Path: pace_up_ex.py
from race import Runner, Race
from tests import test_race


def entry_condition(runner: Runner, race: Race) -> bool:
    strategy = runner.entry.strategy.value
    order = race.get_race_order()
    position = order.index(runner)

    if strategy <= 1:
        # Non-front runners are ahead of runner
        return any(
            r.entry.strategy.value > strategy
            for r in order[:position]
        )
    else:
        # Pacemaker's strategy should be behind runner
        pacemaker = race.get_pacemaker()
        return pacemaker.entry.strategy.value > strategy


def exit_condition(runner: Runner, race: Race) -> bool:
    strategy = runner.entry.strategy.value
    order = race.get_race_order()
    position = order.index(runner)

    # No runner whose strategy should be behind is ahead
    return not any(
        r.entry.strategy.value > strategy
        for r in order[:position]
    )


if __name__ == '__main__':
    test_race.runners[0].state.position.distance = 105
    test_race.runners[1].state.position.distance = 100
    test_race.runners[2].state.position.distance = 101
    test_race.runners[3].state.position.distance = 100
    test_race.runners[4].state.position.distance = 110
    test_race.runners[5].state.position.distance = 100
    test_race.runners[6].state.position.distance = 100
    test_race.runners[7].state.position.distance = 100

    assert entry_condition(test_race.runners[1], test_race) is True
    assert entry_condition(test_race.runners[2], test_race) is False
