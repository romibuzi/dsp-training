import os
import pandas as pd
import mlflow

from src.constants import files
from src.preprocess.preprocess import preprocess
from tests.utils import setup_mlruns

LOCAL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def test_preprocess():
    mlruns_path = os.path.join("file:", LOCAL_ROOT, "mlruns_test").replace("C:", "")
    setup_mlruns(mlruns_path)
    mlflow.set_experiment(files.MLFLOW_EXPERIMENT_NAME)
    # Given
    preprocessed_train_path = os.path.join(LOCAL_ROOT, "result_test.csv")

    # When
    preprocess(
        training_file_path=os.path.join(LOCAL_ROOT, "loans_test.csv"),
        preprocessed_train_path=preprocessed_train_path,
        preprocessing_pipeline_name=files.PREPROCESSING_PIPELINE
    )

    # Then
    expected = pd.read_csv(os.path.join(LOCAL_ROOT, "expected.csv"))
    # Read result from csv to avoid problems with nan
    result = pd.read_csv(preprocessed_train_path)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)

    try:
        mlflow.sklearn.load_model(os.path.join(mlflow.active_run().info.artifact_uri, files.PREPROCESSING_PIPELINE))
    except IOError:
        raise AssertionError("The preprocessing pipeline has not been saved with mlflow")
