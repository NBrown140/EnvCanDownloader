"""
First example demonstrating the workflow I use when making use of DataDownloader.

Here, I will download hourly wind speed data for all stations that contain the word 'Montreal'. Then,
I will make wind speed histograms for each stations at different times.
"""

import DataDownloader as dd
import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.style.use('ggplot')

# ############################ Downloading the data ###############################
# # Set working directory
# wd = raw_input('Enter desired working directory: \n')
# 
# # Download/update the daily-updated inventory of all stations from 
# # ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
# stationsDict = dd.genStationsDict(wd)
# 
# # Find all stations that contain 'montreal' in their name, have hourly data and have data somewhere
# # between 1970 and 2016.
# stations = dd.findStations(stationsDict,name='montreal int',interval='hourly',tp=['1970','2016'],verbose='on')
# 
# # Download all desired files
# dd.multipleDownloads(wd,dd.genDownloadList(stations))
# 

############################### Using the data ##################################




years = range(2013, 2015+1)
months = range(1,12+1)

names = pd.DataFrame()
for year in years:
    for month in months:
        path ='/Users/Nicolas/Desktop/test/51157_hourly_%s_%s.csv' % (year,month)
        print path
        frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
        names = names.append(frame)

print names.head()


ts = pd.Series(names['Wind Spd (km/h)'])
ax = ts.plot(color='#3366ff', kind='line', linewidth=1.0, figsize=(11,7))
ts.rolling(window=48).mean().plot(color='0.35')
ax.set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2015-01-01'))
plt.show()

