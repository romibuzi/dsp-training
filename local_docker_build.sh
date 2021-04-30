docker login -u vincentvilletps

docker build -t vincentvilletps/dsp_training_no_mlflow:latest .

docker push vincentvilletps/dsp_training_no_mlflow:latest

# pour lancer en local
docker run vincentvilletps/dsp_training_no_mlflow:latest
docker run -it vincentvilletps/dsp_training_no_mlflow:latest /bin/bash