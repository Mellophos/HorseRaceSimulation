# Path: horse-racing-sim/course\presets\racecourses\japan\jra\hakodate.py
# hakodate.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Hakodate(Racecourse):
    TRACK_ID = TrackID.HAKODATE

    def build_course(self, config: CourseConfig) -> Course:
        pass
