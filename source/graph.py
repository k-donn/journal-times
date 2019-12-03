# TODO
# 1. Put in README how to export Day One data

# Types
from typing import Type, Dict, List, Tuple
from matplotlib.axes._subplots import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.lines import Line2D

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


def calc_full_dates(raw_dates: List[str]) -> List[Type[datetime.datetime]]:
    full_dates: List[Type[datetime.datetime]] = [datetime.datetime.strptime(
        raw_date, "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York")) for raw_date in raw_dates]
    return full_dates


def calc_colors() -> List[str]:
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
    return colors


def calc_points(raw_dates: List[str]) -> Tuple[List[float], List[float], List[List[float]]]:
    full_dates = calc_full_dates(raw_dates)

    x_vals: List[float] = [mpl.dates.date2num(
        full_day.date()) for full_day in full_dates]
    # Y-values get inverted for some time-zone related reason.
    y_vals: List[float] = [
        (int(x_vals[0]) + abs(1.0 - (mpl.dates.date2num(full_day) % 1))) for full_day in full_dates]

    combined_xy: List[List[float]] = [[x_val, y_val]
                                      for x_val, y_val in zip(x_vals, y_vals)]

    return x_vals, y_vals, combined_xy


def combine_points_colors(points: List[List[int]], colors: List[str]) -> List[Dict[str, str]]:
    combined_vals_color: List[Dict[str, str]] = [
        {"color": color, "values": vals} for color, vals in zip(colors, points)]

    return combined_vals_color


def plot_values(ax: Type[Axes], points_colors: List[Dict[str, str]]) -> List[Line2D]:
    X_VAL: int = 0
    Y_VAL: int = 1

    lines: List[Line2D] = [ax.plot_date(point["values"][X_VAL], point["values"]
                                        [Y_VAL], point["color"]) for point in points_colors]

    return lines


def format_x_axis(ax: Type[Axes]) -> None:
    ax.xaxis_date()
    # Pad the x on the left five in the past and pad the right five in the future
    ax.set_xlim(left=(min(x_vals) - 5),
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


if __name__ == "__main__":
    mpl.use("Qt5Agg")

    parser = argparse.ArgumentParser(prog="python3.7 source/graph.py",
                                     description="Display a graph of journal entries from Day One JSON")
    parser.add_argument("file", help="Path to exported Day One JSON file")

    args = parser.parse_args()

    with open(args.file, "r") as f:
        daily = json.load(f)

    raw_dates: List[str] = [entry["creationDate"]
                            for entry in daily["entries"]]

    fig: Type[Figure] = plt.figure()
    ax: Type[Axes] = fig.add_subplot(111)

    x_vals, y_vals, combined_points = calc_points(raw_dates)
    colors = calc_colors()
    combined_points_colors = combine_points_colors(combined_points, colors)

    plot_values(ax, combined_points_colors)

    format_x_axis(ax)
    format_y_axis(ax, int(y_vals[0]), int(y_vals[0]) + 1)

    ax.set_title("Journal entry date/time of day",
                 fontdict={"fontsize": 18}, pad=25)

    figManager: [FigureManagerQT] = plt.get_current_fig_manager()
    format_figure(figManager)

    format_plot(plt)

    plt.show()
