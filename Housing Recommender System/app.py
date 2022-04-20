import numpy as np
import json
import logging
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, request, render_template
from ML.rp.main import reward_punishment_orchestrator
from ML.cosine_similarity.recommender import generatePreferences
from DataVisualization.plot_recommendations import *
from DataVisualization.plot_covid_data import *
from DataVisualization.utility import *
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def runRewardandPunishmentModel(user_inputs):
    logging.info("Running Reward and Punishment Model..")
    # Working directory is assumed as "Housing Recommender System/"
    dataset = pd.read_csv("ML/rp/data/rp-final-dataset.csv")
    pivot_recommendations = reward_punishment_orchestrator(dataset, user_inputs)
    logging.info(f"Pivot Recommendations {pivot_recommendations}")
    return pivot_recommendations

#@app.route('/recommended')
def plot_recommendations(final_recommendations):
    header = "Recommendations"
    description = """
        """
    # Plot 1
    fig_1 = generate_recommend_plot(df_recommend=final_recommendations)

    graph_json_1 = json.dumps(fig_1, cls=plotly.utils.PlotlyJSONEncoder)

    # Plot 2
    fig_2 = generate_percent_vaccinated_plot()
    graph_json_2 = json.dumps(fig_2, cls=plotly.utils.PlotlyJSONEncoder)

    # Plot 3
    fig_3 = generate_covid_daily_cases_plot()
    graph_json_3 = json.dumps(fig_3, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json_1,graph_json_2,graph_json_3

@app.route('/')
def home():
    os.chdir(".")
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/visuals')
def visuals():
    return render_template('visuals.html')

@app.route('/team')
def team():
    return render_template('Team.html')

@app.route('/recommendations', methods=['POST'])
def runRecommendations():
    if request.method == 'POST':
        user_inputs = request.form.to_dict()
        logging.info(f"User Preference List: {user_inputs}")
        # Make sure the user_inputs have the same form as sample_input in rp/main.py
        pivot_recommendations = runRewardandPunishmentModel(user_inputs)
        final_recommendations = generatePreferences(pivot_recommendations)
        graph_json_1,graph_json_2,graph_json_3= plot_recommendations(final_recommendations)

        return render_template('index.html')

        #return ""  # this is just to test R&P working with actual user data
        # return render_template("result.html", prediction=prediction)

# Embedding a plotly sample chart into the application
# Use route {host}/recommended to see it


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)