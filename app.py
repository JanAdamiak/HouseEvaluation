from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("regression_model.sav", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():

    features = [x for x in request.form.values()]
    data = {"bedrooms": [int(features[0])], "toilets": [int(features[1])], "other_rooms": [int(features[2])], "postcode": [features[3]]}
    user_values = pd.DataFrame.from_dict(data)
    predicted_price = model.predict(user_values).values[0]

    return render_template("index.html", prediction_text="House is worth £ {:0.0f}".format(predicted_price))

@app.route("/results",methods=["POST"])
def results():

    data = request.get_json()
    temp_dict = {"bedrooms": [data["bedrooms"]], "toilets": [data["toilets"]], "other_rooms": [data["other_rooms"]], "postcode": [data["postcode"]]}
    dataframe = pd.DataFrame.from_dict(temp_dict)
    output = model.predict(dataframe).values[0]
    return jsonify({"Price" : int(output)})

if __name__ == "__main__":
    app.run()
