import logging

import constants.columns as c
import constants.models as m
import constants.files as files
from sklearn.metrics import f1_score

from utils import load_pandas_df_from_s3


def evaluate(prediction_file_path):
    """
    Evaluate the performance of the model on test data.

    :param prediction_file_path: path to prediction data.

    :return: None
    """
    prediction_df = load_pandas_df_from_s3(files.S3_BUCKET, prediction_file_path)

    logging.info(f"Evaluating {m.LOGISTIC_REG_MODEL_NAME}")

    y_test = prediction_df[c.Loans.target()].values
    y_pred = prediction_df["prediction"].values

    score = round(f1_score(y_test, y_pred, pos_label="Y"), 2)

    logging.info(f"F1 score for model {m.LOGISTIC_REG_MODEL_NAME} is {score}")
