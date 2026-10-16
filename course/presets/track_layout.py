# Path: horse-racing-sim/course\presets\track_layout.py
from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Iterable

from course import CourseEvent, PRIORITY


class TrackLayout(ABC):
    def __init__(self, events: Iterable[CourseEvent]):
        self.events = tuple(events)

    @abstractmethod
    def events_until(self, distance: int) -> list[CourseEvent]:
        """Return all track events encountered within ``distance`` metres
        of the canonical layout.

        The returned events represent the underlying track geometry only.
        Racecourse-specific starting positions, chutes, and
        distance-specific modifications are not applied here.
        """
        pass


class LoopingTrackLayout(TrackLayout):
    def __init__(self, lap_distance: int, events: Iterable[CourseEvent]):
        super().__init__(events)
        self.lap_distance = lap_distance

    def events_until(self, distance: int) -> list[CourseEvent]:
        event_list = []
        total_dist = distance
        laps = total_dist // self.lap_distance + 1
        for lap in range(laps):
            for idx, event in enumerate(self.events[1:-1]):
                if event.trigger_location <= distance:
                    event_list.append(
                        replace(
                            event,
                            trigger_location=distance - event.trigger_location
                        )
                    )
                else:
                    break
            distance -= self.lap_distance
        event_list.append(
            replace(
                self.events[0], trigger_location=total_dist
            )
        )
        return sorted(
            event_list, key=lambda e: (
                e.trigger_location, PRIORITY.get(type(e), 99)
            )
        )


class LinearTrackLayout(TrackLayout):
    def __init__(self, events: Iterable[CourseEvent]):
        super().__init__(events)

    def events_until(self, distance: int) -> list[CourseEvent]:
        event_list = []
        for event in self.events[1:-1]:
            if event.trigger_location <= distance:
                event_list.append(
                    replace(
                        event,
                        trigger_location=distance - event.trigger_location
                    )
                )
        event_list.append(
            replace(
                self.events[0], trigger_location=distance
            )
        )
        return sorted(
            event_list, key=lambda e: (
                e.trigger_location, PRIORITY.get(type(e), 99)
            )
        )