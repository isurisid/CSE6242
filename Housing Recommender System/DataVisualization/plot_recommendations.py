import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px
from . import utility as utility 




def get_recommendations(df_recommend):
    df_fips = utility.get_county_fips()
    df_merge = pd.merge(df_recommend, df_fips, on=["county", "state"])
    df_fips_recommend = df_merge.head(100)
    return df_fips_recommend

# called from UI
def generate_recommend_plot(df_recommend):
    df_fips_recommend = get_recommendations(df_recommend)
    counties = utility.get_county_geojson()
    
    fig = px.choropleth(
        df_fips_recommend,
        geojson=counties,
        locations='fips',
        color=df_fips_recommend.index,
        color_continuous_scale="aggrnyl",
        range_color=(0, 50),
        scope="usa",
        labels={'index': 'county rank'},
        hover_data=['county', 'state']
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
