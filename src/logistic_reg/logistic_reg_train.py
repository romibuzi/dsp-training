import pandas as pd
from sklearn.linear_model import LogisticRegression
import mlflow
import logging

import src.constants.columns as c
import src.constants.files as files


def logistic_reg_train(preprocessed_train_path, logistic_reg_model_name):
    """
    Read preprocessed train data, instantiate model, fit on train data and save model.

    :param preprocessed_train_path: path to preprocessed training data.
    :param logistic_reg_model_name: name of logistic reg model to be saved with mlflow.

    :return: None
    """
    train_df = pd.read_csv(preprocessed_train_path)

    logistic_reg = LogisticRegression()
    
    logistic_reg.fit(
        train_df.drop(c.Loans.target(), axis=1).values,
        train_df[c.Loans.target()].values
    )

    logging.info("Saving model")
    with open(files.CURRENT_RUN_ID) as file:
        current_run_id = file.read()
    with mlflow.start_run(run_id=current_run_id):
        mlflow.sklearn.log_model(logistic_reg, logistic_reg_model_name)
