# Move into the Terraform directory
Set-Location "$PSScriptRoot\..\terraform"

# Show the resources Terraform currently manages
terraform state list

# Stop if Terraform state cannot be read
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unable to read Terraform state."
    exit 1
}

# Ask for explicit confirmation before destruction
$confirmation = Read-Host "Type DESTROY to continue"

if ($confirmation -ne "DESTROY") {
    Write-Host "Destruction cancelled."
    exit 0
}

# Preview resources that Terraform plans to destroy
terraform plan -destroy

# Stop if the destroy plan fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform destroy plan failed."
    exit 1
}

# Ask for a second confirmation
$finalConfirmation = Read-Host "Type DESTROY again to permanently delete the planned resources"

if ($finalConfirmation -ne "DESTROY") {
    Write-Host "Destruction cancelled."
    exit 0
}

# Destroy the Terraform-managed infrastructure
terraform destroy -auto-approve

# Stop if destruction fails
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform destruction failed."
    exit 1
}

# Confirm successful destruction
Write-Host "Terraform infrastructure destroyed successfully."