"""

ftp://ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Readme.txt
ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
"""
import time, sys, os
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
    """
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


def genStationsList(wd):
    """
    Downloads the daily-updated .csv file that contains all station IDs (and more) to the working directory.
    """
    os.chdir(wd)
    print 'Working directory set to: '+wd

    print 'Downloading StationInventoryEN.csv to '+wd
    f = urllib2.urlopen('ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv')
    data = open("StationInventoryEN.csv","w")
    data.write(f.read())
    data.close()
    print 'Done Downloading StationInventoryEN.csv'


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




