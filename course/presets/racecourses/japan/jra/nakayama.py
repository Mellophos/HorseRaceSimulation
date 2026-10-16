# Path: horse-racing-sim/course\presets\racecourses\japan\jra\nakayama.py
# nakayama.py
from course import Course
from course.presets.config import CourseConfig, TrackID
from course.presets.racecourse import Racecourse


class Nakayama(Racecourse):
    TRACK_ID = TrackID.NAKAYAMA

    def build_course(self, config: CourseConfig) -> Course:
        pass
