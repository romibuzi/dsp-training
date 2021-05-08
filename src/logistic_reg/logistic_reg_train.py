import pandas as pd
from sklearn.linear_model import LogisticRegression
import logging
import os

import constants.columns as c
import constants.files as files
from utils import upload_ml_object_to_s3, load_pandas_df_from_s3


def logistic_reg_train(preprocessed_train_path, logistic_reg_model_path):
    """
    Read preprocessed train data, instantiate model, fit on train data and save model.

    :param preprocessed_train_path: path to preprocessed training data.
    :param logistic_reg_model_path: path to the logistic reg model.

    :return: None
    """
    train_df = load_pandas_df_from_s3(files.S3_BUCKET, preprocessed_train_path)

    logistic_reg = LogisticRegression()
    
    logistic_reg.fit(
        train_df.drop(c.Loans.target(), axis=1).values,
        train_df[c.Loans.target()].values
    )

    logging.info("Saving model")
    upload_ml_object_to_s3(logistic_reg, files.S3_BUCKET, logistic_reg_model_path)
