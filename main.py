import logging
import os

from preprocess.preprocess import preprocess, load_and_split_data
from logistic_reg.logistic_reg_train import logistic_reg_train
from evaluation.evaluate import evaluate
from predict.predict import predict
import constants.files as files
import constants.models as m
from utils import setup_logs, upload_logs_to_s3


def main(bool_dict):
    """
    Launch all project steps.

    :param bool_dict: Dictionnary with step names as keys and boolean as values allowing to bypass steps. This can be
    useful to re-run all steps but model training steps if they are already done for example.
    :return:
    """
    setup_logs()

    if bool_dict["load_and_split"]:
        logging.info("*********** 1/5 Loading and splitting data ***********")
        load_and_split_data(raw_data_path=files.LOANS,
                            training_file_path=files.TRAIN,
                            test_file_path=files.TEST)

    if bool_dict["preprocess"]:
        logging.info("*********** 2/5 Preprocessing ***********")
        preprocess(training_file_path=files.TRAIN,
                   preprocessed_train_path=files.PREPROCESSED_TRAIN,
                   preprocessing_pipeline_path=files.PREPROCESSING_PIPELINE)

    if bool_dict["logistic_reg_train"]:
        logging.info("*********** 3/5 Modeling ***********")
        logistic_reg_train(preprocessed_train_path=files.PREPROCESSED_TRAIN,
                           logistic_reg_model_path=os.path.join(files.MODELS, m.LOGISTIC_REG_MODEL_NAME))

    if bool_dict["predict"]:
        logging.info("*********** 4/5 Prediction ***********")
        predict(test_file_path=files.TEST,
                preprocessing_pipeline_path=files.PREPROCESSING_PIPELINE,
                logistic_reg_model_path=os.path.join(files.MODELS, m.LOGISTIC_REG_MODEL_NAME),
                prediction_file_path=files.PREDICTIONS_TEST)

    if bool_dict["evaluate"]:
        logging.info("*********** 5/5 Evaluation ***********")
        evaluate(prediction_file_path=files.PREDICTIONS_TEST)

    logging.info("Upload logs to S3")
    upload_logs_to_s3()


if __name__ == "__main__":
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict":True,
                 "evaluate": True
                 }
    main(bool_dict)
