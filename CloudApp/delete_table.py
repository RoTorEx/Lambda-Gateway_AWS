import boto3
from set_env import AWS_CREDS


client = boto3.client('dynamodb', region_name='us-east-1', **AWS_CREDS)

try:
    resp = client.delete_table(
        TableName="Customers",
    )
    print("Table deleted successfully!")

except Exception as e:
    print("Error deleting table:")
    print(e)
