from dash import html, dcc 
import dash_bootstrap_components as dbc
from app import app

list_of_locations = {
    'Todas': 0,
    'Manhattan': 1,
    'Bronx': 2,
    'Brooklyn': 3,
    'Queens': 4,
    'Staten Island': 5,
}

slider_size = [ 100, 500, 1000, 10000, 10000000]

controllers = dbc.Row([
    html.Img(id='logo', src=app.get_asset_url('logo.png'), style={'width': '50%', 'margin-top': '20px'}),
    html.H3('Venda de imóveis em Nova York', style= {'margin-top':'30px'} ),
    html.P(''' Dashboard teste com dados de imóveis da cidade 
                de Nova York''', style= {'margin-top':'30px'}),
    html.H4('Distrito', style = {'margin-top': '50px','margin-bottom': '20px'}),
    dcc.Dropdown(
        id = 'location-dropdown', # id para callbacks
        options = [{'label': i, 'value': j} for i, j in list_of_locations.items()], #opções do dropdown
        value = 0, #label inicial do drop
        placeholder = 'Selecione um distrito' #texto inicial
    ),
    html.H4('Metragem (m²)', style = {'margin-top': '50px','margin-bottom': '20px'}),
    
    dcc.Slider(min = 0, max = 4, id='slider-square-size', #defino quantas opções vão ter: (0 1 2 3 4)
               marks={ i: str(j) for i, j in enumerate(slider_size)},
               step=None),
    
   dcc.Dropdown(
        id = 'dropdown-color',
        options = [{'label': 'YEAR BUILT', 'value': 'YEAR BUILT'},
                   {'label': 'TOTAL UNITS', 'value': 'TOTAL UNITS'},
                   {'label': 'SALE PRICE', 'value': 'SALE PRICE'},
        ],
        value = 'SALE PRICE',
        placeholder = 'Ano, Unidades ou preço?' 
        )
         
   
])  