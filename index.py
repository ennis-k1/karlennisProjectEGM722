import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely import Point


#N.B FOR REFERENCE, A 'UNIT' IN TERMS OF SOCIAL HOUSING REFERS TO A PLACE OF HABITATION, 
# EG A HOUSE IS A UNIT WHICH WILL HOME MULTIPLE PEOPLE, 
# AN APPARTMENT IS A UNIT WITHIN AN APPARTMENT BLOCK WHICH HAS MANY UNITS


center = (54.74276974698906, -6.7424020479405)
mapObj = folium.Map(location=center,zoom_start=8,tiles='Stamen Terrain')
pd.set_option('display.max_columns',None)

#import Local Government Districts (11 Council Boundaries)
lgd = gpd.read_file('data_files/OSNI_Open_Data_-_Largescale_Boundaries_-_Local_Government_Districts_(2012).shp')
lgd_itm = lgd.to_crs(epsg=4326)
mapObj = lgd_itm.explore('LGDNAME',cmap='viridis')
print(lgd_itm)

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
print('DEVELOPMENTS BY STATUS IN A LGD:\n',join.groupby(['LGDNAME', 'Status'])['Units'].sum())
#CREATE A DATAFRAME OF ALL DEVELOPMENTS IN EACH LGD WHICH CAN LATER BE MATCHED TO THE NEEDS IN EACH LGD
lgdDevelopmentsSummary = join.groupby(['LGDNAME'])['Units'].sum();
#GROUP AND SUMMARISE ALL DEVELOPMENTS IN EACH LGD
print('ALL DEVELOPMENTS IN A LGD:\n',lgdDevelopmentsSummary)

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
lgdNeedsSummary = joinHousingNeeds.groupby(['LGDNAME'])['Total 5 Year Need Projection'].sum();
print('NUMBER OF UNITS NEEDED IN A LGD:\n',lgdNeedsSummary) # summarize the road lengths by CountyName, Road_class


#*********************** MERGE BOTH DATA SETS *************************
#CREATE A NEW DATAFRAME WHICH MERGES THE NUMBER OF DEVELOPMENTS IN A LGD WITH THE TOTAL OF UNITS NEEDED IN A LGD
lgdNeedsAndDevelopments = lgdDevelopmentsSummary.to_frame().merge(lgdNeedsSummary, on='LGDNAME')


#lgdNeedsAndDevelopments['Difference'] = lgdNeedsAndDevelopments['Total 5 Year Need Projection'] - lgdNeedsAndDevelopments['Units']
#lgdNeedsAndDevelopments['Difference'] = lgdNeedsAndDevelopments.apply(lambda x: x['Total 5 Year Need Projection'] - x['Units'], axis=1)
lgdNeedsAndDevelopments = lgdNeedsAndDevelopments.assign(Units_Outstanding = lgdNeedsAndDevelopments['Total 5 Year Need Projection'] - lgdNeedsAndDevelopments['Units'])
print('NUMBER OF UNITS NEEDED AGAINST UNITS DELIVERED:\n',lgdNeedsAndDevelopments)
print(lgdNeedsAndDevelopments.shape[0])
print(lgdNeedsAndDevelopments.shape[1])


#**************************** PLOT EACH LGD BASED ON UNITS OUTSTANDING *********************************************

lgdShapeCombined = lgd.merge(lgdNeedsAndDevelopments,on='LGDNAME')
lgdShapeCombined.rename(columns={'Units': 'Units Deliverable', 'Units_Outstanding': 'Units Outstanding'}, inplace=True)
lgdShapeCombined_itm = lgdShapeCombined.to_crs(epsg=4326)
#mapObj = lgdShapeCombined_itm.explore('LGDNAME',cmap='viridis')


#ADD LGD SHAPEFILE TO MAP
mapObj = lgdShapeCombined_itm.explore(
     column="Units Outstanding", # make choropleth based on "BoroName" column
      scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
      legend=True, # show legend
     k=5, # use 10 bins
     
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
                  legend=False, # don't show a separate legend for the point layer
                 )

#ADD SMALL SETTLEMENT NEEDS AREAS TO THE MAP
housingNeedAreas.explore(
     m=mapObj, # pass the map object
     color="red", # use red color on all points
     marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
     tooltip="Housing Need Assessment Area", # show "name" column in the tooltip
     tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
     popup=True, # show the information as a popup when we click on the marker
    legend=False, # don't show a separate legend for the point layer
     name="housingNeedAreas" # name of the layer in the map
)




#mapObj.show_in_browser()
mapObj.save("map.html")