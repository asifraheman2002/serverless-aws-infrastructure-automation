import json
import logging
import os
import boto3
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["TABLE_NAME"])


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError


def lambda_handler(event, context):

    try:

        logger.info("Fetching employee records...")

        response = table.scan()

        employees = response.get("Items", [])

        while "LastEvaluatedKey" in response:

            response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )

            employees.extend(response.get("Items", []))

        logger.info("Total employees fetched: %s", len(employees))

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(employees, default=decimal_default)
        }

    except Exception as e:

        logger.error(str(e))

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }