import numpy as np
import json
import logging
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, request, render_template
from ML.rp.main import reward_punishment_orchestrator
from ML.Recommender.plot_recommendations import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def runRewardandPunishmentModel(user_inputs):
    logging.info("Running Reward and Punishment Model..")
    dataset = pd.read_csv("ML/rp/data/rp-final-dataset.csv")
    pivot_recommendations = reward_punishment_orchestrator(dataset, user_inputs)
    logging.info(f"Pivot Recommendations {pivot_recommendations}")
    return pivot_recommendations


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/visuals')
def visuals():
    return render_template('visuals.html')


@app.route('/recommendations', methods=['POST'])
def runRecommendations():
    if request.method == 'POST':
        user_inputs = request.form.to_dict()
        logging.info(f"User Preference List: {user_inputs}")
        # pivot_recommendations=runRewardandPunishmentModel(user_inputs)
        # recommendations=generatePreferences(pivot_recommendations)
        prediction ='This will display all the dashboards'
        return render_template("result.html", prediction = prediction)


# Embedding a plotly sample chart into the application
# Use route {host}/recommended to see it
@app.route('/recommended')
def plot_recommendations():
    counties = get_county_geojson()
    df_fips = get_county_fips("ML/Recommender/state_and_county_fips_master.csv")
    # TODO this should read dynamic data instead of static
    df_recommend = get_recommendations(df_fips=df_fips, forecast_path="ML/ppsf_forecast/ppsf_forecast.csv", top_n=50)
    fig = generate_plot(df_recommend=df_recommend, counties=counties)

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Recommendations"
    description = """
        """
    return render_template('plotly_graph.html', graphJSON=graph_json, header=header, description=description)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

