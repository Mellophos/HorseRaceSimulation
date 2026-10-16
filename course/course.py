# Path: horse-racing-sim/course\course.py
"""Define race courses and their event layouts.

This module contains the ``Course`` class, which describes the fixed
properties of a race course and its sequence of course events. It also
provides utilities for determining a course's distance category and
completing an event list with required events.
"""

from copy import deepcopy

from data_types import Surface, DistanceCategory, COURSE_WIDTH
from lookups import DISTANCE_CATEGORIES
from .events import CourseEvent, Corner, MoveLanePoint, PRIORITY


class Course:
    """Represent the fixed properties and event layout of a race course.

    A ``Course`` defines the surface and distance of a race, along with
    the sequence of ``CourseEvent`` objects that describe how the race
    progresses around the course.

    When an event list is provided, it is deep-copied before being
    completed. A required ``MoveLanePoint`` is added automatically when
    necessary.

    Attributes:
        name: Name of the course.
        surface: Surface on which the course is run.
        width: Width of the course in metres.
        distance: Length of the course in metres.
        distance_category: Distance category determined from the course
            distance.
        event_list: Ordered list of events that make up the course.
    """

    def __init__(
            self,
            name: str,
            surface: Surface,
            distance: int,
            course_width: float = 22.5,
            event_list: list[CourseEvent] | None = None
    ):
        """Initialise a race course.

        The distance category is determined automatically from the supplied
        distance. If a course event list is provided, it is deep-copied and
        completed with any required events without modifying the original
        list.

        Args:
            name: Name of the course.
            surface: Surface on which the course is run.
            distance: Length of the course in metres.
            course_width: Width of the course in metres, defaults to 22.5.
            event_list: Optional ordered list of course events. If omitted,
                the course is created with an empty event list.

        Raises:
            ValueError: If ``distance`` does not fall within one of the
                configured distance categories, or if an event list without
                a ``MoveLanePoint`` does not contain a ``Corner`` from which
                one can be created.
        """
        self.name = name
        self.surface = surface
        self.width = course_width / COURSE_WIDTH
        self.distance = distance
        self.distance_category = get_distance_category(distance)

        if event_list is None:
            self.event_list = []
            return
        self.event_list = complete_event_list(
            sorted(
                deepcopy(event_list), key=lambda e: (
                    e.trigger_location, PRIORITY.get(type(e), 99)
                )
            )
        )

    def __repr__(self):
        """Return a concise representation of the course.

        Returns:
            A string containing the course name, surface, distance,
            and event list if it exists.
        """
        return (
            f'{self.__class__.__name__}('
            f'name={self.name!r}, '
            f'surface={self.surface!r}, '
            f'distance={self.distance!r}, '
            f'event_list={self.event_list!r})'
        )


def get_distance_category(distance: int) -> DistanceCategory:
    """Determine the distance category for a course length.

    The configured ranges in ``DISTANCE_CATEGORIES`` are searched in order.
    The first range containing the supplied distance determines the
    resulting category.

    Args:
        distance: Course length in metres.

    Returns:
        The ``DistanceCategory`` corresponding to the supplied distance.

    Raises:
        ValueError: If the distance does not fall within any configured
            distance category.
    """
    for cat, (low, high) in DISTANCE_CATEGORIES.items():
        if low <= distance <= high:
            return cat
    else:
        raise ValueError('Distance out of categorisation range')


def complete_event_list(event_list: list[CourseEvent]) -> list[CourseEvent]:
    """Ensure a course event list contains a MoveLanePoint.

    A ``MoveLanePoint`` is required by the race simulation to represent
    the point at which additional lane movement becomes available.

    If a ``MoveLanePoint`` is already defined, the event list is returned
    unchanged. Otherwise, one is inserted at the
    ``trigger_location`` of the final defined corner.

    This automatic placement is a simulation convention: it allows
    courses with corners to omit an explicit ``MoveLanePoint`` while
    still providing one to the race simulation. Courses without corners
    must define their own ``MoveLanePoint``.

    Args:
        event_list: Ordered list of course events describing the
            layout of the racecourses.

    Returns:
        A new event list containing a ``MoveLanePoint``.

    Raises:
        ValueError: If no ``MoveLanePoint`` is defined and the course
            contains no ``Corner`` from which one can be created.
    """

    # course event list must contain MoveLanePoint for simulation to work well
    if any(isinstance(event, MoveLanePoint) for event in event_list):
        return event_list

    new_list = deepcopy(event_list)

    # Create MoveLanePoint after last corner
    for i in range(len(new_list) - 1, -1, -1):
        event = new_list[i]

        if isinstance(event, Corner):
            last_corner_index = i
            last_corner = event
            break
    else:
        raise ValueError(
            'At least one Corner must be present when no MoveLanePoint exists'
        )

    new_list.insert(
        last_corner_index + 1,
        MoveLanePoint(
            trigger_location=last_corner.trigger_location
        )
    )

    return new_list
