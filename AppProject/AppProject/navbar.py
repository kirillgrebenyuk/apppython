import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "http://orem.su/img/logo.png"

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Поиск")),
        dbc.Col(
            dbc.Button("Поиск", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

def Navbar():
    navbar = dbc.Navbar(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                                dbc.Col(dbc.NavbarBrand("АО «РЭС Групп»", className="ml-2")),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href="https://plot.ly",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
                    dbc.Collapse([
                        dbc.Row([
                                dbc.Col( 
                                    dbc.DropdownMenu(
                                    label="Menu",
                                    children=[
                                        dbc.DropdownMenuItem("Настройки"),
                                        dbc.DropdownMenuItem("О системе"),
                                        dbc.DropdownMenuItem("Справка"),
                                        ],
                                    right=True
                                    )),
                                   ],
                                no_gutters=True,
                                className="ml-auto flex-nowrap mt-3 mt-md-0"
                                )],
                            id="navbar-collapse", 
                            navbar=True)
                ],
                color=theme['secondary'],
                dark=True,
            )
    return navbar
 
            