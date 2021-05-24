# Créer une instance EC2 medium avec Ubuntu 18.04

sudo apt-get update
sudo apt-get install -y build-essential
sudo apt install python3-pip

git clone https://github.com/romibuzi/dsp-training.git
cd dsp-training
git checkout exercice5-solution

pip3 install -r requirements.txt
pip3 install apache-airflow==1.10.12 --constraint airflow_constraints.txt
export AIRFLOW_HOME=$(pwd)/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__WEBSERVER__RBAC=True

export PATH=~/.local/bin/:$PATH

airflow initdb

airflow create_user \
--username admin \
--firstname Peter \
--lastname Parker \
--role Admin \
--email spiderman@superhero.org

airflow webserver --port 5000

# Dans un autre terminal connecté en ssh
cd dsp-training
export AIRFLOW_HOME=$(pwd)/airflow
export PATH=~/.local/bin/:$PATH
airflow scheduler