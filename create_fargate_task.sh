aws ecs create-cluster --cluster-name fargate-cluster
# task definition créée à la main
aws ecs list-task-definitions
# Aller chercher dans les détails de MWAA un SG et un subnet auxquels MWAA est connecté
aws ecs create-service --cluster fargate-cluster --service-name dsp-training-service --task-definition dsp-training:1 --desired-count 1 --launch-type "FARGATE" \
--network-configuration "awsvpcConfiguration={subnets=[subnet-017f112634880ea29, subnet-059a5a00080493341],securityGroups=[sg-0821fa185cc2517ff],assignPublicIp=ENABLED}"
