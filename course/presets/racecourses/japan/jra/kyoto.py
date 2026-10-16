# Path: horse-racing-sim/course\presets\racecourses\japan\jra\kyoto.py
# kyoto.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse, track_config
from data_types import Surface


class Kyoto(Racecourse):
    TRACK_ID = TrackID.KYOTO

    turf_inner = []
    turf_outer = []
    dirt = []

    DISTANCES = {
        Surface.TURF: {
            **track_config(
                turf_inner,
                {1100, 1200, 1400, 1600, 2000},
                "inner"
            ),
            **track_config(
                turf_outer,
                {1400, 1600, 1800, 2000, 2200, 2400, 3000, 3200},
                "outer"
            )
        },
        Surface.DIRT: {
            **track_config(
                dirt,
                {1000, 1100, 1200, 1400, 1800, 1900, 2600}
            )
        }
    }

    def build_course(self, config: CourseConfig) -> Course:
        pass
