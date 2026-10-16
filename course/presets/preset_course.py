# Path: horse-racing-sim/course\presets\preset_course.py
from pprint import pprint

from course.presets.config import TrackID, CourseConfig
from course.presets.racecourses import get_racecourse
from data_types import Surface


def preset_course(
        track_id: TrackID | int,
        surface: Surface,
        distance: int,
        layout: str | None = None
):
    """Get a preset ``Course`` from given configurations.

    Args:
        track_id: A valid ID of a racetrack
        surface: Surface of the desired course
        distance: Distance of the desired course
        layout: The specific layout of the course, if multiple layouts are
            availabe for a given track, surface, and distance. Defaults to
            ``None``.

            For example, Kyoto has both inner and outer configurations for
            T1400m. You would need to specify which specific configuration
            you want.

            >>> preset_course(TrackID.KYOTO, Surface.TURF, 1400,
            ...               layout="inner")

            For consistency, layouts generally use ``"inner"``, ``"outer"``,
            or ``"straight"``. Layouts with well-established names will use
            those instead. For example, the Newmarket July Course is
            selected with ``layout="july"``.

    Returns:
        A ``Course`` object containing the given specifications

    Raises:
        ValueError: If ``track_id`` is invalid, or no matching course
            configuration is found.
    """
    if isinstance(track_id, int):
        try:
            track_id = TrackID(track_id)
        except ValueError:
            raise ValueError(f"Invalid track id: {track_id}") from None

    racecourse = get_racecourse(track_id)

    return racecourse().build_course(
        CourseConfig(
            track=track_id,
            surface=surface,
            distance=distance,
            layout=layout
        )
    )


# Testing
if __name__ == '__main__':
    course = preset_course(
        TrackID.TOKYO,
        Surface.TURF,
        1400
    )

    print(
        f"{course.name}  {course.surface.name.capitalize()}  "
        f"{course.distance}m ({course.distance_category.name.capitalize()})"
    )
    pprint(course.event_list)
    print()
    track = get_racecourse(TrackID.TOKYO)
    pprint(track().turf.events_until(1400))
