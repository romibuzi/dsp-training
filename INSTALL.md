# Installation du projet

Note : Cette procédure devrait fonctionner sur Linux et Mac. Il faut la tester et la compléter pour Windows.

## Dépendances

Le projet utilise `Python3` et des librairies listées dans le fichier [requirements](requirements.txt). 

Nous recommendons d'installer ces dépendances dans un environnement virtuel.

Tester l'installation de `Python3` et `virtualenv` avec ces commandes

    python3 --version
    pip3 --version
    virtualenv --version
    
Note: selon votre installation de python, vous pouvez remplacer les commandes `python3` et `pip3` par `python` et `pip`

Installer `virtualenv` si besoin avec la commande :  `pip3 install virtualenv`

## Installation 

Cloner le projet en local

    git clone https://gitlab.com/USER/PROJECT.git
    cd PROJECT

Créer un environnement virtuel et l'activer

    virtualenv venv --python=python3.7
    source venv/bin/activate

Note: pour les utilisateurs de Windows, la commande d'activation de l'environnement virtuel est
    
    venv\Scripts\activate.bat

Installer les dépendances python 

    pip3 install -r requirements.txt

Ou si vous utilisez anaconda:

    conda create -n dsp-training python=3.7
    conda activate dsp-training
    conda install ipykernel jupyter
    pip install -r requirements.txt
    python -m ipykernel install --user --name=dsp-training

Tester l'installation

    python -m pytest tests

Lancer le projet en local sans Airflow

    export PYTHONPATH="./src/:$PYTHONPATH"    
    python main.py

## Airflow

Les commandes suivantes peuvent être lancées en local sur les Mac et distributions Linux.
Si vous avez un ordinateur Windows, connectez-vous en ssh à une machine Linux sur le cloud (par exemple, une instance EC2) et suivez les instructions du script [ec2_for_airflow_setup.sh](ec2_for_airflow_setup.sh)

Installation

    pip3 install apache-airflow==1.10.12 --constraint airflow_constraints.txt

    cd dsp-training # If you are not already at root dir

    export AIRFLOW_HOME=$(pwd)/airflow
    export AIRFLOW__CORE__LOAD_EXAMPLES=False
    export AIRFLOW__WEBSERVER__RBAC=True

Créer la base de données

    airflow initdb

    airflow create_user \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

Lancer Airflow

    export AIRFLOW_HOME=$(pwd)/airflow
    airflow webserver --port 8080
    
    # en cas d’erreur "no module named airflow.www"
    # https://stackoverflow.com/questions/53583633/how-to-resolve-error-no-module-named-airflow-www-while-starting-airflow-web
    pip3 uninstall -y gunicorn
    pip3 install gunicorn==19.4.0

Lancer le scheduler

    # Dans un 2ème terminal
    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES # https://stackoverflow.com/questions/66676165/airflow-task-for-uploading-file-to-s3-bucket-using-boto3-cause-python-to-crash-a
    export AIRFLOW_HOME=$(pwd)/airflow
    airflow scheduler

Documentation Airflow sur AWS: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html

