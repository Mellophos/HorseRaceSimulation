# Path: horse-racing-sim/course\presets\__init__.py
from .preset_course import preset_course, TrackID
from .racecourses import *

__all__ = [
    'TrackID',
    'get_racecourse',
    'preset_course'
]
