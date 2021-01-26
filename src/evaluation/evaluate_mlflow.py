import os

import mlflow
from joblib import load
import pandas as pd
import logging

import src.constants.files as files
import src.constants.columns as c
from src.logistic_reg.logistic_reg_train import LOGISTIC_REG_MODELS_PATH
from sklearn.metrics import f1_score


def evaluate_mlflow():
    test_df = pd.read_csv(os.path.join(files.INTERIM_DATA, files.TEST))

    preprocessing_pipeline = load(os.path.join(files.PIPELINES, files.PREPROCESSING_PIPELINE))
    preprocessed_test = preprocessing_pipeline.transform(test_df)
    y_test = test_df[c.Loans.Loan_Status].values

    logistic_reg_model_names = [file for file in os.listdir(LOGISTIC_REG_MODELS_PATH) if "joblib" in file]

    with mlflow.start_run():
        for logistic_reg_model_name in logistic_reg_model_names:
            logging.info(f"Evaluating with mlflow {logistic_reg_model_name}")
            model_date = logistic_reg_model_name.replace(".joblib", "")[-8:]

            logistic_reg = load(os.path.join(LOGISTIC_REG_MODELS_PATH, logistic_reg_model_name))
            y_pred = logistic_reg.predict(preprocessed_test)

            score = round(f1_score(y_test, y_pred, pos_label="Y"), 2)

            mlflow.log_metric("f1_score", score)
            mlflow.log_param("model_date", model_date)

            # TODO: investigate how to log the model
            # mlflow.sklearn.log_model(logistic_reg, "logistic_reg")
