import os
from pathlib import Path
import configparser

env_path = str(Path(__file__).resolve().parent.parent) + "/.aws/credentials.ini"

creds = configparser.ConfigParser()
creds.read(env_path)

AWS_CREDS = {
    "aws_access_key_id": creds["dynamodb"]["aws_access_key_id"],
    "aws_secret_access_key": creds["dynamodb"]["aws_secret_access_key"]
}
