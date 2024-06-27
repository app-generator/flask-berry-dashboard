# config for Flask backend to run Sales Forecast API and export to Slack

import os

# Environment
LOCAL_ENV = "uat"  # uat
SSM_ENV = os.environ.get("SSM_ENV")
# S3_ENV = "uat" # *check* may need to add in line with training module


SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
AWS_REGION = os.environ.get("EC2_REGION", "eu-west-1")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_SECRET = os.environ.get("SLACK_SECRET")

WEATHER_FEATURES = [
    "temperaturemax",
    "precipprobability",
    "precipintensity",
    "cloudcover",
]

# SQS
queue_env = SSM_ENV or LOCAL_ENV
queue_env_prefix = "prod" if queue_env == "production" else queue_env
SQS_JOB_QUEUE_NAME = f"rotaready-{queue_env_prefix}-ML-batchPredictSales-jobs"
BATCH_SIZE = 10

# Weather
VISUAL_CROSSING_API_KEY = os.environ.get("VISUAL_CROSSING_API_KEY")
VISUAL_FUTURE_DAYS_LIMIT = 14

# Output files
S3_BUCKET = "rotaready-machine-learning"
S3_PATH = "sales_predictor_models/models"

# Rotaready
CC_SALES_FORECAST_TYPE_ID = 5
CC_RESERVATIONS_FORECAST_TYPE_ID = 5
