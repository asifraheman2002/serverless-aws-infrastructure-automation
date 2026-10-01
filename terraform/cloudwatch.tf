# ==========================================
# CloudWatch Log Group - Get Employees
# ==========================================

resource "aws_cloudwatch_log_group" "get_employees" {
  name              = "/aws/lambda/${aws_lambda_function.get_employees.function_name}"
  retention_in_days = 7
}


# ==========================================
# CloudWatch Log Group - Insert Employee
# ==========================================

resource "aws_cloudwatch_log_group" "insert_employee" {
  name              = "/aws/lambda/${aws_lambda_function.insert_employee.function_name}"
  retention_in_days = 7
}