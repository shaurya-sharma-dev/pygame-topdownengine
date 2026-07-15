# Configuration
param (
    [Parameter(Mandatory = $true, HelpMessage = "Enter the version name")]
    [string]$Version
)

$TARGET_DIR = "built-docs" # Build directory
& "$PSScriptRoot\build.ps1" -Version $Version -TARGET_DIR $TARGET_DIR

# Push to gh-pages branch.
Write-Host "Pushing and forcing update to gh-pages..." -ForegroundColor Green
ghp-import "-n" "-p" "-f" "-s" $TARGET_DIR

# Display success message.
Write-Host "Deployment of version '$Version' completed successfully!" -ForegroundColor Green
Write-Host "The documentation should be up at https://shaurya-sharma-dev.github.io/pygame-topdownengine/ soon." -ForegroundColor Cyan
Write-Host "Visit https://github.com/shaurya-sharma-dev/pygame-topdownengine/actions/workflows/pages/pages-build-deployment for GitHub pages deployment runs." -ForegroundColor Cyan