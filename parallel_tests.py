import threading, urllib2, time, sys
import Queue

urls_to_load = [
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=1&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=2&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=3&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=4&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=5&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=6&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=7&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=8&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=9&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=10&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=11&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2014&Month=12&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=1&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=2&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=3&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=4&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=5&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=6&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=7&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=8&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=9&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=10&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=11&Day=1&timeframe=1&submit= Download+Data',
'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=51157&Year=2015&Month=12&Day=1&timeframe=1&submit= Download+Data',
]

def read_url(url, queue):
    global count, urls_to_load
    name = url.split('&')[2].replace('=','') + url.split('&')[3].replace('=','')
    data = urllib2.urlopen(url).read()
    fileSave = open('/home/nbrown/Desktop/test_parallel/'+name+'.csv',"w")
    fileSave.write(data)
    fileSave.close()
    #print('Fetched %s from %s' % (name, url))
    count = count +1.
    update_progress(count/len(urls_to_load))
    queue.put(data)

def fetch_parallel():
    start = time.time()
    result = Queue.Queue()
    threads = [threading.Thread(target=read_url, args = (url,result)) for url in urls_to_load]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print "Elapsed Time: %s" % (time.time() - start)
    return result

def fetch_sequencial():
    start = time.time()
    result = Queue.Queue()
    for url in urls_to_load:
        read_url(url,result)
    print "Elapsed Time: %s" % (time.time() - start)
    return result

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


count = 0.
fetch_parallel()