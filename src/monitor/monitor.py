from datetime import datetime
import logging
import pandas as pd

from utils import load_pandas_df_from_s3, upload_pandas_df_to_s3
from constants import files


def monitor(prediction_file_path, prediction_history_path, metrics_history_path):
    new_predictions = load_pandas_df_from_s3(files.S3_BUCKET, prediction_file_path)

    logging.info("Append new predictions to history and upload to s3.")
    datetime_now = datetime.now()
    new_predictions["timestamp"] = datetime_now
    try:
        prediction_history = load_pandas_df_from_s3(files.S3_BUCKET, prediction_history_path)
    except:
        logging.info("Prediction history dataframe doesn’t exist yet, creating it now.")
        prediction_history = None

    new_prediction_history = pd.concat([prediction_history, new_predictions])
    upload_pandas_df_to_s3(new_prediction_history, files.S3_BUCKET, prediction_history_path)

    logging.info("Compute new metrics and upload to s3.")
    # TODO 1 : calculer le ratio des attributions de crédits par rapport à l'ensemble des demandes
    # ex: 50 crédits acceptés sur 100 demandes = 50%
    accepted_loans_ratio = NotImplemented()
    logging.info(f"Accepted loans ratio: {accepted_loans_ratio:.5f}")
    new_metric_df = pd.DataFrame.from_records([{"date": datetime_now, "accepted_loans_ratio": accepted_loans_ratio}])

    try:
        metrics_history = load_pandas_df_from_s3(files.S3_BUCKET, metrics_history_path)
    except:
        logging.info("Metrics history dataframe doesn’t exist yet, creating it now.")
        metrics_history = None

    new_metrics_history = pd.concat([metrics_history, new_metric_df])
    upload_pandas_df_to_s3(new_metrics_history, files.S3_BUCKET, metrics_history_path)

    # Alert if necessary
    # TODO 2 : logger un warning et lever une exception si le ratio des attributions de crédits (accepted_loans_ratio)
    #  descend en dessous de 40%

