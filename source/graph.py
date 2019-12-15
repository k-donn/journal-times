# TODO
# Document functions

# Types
from typing import Type, Dict, List, Tuple, Set, Union
from matplotlib.axes._subplots import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.lines import Line2D
from matplotlib.legend import Legend

# Actually used
from matplotlib.dates import (
    HOURLY, WEEKLY, DateFormatter, rrulewrapper, RRuleLocator)
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import pytz
import json
import argparse

# Mapping of tag names to unique colors
ColorMap = Dict[str, Tuple[float, float, float, float]]
# Properties of a JSON entry
Entry = Dict[str, str]
# Represents a point's color and x & y values
PointColorVal = Dict[str, Union[str, float]]


def extract_json(fname):
    """
    Extract JSON from supplied Day One journal export.

    Parameters
    ----------
    fname: `string` path to file

    Returns
    -------

    Nested dictionary object with Day One JSON properties
    """
    with open(fname, "r") as f:
        full_json = json.load(f)
    return full_json


def parse_entries(full_json) -> Tuple[List[PointColorVal], float]:
    """
    Calculate datetime info, primary tag, and respective color for
    each entry in the Day One export.

    Parameters
    ----------
    full_json: `dict`
        extracted JSON file

    Returns
    -------
    `Tuple` with list and float
        Represents parsed info about entries and earliest date of entry
    """
    parsed_entries: List[PointColorVal] = []
    color_map: ColorMap = calc_color_map(full_json)
    x_0: float = mpl.dates.date2num(str_to_date(
        full_json["entries"][0]["creationDate"]))
    for entry in full_json["entries"]:
        entry_info: PointColorVal = {}
        date = str_to_date(entry["creationDate"])
        x_val = mpl.dates.date2num(date.date())
        y_val = int(x_0) + abs(1.0 - (mpl.dates.date2num(date) % 1))
        tag: str = ""
        if "tags" in entry:
            tag = entry["tags"][0]
        else:
            tag = "none"
        entry_info = {"color": color_map[tag],
                      "x_value": x_val, "y_value": y_val}
        parsed_entries.append(entry_info)
    return (parsed_entries, x_0)


def str_to_date(date_str: str) -> datetime.datetime:
    """
    Convert a string in Day One format to a datetime object.

    Parameters
    ----------
    date_str: `str`
        String from an entry in JSON

    Returns
    -------
    `datetime.datetime`
        Parsed datetime object
    """
    return datetime.datetime.strptime(
        date_str, "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York"))


def calc_color_map(full_json) -> ColorMap:
    """
    Create a dictionary to map unique tags to unique colors.

    Parameters
    ----------
    full_json: `dict`

    Returns
    -------
    dictionary of str keys and tuple values
        Each tag's respective color
    """
    entries: List[Entry] = [entry for entry in full_json["entries"]]
    avail_tags: List[str] = find_tags(entries)

    color_map: ColorMap = {}

    minima = 0
    maxima = len(avail_tags)

    norm: colors.Normalize = colors.Normalize(
        vmin=minima, vmax=maxima, clip=True)
    # Intellisense can't find any of the color-map members part of cm
    mapper: cm.ScalarMappable = cm.ScalarMappable(
        norm=norm, cmap=cm.hsv)  # pylint: disable=no-member

    color_map = {tag: mapper.to_rgba(index)
                 for index, tag in enumerate(avail_tags)}

    color_map["none"] = (0.0, 0.0, 0.0, 1.0)

    return color_map


def find_tags(entries: List[Dict[str, str]]) -> List[str]:
    """
    Find all unique and primary, that which is first in the `tags` property, in entries.

    Parameters
    ----------
    entries: `list` of `dict`
        Entries property of exported JSON

    Returns
    -------
    `list` of `str`
        List of tags

    Notes
    -----
    The returned list is sorted in order to get the same mapping every single time given
    the same exported JSON
    """

    avail_tags: List[str] = []

    avail_tags = [entry["tags"][0] for entry in entries if "tags" in entry]

    # Sort them to get the same color-mapping each time
    return sorted(list(set(avail_tags)))


def plot_values(ax: Axes, points: List[PointColorVal]) -> List[Line2D]:
    """
    Plot points representing day v. time of day

    Parameters
    ----------
    ax: `Axes`
        The Axes object describing the graph
    points: `list` of point info
        List of dicts that represent each entry's day and time of day

    Returns
    -------
    `list` of `Line2D` objects
        The returned objects from the matplotlib plotting function
    """
    lines: List[Line2D] = [ax.plot_date(point["x_value"], point["y_value"],
                                        fmt="o", label=point["color"], color=point["color"]) for point in points]

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


def format_figure(figManager: FigureManagerQT) -> None:
    figManager.window.showMaximized()
    figManager.set_window_title("Journal Entry times")


def format_plot(plt: mpl.pyplot, ax: Axes) -> None:
    plt.grid(which="both", axis="both")

    ax.set_title("Journal entry date/time of day",
                 fontdict={"fontsize": 18}, pad=25)


def add_legend(plt: mpl.pyplot, color_map: ColorMap) -> Type[Legend]:
    tags: List[str] = list(color_map.keys())

    lines: List[Line2D] = [Line2D([], [], color=color, label=tag,
                                  marker="o", linestyle="none") for tag, color in color_map.items()]

    return plt.legend(lines, tags)


def main():
    mpl.use("Qt5Agg")

    parser = argparse.ArgumentParser(prog="python3.7 source/graph.py",
                                     description="Display a graph of journal entries from Day One JSON")
    parser.add_argument("file", help="Path to exported Day One JSON file")

    args = parser.parse_args()

    full_json = extract_json(args.file)

    points, x_0 = parse_entries(full_json)

    fig: Type[Figure] = plt.figure()
    ax: Type[Axes] = fig.add_subplot(111)

    plot_values(ax, points)

    format_x_axis(ax, x_0)
    format_y_axis(ax, int(x_0), int(x_0) + 1)

    figManager: [FigureManagerQT] = plt.get_current_fig_manager()
    format_figure(figManager)

    color_map: ColorMap = calc_color_map(full_json)
    add_legend(plt, color_map)
    format_plot(plt, ax)

    plt.show()


if __name__ == "__main__":
    main()
