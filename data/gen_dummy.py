"""
Generate dummy data to see how graphing works.

usage: python3.8 data/gen_dummy.py
"""
# TODO
# add output file option

import json
import sys
from datetime import datetime, timedelta
from random import choice, randint


def generate_entries():
    """Generate tags and dates for entries."""
    res = []
    curr_time = datetime.now()

    words = [
        "telefragged",
        "groundsheets",
        "rumina",
        "vigias",
        "chromatolysis",
        "predisposing",
        "goldenseal",
        "bladderwrack",
        "oxiconazole",
        "dition"]

    for _i in range(100):
        # generate between five to ten entries every day
        curr_time -= timedelta(days=1)
        for _j in range(randint(5, 10)):
            entry = {}

            entry["creationDate"] = curr_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            # five-ish to ten-ish hours between entries each day
            curr_time -= timedelta(hours=randint(5, 10),
                                   minutes=randint(0, 60),
                                   seconds=randint(0, 60))
            entry["tags"] = [choice(words)]
            res.append(entry)
    return res


def write_json(file_data):
    """Write the entries to the JSON file."""
    with open("data/Dummy.json", "w") as dummy:
        json.dump(file_data, dummy)


def main():
    """Generate dummy data."""
    entries = generate_entries()
    file_data = {"metadata": {"version": 1.0}, "entries": entries}
    write_json(file_data)


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__)
        exit(0)

    main()
