"""


"""
import urllib2
from bs4 import BeautifulSoup


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


def urlBuilder(interval='hourly',station='???',day='1',month='1',year='2016',verbose='off'):
    """
    interval = 'hourly', 'daily' or 'monthly'
    station = 'MONTREAL INTL A', etc...
    day = '1'-'31'
    month = '1'-'12'
    year = '1900'-'2016'
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

