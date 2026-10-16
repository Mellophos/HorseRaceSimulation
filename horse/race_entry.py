# Path: horse-racing-sim/horse\race_entry.py
"""Define race-specific horse entry data and stat calculations.

This module contains the data structures used to represent a horse's
intended race selections and its resulting race-specific attributes.
"""
from dataclasses import dataclass, asdict
from random import choice, choices
from typing import Literal

from course import Course
from data_types import Strategy, Mood, GroundCondition, Grade
from lookups import MOOD_MULTIPLIERS, SURFACE_POWER_MODIFIERS, \
    SURFACE_SPEED_MODIFIERS, GRADE_WIT_MULTIPLIERS
from utils import linear_soft_cap, clamp
from .horse import Horse, Stats

StrategySelectionMode = Literal['random', 'best', 'weighted']


def stat_clamp(stat: float) -> float:
    return clamp(stat, 1, 2500)


@dataclass()
class Entry:
    """Describes a horse's intended participation in a race.

    An ``Entry`` contains the horse together with the strategy and mood that
    will be used when creating its race-specific ``RaceEntry``.

    Attributes:
        horse: The horse participating in the race.
        strategy: The strategy selected for the horse.
        mood: The horse's mood for the race.

    Args:
        horse: Horse participating in the race.
        strategy: A ``Strategy`` value, or a selection mode of ``"random"``,
            ``"best"``, or ``"weighted"`` used to select a strategy.
        mood: The horse's mood. If ``None``, a random mood is selected.
    """
    horse: Horse
    strategy: Strategy
    mood: Mood

    def __init__(
            self,
            horse: Horse,
            strategy: Strategy | StrategySelectionMode,
            mood: Mood | None
    ):
        """Initialise an entry for a horse.

        If ``strategy`` is supplied as a string, ``choose_strategy`` is used
        to select the corresponding strategy. If ``mood`` is ``None``, a
        random mood is selected.

        Args:
            horse: Horse participating in the race.
            strategy: A specific ``Strategy`` or a strategy selection mode.
            mood: Mood for the horse. If ``None``, a random mood is selected.
        """
        if isinstance(strategy, str):
            strategy = choose_strategy(horse, strategy)
        if mood is None:
            mood = choice(list(Mood))

        object.__setattr__(self, 'horse', horse)
        object.__setattr__(self, 'strategy', strategy)
        object.__setattr__(self, 'mood', mood)


def choose_strategy(horse: Horse,
                    selection_mode: StrategySelectionMode) -> Strategy:
    """Choose a strategy for a horse based on its strategy aptitudes.

    Args:
        horse: Horse whose strategy aptitudes are used for selection.
        selection_mode: Method used to select the strategy. ``"random"``
            gives all strategies an equal probability, ``"best"`` selects
            randomly from strategies with the highest aptitude, and
            ``"weighted"`` gives higher-rated strategies a greater
            probability of being selected.

    Returns:
        The selected strategy.

    Raises:
        ValueError: If ``selection_mode`` is not a supported selection mode.
    """
    if selection_mode == 'random':
        return choice(list(Strategy))

    strategy_aptitudes = horse.aptitude.strategy

    if selection_mode == 'best':
        best_grade = max(
            strategy_aptitudes.values(),
            key=lambda grade: grade.value
        )
        best_strategies = [
            strategy
            for strategy, grade in strategy_aptitudes.items()
            if grade == best_grade
        ]
        return choice(best_strategies)

    if selection_mode == 'weighted':
        strategies = list(strategy_aptitudes)
        weights = [strategy_aptitudes[strategy].value
                   for strategy in strategies]
        return choices(strategies, weights=weights, k=1)[0]
    raise ValueError(f'Unknown strategy selection mode: {selection_mode!r}')


@dataclass
class RaceEntry:
    """Represent a horse's race-specific attributes.

    A ``RaceEntry`` is created from a ``Horse`` together with the conditions
    of a particular race. Unlike ``Entry``, which represents the player's
    or simulation's initial selection of a horse, strategy, and mood,
    ``RaceEntry`` contains the calculated attributes that result from those
    selections and the race conditions.

    The horse's original stats are not modified. Instead, ``base_stats``
    contains stats after applying the horse's mood modifier, while
    ``final_stats`` additionally includes the effects of the course's
    surface, ground condition, and the horse's aptitude for its chosen
    strategy.

    Attributes:
        horse: The horse participating in the race.
        mood: The horse's mood for this race.
        strategy: The racing strategy selected for this race.
        distance_aptitude: The horse's aptitude for the race's distance
            category.
        surface_aptitude: The horse's aptitude for the race's surface.
        strategy_aptitude: The horse's aptitude for the selected strategy.
        base_stats: The horse's stats after applying the mood modifier.
        final_stats: The horse's stats after all applicable race-specific
            modifiers have been applied.
    """

    horse: Horse
    mood: Mood
    strategy: Strategy
    distance_aptitude: Grade
    surface_aptitude: Grade
    strategy_aptitude: Grade
    base_stats: Stats
    final_stats: Stats

    @classmethod
    def from_entry(
            cls,
            entry: Entry,
            course: Course,
            ground_condition: GroundCondition
    ) -> RaceEntry:
        """Create a RaceEntry from an Entry and race conditions.

        The supplied Entry provides the horse, chosen strategy, and mood.
        The course and ground condition are used to determine the horse's
        relevant aptitudes and apply race-specific stat modifiers.

        The horse's original stats are not modified. Instead, the horse's
        stats are first adjusted according to its mood, then further modified
        according to the course surface, ground condition, and chosen strategy.

        Args:
            entry: The horse, strategy, and mood selected for the race.
            course: Course on which the race is being run.
            ground_condition: Ground condition for the race.

        Returns:
            A ``RaceEntry`` containing the horse, selected race conditions,
            relevant aptitudes, mood-adjusted base stats, and final modified
            stats.
        """
        distance_aptitude = entry.horse.aptitude.distance[
            course.distance_category]
        surface_aptitude = entry.horse.aptitude.surface[course.surface]
        strategy_aptitude = entry.horse.aptitude.strategy[entry.strategy]

        motiv_coef = MOOD_MULTIPLIERS[entry.mood]
        raw_stats = {
            k: stat_clamp(linear_soft_cap(v, 1200, 0.5))
            for k, v in asdict(entry.horse.stats).items()
        }

        base_stats = Stats(
            **{
                key: stat_clamp(value * motiv_coef)
                for key, value in raw_stats.items()
            }
        )

        final_stats = Stats(
            speed=stat_clamp(
                base_stats.speed + SURFACE_SPEED_MODIFIERS[course.surface][
                    ground_condition]
            ),
            stamina=stat_clamp(
                base_stats.stamina
            ),
            power=stat_clamp(
                base_stats.power + SURFACE_POWER_MODIFIERS[course.surface][
                    ground_condition]
            ),
            guts=stat_clamp(base_stats.guts),
            wit=stat_clamp(
                base_stats.wit + GRADE_WIT_MULTIPLIERS[strategy_aptitude]
            )
        )

        return cls(
            horse=entry.horse,
            mood=entry.mood,
            strategy=entry.strategy,
            distance_aptitude=distance_aptitude,
            surface_aptitude=surface_aptitude,
            strategy_aptitude=strategy_aptitude,
            base_stats=base_stats,
            final_stats=final_stats,
        )
