# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 15:02:16 2021

@author: vincer
"""
# Import packages

import geopandas as gpd
import pandas as pd
import json
import geojson
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

# Pre processing

regions = json.load(open("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\Inputs\International_Territorial_Level_1_(May_2021)_UK_BUC.geojson", 'r'))
gdp = pd.read_excel('T:\Personal Drives\Rebecca\Data Visualisation Accelerator\Inputs\February_Regional_Growth.xlsx', sheet_name='Real')

gdp = gdp.rename(columns={'Unnamed: 0': 'Year', 'North East': 'North East (England)', 'North West':'North West (England)', 
                          'South East':'South East (England)', 'South West':'South West (England)', 
                          'East Midlands':'East Midlands (England)', 'West Midlands':'West Midlands (England)', 
                          'East of England':'East'})

regions_list = ['North East (England)', 'North West (England)', 'Yorkshire and The Humber', 'East Midlands (England)', 'East','London', 'South East (England)', 'South West (England)', 'West Midlands (England)', 'Wales', 'Scotland', 'Northern Ireland']

melt = pd.melt(gdp, id_vars=['Year'], value_vars=regions_list)
melt = melt.rename(columns={'variable':'Region'})
melt_21  = melt.loc[melt['Year'] == '2020 Q1']

region_id_map = {}
for feature in regions['features']:
    feature['id'] = feature['properties']['ITL121NM']
    region_id_map[feature['properties']['ITL121NM']] = feature['id']

melt['id'] = melt['Region'].apply(lambda x:region_id_map[x])

# Build map 

fig_reg = px.choropleth(melt, 
                    locations='id', 
                    geojson=regions, 
              color='value', 
              scope='europe')
fig_reg.update_geos(fitbounds='locations', visible=False)
fig_reg.update_layout(title_text='Regional GVA Nowcasting', title_font_size=25, 
                  title_x = 0.5)

fig_reg.show()

# Heatmap

melt_reduced = melt.loc[melt['Year'] > '2012 Q1']

piv = melt_reduced.pivot("Region", "Year", "value")
fig_map = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral)
fig_map.layout.height=500
fig_map.show()

# Dash 


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig_map, 
    style={'width':'49%', 'display':'inline-block'}),
    dcc.Graph(figure=fig_reg,
    style={'width':'49%', 'display':'inline-block'})
])

app.run_server(debug=False, use_reloader=False)  # Turn off reloader if inside Jupyter

