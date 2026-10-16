# Path: horse-racing-sim/course\presets\racecourses\japan\jra\niigata.py
# niigata.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Niigata(Racecourse):
    TRACK_ID = TrackID.NIIGATA

    def build_course(self, config: CourseConfig) -> Course:
        pass
