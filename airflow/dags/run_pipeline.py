from datetime import datetime, timedelta
from airflow.models import DAG
import pytz

import sys
import os
PATH_MODULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src")
sys.path += [PATH_MODULES]

from airflow.operators.python_operator import PythonOperator

from preprocess.preprocess import preprocess, load_and_split_data
from logistic_reg.logistic_reg_train import logistic_reg_train
from evaluation.evaluate import evaluate
from predict.predict import predict

import constants.files as files


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
                   'preprocessing_pipeline_path': files.PREPROCESSING_PIPELINE}
    )

    model = PythonOperator(
        task_id='model',
        python_callable=logistic_reg_train,
        op_kwargs={'preprocessed_train_path': files.PREPROCESSED_TRAIN,
                   'logistic_reg_model_path': files.LOGISTIC_REG_MODEL}
    )

    predict = PythonOperator(
        task_id='predict',
        python_callable=predict,
        op_kwargs={'test_file_path': files.TEST,
                   'preprocessing_pipeline_path': files.PREPROCESSING_PIPELINE,
                   'logistic_reg_model_path': files.LOGISTIC_REG_MODEL,
                   'prediction_file_path': files.PREDICTIONS_TEST}
    )

    evaluate = PythonOperator(
        task_id='evaluate',
        python_callable=evaluate,
        op_kwargs={'prediction_file_path': files.PREDICTIONS_TEST}
    )


load_and_split >> preprocess >> model >> predict >> evaluate
