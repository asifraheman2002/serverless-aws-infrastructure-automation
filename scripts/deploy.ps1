# Move into the Terraform directory
Set-Location "$PSScriptRoot\..\terraform"

# Format Terraform files
terraform fmt

# Validate Terraform configuration
terraform validate

# Stop if validation fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform validation failed."
    exit 1
}

# Preview infrastructure changes
terraform plan

# Stop if the plan fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform plan failed."
    exit 1
}

# Ask for confirmation before changing AWS
$confirmation = Read-Host "Continue with Terraform apply? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "Deployment cancelled."
    exit 0
}

# Apply the Terraform configuration
terraform apply -auto-approve

# Stop if deployment fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform deployment failed."
    exit 1
}

# Confirm successful deployment
Write-Host "Terraform deployment completed successfully."