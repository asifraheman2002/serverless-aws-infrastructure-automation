# ==========================================
# HTTP API
# ==========================================

resource "aws_apigatewayv2_api" "employee_api" {
  name          = "employee-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}


# ==========================================
# GET /employees → getEmployees Lambda
# ==========================================

resource "aws_apigatewayv2_integration" "get_employees" {
  api_id = aws_apigatewayv2_api.employee_api.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_employees.invoke_arn
  integration_method = "POST"

  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "get_employees" {
  api_id = aws_apigatewayv2_api.employee_api.id

  route_key = "GET /employees"
  target    = "integrations/${aws_apigatewayv2_integration.get_employees.id}"
}


# ==========================================
# POST /employees → insertEmployee Lambda
# ==========================================

resource "aws_apigatewayv2_integration" "insert_employee" {
  api_id = aws_apigatewayv2_api.employee_api.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.insert_employee.invoke_arn
  integration_method = "POST"

  payload_format_version = "2.0"
}


resource "aws_apigatewayv2_route" "insert_employee" {
  api_id = aws_apigatewayv2_api.employee_api.id

  route_key = "POST /employees"
  target    = "integrations/${aws_apigatewayv2_integration.insert_employee.id}"
}


# ==========================================
# API Stage
# ==========================================

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.employee_api.id

  name = "$default"

  auto_deploy = true
}


# ==========================================
# Allow API Gateway to invoke GET Lambda
# ==========================================

resource "aws_lambda_permission" "api_get_employees" {
  statement_id  = "AllowAPIGatewayInvokeGet"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_employees.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.employee_api.execution_arn}/*/*"
}


# ==========================================
# Allow API Gateway to invoke INSERT Lambda
# ==========================================

resource "aws_lambda_permission" "api_insert_employee" {
  statement_id  = "AllowAPIGatewayInvokeInsert"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.insert_employee.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.employee_api.execution_arn}/*/*"
}