# TODO
# 1. Put in README how to export Day One data

from typing import Type, Dict, List
from matplotlib.axes._subplots import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import FigureManagerQT

from matplotlib.dates import (
    HOURLY, WEEKLY, DateFormatter, rrulewrapper, RRuleLocator)
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import pytz
import json
import argparse

mpl.use("Qt5Agg")

parser = argparse.ArgumentParser(prog="python3.7 source/graph.py",
                                 description="Display a graph of journal entries from Day One JSON")
parser.add_argument("file", help="Path to exported Day One JSON file")

args = parser.parse_args()

with open(args.file, "r") as f:
    daily = json.load(f)

raw_dates: List[str] = [entry["creationDate"] for entry in daily["entries"]]

colors: List[str] = []
for entry in daily["entries"]:
    if "tags" in entry:
        tag = entry["tags"][0]
        if tag == "daily":
            colors.append("bo")
        elif tag == "dreams":
            colors.append("ro")
        else:
            colors.append("go")
    else:
        colors.append("go")

full_dates: List[Type[datetime.datetime]] = [datetime.datetime.strptime(
    raw_date, "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York")) for raw_date in raw_dates]


x_vals: List[float] = [mpl.dates.date2num(
    full_day.date()) for full_day in full_dates]
# Y-values get inverted for some time-zone related reason.
y_vals: List[float] = [
    (int(x_vals[0]) + abs(1.0 - (mpl.dates.date2num(full_day) % 1))) for full_day in full_dates]

combined_vals = [[x_val, y_val] for x_val, y_val in list(zip(x_vals, y_vals))]

combined_vals_color = []
for index, vals in enumerate(combined_vals):
    combined_vals_color.append({"color": colors[index], "values": vals})

# print(f"Color length: {len(colors)}")
# print(f"Vals length: {len(combined_vals)}")
# print(f"Combined both: {len(combined_vals_color)}")

x_rule: Type[rrulewrapper] = rrulewrapper(WEEKLY)
x_loc: Type[RRuleLocator] = RRuleLocator(x_rule)
x_formatter: Type[DateFormatter] = DateFormatter("%m/%d/%y")

y_rule: Type[rrulewrapper] = rrulewrapper(HOURLY)
y_loc: Type[RRuleLocator] = RRuleLocator(y_rule)
y_formatter: Type[DateFormatter] = DateFormatter("%H:%M:%S")


fig: Type[Figure] = plt.figure()
ax: Type[Axes] = fig.add_subplot(111)

X_VAL: int = 0
Y_VAL: int = 1

# ax.plot_date(x_vals, y_vals, "ro")
for point in combined_vals_color:
    color, values = point.items()
    ax.plot(point["values"][X_VAL], point["values"][Y_VAL], point["color"])

ax.xaxis_date()
# Pad the x on the left five in the past and pad the right five in the future
ax.set_xlim(left=(min(x_vals) - 5),
            right=(mpl.dates.date2num(datetime.datetime.now().date()) + 5))
ax.set_xlabel("Date", fontdict={"fontsize": 15})
ax.get_xaxis().set_major_locator(x_loc)
ax.get_xaxis().set_major_formatter(x_formatter)
ax.get_xaxis().set_tick_params(rotation=30)

ax.yaxis_date()
ax.set_ylim(bottom=int(y_vals[0]), top=int(y_vals[0]) + 1)
ax.set_ylabel("Time of day", fontdict={"fontsize": 15})
ax.get_yaxis().set_major_locator(y_loc)
ax.get_yaxis().set_major_formatter(y_formatter)
# Display morning on top and midnight on bottom. This is different than what
# we did at assigning `y_vals`
ax.invert_yaxis()

ax.set_title("Journal entry date/time of day",
             fontdict={"fontsize": 18}, pad=25)

figManager: [FigureManagerQT] = plt.get_current_fig_manager()
figManager.window.showMaximized()
figManager.set_window_title("Journal Entry times")

plt.grid(which="both", axis="both")

plt.show()
