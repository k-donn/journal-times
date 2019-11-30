# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import numpy as np
# import datetime as dt

# # Make a series of events 1 day apart
# x = mpl.dates.drange(dt.datetime(2009,10,1), 
#                      dt.datetime(2010,1,15), 
#                      dt.timedelta(days=1))
# # Vary the datetimes so that they occur at random times
# # Remember, 1.0 is equivalent to 1 day in this case...
# x += np.random.random(x.size)

# # We can extract the time by using a modulo 1, and adding an arbitrary base date
# times = x % 1 + int(x[0]) # (The int is so the y-axis starts at midnight...)

# # I'm just plotting points here, but you could just as easily use a bar.
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot_date(x, times, 'ro')
# ax.yaxis_date()
# fig.autofmt_xdate()

# # print(times[5])
# # print(times)
# plt.show()
import numpy as np
import matplotlib.pyplot as plt
import datetime

x = [datetime.datetime(2010, 12, 1, 10, 0),
     datetime.datetime(2011, 1, 4, 9, 0),
     datetime.datetime(2011, 5, 5, 9, 0)]
y = [4, 9, 2]

ax = plt.subplot(111)
ax.bar(x, y, width=10)
ax.xaxis_date()

plt.show()
