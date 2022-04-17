import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px
from . import utility as utility

def get_covid_data():
    df_fips = utility.get_county_fips()
    df_covid = pd.read_csv("./DataExtraction/final_data/HousingRecommenderCountyAggregateDataset.csv")
    columns = ['county', 'state_code', 'daily_cases', 'percentage_fully_vaccinated']
    df_covid = pd.DataFrame(df_covid, columns=columns)
    df_covid = df_covid.rename(columns={"state_code": "state"})
    df_fips_covid = pd.merge(df_covid, df_fips, on=["county", "state"])
    return df_fips_covid



# plot daily covid cases
# called from UI
def generate_covid_daily_cases_plot():
    df_fips_covid = get_covid_data()
    counties = utility.get_county_geojson()
    
    fig = px.choropleth(
        df_fips_covid,
        geojson=counties,
        locations='fips',
        color=df_fips_covid['daily_cases'],
        color_continuous_scale="RdYlGn_r",
        range_color=(min(df_fips_covid['daily_cases']), 25000),
        scope="usa",
        labels={'daily_cases':'Daily COVID cases'},
        hover_data=['county', 'state', 'daily_cases', 'percentage_fully_vaccinated'],
        title='Average Daily COVID cases'
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# plot percentage vaccinated
# called from UI
def generate_percent_vaccinated_plot():
    df_fips_covid = get_covid_data()
    counties = utility.get_county_geojson()

    fig = px.choropleth(
        df_fips_covid,
        geojson=counties,
        locations='fips',
        color=df_fips_covid['percentage_fully_vaccinated'],
        color_continuous_scale="RdYlGn",
        range_color=(0, 100),
        scope="usa",
        labels={'percentage_fully_vaccinated':'Percentage - county vaccinated'},
        hover_data=['county', 'state', 'daily_cases', 'percentage_fully_vaccinated'],
        title='Percentage of county vaccinated'
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig