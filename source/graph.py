# TODO
# 1. Convert UTC times from the JSON into EST dates for Python

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import json

with open("data/Daily.json", "r") as f:
    daily = json.load(f)

raw_dates = [entry["creationDate"] for entry in daily["entries"]]

full_dates = list(map(datetime.datetime.strptime,
                      raw_dates, len(raw_dates)*['%Y-%m-%dT%H:%M:%SZ']))


# days = mpl.dates.drange(min(full_dates).date(), max(
#     full_dates).date(), datetime.timedelta(days=1))
# full_days = [mpl.dates.date2num(full_day.date()) for full_day in full_dates]

# y_vals = []
# i = 0
# for day in days:
#     if day in full_days:
#         y_vals.append(mpl.dates.date2num(full_dates[i]) % 1)
#         i += 1
#     else:
#         y_vals.append(0)

days = [mpl.dates.date2num(full_day.date()) for full_day in full_dates]
y_vals = [(mpl.dates.date2num(full_day) % 1) for full_day in full_dates]

# I'm just plotting points here, but you could just as easily use a bar.
ax = plt.subplot(111)
ax.plot_date(days, y_vals, "ro")

# print(hours)

plt.show()

