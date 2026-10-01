import boto3


# Create a DynamoDB client
dynamodb = boto3.client("dynamodb")

# Project DynamoDB table name
TABLE_NAME = "employee-data-dev"


def test_dynamodb_table_exists():
    # Verify that the expected table exists
    response = dynamodb.describe_table(
        TableName=TABLE_NAME
    )

    # Confirm AWS returned the expected table
    assert response["Table"]["TableName"] == TABLE_NAME


def test_dynamodb_table_is_active():
    # Get the current table status
    response = dynamodb.describe_table(
        TableName=TABLE_NAME
    )

    # Confirm the table is ready for use
    assert response["Table"]["TableStatus"] == "ACTIVE"


def test_dynamodb_partition_key():
    # Get the table key definition
    response = dynamodb.describe_table(
        TableName=TABLE_NAME
    )

    # Extract the partition key
    key_schema = response["Table"]["KeySchema"]

    # Confirm employeeId is the partition key
    assert {
        "AttributeName": "employeeId",
        "KeyType": "HASH"
    } in key_schema

# --------------------------------------------------
# Type this to test
# ------------------------------------------------------------
# python -m pytest tests/test_dynamodb.py -v