# Path: horse-racing-sim/horse\state.py

from dataclasses import dataclass, asdict

from data_types import PositionKeepMode


class HorseState:
    def __init__(self, position: Position, health: Health, movement: Movement):
        self.position = position
        self.health = health
        self.movement = movement

        # statuses
        self.position_keep = PositionKeep()

        # simulation
        self.is_racing = False
        self.finish_frames = ()

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a HorseState object from a dictionary."""
        return cls(
            position=Position(**data['position']),
            health=Health(**data['health']),
            movement=Movement(**data['movement']),
        )

    def to_dict(self):
        return {
            'position': asdict(self.position),
            'health': asdict(self.health),
            'movement': asdict(self.movement),
            'finish_frames': self.finish_frames,
        }

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'position={self.position!r}, '
            f'health={self.health!r}, '
            f'movement={self.movement!r}, '
            f'position_keep_mode={self.position_keep!r}, '
            f'is_racing={self.is_racing!r}, '
            f'finish_frames={self.finish_frames!r}, '
            f')')


@dataclass
class Position:
    distance: float
    lane: float


@dataclass
class Health:
    max_hp: float
    hp: float


@dataclass
class Movement:
    target_speed: float
    current_speed: float


@dataclass
class PositionKeep:
    mode: PositionKeepMode = PositionKeepMode.NORMAL
    start_distance: float | None = None
    next_check_frame: int | None = None
