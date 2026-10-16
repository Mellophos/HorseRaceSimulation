# Path: horse-racing-sim/utils\__init__.py

from .math import *
from .race_phase import *

__all__ = [
    'clamp',
    'linear_soft_cap',
    'bracket',
    'lerp',
    'inverse_lerp',
    'section_boundaries',
    'get_current_section',
    'phase_boundaries',
    'get_current_phase'
]
