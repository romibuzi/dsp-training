from main import main
import os
import pandas as pd
from tests.utils import setup_mlruns

from src.constants import files

LOCAL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def test_main_runs():
    mlruns_path = os.path.join("file:", LOCAL_ROOT, "mlruns_test").replace("C:", "")
    setup_mlruns(mlruns_path)

    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)


def test_main():
    mlruns_path = os.path.join("file:", LOCAL_ROOT, "mlruns_test").replace("C:", "")
    setup_mlruns(mlruns_path)

    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)

    # Then
    expected = pd.read_csv(os.path.join(LOCAL_ROOT, "expected_predictions.csv"))
    # Read result from csv to avoid problems with nan
    result = pd.read_csv(files.PREDICTIONS_TEST)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_main_runs_with_preprocess_false():
    mlruns_path = os.path.join("file:", LOCAL_ROOT, "mlruns_test").replace("C:", "")
    setup_mlruns(mlruns_path)

    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)

    bool_dict["preprocess"] = False

    main(bool_dict)
