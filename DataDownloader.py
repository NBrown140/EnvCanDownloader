"""

ftp://ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Readme.txt
ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv

To do:
- Make better use of python OOP. e.g. Make a new class (object) for a list of files to download and
  call a method on it to download or filter.
"""
import datetime, time, sys, os, csv, threading, urllib2
from pprint import pprint
import Queue
import math as m


def checkVar(varNames,stationID,interval,year,verbose='off'):
    """
    Returns True if all strings in the list varNames appears anywhere in the file to download.
    """
    varsPresent = False
    if type(varNames)!=list:
        raise ValueError('Error in parameter input to varNames(). Parameter varNames must be a list.')
    year = str(year)

    url = urlBuilder(stationID,interval,1,1,year,verbose)

    f = urllib2.urlopen(url)
    temp1 = True
    for varName in varNames:
        temp2 = False
        for line in f:
            if varName in line:
                temp2 = True
                break
        temp1 = temp1 and temp2
    varsPresent = temp1
    f.close()

    return varsPresent


def findStations(wd,stationsDict,name,interval,tp,varNames=[],Pr=None,lat=None,lon=None,elev=None,verbose='off'):
    """
    Mandatory Filters:
    Filter1: Name contains a string (e.g. 'MONTREAL' or 'TORONTO'). Enter '' for all.
    Filter2: Interval ('hourly', 'daily' or 'monthly').
    Filter3: Recorded time period tp (e.g. ['1950','2016'])

    Optional Filters:
    Filter4: Desired variable name (e.g. Wind Spd (km/h)). Leave as empty list if all variables are desired.
    Filter5: In one or more provinces/territories.
    Filter6: Within a lat/lon interval.
    Filter7: Within an elevation interval.
    Filter8: With a climateId or a WMO ID.


    And output a list: [['Name_1', 'StationID_1', 'interval_1', 'FirstYear_1', 'LastYear_1'],
                        ['Name_2', 'StationID_2', 'interval_2', 'FirstYear_2', 'LastYear_2'], ...]

    name will always be converted to all uppercase, because stations name in the dict are all uppercase.

    To do:
    - Add the code for ClimateId, Province, lat, lon and elevation constraints
    - Revise the checkVar() algorithm. It uses only the 1st year in range at the 1st month and day. We may miss some stations
      for which data starts later in the year. (I think?, maybe the right variable names are there even without data)
    """
    if len(tp)==2:
        tp[0],tp[1] = str(tp[0]),str(tp[1])
    else:
        raise ValueError('Error in parameter input to findStations(). Parameter tp must be a list with only 2 values.')
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
    #constraints = [name,interval,interv1,interv2,varNames,tp,Pr,lat,lon,elev]

    if verbose=='on': print 'Finding stations containing "'+name+'" at interval "'+interval+'" within time period '+\
    tp[0]+'-'+tp[1]+' containing variable(s) '+str(varNames)

    keys = stationsDict.keys()
    count = 0.
    start = time.time()
    for key in keys:
        if (name.upper() in key) and stationsDict[key][interv1]<=tp[1] and stationsDict[key][interv2]>=tp[0]:
            t1 = max(int(stationsDict[key][interv1]),int(tp[0])); t2 = min(int(stationsDict[key][interv2]),int(tp[1]))
            stations.append([key,stationsDict[key][2],interval,t1,t2])
        count = count + 1
        update_progress(count/len(keys))
    count = 0.
    for station in stations:
        if varNames==[]:
            pass
        elif checkVar(varNames,station[1],station[2],station[3])==False:
            stations.remove(station)
        count = count + 1
        update_progress(count/len(stations))
    print "findStations() Elapsed Time: %s" % (time.time() - start)

# # Attempts to parallelize search
#     def searchVarNames(count,varNames,station,stations,queue):
#         key,stationID,interval,t1,t2 = station[0],station[1],station[2],station[3],station[4]
#         if varNames==[]:
#             pass
#         elif checkVar(varNames,stationID,interval,t1)==False:
#             stations.remove([key,stationsDict[key][2],interval,t1,t2])
#         count = count + 1
#         update_progress(count/len(stations))
#         queue.put(station)

#     def search_parallel(stations):
#         start = time.time()
#         result = Queue.Queue()
#         count = 0.
#         threads = [threading.Thread(target=searchVarNames, args = (count,varNames,station,stations,result)) for station in stations]
#         for t in threads:
#             t.start()
#         for t in threads:
#             t.join()
#         print "findStations() Elapsed Time: %s" % (time.time() - start)
#         return result

#     search_parallel(stations)


    print 'Found '+str(len(stations))+' station(s):'
    pprint(stations) if len(stations)<=100 else pprint('>100 stations, so not displaying')

    ans = raw_input('Do you want to download data for all '+str(len(stations))+' stations? (y/n) \n')
    if ans=='n':
        sys.exit()
    elif ans=='y':
        with open(wd+'findStationsList_"'+str(name)+'".csv', "wb") as f:
            writer = csv.writer(f)
            writer.writerows(stations)
        return stations
    else:
        raise ValueError()




def genDownloadList(stations, verbose='off'):
    """
    Use a list of stations output by findStations and transform it into 
    a downloadList that can be used by multipleDownloads.
    """
    now = datetime.datetime.now(); m=now.month; y=now.year

    downloadList = []

    for station in stations:
        if station[2]=='monthly':
            downloadList.append([station[0],station[1],station[2],'1','1','1'])
        elif station[2]=='daily':
            for year in range(station[3],station[4]+1):
                downloadList.append([station[0],station[1],station[2],'1','1',year])
        elif station[2]=='hourly':
            for year in range(station[3],station[4]+1):
                for month in range(1,12+1):
                    if year==y and month>m:
                        break
                    else:
                        downloadList.append([station[0],station[1],station[2],'1',month,year])
        else:
            raise ValueError('Invalid input to genDownloadList: interval')
    if verbose=='on': print 'Found '+str(len(downloadList))+' files to download:'
    pprint(downloadList) if len(downloadList)<=100 else pprint('>100 stations, so not displaying')

    return downloadList


def multipleDownloads(wd,downloadList,skipExist=True,verbose='off'):
    """
    wd: working directory
    downloadList: a list containing a list for each file to downloade
    skipExist: boolean representing whether to skip existing files when downloading to save time.
    verbose: for debugging

    downloadList must have format:
    [['stationName_1', 'stationID_1', 'interval_1', 'day_1', 'month_1', 'year_1'],
     ['stationName_2', 'stationID_2', 'interval_2', 'day_2', 'month_2', 'year_2'],
     ['stationName_3', 'stationID_3', 'interval_3', 'day_3', 'month_3', 'year_3'], ...]

     To do:
     - Respect Env Can downloading guidelines. They might block downloads if there are too many.
     - add threading.
    """
    # size=0.0
    # count=0.0
    # tot=len(downloadList)
    # for i in downloadList:
    #     if not os.path.exists(wd+'/'+i[0]):
    #         os.makedirs(wd+'/'+i[0])
    #     filename = mkFilename(i[2],i[0],i[1],i[5],i[4])
    #     if skipExist:
    #         if os.path.exists(wd+'/'+i[0]+'/'+filename+'.csv'):
    #             pass
    #         else:
    #             downloader(wd+'/'+i[0],i[0],i[1],i[2],i[3],i[4],i[5],verbose)
    #     else:
    #         downloader(wd+'/'+i[0],i[0],i[1],i[2],i[3],i[4],i[5],verbose)
    #     count=count+1.0
    #     update_progress(count/tot)
    #     size=size+os.path.getsize(wd+'/'+i[0]+'/'+filename+'.csv')
    #     sys.stdout.write(str(round(size,3)/1E6)+' MB')
    #     sys.stdout.flush()

    #Above code works as is. Under is experimental parallel.
    #################################################################################

    os.chdir(wd)

    # Make list of URLs to download and their respective filenames. i.e. [[url1,filename1],[url2,filename2],...]
    urls_to_download = []
    for i in downloadList:
        url = urlBuilder(i[1],i[2],i[3],i[4],i[5])
        filename = mkFilename(i[2],i[0],i[1],i[5],i[4])
        urls_to_download.append([url,filename])


    def download_url(url1,skipExist,queue):
        url,filename = url1[0],url1[1]
        name = filename.split('_')[0]
        try:
            if not os.path.exists(wd+name):
                os.makedirs(wd+name)
        except OSError, e:
            if e.errno != 17:
                pass
        data = urllib2.urlopen(url).read()
        fileSave = open(wd+name+'/'+filename+'.csv',"w")
        fileSave.write(data)
        fileSave.close()
        #size=size+os.path.getsize(wd+'/'+name+'/'+filename+'.csv')
        #sys.stdout.write(str(round(size,3)/1E6)+' MB')
        #sys.stdout.flush()
        queue.put(data)

        # if skipExist:
        #     if os.path.exists(wd+'/'+name+'/'+filename+'.csv'):
        #         pass
        #     else:
        #         data = urllib2.urlopen(url).read()
        #         fileSave = open(wd+'/'+name+'/'+filename+'.csv',"w")
        #         fileSave.write(data)
        #         fileSave.close()
        #         count=count+1.0
        #         update_progress(count/tot)
        #         size=size+os.path.getsize(wd+'/'+name+'/'+filename+'.csv')
        #         sys.stdout.write(str(round(size,3)/1E6)+' MB')
        #         sys.stdout.flush()
        #         queue.put(data)
        # else:
        #     data = urllib2.urlopen(url).read()
        #     fileSave = open(wd+'/'+name+'/'+filename+'.csv',"w")
        #     fileSave.write(data)
        #     fileSave.close()
        #     count=count+1.0
        #     update_progress(count/tot)
        #     size=size+os.path.getsize(wd+'/'+name+'/'+filename+'.csv')
        #     sys.stdout.write(str(round(size,3)/1E6)+' MB')
        #     sys.stdout.flush()
        #     queue.put(data)


    def fetch_parallel(urls_to_download):
        count,size = 0.,0.
        start = time.time()
        result = Queue.Queue()
        threads = [threading.Thread(target=download_url, args = (url,skipExist,result)) for url in urls_to_download]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        #print "Elapsed Time: %s" % (time.time() - start)
        return result

    chunck = 200
    iterations = int(m.ceil(len(urls_to_download)/float(chunck)))
    for i in range(0,iterations):
        if i==((iterations-1)):
            fetch_parallel(urls_to_download[i*chunck:len(urls_to_download)])
        else:
            fetch_parallel(urls_to_download[i*chunck:i*chunck+chunck])
        update_progress(float(i)/iterations)



def downloader(wd,stationName,stationID,interval,day,month,year,verbose='off'):
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
    - Better exception handling
    """
    day,month,year = str(day),str(month),str(year)
    os.chdir(wd)
    if verbose=='on': print 'Working directory set to: '+wd

    url = urlBuilder(stationID,interval,day,month,year,verbose)

    filename = mkFilename(interval,stationName,stationID,year,month)

    if verbose=='on': print 'Downloading from '+url+' to '+filename+'.csv'
    f = urllib2.urlopen(url)
    data = open(filename+'.csv',"w")
    data.write(f.read())
    data.close()
    if verbose=='on': print 'Done Downloading '+filename+'.csv'

    return filename
    
def mkFilename(interval, stationName, stationID, year, month):
    interval,stationName,stationID,year,month = str(interval),str(stationName),str(stationID),str(year),str(month)
    if interval=='hourly':
        filename = stationName+'_'+stationID+'_hourly_'+year+'_'+month
    elif interval=='daily':
        filename = stationName+'_'+stationID+'_daily_'+year
    elif interval=='monthly':
        filename = stationName+'_'+stationID+'_monthly'
    filename = filename.replace('/','')
    return filename


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

    url = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID='+stationID+'&Year='+year+'&Month='+month+'&Day='+day+'&timeframe='+tf+'&submit= Download+Data'
    if verbose=='on': print "Built URL: ",url,'\n'
        
    return url


def genStationsDict(wd,downloadNew=True,ver=True):
    """
    Downloads the daily-updated .csv file that contains all station IDs (and more) to the working directory.
    
    Output dict layout:
    {'Station Name': ['Province', 'Climate ID', 'Station ID', 'WMO ID', 'TC ID',
    'Latitude (decimal degrees)', 'Longitude (decimal degrees)', 'Latitude', 'Longitude',
    'Elevation (m)', 'First Year', 'Last Year', 'HLY First Year', 'HLY Last Year',
    'DLY First Year', 'DLY Last Year', 'MLY First Year', 'MLY Last Year']}

    To Do:
    - Add ability to gen dict without saving the inventory file to disk.
    """
    os.chdir(wd)
    if ver==True: print 'Working directory set to: '+wd
    
    if downloadNew==True:
        try:
            print 'Downloading StationInventoryEN.csv to '+wd
            f = urllib2.urlopen('ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv')
            data = open("StationInventoryEN.csv","w")
            data.write(f.read())
            data.close()
            print 'Done Downloading StationInventoryEN.csv'
        except(URLError): print 'Error getting stationInventoryEN.csv from servers, using previous download if availble.'

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
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress,5)*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()