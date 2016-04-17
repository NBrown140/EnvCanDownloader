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
# Set working directory
wd = raw_input('Enter desired working directory: \n')

# Download/update the daily-updated inventory of all stations from 
# ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
stationsDict = dd.genStationsDict(wd)

# Find all stations that contain 'montreal' in their name, have hourly data and have data somewhere
# between 1970 and 2016.
stations = dd.findStations(stationsDict,name='MONTREAL INTL A',interval='hourly',tp=['1970','2016'],verbose='on')

# Download all desired files
dd.multipleDownloads(wd,dd.genDownloadList(stations))


############################### Using the data ##################################

wd = '/home/nbrown/Desktop/test/MONTREAL INTL A'
#wd = '/Users/Nicolas/Desktop/test'

# Merge csv files into one pandas dataframe
years = range(2013, 2015+1)
months = range(1,12+1)

names = pd.DataFrame()
for year in years:
    for month in months:
        path =wd+'/MONTREAL INTL A_51157_hourly_%s_%s.csv' % (year,month)
        print path
        frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
        names = names.append(frame)

print names.head()


# Plot timeseries
fig1 = plt.figure()
plt.subplot(2,1,1)
ts = pd.Series(names['Wind Spd (km/h)'])
wind_2014 = ts['2014-01-01':'2014-12-31']
ax1 = wind_2014.plot(color='#3366ff', kind='line', linewidth=1.0, figsize=(11,7))
ax2 = wind_2014.rolling(window=48,center=True).mean().plot(color='0.35')
#wind_2014.rolling(window=48).std().plot(color='0.2')
# Fit line
X = pd.Series(range(1, len(wind_2014) + 1), index=wind_2014.index)
Y = wind_2014
model = pd.ols(y=Y, x=X, intercept=True)
print model
print model.beta
lineFit = model.y_fitted
ax3 = lineFit.plot(color='red',style='--')
s1 = 'line: y = '+str(round(model.beta['x'],5))+' * x  + '+str(round(model.beta['intercept'],5))
ax3.text(x=0.6, y=0.94, s=s1, fontsize=10, color='0.5', transform=ax3.transAxes)
ax3.text(x=0.6, y=0.87, s='r2= '+str(round(model.r2,5)), fontsize=10, color='0.5', transform=ax3.transAxes)
# Plot Fourier
plt.subplot(2,1,2)
y = wind_2014.interpolate(method='linear')
Y = np.fft.fft(y)/len(y)
Y = Y[range(len(y)/2)]
Fs = 1.;  # sampling rate
n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(n/2)] # one side frequency range
print Y, len(Y)
ax = plt.plot((1./frq)/24., abs(Y))
plt.xlabel('Period (Days)')
plt.ylabel('Power')
fig1.show()




# Plot histogram
d1=datetime.datetime(year=2014,month=1,day=1); d2=datetime.datetime(year=2014,month=4,day=1)
d3=datetime.datetime(year=2014,month=6,day=1); d4=datetime.datetime(year=2014,month=9,day=1)
wind_2014_jfm = pd.Series(names['Wind Spd (km/h)'][d1:d2], name='jfm')
wind_2014_jja = pd.Series(names['Wind Spd (km/h)'][d3:d4], name='jja')
fig2 = plt.figure()
bins = range(0,61,2)
ax1 = wind_2014_jja.plot.hist(alpha=0.6, bins=bins, normed=True, figsize=(11,7), legend=True)
ax2 = wind_2014_jfm.plot.hist(alpha=0.6, bins=bins, normed=True, figsize=(11,7), legend=True)
fig2.show()

