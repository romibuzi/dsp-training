import os
import pandas as pd
import logging
import mlflow


def predict(test_file_path, preprocessing_pipeline_name, logistic_reg_model_name, prediction_file_path):
    """
    Make prediction on test data with saved model.

    :param test_file_path: path to test data.
    :param preprocessing_pipeline_name: name of the preprocessing pipeline saved with mlflow.
    :param logistic_reg_model_name: name of logistic reg model to be saved with mlflow.
    :param prediction_file_path: path to prediction data.

    :return: None
    """
    test_df = pd.read_csv(test_file_path)

    current_run = mlflow.active_run()

    logging.info("Loading preprocessing pipeline")
    preprocessing_pipeline = mlflow.sklearn.load_model(
        os.path.join(current_run.info.artifact_uri, preprocessing_pipeline_name))

    preprocessed_test = preprocessing_pipeline.transform(test_df)

    logging.info("Loading trained model")
    logistic_reg = mlflow.sklearn.load_model(
        os.path.join(current_run.info.artifact_uri, logistic_reg_model_name))

    logging.info(f"Make predictions with {logistic_reg_model_name}")
    y_pred = logistic_reg.predict(preprocessed_test)

    test_df["prediction"] = y_pred

    logging.info("Saving prediction results")
    test_df.to_csv(prediction_file_path, index=False)
