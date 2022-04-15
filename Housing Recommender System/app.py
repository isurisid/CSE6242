import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import ML.rp.functions
from ML.rp.functions.main import reward_punishment_orchestrator
from ML.cosine_similarity.recommender import generatePreferences
import pandas as pd
import logging

app = Flask(__name__)

def runRewardandPunishmentModel(user_inputs):
    logging.info("Running Reward and Punishment Model..")
    dataset=pd.read_csv("./ML/rp/data/v2-HousingRecommenderFinalDataset.csv")
    pivot_recommendations=reward_punishment_orchestrator(dataset,user_inputs)
    logging.info(f"Pivot Recommendations {pivot_recommendations}")
    return pivot_recommendations


@app.route('/')
def home():
    return render_template('index.html')
app.config['JSON_SORT_KEYS'] = False
@app.route('/recommendations',methods=['POST'])
def runRecommendations():
    if request.method=='POST':
        user_inputs = request.form.to_dict()
        logging.info(f"User Preference List: {user_inputs}")
        pivot_recommendations=runRewardandPunishmentModel(user_inputs)
        recommendations=generatePreferences(pivot_recommendations)
        prediction ='This will display all the dashboards'
        return render_template("result.html", prediction = prediction)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
