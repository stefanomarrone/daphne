# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2020, 1, 1)
end = datetime(2022, 12, 31)

# Create Point for Vancouver, BC
francesco = Point(41.07117, 14.31533, 20)
sasa = Point(41.56725, 14.33181, 20)

# Get daily data for 2018
datafrancesco = Daily(francesco, start, end).fetch()
datasasa = Daily(sasa, start, end).fetch()

# Plot line chart including average, minimum and maximum temperature
datadiff = datafrancesco - datasasa
datadiff.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
