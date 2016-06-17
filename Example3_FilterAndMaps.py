"""
Filter through stations depending on the length and quality of data
Make maps of all filtered stations to see their geographic extent
"""

import DataDownloader as dd
import datetime, os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import iris, cartopy
import iris.plot as iplt
import cartopy.crs as ccrs

matplotlib.style.use('ggplot')


def get_coord(stationName,stationInvFileDir):
    stationInv = dd.genStationsDict(stationInvFileDir,downloadNew=False,ver=False)
    lat,lon,elev = stationInv[stationName][5],stationInv[stationName][6],stationInv[stationName][9]
    return lat,lon,elev


files = sorted(os.listdir('/home/nbrown/Desktop/plots'))
files[:] = [ x for x in files if '_merged.csv' in x ]
lats,lons,elevs = np.empty(0),np.empty(0),np.empty(0)
count=1.
for f in files:
    f = f.split('_')[0]
    try:
        lat,lon,elev = get_coord(f,'/home/nbrown/Desktop/test')
        lats = np.append(lats,lat)
        lons = np.append(lons,lon)
        elevs = np.append(elevs,elev)
    except KeyError,e:
        print e
        pass
    dd.update_progress(count/len(files))
    count=count+1.

fig1 = plt.figure(figsize=(6,9.5))

ax = plt.subplot(111,projection=ccrs.Mollweide(central_longitude=-95))
SC = ax.scatter(lons,lats,marker='o',transform=ccrs.PlateCarree())
#cbar = plt.colorbar(CS, cmap='coolwarm', orientation='horizontal')

plt.gca().coastlines(resolution='50m')
plt.grid()
fig1.show()