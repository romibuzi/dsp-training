from main import main
import os
import pandas as pd

from constants import files
from utils import load_pandas_df_from_s3, upload_pandas_df_to_s3

LOCAL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def initialize_raw_test_data():
    loans_test = pd.read_csv(os.path.join(LOCAL_ROOT, "data_test", "raw", "loans.csv"))
    upload_pandas_df_to_s3(loans_test, files.S3_BUCKET, files.LOANS)


def test_main_runs():
    initialize_raw_test_data()
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)


def test_main():
    initialize_raw_test_data()
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)

    # Then
    expected = pd.read_csv(os.path.join(LOCAL_ROOT, "expected_predictions.csv"))
    # Read result from csv to avoid problems with nan
    result = load_pandas_df_from_s3(files.S3_BUCKET, files.PREDICTIONS_TEST)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_main_runs_with_preprocess_false():
    initialize_raw_test_data()
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict": True,
                 "evaluate": True}

    main(bool_dict)

    bool_dict["preprocess"] = False

    main(bool_dict)
