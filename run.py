"""
Display a graph of journal entries from Day One JSON.

usage: run.py [-h] -f FILE [-d]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to exported Day One JSON file
  -d, --debug           Show the plots instead of writing to file
"""

import argparse

import source

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Display a graph of journal entries from Day One JSON")
    parser.add_argument("-f", "--file", required=True,
                        help="Path to exported Day One JSON file")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Show the plots instead of writing to file")

    args = parser.parse_args()

    source.main(args.file, args.debug)
