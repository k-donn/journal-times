# TODO
# 1. Use a cmd paramter for data filename
# 2. Color dots based on entry type
# 3. Ascertain Chuthulu and fix Qt backend import issue
# 4. Put in README how to export Day One data

from typing import Type, Dict, List
from matplotlib.axes._subplots import Axes
from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5 import FigureManagerQT

from matplotlib.dates import (
    MONTHLY, DateFormatter, rrulewrapper, RRuleLocator)
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import pytz
import json
import argparse

parser = argparse.ArgumentParser(prog="python3.7 source/graph.py",
    description="Display a graph of journal entries from Day One JSON")
parser.add_argument("file", help="Path to exported Day One JSON file")

args = parser.parse_args()

with open(args.file, "r") as f:
    daily = json.load(f)

raw_dates: List[str] = [entry["creationDate"] for entry in daily["entries"]]

full_dates: List[Type[datetime.datetime]] = [datetime.datetime.strptime(
    raw_date, "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York")) for raw_date in raw_dates]


days: List[float] = [mpl.dates.date2num(
    full_day.date()) for full_day in full_dates]
# Y-values get inverted for some time-zone related reason.
y_vals: List[float] = [
    (int(days[0]) + abs(1.0 - (mpl.dates.date2num(full_day) % 1))) for full_day in full_dates]

x_rule: Type[rrulewrapper] = rrulewrapper(MONTHLY)
x_loc: Type[RRuleLocator] = RRuleLocator(x_rule)
x_formatter: Type[DateFormatter] = DateFormatter("%m/%d/%y")

y_formatter: Type[DateFormatter] = DateFormatter("%H:%M:%S")


fig: Type[Figure] = plt.figure()
ax: Type[Axes] = fig.add_subplot(111)

ax.plot_date(days, y_vals, "ro")
ax.xaxis_date()
ax.set_xlabel("Date", fontdict={"fontsize": 15})
ax.get_xaxis().set_major_locator(x_loc)
ax.get_xaxis().set_major_formatter(x_formatter)
ax.get_xaxis().set_tick_params(rotation=30)

ax.yaxis_date()
ax.set_ylabel("Time of day", fontdict={"fontsize": 15})
ax.get_yaxis().set_major_formatter(y_formatter)
# Display morning on top and midnight on bottom. This is different than what
# we did at assigning `y_vals`
ax.invert_yaxis()

ax.set_title("Journal entry date/time of day",
             fontdict={"fontsize": 18}, pad=25)

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
figManager.set_window_title("Journal Entry times")


plt.show()
