# ==========================================
# Lambda - Get Employees
# ==========================================

data "archive_file" "get_employees" {
  type        = "zip"
  source_file = "${path.module}/../application/backend/getEmployees.py"
  output_path = "${path.module}/getEmployees.zip"
}

resource "aws_lambda_function" "get_employees" {
  function_name = "get-employees"
  role          = aws_iam_role.get_employees_role.arn

  runtime = "python3.12"
  handler = "getEmployees.lambda_handler"

  filename         = data.archive_file.get_employees.output_path
  source_code_hash = data.archive_file.get_employees.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.employee_table.name
    }
  }
}


# ==========================================
# Lambda - Insert Employee
# ==========================================

data "archive_file" "insert_employee" {
  type        = "zip"
  source_file = "${path.module}/../application/backend/insertEmployeeData.py"
  output_path = "${path.module}/insertEmployeeData.zip"
}

resource "aws_lambda_function" "insert_employee" {
  function_name = "insert-employee"
  role          = aws_iam_role.insert_employee_role.arn

  runtime = "python3.12"
  handler = "insertEmployeeData.lambda_handler"

  filename         = data.archive_file.insert_employee.output_path
  source_code_hash = data.archive_file.insert_employee.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.employee_table.name
    }
  }
}