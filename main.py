import os
import mlflow
from datetime import datetime
import logging

from src.utils import download_file_from_url
from src.preprocess.preprocess import preprocess, load_and_split_data
from src.logistic_reg.logistic_reg_train import logistic_reg_train
from src.evaluation.evaluate import evaluate
from src.predict.predict import predict
import src.constants.files as files
import src.constants.models as m


def main(bool_dict):
    """
    Launch all project steps.

    :param bool_dict: Dictionnary with step names as keys and boolean as values allowing to bypass steps. This can be
    useful to re-run all steps but model training steps if they are already done for example.
    :return:
    """
    download_file_from_url(files.LOANS_DATA_URL, os.path.join(files.RAW_DATA, files.LOANS))

    today_str = str(datetime.date(datetime.now()))
    mlflow.set_tracking_uri(files.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(files.MLFLOW_EXPERIMENT_NAME)
    with mlflow.start_run(run_name=today_str):
        if bool_dict["load_and_split"]:
            logging.info("*********** 1/5 Loading and splitting data ***********")
            load_and_split_data(raw_data_path=files.LOANS,
                                training_file_path=files.TRAIN,
                                test_file_path=files.TEST)

        if bool_dict["preprocess"]:
            logging.info("*********** 2/5 Preprocessing ***********")
            preprocess(training_file_path=files.TRAIN,
                       preprocessed_train_path=files.PREPROCESSED_TRAIN,
                       preprocessing_pipeline_name=files.PREPROCESSING_PIPELINE)

        if bool_dict["logistic_reg_train"]:
            logging.info("*********** 3/5 Modeling ***********")
            logistic_reg_train(preprocessed_train_path=files.PREPROCESSED_TRAIN,
                               logistic_reg_model_name=m.LOGISTIC_REG_MODEL_NAME)

        if bool_dict["predict"]:
            logging.info("*********** 4/5 Prediction ***********")
            predict(test_file_path=files.TEST,
                    preprocessing_pipeline_name=files.PREPROCESSING_PIPELINE,
                    logistic_reg_model_name=m.LOGISTIC_REG_MODEL_NAME,
                    prediction_file_path=files.PREDICTIONS_TEST)

        if bool_dict["evaluate"]:
            logging.info("*********** 5/5 Evaluation ***********")
            evaluate(prediction_file_path=files.PREDICTIONS_TEST)


if __name__ == "__main__":
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict":True,
                 "evaluate": True
                 }
    main(bool_dict)
