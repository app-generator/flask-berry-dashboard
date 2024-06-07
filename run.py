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
from flask import render_template, request, session, jsonify
from flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from localStoragePy import localStoragePy

from apps.config import config_dict
from apps import create_app, db

from apps.salesfc.inference import Inference
import apps.salesfc.config as config

from apps.analytics import quicksight_embed as qe
from apps.analytics import bedrock_rag as rag
from apps.analytics import bedrock_rag_enhanced as re
from apps.analytics import bedrock_rag_LangChain as lc

from slack import WebClient


# # importing BatchEngine from root folder *check* if better way of doing this
import sys
sys.path.insert(0, '/Users/barry.walsh/rotaready/rr_repos/ML-API')

from modules.batch_engine import BatchEngine
#import modules.config as config

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
kb_id = "WSVBOTTJJX" # *check* move to env. variable WSVBOTTJJX for S3 version, 9PLBA6IA3M for CW version


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

    if isinstance(batchOutput['display_msg'], pd.DataFrame): # i.e. a prediction has been returned

        # *check* refactor below - too complicated
        df = batchOutput['display_msg']

        session["fcast_sales"]=int(df.to_dict('list')['sales'][0]) # example forecasted revenue for 1st day of forecast for coststream 1

        session["output"]=f"{str(batchOutput['display_msg'])}" # NB session variable must be a string to render in html

        print("session[output] Output: ", session["output"])  

        session["realm-site"]=realm + " - " + site

        session["fcast_dates"]= [x.strftime('%d-%b') for x in df.loc[df['stream_id'] == '1'].to_dict('list')['time']] # example forecasted revenue list of vals for chart or use dummy example [-3, 15, 15, 35, 65, 40, 80, 25, 15, 85, 25, 75] 
        
        for i in df['stream_id'].unique():

            # *check* for now stream_id 1 only
            forecast_sales = df.loc[df['stream_id'] == i] [['time', 'sales']]

            session[f"fcast_vals_raw_{i}"]= [int(x) for x in forecast_sales.to_dict('list')['sales']] # example forecasted revenue list of vals for chart or use dummy example [-3, 15, 15, 35, 65, 40, 80, 25, 15, 85, 25, 75] 

          

    return render_template('pages/sample-page.html' ) 


@app.route("/analytics", methods=['GET'])
def analytics(): 

    session["qs_url"]=qe.getDashboardURL()

    print("session[qs_url]: ", session["qs_url"])

    return render_template('pages/typography.html')


@app.route("/gen_ai", methods=['GET'])
def gen_ai(): 

    # example questions:
    #target_qu = "What are the key anomalies we are seeing in the model training process ?"
    #target_qu = "What are the main errors we are seeing in the inference process ?"
    #"What are the key anomalies we are seeing in the model training process ?"
    # "can you tell me approximately how many training jobs failed within the last month with the train_size=None error and what percentage this is of all the training jobs in that period ?""

    target_qu = request.args["target_qu"]

    # custom responses from LLM (Anthropic) to the question posed in the last cell
    response = rag.retrieveAndGenerate(
        target_qu, kb_id
    )

    session["genai_resp"]= response["output"]["text"]

    print("session[genai]: ", session["genai_resp"])

    return render_template('pages/typography.html')

# chatbot UI invocation of bedrock - just call the RAG function
@app.route("/ask", methods=['GET', 'POST'])
def ask(): 

    # example questions:
    #target_qu = "What are the key anomalies we are seeing in the model training process ?"
    #target_qu = "What are the main errors we are seeing in the inference process ?"
    #"What are the key anomalies we are seeing in the model training process ?"
    # "can you tell me approximately how many training jobs failed within the last month with the train_size=None error and what percentage this is of all the training jobs in that period ?""

    # target_qu = request.args["target_qu"]
    target_qu = eval(request.data)['prompt']


    # basic model - custom responses from LLM (Anthropic) to the question posed in the last cell
    rag_result = rag.retrieveAndGenerate(
        target_qu, kb_id
    )

    print(rag_result["output"]["text"]) # debug

    # enhanced model - passes chunked vectors from KB to LLM for context-specific, sophisticted answer
    # rag_e_result = re.rag_enhanced(
    #     target_qu, kb_id
    # )

    # LangChain - recommended API for LLMs *check* but its not doing a good job and doesnt seem very context-specific
    # lc_result = lc.LangChain(
    #     target_qu, kb_id
    # )



    # session["genai_resp"]= response["output"]["text"]

    # print("session[genai]: ", session["genai_resp"])

    genai_response = {"success": True, "message": rag_result["output"]["text"]} # {"success": True, "message": lc_result}

    return genai_response


# genai chatbot route, shows genai-chatbot.html view
@app.route('/genai-chatbot')
def genai_chatbot():
    return render_template('pages/genai-chatbot.html')

# data for charts
@app.route('/chart_salesfc', methods=["GET"])
def chart_salesfc():    
    return str(session["fcast_sales"]['sales'])
    # return render_template('index.html', output = f"{session["fcast_sales"]['sales']}")


if __name__ == "__main__":
    # Start the Flask web server    
    app.run(debug=True, port=5002)
