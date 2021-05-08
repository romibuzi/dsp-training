import os
import pandas as pd

from constants import files
from preprocess.preprocess import preprocess
from utils import upload_pandas_df_to_s3, load_pandas_df_from_s3

LOCAL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def test_preprocess():
    # Given
    loans_test = pd.read_csv(os.path.join(LOCAL_ROOT, "loans_test.csv"))
    loans_path_in_s3 = os.path.join("tests", "loans_test_s3.csv")
    upload_pandas_df_to_s3(loans_test, files.S3_BUCKET, loans_path_in_s3)

    preprocessed_train_path = os.path.join("tests", "preprocessed_train_s3.csv")

    # When
    preprocess(
        training_file_path=loans_path_in_s3,
        preprocessed_train_path=preprocessed_train_path,
        preprocessing_pipeline_path=files.PREPROCESSING_PIPELINE
    )

    # Then
    expected = pd.read_csv(os.path.join(LOCAL_ROOT, "expected.csv"))
    # Read result from csv to avoid problems with nan
    result = load_pandas_df_from_s3(files.S3_BUCKET, preprocessed_train_path)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)
