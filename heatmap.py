#!/usr/bin/env python3

import folium
from folium import plugins
import os
import glob
import pandas as pd

'''
# Convert KML to geojson
import kml2geojson
for path in glob.glob('police_data/boundaries/force_kmls/*.kml'):
    kml2geojson.main.convert(path, 'police_data/force_geo/')
'''

m = folium.Map(
    location=[51.517742, -0.187590],
    zoom_start=14,
    control_scale=True
)

# Police force boundaries
if False:
    force_geo = 'police_data/boundaries/force_geo'
    folium.GeoJson(f'{force_geo}/metropolitan.geojson', name='metro').add_to(m)
    folium.GeoJson(f'{force_geo}/city-of-london.geojson', name='city').add_to(m)


if False:
    # neighborhood Boundaries
    # https://data.police.uk/data/boundaries/
    neighborood_geo = 'police_data/boundaries/neighborhood/2019-03'
    for path in glob.glob(f'{neighborood_geo}/*/*.geojson'):
        name = os.path.basename(path)
        folium.GeoJson(path, name=name,
                       tooltip=folium.features.Tooltip(name, sticky=False),
                       ).add_to(m)

# Crime HeatMap
if True:
    crime_data = 'police_data/crime/'
    crime_dfs = []
    i = 0
    for path in glob.glob(f'{crime_data}/*.csv'):
        df_crime = pd.read_csv(path, usecols=['Latitude', 'Longitude'])
        df_crime = df_crime.dropna(subset=['Latitude', 'Longitude'])
        crime_dfs.append(df_crime)
        i = i+1
        if i > 4:
            break  # Don't overload the map javascript.

    all_crime = pd.concat(crime_dfs)
    crime_arr = all_crime[['Latitude', 'Longitude']].values
    m.add_child(plugins.HeatMap(crime_arr, radius=10))


# Crime Points
if False:
    # df_crime = pd.DataFrame(df_crime, columns = ['Latitude','Longitude', 'LSOA code', 'Crime type'])
    crime_layer = folium.FeatureGroup(name='Crime Locations')
    for i, row in df_crime.iterrows():
        crime_layer.add_child(
            folium.CircleMarker([row['Latitude'], row['Longitude']],
                                popup=row['Crime type'],
                                radius=5,
                                fill_color="#3db7e4",
                                ))
        if i > 100000:
            break
    m.add_child(crime_layer)

folium.LayerControl().add_to(m)

m.save('index.html')

m
