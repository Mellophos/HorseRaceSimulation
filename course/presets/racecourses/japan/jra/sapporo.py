# Path: horse-racing-sim/course\presets\racecourses\japan\jra\sapporo.py
# sapporo.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Sapporo(Racecourse):
    TRACK_ID = TrackID.SAPPORO

    def build_course(self, config: CourseConfig) -> Course:
        pass
