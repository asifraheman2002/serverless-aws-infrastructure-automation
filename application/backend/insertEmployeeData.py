import json
import logging
import os
import boto3
from decimal import Decimal

# Configure logging for CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):

    try:
        logger.info("Received event: %s", json.dumps(event))

        # Parse request body from API Gateway
        body = json.loads(event["body"])

        employeeid = body.get("employeeid")
        name = body.get("name")
        department = body.get("department")
        salary = body.get("salary")

        # Validate input
        if not all([employeeid, name, department, salary]):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "All fields are required."
                })
            }

        # Insert into DynamoDB
        table.put_item(
            Item={
                "employeeId": employeeid,
                "name": name,
                "department": department,
                "salary": salary
            }
        )

        logger.info("Employee inserted successfully.")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Employee saved successfully."
            })
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