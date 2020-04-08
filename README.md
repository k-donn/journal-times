# Journal Entry Times

A visual representation of entries in a Day One journal.

## Usage

```
usage: python3.7 source/graph.py [-h] -f FILE [-d]

Display a graph of journal entries from Day One JSON

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to exported Day One JSON file
  -d, --debug           Show the plot instead of writing to file
```

## Running

To run from the root dir,

-   Create conda env from spec-file.txt (see [Install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html))
-   `pip` can also be configured with requirements.txt
-   Copy journal [JSON Export](#exporting-journal-json) into ./data or [create dummy data](#generate-dummy-data)
-   From the root of the folder,

```
python3.7 ./source/graph.py --file ./data/<JOURNAL>.json
```

## Generate Dummy Data

-   From the root of the foler,

```
python3.7 ./data/gen_dummy.py
```

-   Now, just pass in the new ./data/Dummy.json file to the program

## Exporting Journal JSON

See [Exporting Entries](https://help.dayoneapp.com/en/articles/440668-exporting-entries) for instructions.

Export as JSON and place file in ./data directory.

## Meta

I got the inspiration from seeing [jiuguangw](https://github.com/jiuguangw/)'s [Agenoria](https://github.com/jiuguangw/Agenoria)
