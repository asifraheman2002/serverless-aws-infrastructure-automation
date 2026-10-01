# Move into the Terraform directory
Set-Location "$PSScriptRoot\..\terraform"

# Format Terraform files
terraform fmt -check

# Validate Terraform configuration
terraform validate

# Stop if validation fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform validation failed."
    exit 1
}

# Confirm successful validation
Write-Host "Terraform validation passed."