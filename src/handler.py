import pandas as pd
from rossmann import Rossmann
from flask import Flask, request

# initialize API
app = Flask(__name__)

# create endpoint
@app.route('/predict', methods=['POST'])

def rossmann_predict():
    df_raw_json = request.get_json()

    if df_raw_json:
        if isinstance(df_raw_json, dict):
            df_raw = pd.DataFrame(df_raw_json, index=[0])

        else:
            df_raw = pd.DataFrame(df_raw_json, index=df_raw_json[0].keys())

    # instantiate rossmann class
    papeline = Rossmann()