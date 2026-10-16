# Path: horse-racing-sim/course\presets\racecourses\japan\jra\fukushima.py
# fukushima.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Fukushima(Racecourse):
    TRACK_ID = TrackID.FUKUSHIMA

    def build_course(self, config: CourseConfig) -> Course:
        pass
