import boto3
from set_env import AWS_CREDS, AWS_VARS


dynamodb = boto3.resource('dynamodb', region_name='us-east-1', **AWS_CREDS)
table = dynamodb.Table(AWS_VARS["table_name"])

resp = table.get_item(Key={"CustomerID": 1, "Gender": "Male"})

print(resp['Item'])
