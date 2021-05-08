import os
import constants.models as m


def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


# equals True when running test with pytest because of environment variable specified in pytest.ini
is_running_test = eval(os.getenv("IS_RUNNING_TEST", "False"))

S3_ROOT_PATH = ""

if not is_running_test:
    DATA_PATH = os.path.join(S3_ROOT_PATH, "data")
else:
    DATA_PATH = os.path.join(S3_ROOT_PATH, "tests", "integration_test", "data_test")

RAW_DATA = os.path.join(DATA_PATH, "raw")
INTERIM_DATA = os.path.join(DATA_PATH, "interim")
OUTPUT_DATA = os.path.join(DATA_PATH, "output")
MODELS = os.path.join(DATA_PATH, "models")
PIPELINES = os.path.join(DATA_PATH, "pipelines")
LOGISTIC_REG_MODELS_PATH = os.path.join(MODELS, "logistic_reg")

CURRENT_RUN_ID = os.path.join(DATA_PATH, "current_run_id")

LOANS = os.path.join(RAW_DATA, "loans.csv")

TRAIN = os.path.join(INTERIM_DATA, "train.csv")
TEST = os.path.join(INTERIM_DATA, "test.csv")
PREPROCESSED_TRAIN = os.path.join(INTERIM_DATA, "preprocessed_train.csv")

PREPROCESSING_PIPELINE = os.path.join(PIPELINES, "pipeline")
LOGISTIC_REG_MODEL = os.path.join(LOGISTIC_REG_MODELS_PATH, m.LOGISTIC_REG_MODEL_NAME + ".joblib")

PREDICTIONS_TEST = os.path.join(OUTPUT_DATA, f"{m.LOGISTIC_REG_MODEL_NAME}_predictions.csv")

S3_BUCKET = "mlflow-dsp-training"