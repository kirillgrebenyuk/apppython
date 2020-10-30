import dash_bootstrap_components as dbc

def Navbar():
     navbar = dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Active", active=True, href="#ind1")),
                dbc.NavItem(dbc.NavLink("A link", href="#ind2")),
                dbc.NavItem(dbc.NavLink("Another link", href="#ind3")),
                dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#ind4")),        
            ],
            pills=True
        )
     return navbar