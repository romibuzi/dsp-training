import logging
import os

from monitor.monitor import monitor_loans_ratio, monitor_input_drift
from predict.predict import predict
import constants.files as files
import constants.models as m


def predict_and_monitor():
    """
    Launch predict on new file and monitor.
    """
    logging.info("*********** 1/5 Loading and splitting data ***********")

    monitor_input_drift(files.NEW_LOANS_TO_ACCEPT, files.INPUT_STATS_HISTORY)

    predict(test_file_path=files.NEW_LOANS_TO_ACCEPT,
            preprocessing_pipeline_path=files.PREPROCESSING_PIPELINE,
            logistic_reg_model_path=os.path.join(files.MODELS, m.LOGISTIC_REG_MODEL_NAME),
            prediction_file_path=files.NEW_PREDICTIONS)

    monitor_loans_ratio(prediction_file_path=files.NEW_PREDICTIONS,
                        prediction_history_path=files.PREDICTIONS_HISTORY,
                        metrics_history_path=files.METRICS_HISTORY)


if __name__ == "__main__":
    predict_and_monitor()
