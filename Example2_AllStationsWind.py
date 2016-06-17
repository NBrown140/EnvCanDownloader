"""
Example of:
Downloading all Canadian stations with monthly wind data (~20 Gb)
Merging CSVs together with Pandas and making basic plots with the data
"""

import DataDownloader as dd
import datetime, os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

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

def merge_csv(data_dir, out_dir, plot=False, ver=False):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    os.chdir(out_dir)

    files = sorted(os.listdir(data_dir))
    syear,eyear = int(files[0].split('_')[3]), int(files[-1].split('_')[3])
    smonth,emonth = int(files[0].split('_')[4][0:-4]), int(files[-1].split('_')[4][0:-4])
    name = files[0].split('_')[0:3]

    if os.path.exists(out_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_merged.csv'):
        return name,'no errors'

    # Merge csv files into one pandas dataframe
    def read_append(data_dir,names,name,year,month,ver=False):
        path =data_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_%s_%s.csv' % (year,month)
        frame = pd.read_csv(path, header=14, parse_dates=['Date/Time'], index_col=['Date/Time'])
        names = names.append(frame)
        if ver==True: print path
        return names

    years = range(syear, eyear+1)
    months,smonths,emonths = range(1,12+1), range(smonth,12+1), range(1,emonth+1)
    names = pd.DataFrame()
    for year in years:
        if year==eyear:
            for month in emonths:
                try:
                    names = read_append(data_dir,names,name,year,month)
                except ValueError, e:
                    print e
                    return name,e
                except IOError, e:
                    print e
                    dd.downloader(data_dir,name[0],name[1],name[2],1,month,year,verbose='on')
                    names = read_append(data_dir,names,name,year,month)
                    return name, e
        elif year==syear:
            for month in smonths:
                try:
                    names = read_append(data_dir,names,name,year,month)
                except ValueError, e:
                    print e
                    return name,e
                except IOError, e:
                    print e
                    dd.downloader(data_dir,name[0],name[1],name[2],1,month,year,verbose='on')
                    names = read_append(data_dir,names,name,year,month)
                    return name, e
        else:
            for month in months:
                try:
                    names = read_append(data_dir,names,name,year,month)
                except ValueError, e:
                    print e
                    return name,e
                except IOError, e:
                    print e
                    dd.downloader(data_dir,name[0],name[1],name[2],1,month,year,verbose='on')
                    names = read_append(data_dir,names,name,year,month)
                    return name, e
    names.to_csv(out_dir+'/'+name[0]+'_'+name[1]+'_'+name[2]+'_merged.csv')

def station_plot(path_csv, out_dir):
    name = path_csv.split('/')[-1].split('_')[0:2]
    df = pd.read_csv(path_csv, parse_dates=['Date/Time'], index_col=['Date/Time'])
    wind_ts = pd.Series(df['Wind Spd (km/h)'])

    fig1 = plt.figure()
    plt.subplot(2,1,1)
    #wind = ts[str(syear)+'-'+str(smonth)+'-01':str(eyear)+'-'+str(emonth)+'-01']
    ax1 = wind_ts.plot(color='#3366ff', kind='line', linewidth=1.0, figsize=(11,7))
    ax2 = wind_ts.rolling(window=48,center=True).mean().plot(color='0.35')
    plt.savefig(out_dir+'/'+name+'.pdf', bbox_inches='tight')
    plt.close(fig1)





# Merge CSVs
files = sorted(os.listdir('/home/nbrown/Desktop/test'))
files = ['/home/nbrown/Desktop/test/' + s for s in files]
files[:] = [ x for x in files if '.csv' not in x ]
errors = []
count = 1
for i in files:
    print 'Merging CSVs %s' %(i)
    nam,err = merge_csv(i,'/home/nbrown/Desktop/plots')
    if err!='no errors':
        errors.append([nam,err])
    print 'Done %s of %s.' %(count,len(files))
    count = count +1
pprint(errors)


# Make plots
files = sorted(os.listdir('/home/nbrown/Desktop/plots'))
files[:] = [ x for x in files if '_merged.csv' in x ]
files = ['/home/nbrown/Desktop/plots/' + s for s in files]
count = 0
for path in files:
    print 'Plotting %s' %(path)
    station_plot(path,'/home/nbrown/Desktop/plots')
    print 'Done %s of %s' %(count,len(files))
    count = count +1