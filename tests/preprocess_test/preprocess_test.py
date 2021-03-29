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
    # TODO 1 : initialiser la variable preprocessed_train_path avec le chemin vers le fichier result_test.csv du dossier
    #  preprocess_test, et la variable training_file_path avec le chemin vers le fichier loans_test.csv du même dossier.
    preprocessed_train_path = NotImplementedError()
    training_file_path = NotImplementedError()

    # When
    preprocess(
        training_file_path=training_file_path,
        preprocessed_train_path=preprocessed_train_path,
        preprocessing_pipeline_name=files.PREPROCESSING_PIPELINE
    )

    # Then
    # TODO 2 : charger le fichier expected.csv des résultats attendus.
    expected = NotImplementedError()
    # Read result from csv to avoid problems with nan
    result = pd.read_csv(preprocessed_train_path)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)

    try:
        # TODO 3 : charger le preprocessing pipeline depuis mlflow.
        #  indice : inspirez-vous du code de predict.py
        active_run = mlflow.active_run()
        NotImplementedError()
    except IOError:
        raise AssertionError("The preprocessing pipeline has not been saved with mlflow")
