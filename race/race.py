# Path: horse-racing-sim/race\race.py
from copy import deepcopy
from dataclasses import dataclass
from random import shuffle, choice

from course import Course
from data_types import GroundCondition, HORSE_LANE, Strategy, Mood
from horse import Entry, RaceEntry, HorseState
from simulation.mechanics.hp import calculate_max_hp
from utils import bracket


@dataclass
class Runner:
    """Represents a horse participating in a race.

    A ``Runner`` combines the horse's race-specific entry information with
    its mutable state during the race.

    Attributes:
        entry: The race-specific information for the horse, including its
            selected strategy and mood.
        state: The horse's mutable state during the race, including its
            position, health, and movement information.
    """
    entry: RaceEntry
    state: HorseState


class Race:
    """Represents a race and its participating runners.

    A ``Race`` owns a copy of the supplied course and entries and uses them
    to create the runners that participate in the race. The race also stores
    the ground condition under which it is run.

    A race can be reset after simulation so that the same race configuration
    can be used for another simulation, optionally with different entries,
    runner order, ground conditions, or moods.

    Attributes:
        name: The name of the race.
        course: A deep copy of the course on which the race is run.
        ground_condition: The ground condition for the race.
        runners: The runners currently participating in the race.

    Args:
        name: Name of the race.
        course: Course on which the race is run.
        entry_list: Entries used to initialise the race's runners.
        ground_condition: Ground condition for the race. If ``None``, a
            ground condition is selected at random.
    """

    def __init__(
            self, name: str,
            course: Course,
            entry_list: list[Entry],
            ground_condition: GroundCondition | None = None
    ):
        """Initialise a race and create its runners.

        The supplied course and entry list are deep-copied so that changes
        made to the race do not directly modify the original objects.

        Args:
            name: Name of the race.
            course: Course on which the race is run.
            entry_list: Entries used to initialise the race's runners.
            ground_condition: Ground condition for the race. If ``None``, a
                ground condition is selected at random.
        """
        self.name = name
        self.course = deepcopy(course)

        self._entry_list = deepcopy(entry_list)

        if ground_condition is None:
            self.randomise_ground_condition()
        else:
            self.ground_condition = ground_condition

        self.runners = create_runner_objects(
            self._entry_list,
            self.course,
            self.ground_condition
        )

    def __str__(self):
        """Return a human-readable summary of the race.

        The summary includes the race name, course information, ground
        condition, and each runner's post position, horse name, strategy,
        and mood.

        Returns:
            A formatted string containing the race summary.
        """
        result = [
            '',
            self.name,
            f'{self.course.name}  '
            f'{self.course.surface.name.capitalize()}  '
            f'{self.course.distance}m ('
            f'{self.course.distance_category.name.capitalize()})  '
            f'{self.ground_condition.name.capitalize()}',
            '[BK][PP] HORSE............. -> | STRAT | MOOD   | '
        ]
        for i, runner in enumerate(self.runners, start=1):
            result.append(
                f'[{bracket(i, len(self.runners)):<2}][{i:<2}] '
                f'{runner.entry.horse.name:.<18} -> | '
                f'{runner.entry.strategy.name.capitalize():<5} | '
                f'{runner.entry.mood.name.capitalize():<6} | '
            )
        return '\n'.join(result)

    def __repr__(self):
        """Return an unambiguous representation of the race.

        The representation includes the race name, course name, and number
        of runners without including the complete runner state.

        Returns:
            A string representation suitable for debugging.
        """
        return (
            f'{type(self).__name__}('
            f'name={self.name!r}, '
            f'course={self.course.name!r}, '
            f'runners={len(self.runners)})'
        )

    def reset(
            self, *,
            new_entry_list: list[Entry] | None = None,
            shuffle_runners: bool = False,
            change_ground_condition: bool = False,
            change_moods: bool = False
    ) -> None:
        """Reset the race so that it can be simulated again.

        The existing course is retained while new runner objects are
        created from the current or newly supplied entries. Optional
        arguments can change the entries, runner order, ground condition,
        or moods before the next simulation.

        If ``new_entry_list`` is provided, ``change_moods`` is ignored
        because the moods are taken from the supplied entries.

        Args:
            new_entry_list: Optional replacement list of entries. If
                provided, the current entries are replaced.
            shuffle_runners: If ``True``, randomly shuffle the order of the
                newly created runners.
            change_ground_condition: If ``True``, randomly select a new
                ground condition.
            change_moods: If ``True`` and ``new_entry_list`` is not provided,
                randomly select a new mood for each existing entry.

        Returns:
            ``None``.
        """
        if new_entry_list is not None:
            self._entry_list = deepcopy(new_entry_list)

        if change_ground_condition:
            self.randomise_ground_condition()

        if change_moods and new_entry_list is None:
            for i, entry in enumerate(self._entry_list):
                self._entry_list[i].mood = choice(list(Mood))

        self.runners = []
        self.runners = create_runner_objects(
            self._entry_list,
            self.course,
            self.ground_condition,
        )

        if shuffle_runners:
            self.shuffle_runners()

    def randomise_ground_condition(self) -> None:
        """Randomly select and assign a ground condition.

        The selected condition is taken from the available
        ``GroundCondition`` enum values.

        Returns:
            ``None``.
        """
        self.ground_condition = choice(list(GroundCondition))

    def shuffle_runners(self) -> None:
        """Randomly shuffle the order of the race's runners.

        The existing ``Runner`` objects are retained; only their order in
        ``self.runners`` is changed.

        Returns:
            ``None``.
        """
        shuffle(self.runners)

    # Might move to different module
    def get_race_order(self) -> list[Runner]:
        return sorted(self.runners,
                      key=lambda runner: runner.state.position.distance,
                      reverse=True)

    # Might move to different module
    def get_strategy_order(self, strategy: Strategy) -> list[Runner]:
        same_strat_runners = [
            r for r in self.runners
            if r.entry.strategy == strategy
        ]

        return sorted(
            same_strat_runners,
            key=lambda runner: runner.state.position.distance,
            reverse=True
        )

    # Might move to different module
    def get_runner_behind(self, runner: Runner) -> Runner:
        order = self.get_race_order()

        try:
            return order[order.index(runner) + 1]
        except (ValueError, IndexError):
            raise IndexError(f'Runner {runner} not in race order or is last')

    # Might move to different module
    def get_strategy_position(self, runner: Runner) -> int:
        order = self.get_strategy_order(runner.entry.strategy)

        return order.index(runner)

    # Might move to different module
    def get_pacemaker(self) -> Runner:
        strat_order = self.get_strategy_order(
            Strategy(min(
                (r.entry.strategy for r in self.runners),
                key=lambda x: x.value)
            )
        )
        return strat_order[0]


def create_runner_objects(
        entry_list: list[Entry],
        course: Course,
        ground_condition: GroundCondition,
) -> list[Runner]:
    """Create runners from a list of race entries.

    Each entry is converted into a ``RaceEntry`` using the supplied course
    and ground condition. A corresponding ``HorseState`` is then created
    for each race entry. The resulting entry and state are combined into a
    ``Runner``.

    The order of the returned runners matches the order of ``entry_list``.

    Args:
        entry_list: Entries describing the horses participating in the race.
        course: Course on which the race is being run.
        ground_condition: Ground condition for the race.

    Returns:
        A list of initialised ``Runner`` objects.
    """
    runners = []

    entries = [
        initialise_race_entry(entry, course, ground_condition)
        for entry in entry_list
    ]
    horse_states = [initialise_horse_state(i, entry, course) for i, entry in
                    enumerate(entries, start=1)]

    for entry, state in zip(entries, horse_states):
        runners.append(Runner(entry, state))
    return runners


def initialise_race_entry(
        entry: Entry,
        course: Course,
        ground_condition: GroundCondition
) -> RaceEntry:
    """Create a race-specific entry from an Entry and race conditions.

    This function delegates race-entry creation to
    ``RaceEntry.from_entry()``.

    Args:
        entry: The horse, strategy, and mood selected for the race.
        course: Course on which the race is being run.
        ground_condition: Ground condition for the race.

    Returns:
        A ``RaceEntry`` containing the horse's race-specific aptitudes
        and calculated stats.
    """
    return RaceEntry.from_entry(entry, course, ground_condition)


def initialise_horse_state(post_position: int, race_entry: RaceEntry,
                           course: Course) -> HorseState:
    """Create the initial state of a horse entering a race.

    The horse's maximum health is calculated from its race entry and the
    course distance. Its starting lane is calculated from its post position.
    Distance travelled starts at zero, health starts at maximum health,
    and movement starts with a target speed of 3 and a current speed of 3.

    Args:
        post_position: The horse's starting post position.
        race_entry: Race-specific entry information for the horse.
        course: Course on which the race is being run.

    Returns:
        A ``HorseState`` containing the horse's initial position, health,
        and movement state.
    """
    horse_state_dict = {}
    max_hp = calculate_max_hp(race_entry, course.distance)
    start_lane = calculate_start_lane(post_position)

    horse_state_dict['position'] = {
        'distance': 0,
        'lane': start_lane
    }
    horse_state_dict['health'] = {
        'max_hp': max_hp,
        'hp': max_hp
    }
    horse_state_dict['movement'] = {
        'target_speed': 3,
        'current_speed': 3
    }
    return HorseState.from_dict(horse_state_dict)


# Might move to different module
def calculate_start_lane(post_position: int) -> float:
    """Calculate the starting lane for a horse.

    Horses in post positions below 10 start at a lane calculated directly
    from their post position and ``HORSE_LANE``. Post positions of 10 or
    greater receive an additional adjustment of ``0.6``.

    Args:
        post_position: The horse's post position.

    Returns:
        The calculated starting lane as a numeric value.
    """
    if post_position >= 10:
        adjuster = 0.6
    else:
        adjuster = 0
    return post_position * HORSE_LANE + adjuster
