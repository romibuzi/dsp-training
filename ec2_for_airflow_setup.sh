# Créer une instance EC2 medium avec Ubuntu 18.04

sudo apt-get update
sudo apt-get install -y build-essential
sudo apt install -y python3-pip

git clone https://github.com/romibuzi/dsp-training.git
# To be able to copy/paste files from local to EC2 instance (see copy/paste command at end of file)
sudo chmod 777 -R dsp-training
cd dsp-training
git checkout exercice5

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

# To copy / paste a file from local machine to EC2 instance
# scp -i private_key.pem myfile ubuntu@ec2-<ip-adress>.eu-west-1.compute.amazonaws.com:/home/ubuntu/dsp-training/path-to-folder