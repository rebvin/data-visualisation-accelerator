# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 09:08:29 2021

@author: vincer
"""

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
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
import ast
from IPython.display import Image

regions = json.load(open("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\Inputs\International_Territorial_Level_1_(May_2021)_UK_BUC.geojson", 'r'))
gdp = pd.read_excel('T:\Personal Drives\Rebecca\Data Visualisation Accelerator\Inputs\February_Regional_Growth.xlsx', sheet_name='Real')
rsme = pd.read_excel("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\Inputs\\uncertainty_data.xlsx")



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

img = 'T:\Personal Drives\Rebecca\Data Visualisation Accelerator\ons_logo.png'
Image(url=img)

# Build map 

fig_reg = px.choropleth(melt, 
                    locations='id', 
                    geojson=regions, 
              color='value', 
              scope='europe')
fig_reg.update_geos(fitbounds='locations', visible=False)
fig_reg.update_layout(title_text='Regional GVA Nowcasting', title_font_size=25, 
                  title_x = 0.5)

# Heatmap

melt_reduced = melt.loc[melt['Year'] > '2012 Q1']

piv = melt_reduced.pivot("Region", "Year", "value")
fig_map = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral)
#fig_map.layout.height=500
#fig_map.show()

# Line graph

fig_line = px.line(melt, x='Year', y='value', color='Region')
#fig_line.show()

# Spider chart

fig_spider = px.line_polar(melt_21, r='value', theta='Region', line_close=True)
#fig_spider.show()

# ITL2

itl2 = json.load(open("T:\\Personal Drives\\Rebecca\\Data Visualisation Accelerator\\ITL2\\International_Territorial_Level_2_(May_2021)_UK_BUC.geojson", 'r'))
gdp2 = pd.read_csv("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\ITL2\itl2_faked.csv")
columns_reg = ['Tees Valley and Durham',	'Northumberland, and Tyne and Wear',	'Cumbria', 'Greater Manchester',	'Lancashire',	'Cheshire',	'Merseyside'	,'East Yorkshire and Northern Lincolnshire',	'North Yorkshire',	'South Yorkshire',	'West Yorkshire'	,'Derbyshire and Nottinghamshire',	'Leicestershire, Rutland and Northamptonshire',	'Lincolnshire',	'Herefordshire, Worcestershire and Warwickshire',	'Shropshire and Staffordshire',	'West Midlands',	'East Anglia',	'Bedfordshire and Hertfordshire',	'Essex',	'Inner London - West	', 'Inner London - East',	'Outer London - East and North East',	'Outer London - South',	'Outer London - West and North West', 'Berkshire, Buckinghamshire and Oxfordshire',	'Surrey, East and West Sussex',	'Hampshire and Isle of Wight	','Kent',	'Gloucestershire, Wiltshire and Bath/Bristol area',	'Dorset and Somerset', 'Cornwall and Isles of Scilly',	'Devon',	'West Wales and The Valleys',	'East Wales',	'North Eastern Scotland',	'Highlands and Islands',	'Eastern Scotland',	'West Central Scotland', 	'Southern Scotland',	'Northern Ireland']
gdp2 = gdp2.rename(columns={'Northumberland and Tyne and Wear':'Northumberland, and Tyne and Wear'})

melt2 = pd.melt(gdp2, id_vars=['Year'], value_vars=columns_reg)
melt2 = melt2.rename(columns={'variable':'Region'})
melt2_21  = melt2.loc[melt2['Year'] == '2020 Q1']

region_id_map = {}
for feature in itl2['features']:
    feature['id'] = feature['properties']['ITL221NM']
    region_id_map[feature['properties']['ITL221NM']] = feature['id']
    

melt2['Region'].replace({'Inner London - West\t':'Inner London - West', 'Hampshire and Isle of Wight\t':'Hampshire and Isle of Wight'}, inplace=True)

melt2['id'] = melt2['Region'].apply(lambda x:region_id_map[x])

fig2 = px.choropleth(melt2, 
                    locations='id', 
                    geojson=itl2, 
              color='value', 
              scope='europe')
fig2.update_geos(fitbounds='locations', visible=False)
fig2.update_layout(title_text='Regional GVA Nowcasting', title_font_size=25, 
                  title_x = 0.5)


# ITL3

itl3 = pd.read_csv("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\ITL3\itl3_faked_data.csv")
itl3_json = json.load(open("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\ITL3\International_Territorial_Level_3_(May_2021)_UK_BUC.geojson", 'r'))
itl3_csv = pd.read_excel("T:\Personal Drives\Rebecca\Data Visualisation Accelerator\ITL3\itl3_regions.xlsx")
itl3_list = itl3_csv.columns.to_list()


melt3 = pd.melt(itl3, id_vars=['Year'], value_vars=itl3_list)
melt3 = melt3.rename(columns={'variable':'Region'})
melt3_21  = melt3.loc[melt3['Year'] == '2020 Q1']

region_id_map = {}
for feature in itl3_json['features']:
    feature['id'] = feature['properties']['ITL321NM']
    region_id_map[feature['properties']['ITL321NM']] = feature['id']
    
melt3['id'] = melt3['Region'].apply(lambda x:region_id_map[x])

fig3 = px.choropleth(melt3, 
                    locations='id', 
                    geojson=itl3_json, 
              color='value', 
              scope='europe')
fig3.update_geos(fitbounds='locations', visible=False)
fig3.update_layout(title_text='Regional GVA Nowcasting', title_font_size=25, 
                  title_x = 0.5)

# Dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab1 = html.Div([
    html.H3(children='ITL 1', style={'font-family': 'Arial'}),
    dcc.Dropdown(id='my-dropdown-1', value='2012 Q2',
                 options=[{'label': x, 'value': x} for x in
                          melt_reduced.Year.unique()]),
    dcc.Graph(id='my-graph-1', figure={}, style={'width': '49%', 'display': 'inline-block'}),
    dcc.Graph(
        id='line-graph-1',
        figure={}, style={'width': '49%', 'display': 'inline-block'}),
    
    
    dcc.Graph(
        figure = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral),
        style={'width': '49%', 'display': 'inline-block'}),
    
    dcc.Graph(
        figure = px.line_polar(rsme, r='RMSE (Q2 2019 to Q4 2020)', theta='Region', line_close=True),
        style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div(id='my-hoverdata-1')
    ])

tab2 = html.Div([
    html.H3(children='ITL 2', style={'font-family': 'Arial'}),
    dcc.Dropdown(id='my-dropdown-2', value='2012 Q2',
                 options=[{'label': x, 'value': x} for x in
                          melt_reduced.Year.unique()]),
    dcc.Graph(id='my-graph-2', figure={}, style={'width': '49%', 'display': 'inline-block'}),
    dcc.Graph(
        id='line-graph-2',
        figure={}, style={'width': '49%', 'display': 'inline-block'}),
    
    
    dcc.Graph(
        figure = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral),
        style={'width': '49%', 'display': 'inline-block'}),
    
    dcc.Graph(
        figure = px.line_polar(rsme, r='RMSE (Q2 2019 to Q4 2020)', theta='Region', line_close=True),
        style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div(id='my-hoverdata-2')
    ]),

tab3 =  html.Div([
    html.H3(children='ITL 3', style={'font-family': 'Arial'}),
    dcc.Dropdown(id='my-dropdown-3', value='2012 Q2',
                 options=[{'label': x, 'value': x} for x in
                          melt_reduced.Year.unique()]),
    dcc.Graph(id='my-graph-3', figure={}, style={'width': '49%', 'display': 'inline-block'}),
    dcc.Graph(
        id='line-graph-3',
        figure={}, style={'width': '49%', 'display': 'inline-block'}),
    
    dcc.Graph(
        figure = px.imshow(piv, color_continuous_scale=px.colors.diverging.Spectral),      
        style={'width': '49%', 'display': 'inline-block'}),
 
    dcc.Graph(
        figure = px.line_polar(rsme, r='RMSE (Q2 2019 to Q4 2020)', theta='Region', line_close=True),
        style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div(id='my-hoverdata-3')
    ])


app.layout = html.Div([
    html.H1(children = 'Model-based estimates of regional GVA',  style={'font-family': 'Arial', 'font-size':'2em'}),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(id="tab-1", label='ITL 1', value='tab-1-example', style={'font-family': 'Arial'}),
        dcc.Tab(id="tab-2", label='ITL 2', value='tab-2-example', style={'font-family': 'Arial'}),
        dcc.Tab(id="tab-3", label='ITL 3', value='tab-3-example', style={'font-family': 'Arial'})
    ]),
    html.Div(id='tabs-content-example',
             children = tab1)
])

@app.callback(dash.dependencies.Output('tabs-content-example', 'children'),
             [dash.dependencies.Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1
    elif tab == 'tab-2-example':
        return tab2
    elif tab == 'tab-3-example':
        return tab3
    
@app.callback(
    dash.dependencies.Output(component_id='my-graph-1', component_property='figure'),
    dash.dependencies.Input(component_id='my-dropdown-1', component_property='value')
)
def update_graph(year_chosen):
    dff = melt_reduced[melt_reduced.Year == year_chosen]
    fig = px.choropleth(dff, 
                    locations='id', 
                    geojson=regions, 
              color='value',
              color_continuous_scale=px.colors.diverging.Spectral,
              scope='europe')
    fig.update_geos(fitbounds='locations', visible=False),
    fig.update_layout(margin=dict(l=60, r=60, t=50, b=50))
    fig.update_layout(coloraxis_colorbar_x=-0.1)

    return fig


@app.callback(
    dash.dependencies.Output(component_id='line-graph-1', component_property='figure'),
    dash.dependencies.Input(component_id='my-graph-1', component_property='hoverData')
)
def update_side_graph(hoverData):
        hov_region = hoverData['points'][0]['location']
        dff2 = melt[melt.Region == hov_region]
        fig2 = px.line(dff2, x='Year', y='value', title=hov_region)
        return fig2

@app.callback(
    dash.dependencies.Output(component_id='my-graph-2', component_property='figure'),
    dash.dependencies.Input(component_id='my-dropdown-2', component_property='value')
)
def update_graph_2(year_chosen):
    dff_itl2 = melt2[melt2.Year == year_chosen]
    fig_itl2 = px.choropleth(dff_itl2, 
                    locations='id', 
                    geojson=itl2, 
              color='value',
              color_continuous_scale=px.colors.diverging.Spectral,
              scope='europe')
    fig_itl2.update_geos(fitbounds='locations', visible=False),
    fig_itl2.update_layout(margin=dict(l=60, r=60, t=50, b=50))
                           
    return fig_itl2

@app.callback(
    dash.dependencies.Output(component_id='line-graph-2', component_property='figure'),
    dash.dependencies.Input(component_id='my-graph-2', component_property='hoverData')
)
def update_side_graph_2(hoverData):
        hov_region = hoverData['points'][0]['location']
        dff2a = melt2[melt2.Region == hov_region]
        fig2a = px.line(dff2a, x='Year', y='value', title=hov_region)
        return fig2a
    
@app.callback(
    dash.dependencies.Output(component_id='my-graph-3', component_property='figure'),
    dash.dependencies.Input(component_id='my-dropdown-3', component_property='value')
)
def update_graph_3(year_chosen):
    dff3 = melt3[melt3.Year == year_chosen]
    fig3 = px.choropleth(dff3, 
                    locations='id', 
                    geojson=itl3_json, 
              color='value', 
              color_continuous_scale=px.colors.diverging.Spectral,
              scope='europe')
    fig3.update_geos(fitbounds='locations', visible=False),
    fig3.update_layout(margin=dict(l=60, r=60, t=50, b=50))
    return fig3

@app.callback(
    dash.dependencies.Output(component_id='line-graph-3', component_property='figure'),
    dash.dependencies.Input(component_id='my-graph-3', component_property='hoverData')
)
def update_side_graph_3(hoverData):
        hov_region = hoverData['points'][0]['location']
        dff3a = melt3[melt3.Region == hov_region]
        fig3a = px.line(dff3a, x='Year', y='value', title=hov_region)
        return fig3a


if __name__ == '__main__':
    app.run_server(debug=False)
