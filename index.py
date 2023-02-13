from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
#importando dos outros arquivos que criei
from app import app
from _map import * 
from _histogram import *
from _controllers import *
import os
    
#=====================================
#Ingestão de dados
#=====================================
    
df_data = pd.read_csv('dataset/cleaned_data.csv', index_col=0)

#calculando a média da long e lat    
mean_lat = df_data['LATITUDE'].mean()
mean_long = df_data['LONGITUDE'].mean()

#criei uma coluna size_m2 e transformei pé quadrado em metro quadrado
df_data['size_m2'] = df_data['GROSS SQUARE FEET'] / 10.764

#eliminar dados nulos do ano
df_data = df_data[df_data['YEAR BUILT'] > 0 ]
#df_data.info()
# MUDANDO O TIPO DE DATA PARA  CONSUMIR MELHOR
df_data['SALE DATE'] = pd.to_datetime(df_data['SALE DATE'])
df_data['SALE DATE'].info()

# QUANDO A METRAGEM QUADRADA FOR MAIOR DO QUE 10.000M², DEIXAR NO TETO DE 10.000 PAR ANAO ZUAR O GRAFICO
df_data.loc[df_data['size_m2'] > 10000, 'size_m2'] = 10000
# ESTABELECENDO O TETO MÁXIMO DO PREÇO DE VENDA
df_data.loc[df_data['SALE PRICE'] > 50000000, 'SALE PRICE'] = 50000000
# ESTABELENCDO O PREÇO MÍNIMO+
 
df_data.info()
#=====================================
#Layout
#=====================================
app.layout = dbc.Container(
        children=[
                dbc.Row([
                        dbc.Col([controllers], md = 3),
                        dbc.Col([map, hist], md = 9),
                        
                ], style ={ 'margin-left': '30px'})
                

        ], fluid=True, )

#=====================================
#Layout
#=====================================

@app.callback([Output('hist-graph', 'figure'), Output('map-graph', 'figure')], #definindo o elemento que irá receber os parametros do input do histograma.
                #vou alterar a fig
              [Input('location-dropdown', 'value'), #id do input dos distritos, pegando o valor de cada distrito
               Input('slider-square-size', 'value'),#id do input do slider da metragem, pegando o valor de cada item do slider
               Input('dropdown-color', 'value') # id do input que irá definir a cor do gráfico
               ],)

#update do histograma e mapa
def update_hist (location, square_size, color_map):
        #location é a variavel do drop dos distritos:( 0 1 2 3 4) que são keys de dic
        if location is None:
                df_intermediate = df_data.copy() #garantindo que não dê merda no callback
        else: 
                #corte do location
                df_intermediate = df_data[df_data['BOROUGH'] == location] if location != 0 else df_data.copy()

                #definindo
                size_limit = slider_size[square_size] if square_size is not None else df_data['GROSS SQUARE FEET'].max()
                df_intermediate = df_intermediate[df_intermediate['GROSS SQUARE FEET'] <= size_limit]
        
        hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
        hist_layout = go.Layout(
                margin = go.layout.Margin(l=10, r=0 , t=0, b=50),
                showlegend=False,
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)'
        )
        hist_fig.layout = hist_layout
        
       
        #MAPA
        px.set_mapbox_access_token(open("keys/mapobox_key").read())
        
        #arrumando a escala de cores
        
        #color_map = 'SALE PRICE'
        colors_rgb = px.colors.sequential.Bluyl #estilo de gradientes 
        df_quantiles = df_data[color_map].quantile(np.linspace(0,1, len(colors_rgb))).to_frame() #quantiles vê a porcentagem equivalente da distribuição dos dados
        df_quantiles = (df_quantiles - df_quantiles.min())/ (df_quantiles.max() - df_quantiles.min())
        #df_quantiles # analiso a distribuição
        df_quantiles['colors'] = colors_rgb
        #como instruir o plotly à entender a nova escala de distribuição de cores?
        df_quantiles.set_index(color_map, inplace=True)
        
        color_scale = [ [i, j] for i, j in df_quantiles ["colors"] .iteritems()]
        
        
        map_fig = px.scatter_mapbox(df_intermediate, lat="LATITUDE", lon="LONGITUDE",     
                                    color=color_map, size="size_m2",
                                    size_max=15, 
                                    zoom=10, 
                                    opacity=0.4)
        
        map_fig.update_layout(mapbox = dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_long)), #definindo o ponto médio para começar a vizualização
                              template='plotly_dark', #template
                              paper_bgcolor = 'rgba(0, 0, 0, 0)', #estilo
                              margin = go.layout.Margin(l=10,  r= 10 , t=10, b=10),) #margem 
        
        map_fig.update_coloraxes(colorscale = color_scale)
        
        return hist_fig, map_fig

     

if __name__ == '__main__':
    app.run_server(debug=True, port = 8050 | int(os.environ['PORT']))
    
