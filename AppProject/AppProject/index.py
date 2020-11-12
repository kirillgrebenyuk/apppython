from navbar import Navbar,Sidebar

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

nav = Navbar()            # Подключаем код навигационной панели
sidebar = Sidebar()       # Подключаем код левого меню

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Система ИАС УЭР Металлоинвест"           # Название сайта

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,    
    dbc.Row([
             dbc.Col(sidebar, id="left", className="leftMenu", md=2),
             dbc.Col([
               html.Div(id='page-content',children=[
                  html.P('Главная страница'),
                  dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-oemk', n_clicks = 0), href='/page-1')]
               )
             ])
            ])
    ])
#------------------------------------
# Главная страница
#------------------------------------

index_page = html.Div([
                    html.P('Главная страница'),
                    dcc.Link(html.Img(src='assets/unnamed.png', id='image-btn-oemk', n_clicks = 0), href='/page-1')
    ])

#------------------------------------
# Второй уровень по сайту
#------------------------------------

page_1_layout = html.H4('Страница предназначенная для мониторинга')
page_2_layout = html.H4('Страница предназначенная для анализа')
page_3_layout = html.H4('Страница предназначенная для планирования и прогнозирования')
page_4_layout = html.H4('Страница предназначенная для мнемосхем')

#------------------------------------
# Указываем активные в левом меню
#------------------------------------

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]

#----------------------------------------------
# Скрываем левое меню в зависимости от страницы
#----------------------------------------------

@app.callback(Output('left', 'style'), 
              [Input('url', 'pathname')])
def update_style(pathname):
    if pathname == '/':
        return {'display': 'none'}
    elif pathname == '/page-1':
        return {'display': 'block'}
    elif pathname == '/page-2':
        return {'display': 'block'}
    elif pathname == '/page-3':
        return {'display': 'block'}
    elif pathname == '/page-4':
        return {'display': 'block'}
    elif pathname == '/setting':
        return {'display': 'block'}
    elif pathname == '/about':
        return {'display': 'block'}
    elif pathname == '/help':
        return {'display': 'block'}
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Страница не найдена", className="text-danger"),
                html.Hr(),
                html.P(f"Страница {pathname} не найдена..."),
            ]
        )    

#--------------------------------------------------
# Обработка ссылок и открытие необходимого контента
#--------------------------------------------------

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/':
        return index_page
    elif pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/setting':
        return page_setting
    elif pathname == '/about':
        return page_help
    elif pathname == '/help':
        return page_about
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Страница не найдена", className="text-danger"),
                html.Hr(),
                html.P(f"Страница {pathname} не найдена..."),
            ]
        )
    # Последним указывается код для несуществующей страницы

if __name__ == '__main__':
    app.run_server()