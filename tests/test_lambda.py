import boto3


# Test that the required Lambda functions exist
def test_lambda_functions_exist():
    # Create a Lambda client
    lambda_client = boto3.client("lambda")

    # Get deployed Lambda functions
    response = lambda_client.list_functions()

    # Extract function names
    function_names = [
        function["FunctionName"]
        for function in response["Functions"]
    ]

    # Verify both project Lambda functions exist
    assert "get-employees" in function_names
    assert "insert-employee" in function_names
    
# -------------------------------------------------------
# run this to test
# -------------------------------------------------------
 
    # python -m pytest tests/test_lambda.py -v