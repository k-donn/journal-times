"""
usage:
python3.7 source/graph.py
description:
Display a graph of journal entries from Day One JSON
"""
# TODO
# Add NoReturn type

import argparse
import datetime
import json
from operator import itemgetter
from typing import Dict, List, Tuple, Union

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pytz
from matplotlib.axes._subplots import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.dates import (HourLocator, DayLocator, DateFormatter)
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D

# Mapping of tag names to unique colors
ColorMap = Dict[str, Tuple[float, float, float, float]]

# Represents a point's color and x & y values
PointColorVal = Dict[str, Union[str, float]]

# Day One weather properties
WeatherProps = Dict[str, Union[str, int, float]]

# Day One coordinates description
Coordinates = Dict[str, float]

# Day One location region description
RegionProps = Dict[str, Union[str, float, Coordinates]]

# Day One location properties
LocationProps = Dict[str, Union[str, float, RegionProps]]

# Properties of a JSON entry
Entry = Dict[str, Union[str, bool, int, WeatherProps, LocationProps]]

# Day One export metadata info
MetadataProps = Dict[str, str]

# structure of an exported journal
Export = Dict[str, Union[MetadataProps, List[Entry]]]


def extract_json(fname: str) -> Export:
    """Extract JSON from supplied Day One journal export.

    Parameters
    ----------
    fname: `str`
        path to file

    Returns
    -------
    `Export`
        Nested dictionary object with Day One JSON properties

    """
    with open(fname, "r") as file:
        full_json = json.load(file)
    return full_json


def parse_entries(full_json: Export) -> Tuple[List[PointColorVal], float]:
    """Calculate datetime info, primary tag, and respective color for each entry
    in the Day One export.

    Parameters
    ----------
    full_json: `Export`
        Nested dictionary object with Day One JSON properties

    Returns
    -------
    `Tuple[List[PointColorVal], float]`
        Represents parsed info about entries and earliest date of entry

    """
    parsed_entries: List[PointColorVal] = []
    color_map: ColorMap = calc_color_map(full_json)

    earliest_entry: Entry = min(
        full_json["entries"], key=itemgetter("creationDate"))
    x_0: float = mpl.dates.date2num(str_to_date(earliest_entry["creationDate"]))

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
    """Convert a string in Day One format to a datetime object.

    Parameters
    ----------
    date_str: `str`
        String from an entry in JSON

    Returns
    -------
    `datetime.datetime`
        Parsed datetime object

    """
    eastern_timezone: pytz.tzfile.DstTzInfo = pytz.timezone("America/New_York")
    correction: datetime.timedelta = datetime.timedelta(hours=2)
    final: datetime.datetime = datetime.datetime.strptime(
        date_str, "%Y-%m-%dT%H:%M:%SZ").astimezone(eastern_timezone) - correction
    return final


def calc_color_map(full_json: Export) -> ColorMap:
    """Create a dictionary to map unique tags to unique colors.

    Parameters
    ----------
    full_json: `Export`
        Nested dictionary object with Day One JSON properties

    Returns
    -------
    `ColorMap`
        Each tag's respective color

    """
    entries: List[Entry] = full_json["entries"]
    avail_tags: List[str] = find_tags(entries)

    color_map: ColorMap = {}

    minima = 0
    maxima = len(avail_tags)

    norm: colors.Normalize = colors.Normalize(
        vmin=minima, vmax=maxima, clip=True)
    # Intellisense can't find any of the color-map members part of cm
    mapper: cm.ScalarMappable = cm.ScalarMappable(
        norm=norm, cmap=cm.gist_ncar)  # pylint: disable=no-member

    color_map = {tag: mapper.to_rgba(index)
                 for index, tag in enumerate(avail_tags)}

    color_map["none"] = (0.0, 0.0, 0.0, 1.0)

    return color_map


def find_tags(entries: List[Entry]) -> List[str]:
    """Find all unique and primary, that which is first in the `tags` property,
    in entries.

    Parameters
    ----------
    entries: `List[Entry]`
        Entries property of exported JSON

    Returns
    -------
    `List[str]`
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


def plot_values(axes: Axes, points: List[PointColorVal]) -> List[Line2D]:
    """Plot points representing day v. time of day.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph
    points: `List[PointColorVal]`
        List of dicts that represent each entry's day and time of day

    Returns
    -------
    `List[Line2D]`
        The returned objects from the matplotlib plotting function

    """
    lines: List[Line2D] = [
        axes.plot_date(
            point["x_value"],
            point["y_value"],
            fmt="o", label=point["color"],
            color=point["color"]) for point in points]

    return lines


def format_x_axis(axes: Axes, x_0: float) -> None:
    """Draw the ticks, format the labels, and adjust sizing for the day-axis.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph
    x_0: `float`
        The earliest day of entry

    """
    axes.xaxis_date()
    # Pad the x on the left five in the past and pad the right five in the future
    axes.set_xlim(left=(x_0 - 5),
                  right=(mpl.dates.date2num(datetime.datetime.now().date()) + 5))
    axes.set_xlabel("Date", fontdict={"fontsize": 15})
    axes.grid(axis="x")

    x_loc: DayLocator = DayLocator(interval=10)
    x_formatter: DateFormatter = DateFormatter("%m/%d/%y")

    x_axis: XAxis = axes.get_xaxis()

    x_axis.set_major_locator(x_loc)
    x_axis.set_major_formatter(x_formatter)
    x_axis.set_tick_params(rotation=30)


def format_y_axis(axes: Axes, bottom: int, top: int) -> None:
    """Draw the ticks, format the labels, and adjust sizing for the day-axis.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph
    bottom: `int`
        Midnight of the earliest day
    top: `int`
        Dawn of the earliest day

    """
    axes.yaxis_date()
    axes.set_ylim(bottom=bottom, top=top)
    axes.set_ylabel("Time of day", fontdict={"fontsize": 15})
    axes.grid(axis="y")

    y_loc: HourLocator = HourLocator(interval=2)
    y_formatter: DateFormatter = DateFormatter("%-I:%M:%S %p")

    y_axis: YAxis = axes.get_yaxis()

    y_axis.set_major_locator(y_loc)
    y_axis.set_major_formatter(y_formatter)

    # Display morning on top and midnight on bottom. This is different than what
    # we did at assigning `y_vals`
    axes.invert_yaxis()


def format_figure(fig_manager: FigureManagerQT) -> None:
    """Adjust the sizing of the figure (the whole window including tool-bar) to
    be maximized and have a window title.

    fig_manager: `FigureManagerQT`
        The returned wrapper around the figure

    """
    fig_manager.set_window_title("Journal Entry times")


def format_axes(axes: Axes) -> None:
    """Adjust grid lines and title for the plot (the part that's not the tool-
    bar).

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph

    """
    plt.grid(which="both", axis="both")

    axes.set_title("Journal entry date/time of day",
                   fontdict={"fontsize": 18, "family": "Poppins"}, pad=25)


def add_legend(color_map: ColorMap) -> Legend:
    """Add a legend that shows the mapping from unique tags to unqiue colors.

    Parameters
    ----------
    color_map: `ColorMap`
        The dictionary with unique tags and unique colors

    Returns
    -------
    `Legend`
        Object describing the added legend

    """
    tags: List[str] = list(color_map.keys())

    lines: List[Line2D] = [Line2D([], [], color=color, label=tag,
                                  marker="o", linestyle="none") for tag, color in color_map.items()]

    return plt.legend(lines, tags, loc=7, bbox_to_anchor=(1.12, 0.5))


def format_plt():
    """Set all top-level attributes of the plot"""
    plt.style.use("ggplot")


def main():
    """Display a graph of journal entries from Day One JSON."""

    parser = argparse.ArgumentParser(
        prog="python3.7 source/graph.py",
        description="Display a graph of journal entries from Day One JSON")
    parser.add_argument("-f", "--file", required=True,
                        help="Path to exported Day One JSON file")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Show the plot instead of writing to file")

    args = parser.parse_args()

    full_json: Export = extract_json(args.file)

    points, x_0 = parse_entries(full_json)

    fig: Figure = plt.figure(figsize=(16, 9), dpi=120)

    format_plt()

    axes: Axes = fig.add_subplot(111)

    plot_values(axes, points)

    format_x_axis(axes, x_0)
    format_y_axis(axes, int(x_0), int(x_0) + 1)

    fig_manager: FigureManagerQT = plt.get_current_fig_manager()
    format_figure(fig_manager)

    color_map: ColorMap = calc_color_map(full_json)
    add_legend(color_map)
    format_axes(axes)

    if args.debug:
        plt.show()
    else:
        fig.savefig("figures/journal-entry-times.png")


if __name__ == "__main__":
    main()
