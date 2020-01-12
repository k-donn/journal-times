# Journal Entry Times

A visual representation of each of the times an entry is made into a Day One journal.

## Running

To run from the root dir:

-   Create conda env from requirements.txt (see [Install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html))
-   Copy journal JSON export into ./data or use [Dummy.json](https://github.com/k-donn/journal-times/blob/master/data/gen-dummy.py)
-   From the root of the folder,

```
python3 ./source/graph.py --file ./data/<JOURNAL>.json
```

## Generate Dummy Data

-   From the root of the foler,

```
python3 ./data/gen_dummy.py
```

-   Now, just pass in the new ./data/Dummy.json file to the program

## Exporting Journal JSON

See [Exporting Entries](https://help.dayoneapp.com/en/articles/440668-exporting-entries) for instructions.

Export as JSON and place file in ./data directory.

## Meta

I got the inspiration from seeing [jiuguangw](https://github.com/jiuguangw/)'s [Agenoria](https://github.com/jiuguangw/Agenoria)
