import boto3
from set_env import AWS_CREDS, AWS_VARS


# Using mall_customers.csv dataset
client = boto3.client('dynamodb', region_name='us-east-1', **AWS_CREDS)

try:
    resp = client.create_table(
        TableName=AWS_VARS["table_name"],
        KeySchema=[
            {
                "AttributeName": "CustomerID",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Gender",
                "KeyType": "RANGE"
            }
        ],

        AttributeDefinitions=[
            {
                "AttributeName": "CustomerID",
                "AttributeType": "N"
            },
            {
                "AttributeName": "Gender",
                "AttributeType": "S"
            }
        ],

        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    print("Table created successfully!")

except Exception as e:
    print("Error creating table:")
    print(e)
