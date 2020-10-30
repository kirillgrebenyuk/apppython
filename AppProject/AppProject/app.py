from navbar import Navbar
from dash.dependencies import Input, Output, State

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import dash.dependencies
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import pyodbc
import base64
import datetime

nav = Navbar()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')
date = '2020-10-29'
query = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+date+"' AND (dat.OBJECT IN(4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
df=pd.read_sql(query, con=cnn, parse_dates=['DATA_DATE'])

cursor = cnn.cursor()
cursor.execute(query)

data_uri = base64.b64encode(open('assets/unnamed.png', 'rb').read()).decode('utf-8')

for row in cursor:
	ch = row[0]
fig = px.line(df, x="DATA_DATE", y="VALUE0",color="NAME")
body = html.Div([	
    dcc.Graph(
        id='example-graph1',
        figure=fig        
    ),
	html.H4(children=ch),
	dt.DataTable(
		data=df.to_dict('record'),
		columns=[{'id': c, 'name': c} for c in df.columns],
        page_size=10
	),
    html.P(id="button-clicks"),
    html.A(html.Img(src='data:image/png;base64,{}'.format(data_uri)), href='#zavod1'),
    html.A(html.Img(src='data:image/png;base64,{}'.format(data_uri)), href='#zavod2'),
    html.A(html.Img(src='data:image/png;base64,{}'.format(data_uri)), href='#zavod3'),
    html.A(html.Img(src='data:image/png;base64,{}'.format(data_uri)), href='#zavod4')
])

def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

app.layout = Homepage()

cnn.close()


if __name__ == '__main__':
    # Run the app server on localhost:8050
    app.run_server()


#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
#fig = px.scatter(df, x="gdp per capita", y="life expectancy",
#                 size="population", color="continent", hover_name="country",
#                log_x=True, size_max=60)