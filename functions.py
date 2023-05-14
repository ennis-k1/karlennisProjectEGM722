import numpy as np
import folium
import ee
from shapely.ops import nearest_points
from math import sin, cos, sqrt, atan2, radians
import geopandas as gpd
import pandas as pd
from pathlib import Path  
exportPath = Path('data_files/exports')

def prettyPrint(title, data):
  
  '''Formats the object to be printed in a prettier format, Object Title In Uppercase followed by Object Data on a new line'''
  title = title.upper()
  print(title,":\n",data, "\n\n")

def caclDistance(lon1,lon2,lat1,lat2):
    '''Calculates the distance between 2 points of Lat, Long using the Haversine Formula giving an As The Crow Flies result'''
    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance_haversine_formula = 6371 * c # Radius of earth in kilometers. Determines return value units.
    distance_haversine_formula = round(distance_haversine_formula* 0.62137,2) # ANSWER IN MILES ROUNDED TO 2 DECIMAL PLACES
    return distance_haversine_formula


def get_nearest_values(row, other_gdf, point_column='geometry', value_column="geometry"):
    """Find the nearest point and return the corresponding value from specified value column."""
    
    # Create an union of the other GeoDataFrame's geometries:
    other_points = other_gdf["geometry"].unary_union
    
    # Find the nearest points
    nearest_geoms = nearest_points(row[point_column], other_points)
    
    # Get corresponding values from the other df
    nearest_data = other_gdf.loc[other_gdf["geometry"] == nearest_geoms[1]]
    
    nearest_value = nearest_data[value_column].values[0]
    
    return nearest_value


def exportToCsv (df,title):
   filepath = Path('data_files/exports/'+ title + '.csv')  
   filepath.parent.mkdir(parents=True, exist_ok=True)  
   df.to_csv(filepath)  
