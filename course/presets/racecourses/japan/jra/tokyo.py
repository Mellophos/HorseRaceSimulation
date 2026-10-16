# Path: horse-racing-sim/course\presets\racecourses\japan\jra\tokyo.py
from dataclasses import replace

from course import Course
from course.events import CourseEvent, Straight, Corner, Slope, SurfaceChange
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse, CourseBuilder, track_config
from course.presets.track_layout import LoopingTrackLayout
from data_types import Surface


class Tokyo(Racecourse):
    TRACK_ID = TrackID.TOKYO

    turf = LoopingTrackLayout(
        lap_distance=2083,
        events=[
            Straight(trigger_location=0, straight_type=1, is_start=False),
            Slope(trigger_location=471, gradient=1.19, length=176),
            Straight(trigger_location=525, straight_type=1, is_start=True),
            Corner(trigger_location=770, corner_number=4, length=245),
            Slope(trigger_location=882, gradient=0.1, length=411),
            Corner(trigger_location=1035, corner_number=3, length=265),
            Straight(trigger_location=1035, straight_type=2, is_start=False),
            Slope(trigger_location=1145, gradient=-0.84, length=263),
            Slope(trigger_location=1281, gradient=1.75, length=80),
            Straight(trigger_location=1479, straight_type=2, is_start=True),
            Corner(trigger_location=1737, corner_number=2, length=258),
            Slope(trigger_location=1898, gradient=-0.28, length=617),
            Corner(trigger_location=2000, corner_number=1, length=263),
            Straight(trigger_location=2000, straight_type=1, is_start=False),
            Straight(trigger_location=2083, straight_type=1, is_start=True)
        ]
    )

    dirt = LoopingTrackLayout(
        lap_distance=1899,
        events=[
            Straight(trigger_location=0, straight_type=1, is_start=False),
            Slope(trigger_location=500, gradient=1.5, length=250),
            Straight(trigger_location=501, straight_type=1, is_start=True),
            Corner(trigger_location=725, corner_number=4, length=224),
            Corner(trigger_location=950, corner_number=3, length=225),
            Straight(trigger_location=950, straight_type=2, is_start=False),
            Slope(trigger_location=1025, gradient=-1, length=200),
            Straight(trigger_location=1400, straight_type=2, is_start=True),
            Corner(trigger_location=1650, corner_number=2, length=250),
            Corner(trigger_location=1899, corner_number=1, length=249),
            Straight(trigger_location=1899, straight_type=1, is_start=False),
            Straight(trigger_location=1899, straight_type=1, is_start=True),
        ]
    )

    DISTANCES = {
        Surface.TURF: {
            **track_config(
                turf,
                {1400, 1600, 1800, 2000, 2300, 2400, 2500, 2600, 3400}
            )
        },
        Surface.DIRT: {
            **track_config(
                dirt,
                {1200, 1300, 1400, 1600, 2100, 2400}
            )
        }
    }

    def build_course(self, config: CourseConfig) -> Course:
        assert config.track.name.capitalize() == self.__class__.__name__, (
            f"Factory routing error: "
            f"'{self.__class__.__name__}' class received configuration for "
            f"'{config.track.name}'"
        )
        if not self.DISTANCES[config.surface][
            (config.distance, config.layout)
        ]:
            raise ValueError(
                f"'{self.__class__.__name__}' class does not have "
                f"configuration "
                f"for {config.surface} {config.distance}"
            )

        event_list = self.build_events(config)

        builders: dict[Surface, dict[int, CourseBuilder]] = {
            Surface.TURF: {
                1400: self._turf_1400,
                1600: self._turf_1600,
                1800: self._turf_1800,
                2000: self._turf_2000,
                2300: self._turf_2300,
                2400: self._turf_2400,
                2500: self._turf_2500,
                3400: self._turf_3400,
            },
            Surface.DIRT: {
                1200: self._dirt_1200,
                1300: self._dirt_1300,
                1400: self._dirt_1400,
                1600: self._dirt_1600,
                2100: self._dirt_2100,
                2400: self._dirt_2400,
            },
        }
        builder = builders.get(config.surface, {}).get(config.distance)

        if builder is None:
            raise ValueError(
                f"Unsupported course for {self.__class__.__name__}: "
                f"{config.surface}, {config.distance}"
            )

        event_list = builder(event_list)

        return Course(
            name=self.__class__.__name__,
            surface=config.surface,
            distance=config.distance,
            event_list=event_list,
        )

    @staticmethod
    def _turf_1400(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Slope(trigger_location=0, gradient=-0.28, length=119)
        )
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=2, is_start=True)
        )
        return events

    @staticmethod
    def _turf_1600(events: list[CourseEvent]) -> list[CourseEvent]:
        events[0] = replace(
            events[0],
            trigger_location=0
        )
        return events

    @staticmethod
    def _turf_1800(events: list[CourseEvent]) -> list[CourseEvent]:
        events[0] = Corner(
            trigger_location=160, corner_number=2, length=171
        )
        return events

    @staticmethod
    def _turf_2000(events: list[CourseEvent]) -> list[CourseEvent]:
        del events[0], events[1]
        events[0] = Corner(trigger_location=155, corner_number=2, length=275)
        events[1] = Slope(trigger_location=387, gradient=-0.28, length=332)
        events[2] = Straight(trigger_location=430, straight_type=2,
                             is_start=True)
        return events

    @staticmethod
    def _turf_2300(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=1, is_start=True)
        )
        return events

    @staticmethod
    def _turf_2400(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Slope(trigger_location=0, gradient=1.19, length=22)
        )
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=1, is_start=True)
        )
        return events

    @staticmethod
    def _turf_2500(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Slope(trigger_location=0, gradient=1.19, length=122)
        )
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=1, is_start=True)
        )
        return events

    @staticmethod
    def _turf_3400(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Slope(trigger_location=0, gradient=-0.28, length=36)
        )
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=2, is_start=True)
        )
        return events

    @staticmethod
    def _dirt_1200(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=2, is_start=True)
        )
        return events

    @staticmethod
    def _dirt_1300(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=2, is_start=True)
        )
        return events

    @staticmethod
    def _dirt_1400(events: list[CourseEvent]) -> list[CourseEvent]:
        return events

    @staticmethod
    def _dirt_1600(events: list[CourseEvent]) -> list[CourseEvent]:
        events[0] = replace(
            events[0],
            trigger_location=0
        )
        events.insert(
            1,
            SurfaceChange(trigger_location=100)
        )
        return events

    @staticmethod
    def _dirt_2100(events: list[CourseEvent]) -> list[CourseEvent]:
        events.insert(
            0,
            Straight(trigger_location=0, straight_type=1, is_start=True)
        )
        return events

    @staticmethod
    def _dirt_2400(events: list[CourseEvent]) -> list[CourseEvent]:
        return events
