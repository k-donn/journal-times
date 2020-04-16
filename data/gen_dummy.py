"""
Generate dummy data to see how graphing works.

usage: python3.7 data/gen_dummy.py
"""
import json
from datetime import datetime, timedelta
from random import randint

from random_word import RandomWords


def generate_entries():
    """Generate tags and dates for entries."""
    rand_words = RandomWords()
    res = []
    curr_day = datetime.now()
    avail_tags = rand_words.get_random_words(limit=randint(5, 10))
    for _i in range(100):
        # generate between two to five entries every day
        curr_day -= timedelta(days=1)
        for _j in range(randint(2, 5)):
            entry = {}

            entry["creationDate"] = curr_day.strftime("%Y-%m-%dT%H:%M:%SZ")
            # five-ish to ten-ish hours between entries each day
            curr_day -= timedelta(hours=randint(5, 10),
                                  minutes=randint(0, 60),
                                  seconds=randint(0, 60))
            entry["tags"] = []
            entry["tags"].append(avail_tags[randint(0, len(avail_tags) - 1)])
            res.append(entry)
    return res


def write_json(file_data):
    """Write the entries to the JSON file."""
    with open("data/Dummy.json", "w") as dummy:
        entries_str = json.dumps(file_data, indent=4, sort_keys=True)
        dummy.write(entries_str)


def main():
    """Generate dummy data."""
    entries = generate_entries()
    file_data = {"metadata": {"version": 1.0}, "entries": entries}
    write_json(file_data)


if __name__ == "__main__":
    main()
