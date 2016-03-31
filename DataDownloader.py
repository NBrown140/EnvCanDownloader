"""

ftp://ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Readme.txt
ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
"""
import datetime, time, sys, os, csv
import urllib2

def multipleDownloads(inputList):
    """
    inputList must have format:
    [stationID_1, interval_1, 
     stationID_2, interval_2, ]
    """



def downloader(wd,interval,stationID,day=1,month=1,year=2016,verbose='off'):
    """
    wd (str): working directory where files will be downloaded........ e.g. '/home/usrname/weatherdata'
    interval (str): hourly, daily or monthly data..................... 'hourly' or 'daily' or 'monthly'
    stationID (str): stationID number 
    day (int):
    month (int):
    year (int):
    verbose (str):

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

    url = urlBuilder(interval,stationID,day,month,year,verbose)

    if interval=='hourly':
        filename = stationID+'_hourly_'+year+'_'+month+'_'+day
    elif interval=='daily':
        filename = stationID+'_hourly_'+year+'_'+month
    elif interval=='monthly':
        filename = stationID+'_hourly_'+year

    if verbose=='on': print 'Downloading from '+url+' to '+filename+'.csv'
    f = urllib2.urlopen(url)
    data = open(filename+'.csv',"w")
    data.write(f.read())
    data.close()
    if verbose=='on': print 'Done Downloading '+filename+'.csv'


def urlBuilder(interval='hourly',stationID='???',day='1',month='1',year='2016',verbose='off'):
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
        print "Invalid input to urlBuilder: interval"
        print my_func.__doc__
        return None

    url = 'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID='+stationID+'&Year='+year+'&Month='+month+'&Day='+day+'&timeframe='+tf+'&submit= Download+Data'

    if verbose=='on': print "Built URL: ",url,'\n'
        
    return url


def setWorkingDir():
    wd = input('Enter the working directory you wish to use. It will be used to download the list of stations (~2Mb) and output the downloaded files:')
    os.chdir(wd)
    print 'Working directory set to: '+wd
    return None


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
    barLength = 10 # Modify this to change the length of the progress bar
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




