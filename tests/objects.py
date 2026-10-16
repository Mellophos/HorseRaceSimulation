# Path: horse-racing-sim/tests\objects.py
# objects.py
from course.course import Course
from course.events import create_event
from data_types import Surface, Grade, DistanceCategory, Strategy, Mood, \
    GroundCondition
from horse.horse import Horse, Aptitude, Stats
from horse.race_entry import Entry, RaceEntry
from horse.state import HorseState
from race.race import Race
from simulation.mechanics.hp import calculate_max_hp

# Nakayama T2500(Inner)
test_event_list = [
    create_event(event_id=0, trigger_location=100, corner_number=3,
                 length=146),
    create_event(event_id=0, trigger_location=246, corner_number=4,
                 length=250),
    create_event(event_id=2, trigger_location=496, straight_type=1,
                 is_start=True),
    create_event(event_id=5, trigger_location=621, gradient=2,
                 length=110),
    create_event(event_id=5, trigger_location=825, gradient=1.5,
                 length=200),
    create_event(event_id=2, trigger_location=875, straight_type=1,
                 is_start=False),
    create_event(event_id=0, trigger_location=875, corner_number=1,
                 length=250),
    create_event(event_id=0, trigger_location=1125, corner_number=2,
                 length=250),
    create_event(event_id=5, trigger_location=1125, gradient=-1.5,
                 length=400),
    create_event(event_id=2, trigger_location=1375, straight_type=2,
                 is_start=True),
    create_event(event_id=2, trigger_location=1700, straight_type=2,
                 is_start=False),
    create_event(event_id=0, trigger_location=1700, corner_number=3,
                 length=250),
    create_event(event_id=0, trigger_location=1950, corner_number=4,
                 length=240),
    create_event(event_id=2, trigger_location=2190, straight_type=1,
                 is_start=True),
    create_event(event_id=5, trigger_location=2325, gradient=2,
                 length=110),
    create_event(event_id=2, trigger_location=2500, straight_type=1,
                 is_start=False),
]

test_course = Course(
    'Test',
    Surface.TURF,
    1000,
    event_list=test_event_list
)

test_horse = Horse(
    name='Special Week',
    aptitude=Aptitude(
        surface={
            Surface.TURF: Grade.A,
            Surface.DIRT: Grade.G,
        },
        distance={
            DistanceCategory.SPRINT: Grade.F,
            DistanceCategory.MILE: Grade.C,
            DistanceCategory.INTERMEDIATE: Grade.A,
            DistanceCategory.LONG: Grade.A,
            DistanceCategory.EXTENDED: Grade.A
        },
        strategy={
            Strategy.FRONT: Grade.G,
            Strategy.PACE: Grade.A,
            Strategy.LATE: Grade.A,
            Strategy.END: Grade.C
        }
    ),
    stats=Stats(
        speed=102,
        stamina=108,
        power=120,
        guts=110,
        wit=110
    )
)

test_entry = Entry(
    horse=test_horse,
    strategy=Strategy.FRONT,
    mood=Mood.NORMAL
)

test_race_entry = RaceEntry.from_entry(
    test_entry,
    test_course,
    GroundCondition.FIRM
)

test_horse_state = HorseState.from_dict(
    {
        'position': {
            'distance': 0,
            'lane': 0
        },
        'health': {
            'max_hp': calculate_max_hp(test_race_entry, test_course.distance),
            'hp': calculate_max_hp(test_race_entry, test_course.distance)
        },
        'movement': {
            'target_speed': 3,
            'current_speed': 3
        }
    }
)

test_race = Race(
    'Test',
    test_course,
    [
        Entry(test_horse, Strategy.FRONT, None),
        Entry(test_horse, Strategy.FRONT, None),
        Entry(test_horse, Strategy.PACE, None),
        Entry(test_horse, Strategy.PACE, None),
        Entry(test_horse, Strategy.LATE, None),
        Entry(test_horse, Strategy.LATE, None),
        Entry(test_horse, Strategy.END, None),
        Entry(test_horse, Strategy.END, None),
    ],
    GroundCondition.FIRM
)
