import logging

import constants.files as files
from utils import load_ml_object_from_s3, upload_pandas_df_to_s3, load_pandas_df_from_s3


def predict(test_file_path, preprocessing_pipeline_path, logistic_reg_model_path, prediction_file_path):
    """
    Make prediction on test data with saved model.

    :param test_file_path: path to test data.
    :param preprocessing_pipeline_path: path to the preprocessing pipeline saved with mlflow.
    :param logistic_reg_model_path: path to the logistic reg model.
    :param prediction_file_path: path to prediction data.

    :return: None
    """
    test_df = load_pandas_df_from_s3(files.S3_BUCKET, test_file_path)

    logging.info("Loading preprocessing pipeline")
    preprocessing_pipeline = load_ml_object_from_s3(files.S3_BUCKET, preprocessing_pipeline_path)

    preprocessed_test = preprocessing_pipeline.transform(test_df)

    logging.info("Loading trained model")
    logistic_reg = load_ml_object_from_s3(files.S3_BUCKET, logistic_reg_model_path)

    logging.info(f"Make predictions with {logistic_reg_model_path}")
    y_pred = logistic_reg.predict(preprocessed_test)

    test_df["prediction"] = y_pred

    logging.info("Saving prediction results")
    upload_pandas_df_to_s3(test_df, files.S3_BUCKET, prediction_file_path)
