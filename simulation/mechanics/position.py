# Path: horse-racing-sim/simulation\mechanics\position.py
from fractions import Fraction

from horse.state import HorseState
from simulation.mechanics.speed import update_current_speed
from tests import test_horse_state


def update_position(horse_state: HorseState, old_speed: float,
                    duration: float):
    average_speed = Fraction((
                                     old_speed +
                                     horse_state.movement.current_speed) /
                             2).limit_denominator()
    horse_state.position.distance += (average_speed * duration)


if __name__ == "__main__":
    FPS = 15
    FRAME_DURATION = 1 / 15
    # print(test_horse_state.movement.current_speed)
    print(test_horse_state.position.distance)
    for i in range(FPS):
        prev_speed = test_horse_state.movement.current_speed
        update_current_speed(test_horse_state, 10, FRAME_DURATION)
        update_position(test_horse_state, prev_speed, FRAME_DURATION)
        print(test_horse_state.position.distance)
        # print(test_horse_state.movement.current_speed)
