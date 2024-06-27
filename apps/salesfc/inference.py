# invoke Inference process for Flask backend to run Sales Forecast API and export to Slack

import apps.salesfc.config

import os
from io import BytesIO

import boto3

import json
from typing import Any, Dict, List

from slack.web.client import WebClient

import xgboost as xgb

# # importing MLBase from root folder *check* if better way of doing this
import sys
sys.path.insert(0, '/Users/barry.walsh/rotaready/rr_repos/ML-API')
from slack_scripts.ml_base import MLBase


class Inference(MLBase):
    def __init__(
        self,
        region: str,
        queue_name: str,
        channel: str,
        slack_client: WebClient,
        batch_size: int,
        env: str,
        realm: str,
        start_date: str,
        future_predictions: str,
    ):
        super().__init__(
            region,
            queue_name,
            channel,
            slack_client,
            batch_size,
            env,
            realm,
        )
        self.start_date = start_date
        self.future_predictions = future_predictions

    def make_job_info(self, realm: str):
        return {
            "Id": f"job_{realm}",
            "MessageBody": json.dumps(
                {
                    "realm": self.realm,
                    "start_date": self.start_date,
                    "future_predictions": self.future_predictions,
                }
            ),
        }

    def jobs(self):
        return [self.make_job_info(self.realm)]

class ModelConfig:
    def __init__(self, realm: str):
        self.realm = realm
        self.s3 = boto3.resource("s3")
        self.env = config.SSM_ENV or config.LOCAL_ENV
        self.model_path = config.S3_PATH

        self.sales_model = self.load_models(f"sales-xgboost-{self.realm}.json")

        self.job_settings = self.fetch_job_settings_from_s3("sales")
        self.hourly_data = self.job_settings.get("hourly_data")

    def load_models(self, model_filename: List[str]):
        """
        Load sales model from S3
        """
        try:

            model_filename = os.path.join(
                self.model_path, self.env, "latest", model_filename
            )

            return self.json_retrieve(model_filename)

        except ModuleNotFoundError as e:
            msg = f"Failed to load Prophet model from S3: {model_filename}"
            print(
                "{}. Could be due to models saved with diff lib version.Err: {}".format(
                    msg, e
                )
            )
        except Exception:
            print(f"Failed to load XGBoost models from S3: {model_filename}")


    def json_retrieve(self, file: str):
        with BytesIO() as model_file:
            self.s3.Bucket(config.S3_BUCKET).download_fileobj(file, model_file)
            model_file.seek(0)  # move back to the beginning after writing
            model = xgb.Booster()
            model.load_model(fname=bytearray(model_file.read()))
            return model
        
    def fetch_job_settings_from_s3(self, training_type) -> Dict:
        """
        Fetch the JSON settings overrides for a realm - entity - stream.
        This includes data cleaning params and industry details.
        """

        key = (
            f"settings/{config.SSM_ENV or config.LOCAL_ENV}/{self.realm}/"
            f"settings-{self.realm}-{training_type}"
        )

        try:
            settings = json.load(
                self.s3.Bucket(config.S3_BUCKET).Object(key=key).get()["Body"]
            )
            print(f"Found existing S3 settings: {settings}")
            return settings
        except Exception:
            print(f"No setting overrides found in S3 '{key}' for job")
            return {}

