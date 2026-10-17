# Path: horse-racing-sim/course/presets/racecourses/__init__.py
"""Racecourse implementations and their registry.

Importing this package discovers and registers all racecourse implementations.
"""
import importlib
import pkgutil

from course.presets.config import TrackID
from course.presets.racecourse import Racecourse


def _load_racecourses():
    for module in pkgutil.walk_packages(
            __path__,
            prefix=f"{__name__}.",
    ):
        importlib.import_module(module.name)


def get_racecourse(track_id: TrackID) -> type[Racecourse]:
    try:
        return Racecourse.REGISTRY[track_id]
    except KeyError:
        raise ValueError(
            f"No racecourse registered for {track_id!r}"
        ) from None


_load_racecourses()

__all__ = ["get_racecourse"]
