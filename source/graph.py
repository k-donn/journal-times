# TODO
# 1. Refactor color mapping into point creation
#   - Basically, go through all of the entries one by one
#   - Get the tag and date for that entry
#   - Have a seperate calc_color that makes the color_map
#   - Use that color map directly in iterating over entries
#   - No need to keep track of temp lists that rely on order
# 2. Put in README how to export Day One data

# Types
from typing import Type, Dict, List, Tuple, Set
from matplotlib.axes._subplots import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.lines import Line2D
from matplotlib.legend import Legend

# Actually used
from matplotlib.dates import (
    HOURLY, WEEKLY, DateFormatter, rrulewrapper, RRuleLocator)
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import pytz
import json
import argparse

_colors: List[str] = ["b", "g", "r", "c", "m"]


def parse_entries(full_json):
    parsed_entries = []
    color_map: Dict[str, str] = calc_color_map(full_json)
    x_0 = mpl.dates.date2num(datetime.datetime.strptime(
        full_json["entries"][0]["creationDate"], "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York")))
    for entry in full_json["entries"]:
        entry_info = {}
        date = datetime.datetime.strptime(
            entry["creationDate"], "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York"))
        x_val = mpl.dates.date2num(date.date())
        y_val = int(x_0) + abs(1.0 - (mpl.dates.date2num(date) % 1))
        tag: str = ""
        if "tags" in entry:
            tag = entry["tags"][0]
        else:
            tag = "none"
        entry_info = {"color": color_map[tag], "values": [x_val, y_val]}
        parsed_entries.append(entry_info)
    return parsed_entries, x_0


def calc_color_map(full_json):
    entries: List[str] = [entry for entry in full_json["entries"]]
    avail_tags: List[str] = find_tags(entries)

    avail_tags.append("none")
    _colors.append("k")

    # print(dict(zip(avail_tags, _colors)))
    return dict(zip(avail_tags, _colors))


def calc_colors(entries: List[str]) -> List[str]:
    res: List[str] = []
    avail_tags: List[str] = find_tags(entries)

    color_map: Dict[str, str] = dict(zip(avail_tags, _colors))
    for entry in entries:
        if "tags" in entry:
            res.append(color_map[entry["tags"][0]])
        else:
            res.append("k")
    return res


def find_tags(entries: List[str]) -> List[str]:
    avail_tags = set()

    for entry in entries:
        if "tags" in entry:
            avail_tags.add(entry["tags"][0])

    return sorted(avail_tags)


def plot_values(ax: Type[Axes], points_colors: List[Dict[str, str]]) -> List[Line2D]:
    X_VAL: int = 0
    Y_VAL: int = 1

    lines: List[Line2D] = [ax.plot_date(point["values"][X_VAL], point["values"]
                                        [Y_VAL], f"{point['color']}o", label=point["color"]) for point in points_colors]

    return lines


def format_x_axis(ax: Type[Axes], x_0) -> None:
    ax.xaxis_date()
    # Pad the x on the left five in the past and pad the right five in the future
    ax.set_xlim(left=(x_0 - 5),
                right=(mpl.dates.date2num(datetime.datetime.now().date()) + 5))
    ax.set_xlabel("Date", fontdict={"fontsize": 15})

    x_rule: Type[rrulewrapper] = rrulewrapper(WEEKLY)
    x_loc: Type[RRuleLocator] = RRuleLocator(x_rule)
    x_formatter: Type[DateFormatter] = DateFormatter("%m/%d/%y")

    ax.get_xaxis().set_major_locator(x_loc)
    ax.get_xaxis().set_major_formatter(x_formatter)
    ax.get_xaxis().set_tick_params(rotation=30)


def format_y_axis(ax: Type[Axes], bottom: int, top: int) -> None:
    ax.yaxis_date()
    ax.set_ylim(bottom=bottom, top=top)
    ax.set_ylabel("Time of day", fontdict={"fontsize": 15})

    y_rule: Type[rrulewrapper] = rrulewrapper(HOURLY)
    y_loc: Type[RRuleLocator] = RRuleLocator(y_rule)
    y_formatter: Type[DateFormatter] = DateFormatter("%H:%M:%S")

    ax.get_yaxis().set_major_locator(y_loc)
    ax.get_yaxis().set_major_formatter(y_formatter)

    # Display morning on top and midnight on bottom. This is different than what
    # we did at assigning `y_vals`
    ax.invert_yaxis()


def format_figure(figManager: Type[FigureManagerQT]) -> None:
    figManager.window.showMaximized()
    figManager.set_window_title("Journal Entry times")


def format_plot(plt) -> None:
    plt.grid(which="both", axis="both")


def add_legend(plt, color_map: Dict[str, str]) -> Type[Legend]:
    lines: List[Line2D] = []

    tags = list(color_map.keys())
    tag_color_list = map(list, color_map.items())
    for tag, color in tag_color_list:
        lines.append(Line2D([], [], color=color, label=tag,
                            marker="o", linestyle="none"))

    return plt.legend(lines, tags)


if __name__ == "__main__":
    mpl.use("Qt5Agg")

    parser = argparse.ArgumentParser(prog="python3.7 source/graph.py",
                                     description="Display a graph of journal entries from Day One JSON")
    parser.add_argument("file", help="Path to exported Day One JSON file")

    args = parser.parse_args()

    with open(args.file, "r") as f:
        full_json = json.load(f)

    points, x_0 = parse_entries(full_json)

    fig: Type[Figure] = plt.figure()
    ax: Type[Axes] = fig.add_subplot(111)

    plot_values(ax, points)

    format_x_axis(ax, x_0)
    format_y_axis(ax, int(x_0), int(x_0) + 1)

    ax.set_title("Journal entry date/time of day",
                 fontdict={"fontsize": 18}, pad=25)

    figManager: [FigureManagerQT] = plt.get_current_fig_manager()
    format_figure(figManager)

    color_map: Dict[str, str] = calc_color_map(full_json)
    add_legend(plt, color_map)
    format_plot(plt)

    plt.show()
