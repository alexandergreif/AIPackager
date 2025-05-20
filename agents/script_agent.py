def generate_psadt_script(filename: str) -> str:
    return f"""<#
.SYNOPSIS
    AIPackager-generated deployment script for {filename}
#>

Deploy-Application -DeploymentType 'Install'

Write-Host "Installing {filename}..."
# Insert logic here

Exit-Script -ExitCode 0
"""