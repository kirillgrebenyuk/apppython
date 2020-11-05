from navbar import Navbar
from math import ceil
from dash.dependencies import Output,Input,State

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import pyodbc
import datetime
import dash_table as dt

nav = Navbar()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР"           # Название сайта

cnn = pyodbc.connect('DRIVER={SQL Server};PORT=port;SERVER=192.168.0.85;PORT=1433;DATABASE=Piramida2000;UID=sa;PWD=pswd')  #Подключение к БД

LGOK = '4407,4408,4409,4410,4411,4412,4413,4414'
MGOK = '4418,4407,4408,4409,4410,4411,4412,4413,4415'
OEMK = '4417,4414,4415,4417'
YSTAL = '4418,4369,4413,4414,4415'

sqlsummaLGOK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+LGOK+") AND dat.ITEM = 1"
sqlsummaMGOK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+MGOK+") AND dat.ITEM = 1"
sqlsummaOEMK = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+OEMK+") AND dat.ITEM = 1"
sqlsummaYSTAL = "SELECT SUM(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+YSTAL+") AND dat.ITEM = 1"
cursor = cnn.cursor().execute(sqlsummaLGOK)
for row in cursor:summaLGOK = row[0]
cursor = cnn.cursor().execute(sqlsummaMGOK)
for row in cursor:summaMGOK = row[0]
cursor = cnn.cursor().execute(sqlsummaOEMK)
for row in cursor:summaOEMK = row[0]
cursor = cnn.cursor().execute(sqlsummaYSTAL)
for row in cursor:summaYSTAL = row[0]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])


index_page = html.Div([
    #html.H2('Потребление по всему заводу',id="button-clicks", className="TitleSite"),
    html.Div(className="divZavod",children=[        
    html.P(str(ceil(summaLGOK))+' кВт*ч',className="Potreblenie"),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-1'),
    
    html.P(str(ceil(summaMGOK))+' кВт*ч',className="Potreblenie"),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-3'),
    
    html.P(str(ceil(summaOEMK))+' кВт*ч',className="Potreblenie"),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-4'),
    
    html.P(str(ceil(summaYSTAL))+' кВт*ч',className="Potreblenie"),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-5')]),
    #html.Br(),
    #dcc.Link('Go to Page 2', href='/page-2'),
])

#-----------Для теста вывода в таблицу----------------------------------------------
sqltesttable = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020' AND (dat.OBJECT IN(4407,4408,4409,4410,4411,4412,4413,4414)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE DESC"
dftesttable = pd.read_sql_query(sqltesttable,con=cnn)  
#-----------------------------------------------------------------------------------

page_1_layout = html.Div([
    html.H6("Вывод SQL запроса"),
    html.Div(["Введите даты: ",
              dcc.DatePickerRange(id='my-input', 
                                   min_date_allowed=datetime.date(2020, 1, 1),
                                   max_date_allowed=datetime.date(2020, 11, 1),
                                   start_date = datetime.date(2020,1, 1),
                                   end_date=datetime.date(2020, 11, 1))]),
    dcc.Graph(id='graph-with-slider'),
    #Для теста вывода в таблицу--------------------------------------------------------
    dt.DataTable(id='table_data',
		data=dftesttable.to_dict('record'),
		columns=[{'id': c, 'name': c} for c in dftesttable.columns]
	),
    #-----------------------------------------------------------------------------------
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])
@app.callback(
    Output(component_id='graph-with-slider', component_property='figure'),
    [Input(component_id='my-input', component_property='start_date'),
     Input(component_id='my-input', component_property='end_date')]
)
def update_figure(start_date,end_date):
    #qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4408,4409,4410,4411,4412,4413)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
    qsql = "SELECT dev.NAME,dat.PARNUMBER,dat.ITEM,dat.VALUE0,dat.VALUE1,dat.DATA_DATE FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND dat.DATA_DATE > '"+start_date+"' AND dat.DATA_DATE < '"+end_date+"' AND (dat.OBJECT IN(4407,4408,4409,4410,4411,4412,4413,4414)) AND dat.ITEM = 1 ORDER BY dat.DATA_DATE ASC"
    qsql1 = "SELECT count(VALUE0)as Summa FROM DATA as dat LEFT JOIN DEVICES as dev ON dat.OBJECT = dev.CODE WHERE dat.PARNUMBER = 12 AND (dat.DATA_DATE > '01-01-2020' AND dat.DATA_DATE < '11-01-2020')AND OBJECT IN ("+LGOK+") AND dat.ITEM = 1"
    dff = pd.read_sql_query(qsql,con=cnn)
    print(pd.read_sql_query(qsql,con=cnn))
    fig = px.line(dff, x="DATA_DATE", y="VALUE0", color="NAME", hover_name="NAME")
    fig.update_traces(mode="markers+lines")

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    #fig.update_layout(transition_duration=500)

    return fig

page_6_layout = html.Div([
    html.H1('Page 1'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

page_3_layout = html.Div([
    html.H1('Page 3'),
    html.Div(id='page-3-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_4_layout = html.Div([
    html.H1('Page 4'),
    html.Div(id='page-4-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_5_layout = html.Div([
    html.H1('Page 5'),
    html.Div(id='page-5-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server()