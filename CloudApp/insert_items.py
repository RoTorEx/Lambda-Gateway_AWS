import boto3
from set_env import AWS_CREDS


dynamodb = boto3.resource('dynamodb', region_name='us-east-1', **AWS_CREDS)
table = dynamodb.Table('Customers')

with table.batch_writer() as batch:
    batch.put_item(Item={"CustomerID": 1,
                         "Gender": "Male",
                         "Age": 22,
                         "Income": 100,
                         "Score": 88})
