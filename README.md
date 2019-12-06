# Journal Entry Times
A visual representation of each of the times an entry is made into a Day One journal.

## Running
To run from the root dir:
- Create conda env from requirements.txt (see [Install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html))
- Copy journal JSON export into ./data
- From the root of the folder,
```
python3 ./source/graph.py ./data/<DIARY>.json
```
- If there are any errors, they are most likely backend related.
- Adjust code to use whatever backend you have on your system (project is Qt5Agg)

## Exporting Date JSON

See [Exporting Entries](https://help.dayoneapp.com/en/articles/440668-exporting-entries) for instructions.

Export as JSON and place file in ./data directory.

## Meta
I got the inspiration from seeing [jiuguangw](https://github.com/jiuguangw/)'s [Agenoria](https://github.com/jiuguangw/Agenoria)