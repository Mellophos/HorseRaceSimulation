# Path: horse-racing-sim/course\presets\racecourses\japan\jra\chukyo.py
# chukyo.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Chukyo(Racecourse):
    TRACK_ID = TrackID.CHUKYO

    def build_course(self, config: CourseConfig) -> Course:
        pass
