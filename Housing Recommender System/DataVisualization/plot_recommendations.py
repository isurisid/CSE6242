import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly
import plotly.express as px
from . import utility as utility


def get_recommendations(df_recommend):
    df_fips = utility.get_county_fips()
    df_merge = pd.merge(df_recommend, df_fips, on=["county", "state"])
    df_fips_recommend = df_merge.head(100)
    return df_fips_recommend

# called from UI
def generate_recommend_plot(df_recommend):
    #print(df_recommend.shape)
    df_fips_recommend = get_recommendations(df_recommend)
    print(df_fips_recommend.shape)
    counties = utility.get_county_geojson()
    df_fips_recommend['Info'] = 'Rank - ' + df_fips_recommend['rank'].astype('str') + '<br>' + \
        'County - ' + df_fips_recommend['county'] + '<br>' + 'State - ' + df_fips_recommend['state'] + '<br>' + \
        'Percent Vaccinated - ' + df_fips_recommend['percentage_fully_vaccinated'].astype(int).astype('str') + '%'
    print(df_fips_recommend)
    fig = px.choropleth(df_fips_recommend,
            geojson=counties,
            locations='fips',
            color=df_fips_recommend['Top 20'],
            color_discrete_map={'True':'red', 'False':'Yellow'},
            scope="usa",
            hover_data={'Info'}
           )
        
    fig.add_scattergeo(
        geojson=counties,
        locations = df_fips_recommend['fips'],
        hovertext = df_fips_recommend['Info'],
        hoverinfo = 'text',
        marker = dict(color = '#b2d2cf', size = 0.1),
        showlegend=False)
    fig.update_layout(title_text = 'Recommended Counties (hover over for details)' )
    plotly.offline.plot(fig,filename='./static/recommend.html',config={'displayModeBar': False}, auto_open=False)
    return fig
