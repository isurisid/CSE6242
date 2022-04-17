import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px
import matplotlib.pyplot as plt


def get_county_geojson():
    # returns a dictionary with geojson data
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    return counties


def get_county_fips(fips_file):
    # returns a dataframe with US counties and its fips
    df_fips = pd.read_csv(fips_file)
    df_fips["fips"] = df_fips["fips"].astype("str")
    df_fips['fips'] = df_fips['fips'].apply(lambda x: x.zfill(5))
    df_fips = df_fips.dropna()
    df_fips = df_fips.reset_index(drop=True)
    df_fips = df_fips.rename(columns={"name": "county"})
    return df_fips


def get_recommendations(df_fips, forecast_path, top_n):
    df_ppsf = pd.read_csv(forecast_path)
    df_avg_ppsf = df_ppsf.groupby(['county', 'state'])['median_ppsf'].mean().reset_index()
    df_merge = pd.merge(df_avg_ppsf, df_fips, on=["county", "state"])
    df_recommend = df_merge.head(top_n)
    return df_recommend


def generate_plot(df_recommend, counties):
    fig = px.choropleth(
        df_recommend,
        geojson=counties,
        locations='fips',
        color=df_recommend.index,
        color_continuous_scale="aggrnyl",
        range_color=(0, 50),
        scope="usa",
        labels={'index': 'county rank'},
        hover_data=['county', 'state']
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
