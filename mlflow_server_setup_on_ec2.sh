sudo apt-get update
sudo apt-get install -y build-essential
sudo apt install -y python3-pip

sudo pip3 install mlflow
sudo pip3 install pymysql
sudo pip3 install boto3

# Création de la base de données mysql
sudo apt install mysql-client-core-5.7
mysql -h mlflow-tracking-db.cvx8c1xndnmn.eu-west-1.rds.amazonaws.com -u admin -p
CREATE DATABASE trackingdb;

export BUCKET=s3://dsp-mlflow-tracking-bucket/
export USERNAME_DB=admin
export PASSWORD=formationdsp123
export HOST=mlflow-tracking-db.cvx8c1xndnmn.eu-west-1.rds.amazonaws.com
export PORT=3306
export DATABASE=trackingdb

mkdir mlflow

nohup mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --default-artifact-root ${BUCKET} \
    --backend-store-uri mysql+pymysql://${USERNAME_DB}:${PASSWORD}@${HOST}:${PORT}/${DATABASE}
