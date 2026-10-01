resource "aws_dynamodb_table" "employee_table" {
  name         = "employee-data-dev"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "employeeId"

  attribute {
    name = "employeeId"
    type = "S"
  }
}