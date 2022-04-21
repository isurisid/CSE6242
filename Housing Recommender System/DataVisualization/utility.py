import pandas as pd
from urllib.request import urlopen
import json

def get_county_geojson():
    # returns a dictionary with geojson data
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    return counties

def get_county_fips():
    # returns a dataframe with US counties and its fips
    df_fips = pd.read_csv("/home/housingrecommendations/CSE6242/Housing Recommender System/DataVisualization/data/state_and_county_fips_master.csv")
    df_fips["fips"] = df_fips["fips"].astype("str")
    df_fips['fips'] = df_fips['fips'].apply(lambda x: x.zfill(5))
    df_fips = df_fips.dropna()
    df_fips = df_fips.reset_index(drop=True)
    df_fips = df_fips.rename(columns={"name": "county"})
    return df_fips
