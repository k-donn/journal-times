"""Analyze data and show graphs."""
# TODO
# For hist:
# - Experiment with colors
# Move main() initialization to init_anim()

import argparse
import datetime
import json
from operator import itemgetter
from typing import Dict, List, Optional, Tuple

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pytz
import tzlocal
from matplotlib.axes._subplots import Axes
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.container import BarContainer
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

from .types import *


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
    """Parse the data from the incoming JSON.

    Calculate datetime info, primary tag, and respective color for each entry
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
    x_0: float = mpl.dates.date2num(
        str_to_date(earliest_entry["creationDate"]))

    for entry in full_json["entries"]:
        entry_info: PointColorVal = {}
        date = str_to_date(entry["creationDate"])
        print(f"{date=}")
        x_val = mpl.dates.date2num(date.date())
        y_val = int(x_0) + mpl.dates.date2num(date) % 1

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

    Matplotlib isn't compatible with timezone aware datetime objects.
    If one is passed to date2num, it undergoes unpredicted behaviour.
    This calculates the offset (offset from UTC changes based on a lot of things)
    then applies that offset via a timedelta object that doesn't affect/apply
    timezone info.

    Parameters
    ----------
    date_str: `str`
        String from an entry in JSON

    Returns
    -------
    `datetime.datetime`
        Parsed datetime object

    """
    utc_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    # This automatically calculates the offset to user's timezone
    # The offset is different throughout the year
    local_timezone = tzlocal.get_localzone()
    local_time_auto = utc_time.replace(tzinfo=pytz.utc)
    local_time_auto = utc_time.astimezone(local_timezone)

    local_time = utc_time + local_time_auto.utcoffset()
    return local_time


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
    entries = full_json["entries"]
    avail_tags = find_tags(entries)

    color_map: ColorMap = {}

    vmin = 0
    vmax = len(avail_tags)

    norm: colors.Normalize = colors.Normalize(
        vmin=vmin, vmax=vmax, clip=True)
    # Intellisense can't find any of the color-map members part of cm
    mapper: cm.ScalarMappable = cm.ScalarMappable(
        norm=norm, cmap=cm.gist_ncar)  # pylint: disable=no-member

    color_map = {tag: mapper.to_rgba(index)
                 for index, tag in enumerate(avail_tags)}

    color_map["none"] = (0.0, 0.0, 0.0, 1.0)

    return color_map


def find_tags(entries: List[Entry]) -> List[str]:
    """Find all unique and first tags.

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


def plot_dot_plot(axes: Axes, points: List[PointColorVal]) -> List[Line2D]:
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


def format_dot_x_axis(axes: Axes, x_0: float) -> None:
    """Draw the ticks, format the labels, and adjust sizing for the day-axis.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph

    x_0: `float`
        The earliest day of entry

    """
    axes.xaxis_date()
    # Pad the x on the left five in the past and pad the right five in the
    # future
    axes.set_xlim(left=(x_0 - 5),
                  right=(mpl.dates.date2num(datetime.datetime.now().date()) + 5))
    axes.set_xlabel("Date", fontdict={"fontsize": 15})

    x_loc = DayLocator(interval=10)
    x_formatter = DateFormatter("%m/%d/%y")

    x_axis = axes.get_xaxis()

    x_axis.set_major_locator(x_loc)
    x_axis.set_major_formatter(x_formatter)


def format_dot_y_axis(axes: Axes, bottom: float, top: float) -> None:
    """Draw the ticks, format the labels, and adjust sizing for the day-axis.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph

    bottom: `float`
        Midnight of the earliest day

    top: `float`
        Dawn of the earliest day

    """
    axes.yaxis_date()
    axes.set_ylim(bottom=bottom, top=top)
    axes.set_ylabel("Time of day", fontdict={"fontsize": 15})
    axes.grid(which="major", axis="y", lw=1)
    axes.grid(which="minor", axis="y", lw=0.5)

    y_loc = HourLocator(interval=2)
    y_formatter = DateFormatter("%-I:%M %p")

    y_min_loc = HourLocator(interval=1)

    y_axis = axes.get_yaxis()

    y_axis.set_major_locator(y_loc)
    y_axis.set_major_formatter(y_formatter)

    y_axis.set_minor_locator(y_min_loc)

    # Display morning on top and midnight on bottom. This is different than what
    # we did at assigning `y_vals`
    axes.invert_yaxis()


def format_dot(dot_plot: Figure, axes: Axes) -> None:
    """Format dot plot after it had been rendered.

    Parameters
    ----------
    dot_plot: `Figure`
        The Figure object describing the subplot

    axes: `Axes`
        The Axes object describing the graph

    """
    dot_plot.autofmt_xdate()

    axes.set_title("Journal entries date and time of day",
                   fontdict={"fontsize": 18, "family": "Poppins"}, pad=25)


def add_dot_legend(axes: Axes, color_map: ColorMap) -> Legend:
    """Add a legend that shows the mapping from unique tags to unqiue colors.

    Parameters
    ----------
    axes: `Axes`
        The Axes object describing the graph

    color_map: `ColorMap`
        The dictionary with unique tags and unique colors

    Returns
    -------
    `Legend`
        Object describing the added legend

    """
    tags = list(color_map.keys())

    lines = [Line2D([], [], color=color, label=tag,
                    marker="o", linestyle="none") for tag, color in color_map.items()]
    return axes.legend(lines, tags, loc=7, bbox_to_anchor=(1.12, 0.5))


def format_plt() -> None:
    """Set all top-level attributes of the plot."""
    plt.style.use("ggplot")


def gen_hour_histogram_data(
        points: List[PointColorVal], x_0: int) -> Dict[float, int]:
    """Extract the frequency of entries throughout the day.

    Parameters
    ----------
    points : `List[PointColorVal]`
        List of dicts that represent each entry's day and time of day

    x_0 : `int`
        Earliest day of entry

    Returns
    -------
    `Dict[float, int]`
        A dict where each key is a matplotlib date that corresponds to an hour
        of the day, and where each value is the number of entries made on that
        hour.

    """
    freq: Dict[int, int] = {}
    day = mpl.dates.num2date(x_0)
    delta = datetime.timedelta(hours=1)
    for i in range(1, 25):
        freq[i] = 0
    for point in points:
        date_obj = mpl.dates.num2date(point["y_value"])
        freq[date_obj.hour + 1] += 1
    res: Dict[float, int] = {}
    for hour, length in freq.items():
        res[mpl.dates.date2num(day + (delta * hour))] = length

    return res


def plot_histogram(
        hist_axes: Axes, hour_data: Dict[float, int]) -> BarContainer:
    """Plot bars representing frequency of entries throughout the day.

    Parameters
    ----------
    hist_axes : `Axes`
        The Axes object describing the graph

    hour_data : `Dict[float, int]`
        Frequency of entries throughout the day

    Returns
    -------
    `BarContainer`
        Object containing all of the plotted bars

    """
    bars: BarContainer = hist_axes.bar(
        list(hour_data.keys()), list(hour_data.values()), width=0.025)
    hist_axes.xaxis_date()

    return bars


def format_hist_x_axis(hist_axes: Axes, left: float, right: float) -> None:
    """Format the x-axis of the entry hour frequency histogram.

    Parameters
    ----------
    hist_axes : `Axes`
        The Axes object describing the graph

    left : `float`
        Matplotlib date representing start of day

    right : `float`
        Matplotlib date representing start of day

    """
    hist_axes.set_xlim(left=left, right=right)
    hist_axes.set_xlabel("Time of day")

    x_loc = HourLocator(interval=1)
    x_formatter = DateFormatter("%-I:%M %p")

    x_axis = hist_axes.get_xaxis()

    x_axis.set_major_locator(x_loc)
    x_axis.set_major_formatter(x_formatter)


def format_hist_y_axis(hist_axes: Axes) -> None:
    """Format the y-axis of the entry hour frequency histogram.

    Parameters
    ----------
    hist_axes : `Axes`
        The Axes object describing the graph

    """
    hist_axes.set_ylabel("Number of entries")
    hist_axes.grid(which="major", axis="y", lw=1)
    hist_axes.grid(which="minor", axis="y", lw=0.5)

    y_min_loc = MultipleLocator(5)
    y_maj_loc = MultipleLocator(10)

    y_axis = hist_axes.get_yaxis()

    y_axis.set_major_locator(y_maj_loc)
    y_axis.set_minor_locator(y_min_loc)


def format_hist(histogram: Figure, hist_axes: Axes) -> None:
    """Format graph-wide properties of the hour frequency histogram.

    Parameters
    ----------
    histogram : `Figure`
        The Figure object describing the subplot

    hist_axes : `Axes`
        The Axes object describing the graph

    """
    histogram.autofmt_xdate()

    hist_axes.set_title("Frequency of entries throughout the day",
                        fontdict={"fontsize": 18, "family": "Poppins"}, pad=25)


def main(file: str, debug: bool) -> None:
    """Display a graph of journal entries from Day One JSON.

    Parameters
    ----------
    file : str
        Path to exported JSON
    debug : bool
        Whether or not show graphs
    """
    full_json: Export = extract_json(file)

    dots, x_0 = parse_entries(full_json)

    histogram_data = gen_hour_histogram_data(dots, int(x_0))

    dot_plot: Figure = plt.figure(figsize=(16, 9), dpi=120)
    histogram: Figure = plt.figure(figsize=(16, 9), dpi=120)

    format_plt()

    hist_axes: Axes = histogram.add_subplot(111)
    axes: Axes = dot_plot.add_subplot(111)

    plot_dot_plot(axes, dots)
    plot_histogram(hist_axes, histogram_data)

    format_dot_x_axis(axes, x_0)
    format_dot_y_axis(axes, int(x_0), int(x_0) + 1)

    format_hist_x_axis(hist_axes, int(x_0), int(x_0) + 1.05)
    format_hist_y_axis(hist_axes)

    fig_manager: Optional[FigureManagerQT] = plt.get_current_fig_manager()
    if fig_manager is not None:
        fig_manager.set_window_title("Journal Entry Times")

    color_map: ColorMap = calc_color_map(full_json)
    add_dot_legend(axes, color_map)

    format_dot(dot_plot, axes)
    format_hist(histogram, hist_axes)

    if debug:
        plt.show()
    else:
        dot_plot.savefig("figures/journal-entry-times.png")
        histogram.savefig("figures/histogram.png")
