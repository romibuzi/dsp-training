aws cloudformation create-stack --stack-name mwaa-environment-public-network --template-body file://mwaa_public_network.yml --capabilities CAPABILITY_IAM

# get bucket name
aws s3 ls
# replace bucket name with yours
aws s3 cp src s3://mwaa-environment-public-network-environmentbucket-vkj4st8qwchi/dags/ --recursive
aws s3 cp requirements.txt s3://mwaa-environment-public-network-environmentbucket-vkj4st8qwchi/dags/

# Get worker permissions
aws mwaa get-environment --name mwaa-environment-public-network-MwaaEnvironment --region=eu-west-1 | jq -r '.Environment | .ExecutionRoleArn'
# ==> arn:aws:iam::733964877523:role/service-role/mwaa-environment-public-network-MwaaExecutionRole-1HTAL2ZV5TZH4
aws iam list-attached-role-policies --role-name mwaa-environment-public-network-MwaaExecutionRole-1HTAL2ZV5TZH4
