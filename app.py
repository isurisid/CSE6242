import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)


def runmodel(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 12)
    loaded_model = pickle.load(open("model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/')
def home():
    return render_template('index.html')
app.config['JSON_SORT_KEYS'] = False
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        #to_predict_list = request.form.to_dict()
        #to_predict_list = list(to_predict_list.values())
        #to_predict_list = list(map(int, to_predict_list))
        #result = runmodel(to_predict_list)
        #tvalue = request.form['Price']

        #print(request.form)
        #return jsonify(request.form.to_dict())
        #return tvalue
        prediction ='This will display all the dashboards'
        return render_template("result.html", prediction = prediction)

if __name__ == "__main__":
    app.run(debug=True)
