import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px
from . import utility as utility 




def get_recommendations(df_recommend):
    print(f"DF RECOMMEND {df_recommend}")
    print(f" DF RECOMMEND:{df_recommend.columns}")
    df_fips = utility.get_county_fips()
    print(f"DF fips shape:{df_fips.shape}")
    print(f" DF FIPS columns :{df_fips.columns}")
    df_merge = pd.merge(df_recommend, df_fips, on=["county", "state"])
    print(f"MERGED DATAFRAME {df_merge}")
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
            color=df_fips_recommend['Within Top 20 Recommendations'],
            color_discrete_map={'True':'red', 'False':'Yellow'},
            scope="usa",
            hover_data={'Info'},
            title='Recommended Counties based on your input')

    fig.add_scattergeo(
            geojson=counties,
            locations = df_fips_recommend['fips'].head(20),
            text = df_fips_recommend['county'].head(20),
            mode = 'text',
            hovertext = df_fips_recommend['Info'],
            hoverinfo = 'text',
            showlegend=False)


    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
