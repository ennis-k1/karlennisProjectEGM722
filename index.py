import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely import Point


center = (54.74276974698906, -6.7424020479405)
mapObj = folium.Map(location=center,zoom_start=8,tiles='Stamen Terrain')
pd.set_option('display.max_columns',None)

#import Local Government Districts (11 Council Boundaries)
lgd = gpd.read_file('data_files/OSNI_Open_Data_-_Largescale_Boundaries_-_Local_Government_Districts_(2012).shp')
lgd_itm = lgd.to_crs(epsg=4326)
mapObj = lgd_itm.explore('LGDNAME',cmap='viridis')
print(lgd_itm)

# #import the csv file of social housing developments
df = pd.read_csv('data_files/refinedSocialHousingDevelopments.csv')

# create a new geodataframe creating a geomentry column of points
developments = gpd.GeoDataFrame(df, # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['Long'], df['Lat']), # set the geometry using points_from_xy
                             crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

developments.explore('Scheme Name',
                  m=mapObj, # add the markers to the same map we just created
                  marker_type='marker', # use a marker for the points, instead of a circle
                  popup=True, # show the information as a popup when we click on the marker
                  legend=False, # don't show a separate legend for the point layer
                 )
# IDENTIFY DEVELOPMENTS IN EACH LGD BY JOINING THE TABLE TO THE SHAPEFILE
join = gpd.sjoin(lgd_itm, developments, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join
#GROUP AND SUMMARISE THE STATUS OF DEVELOPMENTS IN EACH LGD
print(join.groupby(['LGDNAME', 'Status'])['Units'].sum()) # summarize the road lengths by CountyName, Road_class

#mapObj.show_in_browser()
mapObj.save("map2.html")