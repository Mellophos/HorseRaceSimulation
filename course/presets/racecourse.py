# Path: horse-racing-sim/course\presets\racecourse.py
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import ClassVar

from course import CourseEvent, Course
from course.presets.config import CourseConfig, TrackID
from course.presets.track_layout import TrackLayout
from data_types import Surface

CourseBuilder = Callable[[list[CourseEvent]], list[CourseEvent]]
Configuration = dict[Surface, dict[tuple[int, str | None], TrackLayout]]


class Racecourse(ABC):
    _REGISTRY: ClassVar[dict[TrackID, type["Racecourse"]]] = {}

    TRACK_ID: ClassVar[TrackID]
    DISTANCES: ClassVar[Configuration] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if "TRACK_ID" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must define TRACK_ID"
            )

        if cls.TRACK_ID in Racecourse._REGISTRY:
            raise ValueError(
                f"Duplicate racecourse ID: {cls.TRACK_ID}"
            )

        Racecourse._REGISTRY[cls.TRACK_ID] = cls

    def get_track(self, config: CourseConfig) -> TrackLayout:
        try:
            return self.DISTANCES[config.surface][
                (config.distance, config.layout)
            ]
        except KeyError:
            raise AttributeError(
                f" Class '{self.__class__.__name__}' "
                f"has no track configured for "
                f"{config.surface.name} {config.distance}m"
                f"{f' ({config.layout})' if config.layout else ''}"
            ) from None

    def build_events(
            self,
            config: CourseConfig
    ) -> list[CourseEvent]:
        track = self.get_track(config)
        return track.events_until(config.distance)

    @abstractmethod
    def build_course(self, config: CourseConfig) -> Course:
        pass


def track_config(
        track: TrackLayout,
        distances: Iterable[int],
        layout: str | None = None
) -> dict[tuple[int, str | None], TrackLayout]:
    return {
        (distance, layout): track
        for distance in distances
    }
