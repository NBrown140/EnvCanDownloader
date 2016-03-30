"""

ftp://ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Readme.txt
ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
"""
import time, sys
import urllib2



def downloader(interval='hourly',station='???',day='1',month='1',year='2016',verbose='off'):
    """

    """

    url = urlBuilder(interval,station,day,month,year,verbose)

    f = urllib2.urlopen(url)
    data = open("","w")


def urlBuilder(interval='hourly',stationID='???',day='1',month='1',year='2016',verbose='off'):
    """
    interval = 'hourly', 'daily' or 'monthly'
    station = 'MONTREAL INTL A', etc...
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

    url = 'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID='+stationID+'&Year='+year+'&Month=+'month+'&Day=+'day+'&timeframe=+'+tf+'&submit= Download+Data'

    if verbose=='on':
        print "Built URL: ",url,'\n'
    return url


def setWorkingDir():
    wd = input('Enter the working directory you wish to use. It will be used to download the list of stations (~2Mb) and output the downloaded files:')
    return wd


def genStationsList():



def update_progress(progress):
    """
    Taken from http://stackoverflow.com/questions/3160699/python-progress-bar

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














def getHourly(stations,startDay,startMonth,startYear,endDay,endMonth,endYear):
    pass
def getDaily(stations,startMonth,startYear,endMonth,endYear):
    pass
def getMonthly(stations,startYear,endYear):
    pass


def downloader(interval='hourly',station='???',day='1',month='1',year='2016',verbose='off'):
    """

    """
    url = urlBuilder(interval,station,day,month,year,verbose)

    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)

    table = soup.find('table', attrs={'class':'wet-boew-zebra span-8 '})

    rows = table.findAll('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])

    if verbose=='on':
        for i in data:
            print i
        print '\n'*3,'Removing top 2 empty lists (data[0] and data[1])...','\n'
    
    data = data[2:]

    if verbose=='on':
        for i in data:
            print i

    return data

def urlBuilder(interval='hourly',station='???',day='1',month='1',year='2016',verbose='off'):
    """
    interval = 'hourly', 'daily' or 'monthly'
    station = 'MONTREAL INTL A', etc...
    day = '1'-'31'
    month = '1'-'12'
    year = '1840'-'2016'

    To Do:
    - Allow station to be input as name (str) or id (int).
    - 
    """

    if interval=='hourly':
        url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=QC&StationID='+stationsDict(station)[0]+'&hlyRange=2008-01-08|2016-02-10&Year='+year+'&Month='+month+'&Day='+day+'&cmdB1=Go#'
    elif interval=='daily':
        url = ''
    elif interval=='monthly':
        url = ''
    else:
        print "Invalid input to urlBuilder"
        print my_func.__doc__
        return None
    if verbose=='on':
        print "Built URL: ",url,'\n'
    return url


def stationsDict(stationName):
    """
    Input: Station Name (e.g. MONTREAL INTL A)................................................ str
    Output: list of info...................................................................... list

    Dictionnary format:
    '$name' : ['$StationID','$recordStart','$recordEnd','$province','$lat','$lon','$elevation','$Climate ID','$WMO ID','$TC ID']
    """

    stations = {'MONTREAL INTL A':['51157','13-02-2013','present','QUEBEC','45 28 14.000 N','73 44 27.000 W','36.00','7025251','71627','YUL'],\
    'MCTAVISH':['10761','']}
    # ....
    
    return stations[stationName]

def genStationsDict():
    """

    """