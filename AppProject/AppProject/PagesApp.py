from navbar import Navbar
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

nav = Navbar()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР"           # Название сайта

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])


index_page = html.Div([
    #html.H2('Потребление по всему заводу',id="button-clicks", className="TitleSite"),
    html.Div(className="divZavod",children=[
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-1'),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-3'),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-4'),
    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-lgok', className="btnZavod", n_clicks = 0), href='/page-5')]),
    #html.Br(),
    #dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
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

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
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

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
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
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
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


if __name__ == '__main__':
    app.run_server()