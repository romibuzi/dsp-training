import os
import src.constants.models as m


def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


# equals True when running test with pytest because of environment variable specified in pytest.ini
is_running_test = eval(os.getenv("IS_RUNNING_TEST", "False"))

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",)

if not is_running_test:
    DATA_PATH = create_folder(os.path.join(PROJECT_ROOT_PATH, "data"))
else:
    DATA_PATH = create_folder(os.path.join(PROJECT_ROOT_PATH, "tests", "integration_test", "data_test"))

RAW_DATA = create_folder(os.path.join(DATA_PATH, "raw"))
INTERIM_DATA = create_folder(os.path.join(DATA_PATH, "interim"))
OUTPUT_DATA = create_folder(os.path.join(DATA_PATH, "output"))
MODELS = create_folder(os.path.join(DATA_PATH, "models"))

if not is_running_test:
    LOANS_DATA_URL = "https://storage.googleapis.com/formation-dsp-data/loans.csv"
else:
    LOANS_DATA_URL = "https://storage.googleapis.com/formation-dsp-data/loans_test.csv"

LOANS = os.path.join(RAW_DATA, "loans.csv")

TRAIN = os.path.join(INTERIM_DATA, "train.csv")
TEST = os.path.join(INTERIM_DATA, "test.csv")
PREPROCESSED_TRAIN = os.path.join(INTERIM_DATA, "preprocessed_train.csv")

MLFLOW_EXPERIMENT_NAME = "mlflow-experiment"
# The preprocessing is not attached to a folder because it is saved with mlflow.
PREPROCESSING_PIPELINE = "pipeline"

PREDICTIONS_TEST = os.path.join(OUTPUT_DATA, f"{m.LOGISTIC_REG_MODEL_NAME}_predictions.csv")