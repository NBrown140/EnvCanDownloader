"""


"""
import DataDownloader

# Test urlBuilder
#Check for invalid dates
#DataDownloader.urlBuilder(interval='hourly',stationID='???',day='1',month='1',year='2017',verbose='on')
#DataDownloader.urlBuilder(interval='hourly',stationID='???',day='40',month='1',year='2017',verbose='on')
#DataDownloader.urlBuilder(interval='whatsaninterval',stationID='???',day='3',month='1',year='2014',verbose='on')



# Test genStationsList
#DataDownloader.genStationsDict('/home/nbrown/Desktop')




# Test: Check that the downloader works for a specific page.
#print DataDownloader.downloader(wd='/home/nbrown/Desktop',stationID='1706',interval='hourly',day='14',month='7',year='2001',verbose='off')


# Test multipleDownloads
l = [['51157', 'hourly', '1', '1', '2015'],
     ['51157', 'hourly', '1', '2', '2015'],
     ['51157', 'hourly', '1', '3', '2015'],
     ['51157', 'hourly', '1', '4', '2015'],
     ['51157', 'hourly', '1', '5', '2015'],
     ['51157', 'hourly', '1', '6', '2015'],
     ['51157', 'hourly', '1', '7', '2015'],
     ['51157', 'hourly', '1', '8', '2015'],
     ['51157', 'hourly', '1', '9', '2015'],
     ['51157', 'hourly', '1', '10', '2015'],
     ['51157', 'hourly', '1', '11', '2015'],
     ['51157', 'hourly', '1', '12', '2015']]

#DataDownloader.multipleDownloads('/home/nbrown/Desktop',l)



# Test findStations
wd='/home/nbrown/Desktop'
a = DataDownloader.findStations(DataDownloader.genStationsDict(wd),name='montreal',interval='hourly',tp=['1950','2014'],verbose='on')
b = DataDownloader.genDownloadList(a,verbose='on')


# Test: Check that downloader gives the right errors on wrong inputs or handles input conversion properly


