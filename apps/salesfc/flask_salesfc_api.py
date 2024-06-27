# simple Flask backend to run Sales Forecast API and export to Slack

import os 

from flask import Flask, request, jsonify

# from apps.salesfc.inference import Inference

# # importing BatchEngine from root folder *check* if better way of doing this
import sys
sys.path.insert(0, '/Users/barry.walsh/rotaready/rr_repos/ML-API')

from modules.batch_engine import BatchEngine
import modules.config as config

from slack import WebClient

app = Flask(__name__)

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


env = 'local' # *update {env} param later to config.ENV

@app.route('/')
def entry_point():
    return 'Test API call!'

@app.route('/post', methods=["POST"])
def testpost():
    input_json = request.get_json(force=True) 
    print(input_json)
    
    queue = f"ml-model-training-task-manager-{env}-jobs" # *update {env} param later

    # *check* change approach below to handle many realms defined in job ?
    infer = Inference(
            config.AWS_REGION,
            queue,
            config.SLACK_CHANNEL,
            client,
            config.BATCH_SIZE,
            env,
            input_json['job'][0]['realm'],
            input_json['job'][0]['start_date'],
            input_json['job'][0]['future_predictions'],
        )

    # start job message on slack 
    # NB  *check* hard coded below - update: default_job should look like this: {'future_predictions': 7, 'start_date': '2024-04-23'}
    sqs_batches = [infer.slack_job_start(default_job = {'future_predictions': 7, 'start_date': '2024-04-26'}, #dict(input_json['future_predictions'], input_json['start_date']),
                                                       batches = input_json['job'])]
    
    print("sqs_batches: ", sqs_batches)

    batch = BatchEngine(sqs_batches)
    batch.begin()

    return jsonify(input_json['job'])
