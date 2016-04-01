"""

ftp://ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Readme.txt
ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
"""
import datetime, time, sys, os, csv
from pprint import pprint
import urllib2


def concatCsvFiles():
    pass


def findStations(stationsDict,name,interval,tp,Pr=None,lat=None,lon=None,elev=None,verbose='off'):
    """
    Mandatory Filters:
    Filter1: Name contains a string (e.g. 'MONTREAL' or 'TORONTO'). Enter '' for all.
    Filter2: Interval ('hourly', 'daily' or 'monthly').
    Filter3: Recorded time period tp (e.g. ['1950','2016'])

    Optional Filters:
    Filter4: In one or more provinces/territories.
    Filter5: Within a lat/lon interval.
    Filter6: Within an elevation interval.


    And output a list: [['Name_1', 'StationID_1', 'interval_1', 'FirstYear_1', 'LastYear_1'],
                        ['Name_2', 'StationID_2', 'interval_2', 'FirstYear_2', 'LastYear_2'], ...]

    name will always be converted to all uppercase, because stations name in the dict are all uppercase.

    To do:
    - Add the code for Province, lat, lon and elevation constraints
    """
    stations = []

    if interval=='hourly':
        interv1 = 12; interv2 = 13
    elif interval=='daily':
        interv1 = 14; interv2 = 15
    elif interval=='monthly':
        interv1 = 16; interv2 = 17
    else:
        raise ValueError('Invalid input to findStations: interval='+interval+'.\
            \n'+findStations.__doc__)

    if verbose=='on': print 'Finding stations containing '+name+' at interval '+interval+' within time period '+tp[0]+'-'+tp[1]+'...'
    keys = stationsDict.keys()
    for key in keys:
        if (name.upper() in key) and stationsDict[key][interv1]<=tp[1] and stationsDict[key][interv2]>=tp[0]:
            t1 = max(int(stationsDict[key][interv1]),int(tp[0])); t2 = min(int(stationsDict[key][interv2]),int(tp[1]))
            temp = [key,stationsDict[key][2],interval,t1,t2]
            stations.append(temp)

    if verbose=='on': print 'Found '+str(len(stations))+' stations:'; pprint(stations)
    return stations


def genDownloadList(stations, verbose='off'):
    """
    Use a list of stations output by findStations and transform it into 
    a downloadList that can be used by multipleDownloads.
    """
    downloadList = []

    for station in stations:
        print station
        if station[2]=='monthly':
            downloadList.append([station[1],station[2],'1','1','1'])
        elif station[2]=='daily':
            for year in range(station[3],station[4]+1):
                downloadList.append([station[1],station[2],'1','1',year])
        elif station[2]=='hourly':
            for year in range(station[3],station[4]+1):
                for month in range(0,12+1):
                    downloadList.append([station[1],station[2],'1',month,year])
        else:
            raise ValueError('Invalid input to genDownloadList: interval')
    if verbose=='on': print 'Found '+str(len(downloadList))+' files to download:'; pprint(downloadList)

    return downloadList


def multipleDownloads(wd,downloadList,verbose='off'):
    """
    wd: working directory
    downloadList: a list containing a list for each file to downloade
    verbose: for debugging

    downloadList must have format:
    [['stationID_1', 'interval_1', 'day_1', 'month_1', 'year_1'],
     ['stationID_2', 'interval_2', 'day_2', 'month_2', 'year_2'],
     ['stationID_3', 'interval_3', 'day_3', 'month_3', 'year_3'], ...]
    """
    count=0.0
    tot=len(downloadList)
    for i in downloadList:
        downloader(wd,i[0],i[1],i[2],i[3],i[4],verbose)
        count=count+1.0
        update_progress(count/tot)


def downloader(wd,stationID,interval,day,month,year,verbose='off'):
    """
    wd (str): working directory where files will be downloaded........ e.g. '/home/usrname/weatherdata'
    interval (str): hourly, daily or monthly data..................... 'hourly' or 'daily' or 'monthly'
    stationID (str): stationID number 
    day (int):
    month (int):
    year (int):
    verbose (str): for debugging

    If hourly data is desired, then year and month must be given, but not day.
    If daily data is desired, then year must be given, but not month nor day.
    If monthly data is desired, then neither day, month nor year are required.

    To do:
    - Check in station inventory file if the requested file exists at the desired interval (hourly, daily, monthly) and time period.
    - Better exception handling
    """
    day,month,year = str(day),str(month),str(year)
    os.chdir(wd)
    if verbose=='on': print 'Working directory set to: '+wd

    url = urlBuilder(stationID,interval,day,month,year,verbose)

    if interval=='hourly':
        filename = stationID+'_hourly_'+year+'_'+month
    elif interval=='daily':
        filename = stationID+'_daily_'+year
    elif interval=='monthly':
        filename = stationID+'_monthly'

    if verbose=='on': print 'Downloading from '+url+' to '+filename+'.csv'
    f = urllib2.urlopen(url)
    data = open(filename+'.csv',"w")
    data.write(f.read())
    data.close()
    if verbose=='on': print 'Done Downloading '+filename+'.csv'


def urlBuilder(stationID,interval,day,month,year,verbose='off'):
    """
    interval = 'hourly', 'daily' or 'monthly'
    stationID = '51157', etc.
    day = '1'-'31'
    month = '1'-'12'
    year = '1840'-'2016'

    To Do:
    - Currently no check of stationID. Maybe pass the station dict to the
    function to check if stationId is valid.
    """
    stationID,day,month,year = str(stationID),str(day),str(month),str(year)

    now = datetime.datetime.now(); y=now.year; m=now.month; d=now.day
    # Check date sanity
    if not(datetime.datetime(year=1840,month=1,day=1) < datetime.datetime(year=int(year),month=int(month),day=int(day)) <= datetime.datetime.now()):
        raise ValueError('You have requested to build a url for the following invalid date: %s/%s/%s.\
            \nPlease make sure your date is between 1/1/1840 and %s/%s/%s.' % (day,month,year,d,m,y))

    if interval=='hourly':
        tf=str(1)
    elif interval=='daily':
        tf=str(2)
    elif interval=='monthly':
        tf=str(3)
    else:
        raise ValueError('Invalid input to urlBuilder: interval='+interval+'.\
            \n'+urlBuilder.__doc__)

    url = 'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID='+stationID+'&Year='+year+'&Month='+month+'&Day='+day+'&timeframe='+tf+'&submit= Download+Data'

    if verbose=='on': print "Built URL: ",url,'\n'
        
    return url


def genStationsDict(wd):
    """
    Downloads the daily-updated .csv file that contains all station IDs (and more) to the working directory.
    
    Output dict layout:
    {'Station Name': ['Province', 'Climate ID', 'Station ID', 'WMO ID', 'TC ID',
    'Latitude (decimal degrees)', 'Longitude (decimal degrees)', 'Latitude', 'Longitude',
    'Elevation (m)', 'First Year', 'Last Year', 'HLY First Year', 'HLY Last Year',
    'DLY First Year', 'DLY Last Year', 'MLY First Year', 'MLY Last Year']}

    To Do:
    - Add ability to gen dict without saving the file inventory file to disk.
    """
    os.chdir(wd)
    print 'Working directory set to: '+wd

    print 'Downloading StationInventoryEN.csv to '+wd
    f = urllib2.urlopen('ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv')
    data = open("StationInventoryEN.csv","w")
    data.write(f.read())
    data.close()
    print 'Done Downloading StationInventoryEN.csv'

    with open('StationInventoryEN.csv') as f:
        reader = csv.reader(f)
        for i in range(0,4): reader.next() #skip first 4 lines (header)
        stationsDict = {}
        try:
            for row in reader:
                key = row[0]
                if key in stationsDict:
                    # implement your duplicate row handling here
                    pass
                stationsDict[key] = row[1:]
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % ('StationInventoryEN.csv', reader.line_num, e))

    return stationsDict


def update_progress(progress):
    """
    Copied from http://stackoverflow.com/questions/3160699/python-progress-bar

    update_progress() : Displays or updates a console progress bar
    
    Accepts a float between 0 and 1. Any int will be converted to a float.
    A value under 0 represents a 'halt'.
    A value at 1 or bigger represents 100%
    """
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()