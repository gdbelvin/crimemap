#!/usr/bin/env python3

import folium
import os

print(folium.__version__)

lon, lat = -38.625, -12.875

zoom_start = 8

m = folium.Map(
    location=[lat, lon],
    tiles='OpenStreetMap',
    zoom_start=zoom_start,
    control_scale=True
)

m.save(os.path.join('results', 'ControlScale.html'))

m
