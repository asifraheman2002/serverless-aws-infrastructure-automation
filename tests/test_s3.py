import boto3


# Create an S3 client
s3 = boto3.client("s3")

# Project S3 buckets
FRONTEND_BUCKET = "serverless-employee-frontend-dev"
CLOUDTRAIL_BUCKET = "serverless-cloudtrail-audit-dev"


def test_frontend_bucket_exists():
    # Check that the frontend bucket is accessible
    response = s3.head_bucket(
        Bucket=FRONTEND_BUCKET
    )

    # Successful head_bucket returns HTTP 200
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_cloudtrail_bucket_exists():
    # Check that the CloudTrail audit bucket is accessible
    response = s3.head_bucket(
        Bucket=CLOUDTRAIL_BUCKET
    )

    # Successful head_bucket returns HTTP 200
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_frontend_objects_exist():
    # List objects uploaded to the frontend bucket
    response = s3.list_objects_v2(
        Bucket=FRONTEND_BUCKET
    )

    # Extract object keys
    object_keys = [
        obj["Key"]
        for obj in response.get("Contents", [])
    ]

    # Confirm the Terraform-managed frontend files exist
    assert "index.html" in object_keys
    assert "style.css" in object_keys
    assert "script.js" in object_keys

# --------------------------------------------
# Run only the S3 tests with detailed output
# python -m pytest tests/test_s3.py -v