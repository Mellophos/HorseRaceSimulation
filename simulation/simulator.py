# Path: horse-racing-sim/simulation\simulator.py
import random
from copy import deepcopy
from dataclasses import dataclass

from horse import HorseState
from race import Race
from utils import section_boundaries


class RaceSimulator:
    FPS = 15
    FRAME_DURATION = 1 / FPS

    def __init__(self, race: Race):
        self.race = deepcopy(race)
        self.frames_elapsed = 0
        self.history = []
        self.is_finished = False
        self._section_boundaries = section_boundaries(race.course.distance)

    def run(self):
        self.start()

        while not self.is_finished:
            self.tick()

    def start(self):
        for horse in self.race.runners:
            horse.state.is_racing = True
        self.record_snapshot()

    def tick(self):
        if not self.is_finished:
            self.pre_update_checks()
            self.step()
            self.post_update_checks()
            self.update_finished_runners()
            self.is_finished = self.race_is_finished()
            self.record_snapshot()

    def step(self):
        self.frames_elapsed += 1

        # Update last spurt state
        # Update target speed
        # Calculate acceleration
        # Update phase
        # Calculate distance and position
        # Check for slope

        # Basic temporary movement
        for horse in self.race.runners:
            if horse.state.is_racing:
                horse.state.position.distance += random.uniform(0.5, 2.0)

    def pre_update_checks(self):
        # Check end of Corner
        pass

    def post_update_checks(self):
        # Check start of Corner
        pass

    def update_finished_runners(self):
        for horse in self.race.runners:
            if (horse.state.position.distance >= self.race.course.distance
                    and horse.state.is_racing):
                horse.state.is_racing = False
                horse.state.finish_frames = (self.frames_elapsed - 1,
                                             self.frames_elapsed)

    def reset(
            self, *,
            shuffle_runners: bool = False,
            change_ground_condition: bool = False,
            change_moods: bool = False
    ):
        self.frames_elapsed = 0
        self.history = []
        self.is_finished = False
        self.race.reset(
            shuffle_runners=shuffle_runners,
            change_ground_condition=change_ground_condition,
            change_moods=change_moods
        )

    def race_is_finished(self):
        return all(
            not runner.state.is_racing
            for runner in self.race.runners
        )

    def record_snapshot(self):
        runner_states = {}
        for i, horse in enumerate(self.race.runners, start=1):
            runner_states[i] = deepcopy(horse.state)
        snapshot = {
            'frame': self.frames_elapsed,
            'runner_states': runner_states
        }
        self.history.append(
            FrameSnapshot(**snapshot)
        )


@dataclass
class FrameSnapshot:
    frame: int
    runner_states: dict[int, HorseState]

    def to_dict(self, *, sort_keys: bool = False) -> dict:
        runner_states = {i: state.to_dict() for i, state in
                         self.runner_states.items()}

        if sort_keys:
            runner_states = sorted(runner_states.items(),
                                   key=lambda x: x[1]['position']['distance'])

        return {'frame': self.frame, 'runner_states': runner_states}
