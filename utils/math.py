# Path: horse-racing-sim/utils\math.py
import math


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value to an inclusive range.

    Args:
        value: The value to clamp.
        minimum: The lower bound.
        maximum: The upper bound.

    Returns:
        The value constrained to [minimum, maximum].

    Raises:
        ValueError: If ``minimum`` > ``maximum``.
    """
    if minimum > maximum:
        raise ValueError("minimum must be <= maximum.")
    return max(min(value, maximum), minimum)


def linear_soft_cap(
        x: float,
        cap: float,
        excess_factor: float = 1.0
) -> float:
    """Reduce the excess above a cap by a configurable factor.

    Args:
        x: The input value.
        cap: The threshold above which excess is reduced.
        excess_factor: The fraction of excess to retain, in [0, 1].

    Returns:
        The input value if x <= cap, otherwise, the cap plus the specified
        fraction of the excess.

    Raises:
        ValueError: If excess_factor is outside [0, 1].
    """
    if not 0 <= excess_factor <= 1:
        raise ValueError("excess_factor must be between 0 and 1.")
    return x if x <= cap else cap + (x - cap) * excess_factor


def bracket(post_position, max_runners) -> int:
    """Calculate the bracket number for a horse's post position.

    When there are fewer than eight runners, the bracket number is the same
    as the post position. With eight or more runners, post positions are
    distributed across eight brackets.

    Args:
        post_position: The horse's post position.
        max_runners: Total number of runners in the race.

    Returns:
        The calculated bracket number.
    """
    return math.ceil(
        (post_position * 8) / max_runners
    ) if (max_runners >= 8) else post_position


def lerp(v0: float, v1: float, t: float) -> float:
    """Linearly interpolate between two values.

    Args:
        v0: The starting value.
        v1: The ending value.
        t: The interpolation factor. Values outside [0, 1] perform linear
            extrapolation.

    Returns:
        The interpolated value as a float if ``inverse=False``.
        The fractional position (t) as a float if ``inverse=True``.
    """
    return v0 + t * (v1 - v0)


def inverse_lerp(v0: float, v1: float, value: float) -> float:
    """Calculate the fractional position of a value within a range.

    Args:
        v0: The starting value of the range.
        v1: The ending value of the range.
        value: The value whose fractional position is calculated.

    Returns:
        The fractional position of the value within the range.
        Values outside the range produce results outside [0, 1].

    Raises:
        ZeroDivisionError: If v0 and v1 are equal.
    """
    if v0 == v1:
        raise ZeroDivisionError("Cannot perform inverse lerp when v0 == v1.")
    return (value - v0) / (v1 - v0)


def to_metres(
        miles: float | int = 0,
        furlongs: float | int = 0,
        yards: float | int = 0,
        round_result: bool = False
) -> float:
    """Convert imperial distances to metres.

    The exact conversion factors are:
        - 1 mile: 1760 yards
        - 1 furlong: 220 yards
        - 1 yard: 0.9144 metres

    Args:
        miles: Distance in miles
        furlongs: Distance in furlongs
        yards: Distance in yards
        round_result: Whether to round off to nearest integer. Halfway
            floats are rounded up
    """
    total_yards = (miles * 1760) + (furlongs * 220) + yards
    metres = total_yards * 0.9144

    if round_result:
        return math.floor(metres + 0.5)
    return metres
