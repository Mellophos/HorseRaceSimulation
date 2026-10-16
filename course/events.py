# Path: horse-racing-sim/course\events.py
# events.py
from dataclasses import dataclass


@dataclass
class CourseEvent:
    """Base class for events that occur at a specific point on a racecourses.

    Each event is triggered at a specified distance from the start of the
    racecourses. Subclasses define the additional information associated with
    each type of course event.

    Attributes:
        trigger_location: Distance in metres from the start of the course
            at which the event takes effect.
    """
    trigger_location: int


@dataclass
class Corner(CourseEvent):
    """Represent a numbered corner on the racecourses.

    Notes:
        The corner model will be extended in the future to represent the
        direction of the turn and potentially use a different numbering
        system.

    Attributes:
        trigger_location: Marks the point where the corner begins.
        length: Specifies the length of the corner.

        corner_number: Identifies the corner's position in the course,
        numbered from 1 to 4.

    """
    corner_number: int
    length: int

    name = 'corner'
    event_id = 0

    def __post_init__(self):
        if not 1 <= self.corner_number <= 4:
            raise ValueError(
                f'Corner number {self.corner_number} out of range'
            )


@dataclass
class SurfaceChange(CourseEvent):
    """Represent a change in the surface of the racecourses.

    The surface change takes effect at ``trigger_location``. Currently,
    courses use this event to represent a transition from **turf to dirt**.

    Attributes:
        trigger_location: Distance in metres from the start of the course
            at which the new surface begins.

    Notes:
        This event currently does not store the new surface explicitly.
        The surface-transition model may be expanded in the future to
        support arbitrary surface changes.
    """
    name = 'surface_change'
    event_id = 1


@dataclass
class Straight(CourseEvent):
    """Represent the start or end of a straight section of the course.

    Each straight is represented by two events: one marking its beginning
    and another marking its end.

    Notes:
        This event will be revised to better suit non-Japanese racetracks,
        as not all tracks have only two straight sections. Revised
        implementation is being worked on.

    Attributes:
        straight_type: Identifies the type of straight:
            ``1`` for the home straight, ``2`` for the back straight, and
            ``3`` for a false straight.
        is_start: ``True`` if the event marks the beginning of the straight,
            or ``False`` if it marks the end.
    """
    straight_type: int
    is_start: bool

    name = 'straight'
    event_id = 2

    def __post_init__(self):
        if not 1 <= self.straight_type <= 3:
            raise ValueError(
                f'Straight type {self.straight_type} out of range'
            )


@dataclass
class LaneMaxChange(CourseEvent):
    """Represent a change to the maximum permitted lane value.

    At ``trigger_location``, the maximum permitted lane value changes to
    ``new_value``. The new value remains in effect until another
    ``LaneMaxChange`` event changes it.

    Notes:
        It is unclear whether this event affects the simulation at all.
    """
    new_value: float

    name = 'lane_max_change'
    event_id = 3


@dataclass
class MoveLanePoint(CourseEvent):
    """Represent a point associated with increased lane availability.

    At this point in the course, the race simulation allows horses to use
    an additional movement lane when available. This is particularly
    relevant to horses attempting to move around or overtake other horses.

    The exact behaviour represented by this event is based on an
    interpretation of observed Umamusume race simulation behaviour and
    may not correspond exactly to the underlying game's implementation.

    A ``MoveLanePoint`` may be explicitly defined at any location on a
    course. If a course contains one or more corners but does not define
    one explicitly, ``Course`` initialisation creates one at the
    start of the final corner.

    Notes:
        The relationship between this event, late-race lane availability,
        overtaking behaviour, and the final spurt is not fully established.
    """
    name = 'move_lane_point'
    event_id = 4


@dataclass
class Slope(CourseEvent):
    """Represent a sloped section of the racecourses.

    The slope begins at ``trigger_location`` and extends for ``length``
    metres. ``slope_percentage`` specifies the grade of the section,
    where positive values represent an uphill slope and negative values
    represent a downhill slope.

    Attributes:
        trigger_location: Distance in metres from the start of the course
            at which the slope begins.
        gradient: Gradient of the slope as a percentage.
        length: Length of the sloped section in metres.
    """
    gradient: float
    length: int

    name = 'slope'
    event_id = 5

    def __post_init__(self):
        if not -100 <= self.gradient <= 100:
            raise ValueError(
                f'Slope percentage {self.gradient} out of range'
            )


EVENT_TYPES = {
    event.event_id: event
    for event in (
        Corner,
        SurfaceChange,
        Straight,
        LaneMaxChange,
        MoveLanePoint,
        Slope,
    )
}


def create_event(*, event_id, trigger_location, **kwargs) -> CourseEvent:
    """Create a course event from its event ID.

    The event ID is used to select the appropriate ``CourseEvent``
    subclass from ``EVENT_TYPES``. Additional keyword arguments are passed
    directly to the selected event class.

    Args:
        event_id: Numeric ID identifying the type of course event.
        trigger_location: Distance along the course at which the event
            takes effect.
        **kwargs: Additional arguments required by the selected event type.

    Returns:
        An instance of the ``CourseEvent`` subclass associated with
        ``event_id``.

    Raises:
        ValueError: If ``event_id`` does not correspond to a known event
            type.
    """
    try:
        event_type = EVENT_TYPES[event_id]
    except KeyError:
        raise ValueError(f'Unknown event ID: {event_id}')

    return event_type(
        trigger_location=trigger_location,
        **kwargs
    )


PRIORITY = {
    Straight: 1,
    Corner: 2,
    MoveLanePoint: 3,
    Slope: 4,
    SurfaceChange: 5,
    LaneMaxChange: 6,
}