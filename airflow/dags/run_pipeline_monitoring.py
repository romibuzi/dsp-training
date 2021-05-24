from datetime import datetime, timedelta
from airflow.models import DAG
import sys
import os
import pytz
from airflow.operators.email_operator import EmailOperator

from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

PATH_MODULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src")
sys.path += [PATH_MODULES]

from preprocess.preprocess import preprocess, load_and_split_data
from logistic_reg.logistic_reg_train import logistic_reg_train
from evaluation.evaluate import evaluate
from predict.predict import predict
from monitor.monitor import monitor

import constants.files as files
import constants.models as m

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
        'run-pipeline-predict_and_monitor',
        default_args=default_args,
        description='Train model',
        schedule_interval=timedelta(days=1),
        start_date=datetime.now(tz=pytz.timezone("Europe/Paris")),
        tags=['train'],
) as dag:

    predict = PythonOperator(
        task_id='predict',
        python_callable=predict,
        # TODO 3 : remplir les paramètres test_file_path et prediction_file_path avec le nouveau fichier de loans
        #  à prédire ainsi que le chemin vers les prédictions du jour (new_predictions.csv)
        op_kwargs={'test_file_path': '',
                   'preprocessing_pipeline_path': files.PREPROCESSING_PIPELINE,
                   'logistic_reg_model_path': m.LOGISTIC_REG_MODEL_NAME,
                   'prediction_file_path': ''}
    )

    # TODO 4 : implémenter l'opérateur monitor en se basant sur l'exemple de l'opérateur predict
    #  qui appelera la méthode monitor du module monitor
    monitor = NotImplemented

    alert_email = EmailOperator(
        task_id='send_alerting_email',
        to='alerts@creditbanco.com',
        subject='Accepted loans ratio is not ok',
        html_content="""Check the last monitoring pipeline to analyze results""",
        dag=dag,
        trigger_rule=TriggerRule.ONE_FAILED
    )


predict >> monitor >> alert_email
