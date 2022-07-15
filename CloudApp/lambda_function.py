import json
import logging

import boto3

from set_env import AWS_CREDS, AWS_VARS
from custom_encoder import CustomEncoder


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = "product-inventory"
dynamodb = boto3.resource("dynamodb", region_name='us-east-1', **AWS_CREDS)
table = dynamodb.Table(dynamodbTableName)

getMethod = "GET"
postMethod = "POST"
putchMethod = "PUTCH"
deleteMethod = "DELETE"

healthPath = "/health"
productPath = "/product"
productsPath = "/products"


def lambda_handler(event, context):
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }

    logger.info(event)
    httpMethod = event["httpMethod"]
    path = event["path"]

    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)


    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event["queryStringParameters"]["productId"])

    elif httpMethod == getMethod and path == productsPath:
        response = getProducts()

    elif httpMethod == postMethod and path == productPath:
        response = saveProduct(json.loads(event["body"]))

    elif httpMethod == putchMethod and path == productPath:
        requestBody = json.loads(event["body"])
        response = modifyProduct(requestBody["productId"], requestBody["updateKey"], requestBody["updateValue"])

    elif httpMethod == deleteMethod and path == productPath:
        requestBody = json.loads(event["body"])
        response = deleteProduct(requestBody["productId"])

    else:
        response = buildResponse(404, "Not Found\n:'(")

    return response


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }
    if body is not None:
        response["body"] = json.dumps(body, cls=CustomEncoder)

    return response


def getProduct(productId):
    # GET - http://.../product
    try:
        response = table.get_item(
            Key={
                "produtId": productId
            }
        )

        if "item" in response:
            return buildResponse(200, response["Item"])
        else:
            return buildResponse(404, {"Message": "ProductId %s not found" % productId})

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")


def getProducts(productId):
    # GET - http://.../products
    try:
        response = table.scan()
        result = response["Items"]

        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])

        body = {
            "products": result
        }

        return buildResponse(200, body)

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")


def saveProduct(requestsBody):
    # POST - http://.../product
    try:
        table.put_item(Item=requestsBody)
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS",
            "Item": requestsBody
        }
        return buildResponse(200, body)

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")


def modifyProduct(productId, updateKey, updateValue):
    # PUTCH - http://.../product
    try:
        response = table.update_item(
            Key={
                "productId": productId
            },
            UpdateExpression="set %s = :value" % updateKey,
            ExpressionAttributeValues={
                ":value": updateValue
            },
            ReturnValues="UPDATED_NEW"
        )

        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdateAttrebutes": response
        }

        return buildResponse(200, body)

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")


def deleteProduct(productId):
    # DELETE - http://.../product
    try:
        respone = table.delete_item(
            Key={
                "productId": productId
            },
            ReturnValues="ALL_OLD"
        )

        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "deletedItem": respone
        }

        return buildResponse(200, body)

    except:
        logger.exception("Do your custom error here. I am just gonna log it out here!")
