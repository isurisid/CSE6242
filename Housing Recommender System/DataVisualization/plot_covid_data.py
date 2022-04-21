import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly
import plotly.express as px
from . import utility as utility

def get_covid_data():
    df_fips = utility.get_county_fips()
    df_covid = pd.read_csv("/home/housingrecommendations/CSE6242/Housing Recommender System/DataExtraction/final_data/HousingRecommenderCountyAggregateDataset.csv")
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
    df_fips_covid['Info'] = 'County - ' + df_fips_covid['county'] + '<br>' + 'State - ' + df_fips_covid['state'] + '<br>' + \
        'Daily cases - ' + df_fips_covid['daily_cases'].astype('str')

    fig = px.choropleth(
        df_fips_covid,
        geojson=counties,
        locations='fips',
        color=df_fips_covid['daily_cases'],
        color_continuous_scale="RdYlGn_r",
        range_color=(min(df_fips_covid['daily_cases']), 25000),
        scope="usa",
        labels={'daily_cases':'Daily COVID cases'},
        hover_data=['county', 'state', 'daily_cases', 'percentage_fully_vaccinated']
    )
    fig.add_scattergeo(
        geojson=counties,
        locations = df_fips_covid['fips'],
        hovertext = df_fips_covid['Info'],
        hoverinfo = 'text',
        marker = dict(color = '#553355', size = 0.1),
        showlegend=False)

    fig.update_traces(text = "white")
    fig.update_layout(title_text = 'Average Daily COVID cases across US counties')
    p=plotly.offline.plot(fig, filename='/home/housingrecommendations/CSE6242/Housing Recommender System/static/cases.html', config={'displayModeBar': False},auto_open=False)
    return fig

# plot percentage vaccinated
# called from UI
def generate_percent_vaccinated_plot():
    df_fips_covid = get_covid_data().dropna().reset_index()
    counties = utility.get_county_geojson()
    df_fips_covid['Info'] = 'County - ' + df_fips_covid['county'] + '<br>' + 'State - ' + df_fips_covid['state'] + '<br>' + \
    'Percent Vaccinated - ' + df_fips_covid['percentage_fully_vaccinated'].astype(int).astype('str') + '%'

    fig = px.choropleth(
        df_fips_covid,
        geojson=counties,
        locations='fips',
        color=df_fips_covid['percentage_fully_vaccinated'],
        color_continuous_scale="RdYlGn",
        range_color=(0, 100),
        scope="usa",
        labels={'percentage_fully_vaccinated':'% vaccinated'},
        hover_data=['county', 'state', 'daily_cases', 'percentage_fully_vaccinated']
    )
    fig.add_scattergeo(
    geojson=counties,
    locations = df_fips_covid['fips'],
    hovertext = df_fips_covid['Info'],
    hoverinfo = 'text',
    marker = dict(color = '#553355', size = 0.1),
    showlegend=False)

    fig.update_traces(text = "white")
    fig.update_layout(title_text = 'Percentage Vaccinated across US counties')
    plotly.offline.plot(fig, filename='/home/housingrecommendations/CSE6242/Housing Recommender System/static/vaccinated.html', config={'displayModeBar': False},auto_open=False)
    return fig