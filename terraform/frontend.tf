# ==========================================
# Enable static website hosting for the frontend bucket
# ==========================================

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }
}
# ==========================================
# Allow public users to read frontend objects
# ==========================================

resource "aws_s3_bucket_policy" "frontend_public_read" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid       = "PublicReadFrontend"
        Effect    = "Allow"
        Principal = "*"

        Action = [
          "s3:GetObject"
        ]

        Resource = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}

# ==========================================
# Upload the frontend HTML file automatically
# ==========================================

resource "aws_s3_object" "frontend_index" {
  bucket       = aws_s3_bucket.frontend.id
  key          = "index.html"
  source       = "${path.module}/../application/frontend/index.html"
  content_type = "text/html"
}

# ==========================================
# Upload the frontend CSS file automatically
# ==========================================

resource "aws_s3_object" "frontend_style" {
  bucket       = aws_s3_bucket.frontend.id
  key          = "style.css"
  source       = "${path.module}/../application/frontend/style.css"
  content_type = "text/css"
}

# ==========================================
# Generate and upload JavaScript with the current API endpoint
# ==========================================

resource "aws_s3_object" "frontend_script" {
  bucket = aws_s3_bucket.frontend.id
  key    = "script.js"

  content = templatefile(
    "${path.module}/../application/frontend/script.js.tftpl",
    {
      api_endpoint = "${aws_apigatewayv2_api.employee_api.api_endpoint}/employees"
    }
  )

  content_type = "application/javascript"

  depends_on = [
    aws_apigatewayv2_api.employee_api
  ]
}