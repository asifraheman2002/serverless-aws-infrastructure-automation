# ==========================================
# Frontend S3 Bucket
# ==========================================

resource "aws_s3_bucket" "frontend" {
  bucket = "serverless-employee-frontend-dev"
}

# ==========================================
# Block Public Access
# ==========================================

# resource "aws_s3_bucket_public_access_block" "frontend" {
# bucket = aws_s3_bucket.frontend.id

# block_public_acls       = false
# block_public_policy     = false
# ignore_public_acls      = false
# restrict_public_buckets = false
#}

# ==========================================
# Allow Public Access
# ==========================================

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# ==========================================
# S3 Ownership Controls
# ==========================================

resource "aws_s3_bucket_ownership_controls" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}