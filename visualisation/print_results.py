# Path: horse-racing-sim/visualisation\print_results.py
from dataclasses import dataclass
from typing import Any

from data_types import BASHIN
from race.race import bracket, Runner
from simulation.simulator import RaceSimulator
from utils import inverse_lerp

MARGIN_THRESHOLDS = (
    (0.2, 'nse'),
    (0.4, 'hd'),
    (0.8, 'nk'),
    (BASHIN / 2, '1/2'),
    (BASHIN * 3 / 4, '3/4'),
    (BASHIN, '1')
)


@dataclass
class RaceResult:
    runner: Runner
    finish_time: float
    post_position: int


def str_results(sim: RaceSimulator):
    placings = get_final_placings(sim)

    lines = [
        '',
        f'RESULTS: {sim.race.name}',
        f'[FP][BK][PP] HORSE............. | FIN. TIME | MARGIN |'
    ]

    for position, result in enumerate(placings, start=1):
        lines.append(
            format_result_row(
                position=position,
                pp=result.post_position,
                name=result.runner.entry.horse.name,
                finish_time=format_finish_time(result.finish_time),
                margin=get_margin(placings, position),
                runner_count=len(sim.race.runners),
            )
        )

    return '\n'.join(lines)


def get_final_placings(sim: RaceSimulator) -> list[RaceResult]:
    placings = []

    for pp, runner in enumerate(sim.race.runners, start=1):
        finish_time = get_finish_time(sim, pp, runner)
        placings.append(RaceResult(runner, finish_time, pp))

    return sorted(placings, key=lambda x: x.finish_time)


def get_finish_time(sim: RaceSimulator, runner_index: int, runner) -> float:
    finish_frames = runner.state.finish_frames

    distance_1 = (
        sim.history[finish_frames[0]]
        .runner_states[runner_index]
        .position.distance
    )

    distance_2 = (
        sim.history[finish_frames[1]]
        .runner_states[runner_index]
        .position.distance
    )

    subframe = finish_frames[0] + inverse_lerp(
        distance_1, distance_2, sim.race.course.distance
    )

    return subframe * sim.FRAME_DURATION


def get_post_positions(sim: RaceSimulator) -> dict[Any, int]:
    return {
        runner.entry.horse.name: index
        for index, runner in enumerate(sim.race.runners, start=1)
    }


def get_margin(placings, position: int) -> str:
    if position == 1:
        return ''

    finish_time = placings[position - 1].finish_time
    previous_finish_time = placings[position - 2].finish_time

    finish_time_diff = (finish_time - previous_finish_time) * 15

    return format_margin(finish_time_diff)


def format_margin(finish_time_diff: float) -> str:
    if finish_time_diff < BASHIN:
        return get_short_margin(finish_time_diff)

    length, sublength = divmod(finish_time_diff, BASHIN)
    length = int(length)

    if sublength >= BASHIN * 3 / 4:
        return f'{length}.3/4'

    if sublength >= BASHIN / 2:
        return f'{length}.1/2'

    if sublength >= BASHIN / 4:
        return f'{length}.1/4'

    return f'{length}'


def get_short_margin(finish_time_diff: float) -> str:
    for maximum, margin_name in MARGIN_THRESHOLDS:
        if finish_time_diff <= maximum:
            return margin_name
    raise ValueError(
        f'No short margin found for {finish_time_diff=}'
    )


def format_finish_time(finish_time: float) -> str:
    minutes, seconds = divmod(finish_time, 60)
    return f'{int(minutes):>2}:{round(seconds, 1):<6}'


def format_result_row(
        position: int,
        pp: int,
        name: str,
        finish_time: str,
        margin: str,
        runner_count: int) -> str:
    return (
        f'[{position:<2}][{bracket(pp, runner_count)} ][{pp:<2}] '
        f'{name:.<18} | '
        f'{finish_time} |{margin:^8}|'
    )
