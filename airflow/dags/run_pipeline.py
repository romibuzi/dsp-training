from datetime import datetime, timedelta
from airflow.models import DAG
import sys
import os
import pytz

from airflow.operators.python_operator import PythonOperator

PATH_MODULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",)
sys.path += [PATH_MODULES]

from src.preprocess.preprocess import preprocess, load_and_split_data
from src.logistic_reg.logistic_reg_train import logistic_reg_train
from src.evaluation.evaluate import evaluate
from src.predict.predict import predict
from src.utils import download_file_from_url
from main import initialize_mlflow_run

import src.constants.files as files
import src.constants.models as m


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
        'run-pipeline-train',
        default_args=default_args,
        description='Train model',
        schedule_interval=timedelta(days=1),
        start_date=datetime.now(tz=pytz.timezone("Europe/Paris")),
        tags=['train'],
) as dag:

    initialize_mlflow_run = PythonOperator(
        task_id='initialize_mlflow_run',
        python_callable=initialize_mlflow_run
    )

    download = PythonOperator(
        task_id='download',
        python_callable=download_file_from_url,
        op_kwargs={'url': files.LOANS_DATA_URL,
                   'file_path': os.path.join(files.RAW_DATA, files.LOANS)}

    )
    load_and_split = PythonOperator(
        task_id='load_and_split',
        python_callable=load_and_split_data,
        op_kwargs={'raw_data_path': files.LOANS,
                   'training_file_path': files.TRAIN,
                   'test_file_path': files.TEST}
    )

    preprocess = PythonOperator(
        task_id='preprocess',
        python_callable=preprocess,
        op_kwargs={'training_file_path': files.TRAIN,
                   'preprocessed_train_path': files.PREPROCESSED_TRAIN,
                   'preprocessing_pipeline_name': files.PREPROCESSING_PIPELINE}
    )

    model = PythonOperator(
        task_id='model',
        python_callable=logistic_reg_train,
        op_kwargs={'preprocessed_train_path': files.PREPROCESSED_TRAIN,
                   'logistic_reg_model_name': m.LOGISTIC_REG_MODEL_NAME}
    )

    predict = PythonOperator(
        task_id='predict',
        python_callable=predict,
        op_kwargs={'test_file_path': files.TEST,
                   'preprocessing_pipeline_name': files.PREPROCESSING_PIPELINE,
                   'logistic_reg_model_name': m.LOGISTIC_REG_MODEL_NAME,
                   'prediction_file_path': files.PREDICTIONS_TEST}
    )

    evaluate = PythonOperator(
        task_id='evaluate',
        python_callable=evaluate,
        op_kwargs={'prediction_file_path': files.PREDICTIONS_TEST}
    )


initialize_mlflow_run >> download >> load_and_split >> preprocess >> model >> predict >> evaluate
