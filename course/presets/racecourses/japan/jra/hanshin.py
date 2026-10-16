# Path: horse-racing-sim/course\presets\racecourses\japan\jra\hanshin.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Hanshin(Racecourse):
    TRACK_ID = TrackID.HANSHIN

    def build_course(self, config: CourseConfig) -> Course:
        pass
