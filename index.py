
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
from shapely import Point
import functions
import basemaps
import numpy as np
import rasterio as rio
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from folium import plugins
import rasterio.warp
from pyproj import Transformer 
import os
from sentinelsat import SentinelAPI, make_path_filter
from IPython import display # lets us display images that we download
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
api = SentinelAPI(None, None)
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
from numpy.random import randn


pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)


#import Local Government Districts (11 Council Boundaries)
lgd = gpd.read_file('data_files/OSNI_Open_Data_-_Largescale_Boundaries_-_Local_Government_Districts_(2012).shp')

lgd_itm = lgd.to_crs(epsg=4326)
mapObj = lgd_itm.explore('LGDNAME',cmap='viridis')
lgd.to_html('LGD_Data.html',columns=('LGDCode','LGDNAME','AREA','OBJECTID'),float_format='{:20,.2f}'.format) #CREATES HTML FILE
functions.prettyPrint('LGD Data',lgd_itm) #PRINTS DATAFRAME TO CONSOLE


#************* HOUSING DEVELOPMENTS DATA ***************************

# #import the csv file of social housing developments
df = pd.read_csv('data_files/refinedSocialHousingDevelopments.csv')
# create a new geodataframe creating a geomentry column of points
developments = gpd.GeoDataFrame(df, # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['Long'], df['Lat']), # set the geometry using points_from_xy
                             crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon


# IDENTIFY DEVELOPMENTS IN EACH LGD BY JOINING THE TABLE TO THE SHAPEFILE
join = gpd.sjoin(lgd_itm, developments, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join
#GROUP AND SUMMARISE THE STATUS OF DEVELOPMENTS IN EACH LGD
tempDf = join.groupby(['LGDNAME', 'Status'])['Units'].agg(['sum','count'])
tempDf.to_html('Developments_By_Status.html',float_format='{:20,.2f}'.format) #CREATES HTML FILE
functions.prettyPrint("DEVELOPMENTS BY STATUS IN A LGD",join.groupby(['LGDNAME', 'Status'])['Units'].agg(['sum','count']) )
#CREATE A DATAFRAME OF ALL DEVELOPMENTS IN EACH LGD WHICH CAN LATER BE MATCHED TO THE NEEDS IN EACH LGD
lgdDevelopmentsSummary = join.groupby(['LGDNAME'])['Units'].agg(['sum','count'])
lgdDevelopmentsSummary.to_html('Developments In A LGD.html',float_format='{:20,.2f}'.format) #CREATES HTML FILE

#GROUP AND SUMMARISE ALL DEVELOPMENTS IN EACH LGD
functions.prettyPrint("ALL DEVELOPMENTS IN A LGD",lgdDevelopmentsSummary)



#************* HOUSING NEEDS DATA ***************************
#import the csv
housingNeedsDataFrame = pd.read_csv('data_files/refinedSocialHousingNeeds.csv',header=0,sep=",")
# create a new geodataframe creating a geomentry column of points
housingNeedAreas = gpd.GeoDataFrame(housingNeedsDataFrame, # use the csv data, 
                            geometry=gpd.points_from_xy(housingNeedsDataFrame['Long'], housingNeedsDataFrame['Lat']), # set the geometry using points_from_xy
                             crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

# IDENTIFY SMALL SETTLEMENT NEEDS IN EACH LGD BY JOINING THE TABLE TO THE SHAPEFILE
joinHousingNeeds = gpd.sjoin(lgd_itm, housingNeedAreas, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join
pd.set_option('display.max_columns',None)
#GROUP AND SUMMARISE THE TOTAL NUMBER OF UNITS REQUIRED IN EACH LGD
lgdNeedsSummary = joinHousingNeeds.groupby(['LGDNAME'])['Total 5 Year Need Projection'].sum()
lgdNeedsSummary = pd.DataFrame(lgdNeedsSummary)
functions.prettyPrint("NUMBER OF UNITS NEEDED IN A LGD",lgdNeedsSummary )
lgdNeedsSummary.to_html('Need Projected In A LGD.html',float_format='{:20,.2f}'.format) #CREATES HTML FILE


#**********************************************************************

# USE NEAREST LOCATION TO APPEND THE NEAREST HOUSING DEVELOPMENT TO EACH SMALL SETTLEMENT
unary_union = developments.unary_union
housingNeedAreas["Nearest Development Scheme"] = housingNeedAreas.apply(functions.get_nearest_values, other_gdf=developments, point_column="geometry", value_column="Scheme Name", axis=1)
housingNeedAreas["Nearest Development Lat"] = housingNeedAreas.apply(functions.get_nearest_values, other_gdf=developments, point_column="geometry", value_column="Lat", axis=1)
housingNeedAreas["Nearest Development Long"] = housingNeedAreas.apply(functions.get_nearest_values, other_gdf=developments, point_column="geometry", value_column="Long", axis=1)


#CREATE A NEW EMPTY COLUMN TO STORE THE DISTANCE BETWEEN THE SMALL SETTLEMENT AND THE NEAREST DEVELOPMENT
housingNeedAreas['Distance'] = np.nan


for index, row in housingNeedAreas.iterrows():
    lon1 = row['Long']
    lat1 = row['Lat']
    lon2 = row["Nearest Development Long"]
    lat2 = row["Nearest Development Lat"]
    housingNeedAreas.at[index,"Distance"] = functions.caclDistance(lon1,lon2,lat1,lat2)

housingNeedAreas = housingNeedAreas.sort_values('Distance', ascending=False)
housingNeedAreas.rename(columns = {'Distance':'Distance(miles)'}, inplace = True)
functions.exportToCsv(housingNeedAreas,"Small Settlements With Nearest Housing Developments")
functions.prettyPrint('Small Settlements With Nearest Housing Developments.html',housingNeedAreas)
housingNeedAreas.to_html('Small Settlements With Nearest Housing Developments.html',float_format='{:20,.2f}'.format) #CREATES HTML FILE

#*********************** MERGE BOTH DATA SETS *************************

#CREATE A NEW DATAFRAME WHICH MERGES THE NUMBER OF DEVELOPMENTS IN A LGD WITH THE TOTAL OF UNITS NEEDED IN A LGD
lgdNeedsAndDevelopments = lgdDevelopmentsSummary.merge(lgdNeedsSummary, on='LGDNAME')
lgdNeedsAndDevelopments.info()
lgdNeedsAndDevelopments = lgdNeedsAndDevelopments.assign(Units_Outstanding = lgdNeedsAndDevelopments['Total 5 Year Need Projection'] - lgdNeedsAndDevelopments['sum'])
functions.prettyPrint("NUMBER OF UNITS NEEDED AGAINST UNITS DELIVERED",lgdNeedsAndDevelopments)
lgdNeedsAndDevelopments.to_html('LGD Shortfall.html',float_format='{:20,.2f}'.format) #CREATES HTML FILE

#**************************** PLOT EACH LGD BASED ON UNITS OUTSTANDING *********************************************

lgdShapeCombined = lgd.merge(lgdNeedsAndDevelopments,on='LGDNAME')
lgdShapeCombined.rename(columns={'sum': 'Units Deliverable', 'Units_Outstanding': 'Units Outstanding'}, inplace=True)
lgdShapeCombined_itm = lgdShapeCombined.to_crs(epsg=4326)


#ADD LGD SHAPEFILE TO MAP
mapObj = lgdShapeCombined_itm.explore(
     column="Units Outstanding", # make choropleth based on "Units Outstanding" column
      scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
      legend=True, # show legend
     k=5, # use 5 bins
     crs='EPSG3857',
     legend_kwds=dict(colorbar=False), # do not use colorbar
     name="LGD Units Outstanding", # name of the layer in the map
     tooltip=["LGDNAME","Units Outstanding"], # show "BoroName" value in tooltip (on hover)
     popup=["LGDNAME","LGDCode","Total 5 Year Need Projection","Units Deliverable","Units Outstanding"], # show all values in popup (on click)
     tiles="CartoDB positron", # use "CartoDB positron" tiles
     cmap="plasma", # use "Set1" matplotlib colormap
     style_kwds=dict(color="black") # use black outline
    )

#ADD DEVELOPMENTS TO THE MAP
developments.explore('Scheme Name',
                  m=mapObj, # add the markers to the same map we just created
                  marker_type='marker', # use a marker for the points, instead of a circle
                  marker_kwds= {'icon': folium.Icon(color='red', icon='home', prefix='fa')}, # make the markers red with a house icon from FA
                  popup=True, # show the information as a popup when we click on the marker
                  legend=False, # don't show a separate legend for the point layer,
                  name='Housing Developments'
                 )

#ADD SMALL SETTLEMENT NEEDS AREAS TO THE MAP
housingNeedAreas.explore(
     m=mapObj, # pass the map object
     color="red", # use red color on all points
     marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
     tooltip=["Housing Need Assessment Area","Total 5 Year Need Projection"] ,# show "name" column in the tooltip
     tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
     popup=True, # show the information as a popup when we click on the marker
    legend=False, # don't show a separate legend for the point layer
     name="Housing Need Areas" # name of the layer in the map
)

# Add a layer control panel to the map.
mapObj.add_child(folium.LayerControl())

#fullscreen
plugins.Fullscreen().add_to(mapObj)

#GPS
plugins.LocateControl().add_to(mapObj)

#mouse position
fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(mapObj)

#Add the draw 
plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(mapObj)  

#Add measure tool 
plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(mapObj)
 

#mapObj.show_in_browser()
mapObj.save("map.html")