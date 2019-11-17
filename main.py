#https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-mapd-demo/app.py

import dash
import dash_html_components as html 
import dash_core_components as dcc 


from plotly.offline import iplot, init_notebook_mode
import chart_studio.plotly as py
import pandas as pd
import random

df = pd.read_csv('EGOV_DATA_2018.csv')

def getData (param, colorscale):

    data = [ dict(
            type = 'choropleth',
            locations = df['CODE'],
            z = df[param],
            text = df['Country Name'],
            colorscale = colorscale,
            colorbar = {'title':'Score', 'len':0.5, 'y':0.65},
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.3,
                )
            ),
            zmin = 0,

        ) ]
    
    return data

def getLayOut (FigTitle):
    layout = dict(
        title = dict(
            text=FigTitle,
            xanchor = "left",
            pad=dict(t=20),
        ),
       margin=dict(t=80, b=0, l=0, r=0),
       width=800, height=700,
 
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection_type='equirectangular',
            projection = dict(
                type = 'mercator'
            )
        )
    )

    return layout

colorscale = ['YIOrRd', 'Viridis', 'spectral', 'Magma', 'YlGnBu', 'Portland']

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Dropdown(
        id = 'egovIndexDropDown',
        options = [{
            'label':i,
            'value':i
        } for i in df.columns[2:8]],
        value = df.columns[0],
        clearable = False,
        placeholder = 'Select a ranking',
        style={'height': '40px', 'width': '800px'}
        
    ),
    html.Div([
        dcc.Graph( id="chorograph" )
    ], style={"height" : "80vh", "width" : "120vh"}),


])

@app.callback(
    dash.dependencies.Output("chorograph", "figure"),
    [
        dash.dependencies.Input("egovIndexDropDown", "value")
    ],
)

def update_choro(value):
    return  dict( data=getData(value, random.choice(colorscale)), layout=getLayOut('2018 '+value) )
    



if __name__ == '__main__':
    app.run_server(debug=True)