"""

"""

import DataDownloader as dd
import datetime, os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.style.use('ggplot')

# ############################ Downloading the data ###############################
# Set working directory
# wd = '/home/nbrown/Desktop/test/'

# Download/update the daily-updated inventory of all stations from 
# ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
# stationsDict = dd.genStationsDict(wd)

# Find all stations that contain 'montreal' in their name, have hourly data and have data somewhere
# between 1970 and 2016.
# stations = dd.findStations(wd,stationsDict,name='',interval='hourly',tp=['1970','2016'],varNames=['Wind Spd (km/h)'],verbose='on')

# Download all desired files
# dd.multipleDownloads(wd,dd.genDownloadList(stations))


############################### Using the data ##################################

def station_plots(data_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    os.chdir(out_dir)

    files = sorted(os.listdir(data_dir))
    syear,eyear = int(files[0].split('_')[3]), int(files[-1].split('_')[3])
    smonth,emonth = int(files[0].split('_')[4][0:-4]), int(files[-1].split('_')[4][0:-4])
    name = files[0].split('_')[0:3]

    # Merge csv files into one pandas dataframe
    years = range(syear, eyear+1)
    months,smonths,emonths = range(1,12+1), range(smonth,12+1), range(1,emonth+1)
    names = pd.DataFrame()
    for year in years:
        if year==syear:
            for month in smonths:
                path =data_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_%s_%s.csv' % (year,month)
                frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
                names = names.append(frame)
        elif year==eyear:
            for month in emonths:
                path =data_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_%s_%s.csv' % (year,month)
                frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
                names = names.append(frame)
        else:
            for month in months:
                path =data_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_%s_%s.csv' % (year,month)
                frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
                names = names.append(frame)
    print names.head()

    # Plot timeseries
    fig1 = plt.figure()
    plt.subplot(2,1,1)
    ts = pd.Series(names['Wind Spd (km/h)'])
    wind = ts[str(syear)+'-'+str(smonth)+'-01':str(eyear)+'-'+str(emonth)+'-01']
    ax1 = wind.plot(color='#3366ff', kind='line', linewidth=1.0, figsize=(11,7))
    ax2 = wind.rolling(window=48,center=True).mean().plot(color='0.35')
    plt.savefig(out_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'.pdf', bbox_inches='tight')

station_plots('/home/nbrown/Desktop/test/ALERT','/home/nbrown/Desktop/plots')