import os
from datetime import datetime, timedelta
import pytz

from airflow import DAG
from airflow.contrib.operators.ecs_operator import ECSOperator
from airflow.operators.dummy_operator import DummyOperator


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
        'run-pipeline-fargate',
        default_args=default_args,
        description='Train model',
        schedule_interval=timedelta(days=1),
        start_date=datetime.now(tz=pytz.timezone("Europe/Paris")),
        tags=['train'],
) as dag:
    start = DummyOperator(task_id=f'start')

    fargate_task = ECSOperator(
        # Il faut avoir créé la task definition qui utilise l’image Docker poussée par le script local_docker_build.sh
        # et créé un cluster Fargate et un service qui lance la task definition (script create_fargate_task.sh)
        task_id="fargate_task",
        dag=dag,
        aws_conn_id="aws_ecs",
        cluster="fargate-cluster",
        task_definition="dsp-training",
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "dsp-training-container",
                    "command": ["python3", "main.py"],
                },
            ],
        },
        network_configuration={
            "awsvpcConfiguration": {
                # Aller chercher dans les détails de MWAA un SG et un subnet auxquels MWAA est connecté
                "securityGroups": [os.environ.get("SECURITY_GROUP_ID", "sg-0821fa185cc2517ff")],
                "subnets": [os.environ.get("SUBNET_ID", "subnet-017f112634880ea29")],
            },
        },
        awslogs_create_group=True,
        awslogs_group="/ecs/dsp-training",
        awslogs_region="eu-west-1",
        awslogs_stream_prefix="ecs/dsp-training-container",  # prefix with container name
    )

start >> fargate_task