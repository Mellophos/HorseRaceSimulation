# Path: horse-racing-sim/course\presets\racecourses\japan\jra\kokura.py
# kokura.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Kokura(Racecourse):
    TRACK_ID = TrackID.KOKURA

    def build_course(self, config: CourseConfig) -> Course:
        pass
