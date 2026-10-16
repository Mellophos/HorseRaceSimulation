# Path: horse-racing-sim/course\presets\__init__.py
# __init__.py

from .racecourses import *
from .preset_course import preset_course, TrackID

__all__ = [
    'TrackID',
    'RACECOURSES',
    'get_racecourse',
    'preset_course'
]