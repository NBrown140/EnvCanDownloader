"""


"""
import DataDownloader

# Test urlBuilder

#Check for invalid dates
#DataDownloader.urlBuilder(interval='hourly',stationID='???',day='1',month='1',year='2017',verbose='on')
#DataDownloader.urlBuilder(interval='hourly',stationID='???',day='40',month='1',year='2017',verbose='on')

# Test genStationsList

DataDownloader.genStationsDict('/home/nbrown/Desktop')

# Test1: Check that the downloader works for a specific page.

#print DataDownloader.downloader(wd='/home/nbrown/Desktop',interval='hourly',stationID='1706',day='14',month='7',year='2001',verbose='off')



# Test2: Check that downloader gives the right errors on wrong inputs or handles input conversion properly


#Test3: 