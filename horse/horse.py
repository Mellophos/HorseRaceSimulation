# Path: horse-racing-sim/horse\horse.py
"""Represent horses and their intrinsic racing characteristics.

This module defines the Horse, Stats, and Aptitude data structures.
"""

from dataclasses import dataclass

from data_types import Surface, Strategy, DistanceCategory, Grade
from utils import clamp


def stat_clamp(stat: float) -> float:
    return clamp(stat, 1, 2500)


@dataclass
class Stats:
    """Represent the numerical performance statistics of a horse.

    Attributes:
        speed: The horse's speed stat.
        stamina: The horse's stamina stat.
        power: The horse's power stat.
        guts: The horse's guts stat.
        wit: The horse's wit stat.
    """

    speed: float
    stamina: float
    power: float
    guts: float
    wit: float


@dataclass
class Aptitude:
    """Represent a horse's racing aptitudes.

    Aptitudes describe how well a horse is suited to different racing
    conditions and strategies. Each aptitude is represented by a ``Grade``.

    Attributes:
        surface: Mapping of track surfaces to the horse's aptitude for
            each surface.
        distance: Mapping of distance categories to the horse's aptitude
            for each distance.
        strategy: Mapping of racing strategies to the horse's aptitude
            for each strategy.
    """

    surface: dict[Surface, Grade]
    distance: dict[DistanceCategory, Grade]
    strategy: dict[Strategy, Grade]


@dataclass
class Horse:
    """Represent a horse and its racing characteristics.

    A ``Horse`` contains the horse's name, aptitude ratings for different
    racing conditions and strategies, and its numerical performance stats.

    Each stat is clamped between 1 and 2500.

    Attributes:
        name: The horse's name.
        aptitude: The horse's aptitude ratings for surfaces, distances,
            and racing strategies.
        stats: The horse's numerical performance statistics, clamped
            between 1 and 2500.
    """

    name: str
    aptitude: Aptitude
    stats: Stats

    @classmethod
    def from_dict(cls, data: dict) -> Horse:
        """Create a Horse from a dictionary.

        The dictionary is expected to contain the horse's name, aptitude
        ratings for surfaces, distances, and strategies, and numerical
        stats. String grade names in the aptitude data are converted to
        their corresponding ``Grade`` enum values.

        Args:
            data: Dictionary containing the horse's attributes and stats.

        Returns:
            A ``Horse`` initialised from the supplied data.
        """
        aptitude_data = data['aptitude']

        return cls(
            name=data['name'],
            aptitude=Aptitude(
                surface={
                    Surface[key.upper()]: Grade[value]
                    for key, value in aptitude_data['surface'].items()
                },
                distance={
                    DistanceCategory[key.upper()]: Grade[value]
                    for key, value in aptitude_data['distance'].items()
                },
                strategy={
                    Strategy[key.upper()]: Grade[value]
                    for key, value in aptitude_data['strategy'].items()
                }
            ),
            stats=Stats(**{
                key: stat_clamp(value) for key, value in data['stats'].items()
            })
        )
