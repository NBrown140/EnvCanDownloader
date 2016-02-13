"""

urllib usage inspired from https://dzone.com/articles/how-download-file-python

"""
import urllib2
from bs4 import BeautifulSoup


def test1(verbose='off'):
    import pprint

    url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=QC&StationID=30165&hlyRange=2008-01-08|2016-02-10&Year=2016&Month=2&Day=10&cmdB1=Go#'

    html = urllib2.urlopen(url).read()

    soup = BeautifulSoup(html)

    table = soup.find('table', attrs={'class':'wet-boew-zebra span-8 '})

    rows = table.findAll('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if 'LegendNANA' not in ele])

    if verbose=='on':
        for i in data:
            print i
        print '\n'*3,'Removing top 2 empty lists (data[0] and data[1])...','\n'
    
    data = data[2:]

    if verbose=='on':
        for i in data:
            print i


def urlBuilder(type='hourly',station='???',day='1',month='1',year='2016'):
    """

    """

    if type=='hourly':
        url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=QC&StationID=30165&hlyRange=2008-01-08|2016-02-10&Year='+year+'&Month='+month+'&Day='+day+'&cmdB1=Go#'
    elif type=='daily':
        url = ''
    elif type=='monthly':
        url = ''

def stationsDict():
    """
    Dictionnary format:
    '$name' : ['$StationID','$province','$lat','$lon','$elevation','$Climate ID','$WMO ID','$TC ID']
    """
    stations = {'MONTREAL INTL A':['51157','QUEBEC','45 28 14.000 N','73 44 27.000 W','36.00','7025251','71627','YUL'],\
    'MCTAVISH':['10761','QUEBEC','']}
    # ....
    

