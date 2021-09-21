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
import dash
import dash_core_components as dcc
import dash_html_components as html

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

#fig_reg.show()

# Heatmap

melt_reduced = melt.loc[melt['Year'] > '2012 Q1']

piv = melt_reduced.pivot("Region", "Year", "value")
fig_map = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral)
fig_map.layout.height=500
#fig_map.show()

# Line graph

fig_line = px.line(melt, x='Year', y='value', color='Region')
#fig_line.show()

# Dash 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
app.layout = html.Div([

    html.H1("Regional GVA Nowcasting", style={'text-align':'center'}),
    
    dcc.Dropdown(id='my-dropdown', value='2012 Q2',
                 options=[{'label': x, 'value': x} for x in
                          melt_reduced.Year.unique()]),
    dcc.Graph(id='my-graph', figure={}),
    dcc.Graph(
        id='line-graph',
        figure={}),
    ])

@app.callback(
    dash.dependencies.Output(component_id='my-graph', component_property='figure'),
    dash.dependencies.Input(component_id='my-dropdown', component_property='value')
)
def update_graph(year_chosen):
    dff = melt_reduced[melt_reduced.Year == year_chosen]
    fig = px.choropleth(dff, 
                    locations='id', 
                    geojson=regions, 
              color='value', 
              scope='europe')
    fig.update_geos(fitbounds='locations', visible=False)
    return fig

@app.callback(
    dash.dependencies.Output(component_id='line-graph', component_property='figure'),
    dash.dependencies.Input(component_id='my-graph', component_property='hoverData'),
    dash.dependencies.Input(component_id='my-dropdown', component_property='value')
)
def update_side_graph(hov_data, region_chosen):
    if hov_data is None:
        dff2 = melt_reduced[melt_reduced.Region == region_chosen]
        dff2 = dff2[dff2.Region == 'East']

        fig2 = px.line(dff2, x='Year', y='value')

        return fig2
    else:


        dff2 = melt_reduced[melt_reduced.Region == region_chosen]
        hov_region = hov_data['points'][0]['x']
        dff2 = dff2[dff2.Region == hov_region]
        fig2 = px.line(dff2, x='Year', y='value')
        return fig2

if __name__ == '__main__':
    app.run_server(debug=False)



    

