# ==========================================
# IAM Role - Get Employees Lambda
# ==========================================

resource "aws_iam_role" "get_employees_role" {
  name = "get-employees-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}


# ==========================================
# IAM Role - Insert Employee Lambda
# ==========================================

resource "aws_iam_role" "insert_employee_role" {
  name = "insert-employee-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}


# ==========================================
# Get Employees - DynamoDB Read Policy
# ==========================================

resource "aws_iam_role_policy" "get_employees_dynamodb" {
  name = "get-employees-dynamodb"
  role = aws_iam_role.get_employees_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "dynamodb:Scan",
          "dynamodb:GetItem"
        ]

        Resource = aws_dynamodb_table.employee_table.arn
      }
    ]
  })
}


# ==========================================
# Insert Employee - DynamoDB Write Policy
# ==========================================

resource "aws_iam_role_policy" "insert_employee_dynamodb" {
  name = "insert-employee-dynamodb"
  role = aws_iam_role.insert_employee_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "dynamodb:PutItem"
        ]

        Resource = aws_dynamodb_table.employee_table.arn
      }
    ]
  })
}


# ==========================================
# Get Employees - CloudWatch Logs Policy
# ==========================================

resource "aws_iam_role_policy" "get_employees_logs" {
  name = "get-employees-cloudwatch"
  role = aws_iam_role.get_employees_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]

        Resource = "*"
      }
    ]
  })
}


# ==========================================
# Insert Employee - CloudWatch Logs Policy
# ==========================================

resource "aws_iam_role_policy" "insert_employee_logs" {
  name = "insert-employee-cloudwatch"
  role = aws_iam_role.insert_employee_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]

        Resource = "*"
      }
    ]
  })
}