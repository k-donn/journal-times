"""
Generate dummy data to see how graphing works.

usage: python3.8 data/gen_dummy.py
"""
# TODO
# Add try/catch for existance of words file
import json
from datetime import datetime, timedelta
from random import randint


def generate_entries():
    """Generate tags and dates for entries."""
    res = []
    curr_day = datetime.now()

    words = []
    file = "/usr/share/dict/words"
    indices = [randint(0, 50000) for i in range(10)]
    with open(file) as raw_words:
        for i, line in enumerate(raw_words):
            if i in indices:
                words.append(line.strip())

    for _i in range(100):
        # generate between five to ten entries every day
        curr_day -= timedelta(days=1)
        for _j in range(randint(5, 10)):
            entry = {}

            entry["creationDate"] = curr_day.strftime("%Y-%m-%dT%H:%M:%SZ")
            # five-ish to ten-ish hours between entries each day
            curr_day -= timedelta(hours=randint(5, 10),
                                  minutes=randint(0, 60),
                                  seconds=randint(0, 60))
            entry["tags"] = []
            entry["tags"].append(words[randint(0, len(words) - 1)])
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
    main()
