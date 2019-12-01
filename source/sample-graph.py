import matplotlib.pyplot as plt
import matplotlib.dates as mdates

date = ['3 Jan 2013', '4 Jan 2013', '5 Jan 2013', '6 Jan 2013', '7 Jan 2013',
        '8 Jan 2013', '9 Jan 2013', '10 Jan 2013', '11 Jan 2013', '12 Jan 2013',
        '13 Jan 2013', '14 Jan 2013']
time = ['16:44:00', '16:45:00', '16:46:00', '16:47:00', '16:48:00', '16:49:00',
        '16:51:00', '16:52:00', '16:53:00', '16:55:00', '16:56:00', '16:57:00']

# Convert to matplotlib's internal date format.
x = mdates.datestr2num(date)
y = mdates.datestr2num(time)

print(y)

fig, ax = plt.subplots()

ax.plot(x, y, 'ro-')
ax.yaxis_date()
ax.xaxis_date()

# Optional. Just rotates x-ticklabels in this case.
fig.autofmt_xdate()
plt.show()
