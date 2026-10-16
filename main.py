# Path: horse-racing-sim/main.py
import json

from course.presets import preset_course
from data_types import GroundCondition, Surface
from horse import Horse, Entry
from race import Race
from simulation.simulator import RaceSimulator
from visualisation import str_results

if __name__ == '__main__':
    with open('data/horses.json') as f:
        d = json.load(f)
    horse_list = [Horse.from_dict(h) for h in d]
    entry_list = [
        Entry(horse, 'weighted', None)
        for horse in horse_list
    ]

    course = preset_course(10006, Surface.TURF, 1600)

    race = Race('Preview (C5)', course, entry_list, GroundCondition.FIRM)
    sim = RaceSimulator(race)

    sim.race.shuffle_runners()

    print(sim.race)

    sim.run()
    print(str_results(sim))
