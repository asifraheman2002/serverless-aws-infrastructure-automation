import boto3
from botocore.exceptions import ClientError


# ============================================================
# 1. Lambda
# ============================================================

def inspect_lambda():
    # Create a Lambda client
    lambda_client = boto3.client("lambda")

    # List all Lambda functions
    lambda_response = lambda_client.list_functions()

    # Print selected Lambda configuration
    print("\n========== LAMBDA ==========")

    for function in lambda_response["Functions"]:
        print(f"Function: {function['FunctionName']}")
        print(f"Runtime: {function['Runtime']}")
        print(f"Memory: {function['MemorySize']} MB")
        print(f"Timeout: {function['Timeout']} seconds")
        print(f"Log Group: {function['LoggingConfig']['LogGroup']}")
        print("-" * 50)


# ============================================================
# 2. DynamoDB
# ============================================================

def inspect_dynamodb():
    # Create a DynamoDB client
    dynamodb_client = boto3.client("dynamodb")

    table_name = "employee-data-dev"

    # --------------------------------------------------------
    # List Tables
    # --------------------------------------------------------

    # List DynamoDB tables
    table_response = dynamodb_client.list_tables()

    # Print table names
    print("\n========== DYNAMODB TABLES ==========")

    for table_name_item in table_response["TableNames"]:
        print(f"- {table_name_item}")

    # --------------------------------------------------------
    # Describe Table
    # --------------------------------------------------------

    # Get detailed information about the employee table
    table_details = dynamodb_client.describe_table(
        TableName=table_name
    )

    # Extract table information
    table = table_details["Table"]

    # Print selected table information
    print("\n========== DYNAMODB TABLE DETAILS ==========")
    print(f"Table: {table['TableName']}")
    print(f"Status: {table['TableStatus']}")
    print(f"Item Count: {table['ItemCount']}")
    print(f"Table ARN: {table['TableArn']}")
    print("-" * 50)

    # --------------------------------------------------------
    # Scan Data
    # --------------------------------------------------------

    # Retrieve employee records from the table
    scan_response = dynamodb_client.scan(
        TableName=table_name
    )

    # Print employee records
    print("\n========== EMPLOYEE RECORDS ==========")

    for item in scan_response["Items"]:
        print(f"Employee ID: {item['employeeId']['S']}")
        print(f"Name: {item['name']['S']}")
        print(f"Department: {item['department']['S']}")
        print(f"Salary: {item['salary']['S']}")
        print("-" * 50)


# ============================================================
# 3. S3
# ============================================================

def inspect_s3():
    # Create an S3 client
    s3_client = boto3.client("s3")

    # --------------------------------------------------------
    # List Buckets
    # --------------------------------------------------------

    # List all S3 buckets
    bucket_response = s3_client.list_buckets()

    # Print bucket names
    print("\n========== S3 BUCKETS ==========")

    for bucket in bucket_response["Buckets"]:
        print(f"- {bucket['Name']}")

    # --------------------------------------------------------
    # List Objects
    # --------------------------------------------------------

    # Inspect objects inside each S3 bucket
    print("\n========== S3 OBJECTS ==========")

    for bucket in bucket_response["Buckets"]:
        bucket_name = bucket["Name"]

        print(f"\nBucket: {bucket_name}")

        # List objects inside the current bucket
        object_response = s3_client.list_objects_v2(
            Bucket=bucket_name
        )

        if "Contents" in object_response:
            print("Objects:")

            for obj in object_response["Contents"]:
                print(f"  - {obj['Key']}")
        else:
            print("Objects: None")

        print("-" * 50)

    # --------------------------------------------------------
    # Download Object
    # --------------------------------------------------------

    # Download the frontend JavaScript file locally
    s3_client.download_file(
        "serverless-employee-frontend-dev",
        "script.js",
        "automation/reports/script.js"
    )

    print("\nS3 file downloaded successfully.")

    # --------------------------------------------------------
    # Read Object
    # --------------------------------------------------------

    # Retrieve the frontend JavaScript object
    object_response = s3_client.get_object(
        Bucket="serverless-employee-frontend-dev",
        Key="script.js"
    )

    # Read the object content
    content = object_response["Body"].read().decode("utf-8")

    # Display the file content
    print("\n========== S3 OBJECT CONTENT ==========")
    print(content)


# ============================================================
# 4. API Gateway
# ============================================================

def inspect_api_gateway():
    # Create an API Gateway v2 client
    apig_client = boto3.client("apigatewayv2")

    # List HTTP/WebSocket APIs
    api_response = apig_client.get_apis()

    # --------------------------------------------------------
    # APIs
    # --------------------------------------------------------

    print("\n========== API GATEWAY APIS ==========")

    for api in api_response["Items"]:
        print(f"API: {api['Name']}")
        print(f"Protocol: {api['ProtocolType']}")
        print(f"API ID: {api['ApiId']}")
        print(f"Endpoint: {api.get('ApiEndpoint')}")
        print("-" * 50)

    # --------------------------------------------------------
    # Routes
    # --------------------------------------------------------

    print("\n========== API GATEWAY ROUTES ==========")

    for api in api_response["Items"]:
        # List routes for the current API
        route_response = apig_client.get_routes(
            ApiId=api["ApiId"]
        )

        # Print route configuration
        for route in route_response["Items"]:
            print(f"API: {api['Name']}")
            print(f"Route: {route['RouteKey']}")
            print(f"Target: {route.get('Target')}")
            print("-" * 50)

    # --------------------------------------------------------
    # Stages
    # --------------------------------------------------------

    print("\n========== API GATEWAY STAGES ==========")

    for api in api_response["Items"]:
        # List stages for the current API
        stage_response = apig_client.get_stages(
            ApiId=api["ApiId"]
        )

        # Print selected stage configuration
        for stage in stage_response["Items"]:
            print(f"API: {api['Name']}")
            print(f"Stage: {stage['StageName']}")
            print(f"Auto Deploy: {stage.get('AutoDeploy')}")
            print(f"Deployment ID: {stage.get('DeploymentId')}")
            print(
                f"Status: "
                f"{stage.get('LastDeploymentStatusMessage')}"
            )
            print("-" * 50)


# ============================================================
# 5. CloudWatch
# ============================================================

def inspect_cloudwatch():
    # Create a CloudWatch Logs client
    logs_client = boto3.client("logs")

    # --------------------------------------------------------
    # Log Groups
    # --------------------------------------------------------

    # List Lambda log groups
    log_group_response = logs_client.describe_log_groups(
        logGroupNamePrefix="/aws/lambda/"
    )

    # Print selected log group information
    print("\n========== CLOUDWATCH LOG GROUPS ==========")

    for log_group in log_group_response["logGroups"]:
        print(f"Log Group: {log_group['logGroupName']}")
        print(
            f"Retention: "
            f"{log_group.get('retentionInDays', 'Never Expire')}"
        )
        print(
            f"Stored Bytes: "
            f"{log_group.get('storedBytes', 0)}"
        )
        print("-" * 50)

    # --------------------------------------------------------
    # Log Streams
    # --------------------------------------------------------

    log_group_name = "/aws/lambda/get-employees"

    # Get the latest log streams
    stream_response = logs_client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy="LastEventTime",
        descending=True,
        limit=5
    )

    # Print the latest log streams
    print("\n========== LOG STREAMS ==========")

    for stream in stream_response["logStreams"]:
        print(f"Stream: {stream['logStreamName']}")
        print(
            f"Last Event: "
            f"{stream.get('lastEventTimestamp', 'N/A')}"
        )
        print("-" * 50)

    # --------------------------------------------------------
    # Log Events
    # --------------------------------------------------------

    # Use the latest stream when available
    if stream_response["logStreams"]:
        latest_stream = stream_response["logStreams"][0][
            "logStreamName"
        ]

        # Retrieve log events from the latest stream
        events_response = logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=latest_stream,
            limit=20,
            startFromHead=True
        )

        # Print the actual Lambda log messages
        print("\n========== LOG EVENTS ==========")

        for event in events_response["events"]:
            print(event["message"].rstrip())

    else:
        print("\nNo log streams found.")


# ============================================================
# 6. CloudTrail
# ============================================================

def inspect_cloudtrail():
    # Create a CloudTrail client
    cloudtrail_client = boto3.client("cloudtrail")

    # --------------------------------------------------------
    # Trails
    # --------------------------------------------------------

    # List CloudTrail trails
    trail_response = cloudtrail_client.describe_trails(
        includeShadowTrails=False
    )

    # Print selected trail information
    print("\n========== CLOUDTRAIL TRAILS ==========")

    for trail in trail_response["trailList"]:
        print(f"Trail Name: {trail['Name']}")
        print(f"Trail ARN: {trail['TrailARN']}")
        print(
            f"S3 Bucket: "
            f"{trail.get('S3BucketName', 'N/A')}"
        )
        print(
            f"Multi-Region: "
            f"{trail.get('IsMultiRegionTrail', False)}"
        )
        print(
            f"Log Validation: "
            f"{trail.get('LogFileValidationEnabled', False)}"
        )
        print("-" * 50)

    # --------------------------------------------------------
    # CloudTrail Events
    # --------------------------------------------------------

    # Retrieve recent CloudTrail management events
    event_response = cloudtrail_client.lookup_events(
        MaxResults=10
    )

    # Print selected event information
    print("\n========== CLOUDTRAIL EVENTS ==========")

    for event in event_response["Events"]:
        print(
            f"Event: "
            f"{event.get('EventName', 'N/A')}"
        )
        print(
            f"Time: "
            f"{event.get('EventTime', 'N/A')}"
        )
        print(
            f"Username: "
            f"{event.get('Username', 'N/A')}"
        )
        print(
            f"Source: "
            f"{event.get('EventSource', 'N/A')}"
        )
        print("-" * 50)


# ============================================================
# 7. IAM
# ============================================================

def inspect_iam():
    # Create an IAM client
    iam_client = boto3.client("iam")

    # --------------------------------------------------------
    # IAM Roles
    # --------------------------------------------------------

    # List IAM roles
    role_response = iam_client.list_roles()

    # Project Lambda roles
    project_roles = [
        "get-employees-role",
        "insert-employee-role"
    ]

    # Print project-related Lambda roles
    print("\n========== IAM LAMBDA ROLES ==========")

    for role in role_response["Roles"]:
        role_name = role["RoleName"]

        # Filter for roles used by this project
        if role_name in project_roles:
            print(f"Role Name: {role_name}")
            print(f"ARN: {role['Arn']}")
            print(f"Created: {role['CreateDate']}")
            print("-" * 50)

    # --------------------------------------------------------
    # IAM Inline Policies
    # --------------------------------------------------------

    print("\n========== IAM INLINE POLICIES ==========")

    for role_name in project_roles:
        # List policies embedded directly in the role
        policy_response = iam_client.list_role_policies(
            RoleName=role_name
        )

        print(f"\nRole: {role_name}")

        for policy_name in policy_response["PolicyNames"]:
            # Retrieve the actual inline policy document
            policy = iam_client.get_role_policy(
                RoleName=role_name,
                PolicyName=policy_name
            )

            print(f"Policy: {policy_name}")
            print(f"Document: {policy['PolicyDocument']}")
            print("-" * 50)


# ============================================================
# 8. Pagination
# ============================================================

def inspect_lambda_with_pagination():
    # Create a Lambda client
    lambda_client = boto3.client("lambda")

    # Create a paginator for list_functions
    paginator = lambda_client.get_paginator(
        "list_functions"
    )

    # Retrieve all Lambda functions across API pages
    print("\n========== ALL LAMBDA FUNCTIONS ==========")

    for page in paginator.paginate():
        for function in page["Functions"]:
            print(
                f"Function: "
                f"{function['FunctionName']}"
            )


# ============================================================
# 9. Error Handling
# ============================================================

def test_error_handling():
    # Create a DynamoDB client
    dynamodb_client = boto3.client("dynamodb")

    try:
        # Test a DynamoDB operation
        response = dynamodb_client.describe_table(
            TableName="employee-data-dev"
        )

        # Print the table name when successful
        print(
            "\nDynamoDB table:",
            response["Table"]["TableName"]
        )

    except ClientError as error:
        # Extract the AWS error code
        error_code = error.response["Error"]["Code"]

        # Extract the AWS error message
        error_message = error.response["Error"]["Message"]

        print(f"\nAWS Error: {error_code}")
        print(f"Message: {error_message}")
# ============================================================
# Generate_report
# ============================================================
def generate_report():
    # Create a report file
    report_path = "automation/reports/infrastructure_report.txt"

    # Write the report header
    with open(report_path, "w", encoding="utf-8") as report:
        report.write("AWS INFRASTRUCTURE INSPECTION REPORT\n")
        report.write("=" * 50 + "\n")
        report.write("Project: serverless-aws-infrastructure-automation\n")
        report.write("=" * 50 + "\n")

        # Record the inspection sections
        report.write("\nInspected Services:\n")
        report.write("- Lambda\n")
        report.write("- DynamoDB\n")
        report.write("- S3\n")
        report.write("- API Gateway\n")
        report.write("- CloudWatch Logs\n")
        report.write("- CloudTrail\n")
        report.write("- IAM\n")

    # Confirm report creation
    print(f"\nReport generated: {report_path}")

# ============================================================
# Main
# ============================================================

def main():
    # Run all infrastructure inspections
    # inspect_lambda()
    # inspect_dynamodb()
    # inspect_s3()
    # inspect_api_gateway()
    # inspect_cloudwatch()
     inspect_cloudtrail()
    # inspect_iam()

    # Demonstrate Boto3 pagination
    # inspect_lambda_with_pagination()

    # Test AWS-specific error handling
    # test_error_handling()


# ============================================================
# Script Entry Point
# ============================================================

if __name__ == "__main__":
    # Start the infrastructure automation
    main()