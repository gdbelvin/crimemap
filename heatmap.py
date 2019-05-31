#!/usr/bin/env python3

import folium
import os

'''
# Convert KML to geojson
import kml2geojson
import glob
for path in glob.glob('police_data/force_kmls/*.kml'):
    kml2geojson.main.convert(path, 'police_data/force_geo/')
'''

m = folium.Map(
    location=[51.5074, 0.1278],
    zoom_start=12,
    control_scale=True
)

force_geo = 'police_data/force_geo'
folium.GeoJson(f'{force_geo}/metropolitan.geojson', name='metro').add_to(m)
folium.GeoJson(f'{force_geo}/city-of-london.geojson', name='city').add_to(m)

folium.LayerControl().add_to(m)

m.save(os.path.join('results', 'ControlScale.html'))

m
