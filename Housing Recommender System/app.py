
import numpy as np
import json
import logging
import pickle
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, request, jsonify, render_template
import ML.rp.functions
from ML.rp.functions.main import reward_punishment_orchestrator

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def runRewardandPunishmentModel(user_inputs):
    logging.info("Running Reward and Punishment Model..")
    dataset=pd.read_csv("./ML/rp/data/v2-HousingRecommenderFinalDataset.csv")
    pivot_recommendations=reward_punishment_orchestrator(dataset,user_inputs)
    logging.info(f"Pivot Recommendations {pivot_recommendations}")
    return pivot_recommendations


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def runRecommendations():
    if request.method=='POST':
        user_inputs = request.form.to_dict()
        logging.info(f"User Preference List: {user_inputs}")
       # pivot_recommendations=runRewardandPunishmentModel(user_inputs)
       # recommendations=generatePreferences(pivot_recommendations)
        prediction ='This will display all the dashboards'
        return render_template("result.html", prediction = prediction)


# Embedding a plotly sample chart into the application
# Use route {host}/recommended to see it
# TODO: replace this with Samir's interactive plot
@app.route('/recommended')
def plotly_graph():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Cool title for graph"
    description = """
    Cool description
    """
    return render_template('plotly_graph.html', graphJSON=graphJSON, header=header, description=description)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

