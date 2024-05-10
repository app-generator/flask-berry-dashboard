# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, sys
import pandas as pd
import json

import js

import webbrowser
import threading
from threading import Timer
import time

from flask import Flask
from flask import render_template, request, session
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from localStoragePy import localStoragePy

from apps.config import config_dict
from apps import create_app, db

from apps.salesfc.inference import Inference
import apps.salesfc.config as config

from slack import WebClient


# # importing BatchEngine from root folder *check* if better way of doing this
import sys
sys.path.insert(0, '/Users/barry.walsh/rotaready/rr_repos/ML-API')

from modules.batch_engine import BatchEngine
#import modules.config as config

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))



# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
# app = flask.Flask("__main__")

# secret key is needed for session
app.secret_key = b'\x19\x86\x1b\x19\xfe?z\x11\x9e\xc1.\x87\xe7\x00\xd7\xf8'

# local storage
localStorage = localStoragePy('salesfc', 'text')

Migrate(app, db)

env = 'local' # *update {env} param later to config.ENV

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG) )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)

# index route, shows index.html view
@app.route('/')
def index():
    return render_template('index.html')
    
# @app.route('/')
# def index(**kwargs):
#     if 'token' in kwargs:
#         return render_template('index.html', token = kwargs['token'])
#     else:
#         return render_template('index.html')


@app.route("/salesfc", methods=['POST'])
def salesfc_invocation():

    # gather inputs

    # session["realm"]=request.form["realm"]
    # session["site"]=request.form["site"]
    # session["future_preds"]=request.form["future_preds"]
    # session["start_date"]=request.form["start_date"]

    form_df = pd.DataFrame({'realm': [request.form["realm"]],
                            'site': [request.form["site"]],
                                'future_preds': [request.form["future_preds"]],
                                'start_date': [request.form["start_date"]]
                                })
    # form_df.to_csv('form_params.csv') # *check* refactor later just pass temp variables between jquery and flask, no need for a csv  

    # return f"{env}: Forecasting sales for {request.form["realm"]}"

    # *check* consider refactoring as we are using jquery for form handling, is this function even needed anymore ??
    return render_template('pages/sample-page.html', sessionOutput=f"{env}: Forecasting sales for {request.form["realm"]}")

@app.route("/start_salesfc", methods=['GET'])
def start_salesfc(): #realm, site, future_preds, start_date):

    # NB request.args for GET, request.form for POST requests

    realm = request.args["realm"] # input_data['realm'][0] 
    site = request.args["site"] #input_data['site'][0]
    future_preds = request.args["future_preds"] #input_data['future_preds'][0]
    start_date = request.args["start_date"] #input_data['start_date'][0]

    # site = session.get("site",None)
    # future_preds = session.get("future_preds",None)
    # start_date = session.get("start_date",None)

    queue = f"ml-model-training-task-manager-{env}-jobs" # *update {env} param later

    # *check* change approach below to handle many realms defined in job ?
    infer = Inference(
            config.AWS_REGION,
            queue,
            config.SLACK_CHANNEL,
            client,
            config.BATCH_SIZE,
            env,
            realm,
            site,
            future_preds
        )

    job_json = [
                    {
                        "realm": realm,
                        "entity_id": site,
                        "forecast": "true",
                        "future_predictions": future_preds,
                        "start_date": start_date
                    }
                ]
    
    # multi job example:
    # job_json = [
    #                 {
    #                     "realm": "temper",
    #                     "entity_id": "pad",
    #                     "forecast": "true",
    #                     "future_predictions": 1,
    #                     "start_date": "2024-04-26"
    #                 },
    #                 {
    #                     "realm": "temper",
    #                     "entity_id": "whi",
    #                     "forecast": "true",
    #                     "future_predictions": 1,
    #                     "start_date": "2024-04-26"
    #                 }
    #             ]

    # start job message on slack flask
    sqs_batches = [infer.slack_job_start(default_job = {'future_predictions': future_preds, 'start_date': start_date}, batches = job_json)]
    
    #slack_posts = client.conversations_history(channel='ml')
    

    print("sqs_batches: ", sqs_batches)

    batch = BatchEngine(sqs_batches)
    batchOutput = batch.begin(notifications = True)

    session["output"]=f"{str(batchOutput)}" # NB session variable must be a string to render in html

    print("session[output] Output: ", session["output"])

    # print("session Output: ", batchOutput)

    # export status to json file
    # test = {"name": "Harry", "age": 14}
    # with open('apps/templates/pages/salesfc_status.json', 'w', encoding='utf-8') as f:
    #     json.dump(test, f, ensure_ascii=False, indent=4)

    f = open("salesfc_status.txt", "w")
    f.write(str(batchOutput))
    f.close()

    # js.statusVar = batchOutput

    # localStorage.setItem('salesfc', batchOutput)

    # must be a GET request for the param to get passed back to html

    # index(token = batchOutput) # reroute to index page with token

    return render_template('pages/sample-page.html', token = batchOutput ) #sessionOutput=f"{str(batchOutput)}")


if __name__ == "__main__":
    # Start the Flask web server
    app.run(debug=True)
