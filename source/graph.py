# TODO
# 1. Format x-axis to be rotated and neat.
# 2. Format y-axis to be times instead of numbers
# 3. Apply timezones dynamically instead of all just in NY

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import pytz
import json

with open("data/Daily.json", "r") as f:
    daily = json.load(f)

raw_dates = [entry["creationDate"] for entry in daily["entries"]]

full_dates = [datetime.datetime.strptime(
    raw_date, "%Y-%m-%dT%H:%M:%SZ").astimezone(pytz.timezone("America/New_York")) for raw_date in raw_dates]

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

ax = plt.subplot(111)
ax.plot_date(days, y_vals, "ro")

plt.show()
