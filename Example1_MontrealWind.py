"""
First example demonstrating the workflow I use when making use of DataDownloader.

Here, I will download hourly wind speed data for all stations that contain the word 'Montreal'. Then,
I will make wind speed histograms for each stations at different times.
"""

import DataDownloader as dd

############################ Downloading the data ###############################
# Set working directory
wd = raw_input('Enter desired working directory: \n')

# Download/update the daily-updated inventory of all stations from 
# ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
stationsDict = dd.genStationsDict(wd)

# Find all stations that contain 'montreal' in their name, have hourly data and have data somewhere
# between 1970 and 2016.
stations = dd.findStations(stationsDict,name='montreal int',interval='hourly',tp=['1970','2016'],verbose='on')

# Download all desired files
dd.multipleDownloads(wd,dd.genDownloadList(stations))


############################### Using the data ##################################

