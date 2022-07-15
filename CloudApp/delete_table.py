import boto3
from set_env import AWS_CREDS, AWS_VARS


client = boto3.client('dynamodb', region_name='us-east-1', **AWS_CREDS)

try:
    resp = client.delete_table(
        TableName=AWS_VARS["table_name"],
    )
    print("Table deleted successfully!")

except Exception as e:
    print("Error deleting table:")
    print(e)
