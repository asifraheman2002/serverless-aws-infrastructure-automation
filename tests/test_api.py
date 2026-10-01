import boto3


# Create an API Gateway V2 client
apig_client = boto3.client("apigatewayv2")

# Project API Gateway name
API_NAME = "employee-api"


def get_employee_api():
    # Retrieve the project's HTTP API
    response = apig_client.get_apis()

    # Find the API by its configured name
    for api in response["Items"]:
        if api["Name"] == API_NAME:
            return api

    # Fail if the expected API was not found
    raise AssertionError(f"API '{API_NAME}' was not found")


def test_api_exists():
    # Retrieve the project API
    api = get_employee_api()

    # Confirm the API name
    assert api["Name"] == API_NAME


def test_api_protocol():
    # Retrieve the project API
    api = get_employee_api()

    # Confirm that the API is HTTP
    assert api["ProtocolType"] == "HTTP"


def test_api_routes():
    # Retrieve the project API
    api = get_employee_api()

    # Get the API routes
    response = apig_client.get_routes(
        ApiId=api["ApiId"]
    )

    # Extract route keys
    route_keys = [
        route["RouteKey"]
        for route in response["Items"]
    ]

    # Confirm both application routes exist
    assert "GET /employees" in route_keys
    assert "POST /employees" in route_keys

    # Run only the API Gateway tests with detailed output
# python -m pytest tests/test_api.py -v