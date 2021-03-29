import shutil
import mlflow
import os


def setup_mlruns(mlruns_path):
    if os.path.exists(mlruns_path):
        shutil.rmtree(mlruns_path)

    mlflow.set_tracking_uri(mlruns_path)