# Configuration
param (
    [Parameter(Mandatory = $true, HelpMessage = "Enter the version name")]
    [string]$Version,

    [switch]$latest
)

$TARGET_DIR = "built-docs" # Build directory
$REMOTE_URL = (git remote get-url origin) # Automatically grabs repo URL

# Clean up old files
Write-Host "Cleaning old directory..." -ForegroundColor Cyan
if (Test-Path -Path $TARGET_DIR) {
    Remove-Item -Path $TARGET_DIR -Recurse -Force
}

# Clone current gh-pages into target directory.
Write-Host "Fetching existing gh-pages branch from remote..." -ForegroundColor Cyan
git clone $REMOTE_URL --branch gh-pages --single-branch $TARGET_DIR

# If the gh-pages branch doesn't exist yet on remote, initialize a blank folder.
if (-not $?) {
    Write-Host "Remote 'gh-pages' branch not found. Creating a fresh '$TARGET_DIR' folder..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $TARGET_DIR -Force | Out-Null
} else {
    # Remove the cloned .git metadata so ghp-import treats it as a standard static directory
    if (Test-Path -Path "$TARGET_DIR\.git") {
        Remove-Item -Path "$TARGET_DIR\.git" -Recurse -Force
    }
}

# Copy changelog into docs folder.
Copy-Item -Path ".\CHANGELOG.md" -Destination ".\docs\changelog.md"

# Zensical build.
Write-Host "Building version '$Version' using Zensical..." -ForegroundColor Cyan
zensical build --clean
$DestinationPath = "$TARGET_DIR/$Version"
Copy-Item -Path "site/*" -Destination $DestinationPath -Recurse -Force
if ($latest) {
    Copy-Item -Path "site/*" -Destination "$TARGET_DIR/latest" -Recurse -Force
}
Remove-Item -Path "site" -Recurse -Force # Clean up old build folder

# Remove changelog copy from docs folder and copy the changelog folder generated for the deploy into the root site.
Remove-Item -Path ".\docs\changelog.md"
Remove-Item -Path "$TARGET_DIR/changelog" -Recurse
Write-Host "Moving changelog to $TARGET_DIR/changelog..." -ForegroundColor Cyan
if (-not (Test-Path -Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force
}
Move-Item -Path "$DestinationPath/changelog" -Destination $TARGET_DIR -Force

# For the changelog file, replace all url references of the version to latest.
$CHANGELOG_FILE = "$TARGET_DIR/changelog/index.html"
(Get-Content -Path $CHANGELOG_FILE) -replace 'href="../', "../latest/" | Set-Content -Path $CHANGELOG_FILE

# Remove deploy script from build
Remove-Item -Path "$DestinationPath/deploy.ps1"

# Make root redirect.
Write-Host "Setting root index.html redirect to /$Version/..." -ForegroundColor Gray
$RedirectHtml = "<meta http-equiv='refresh' content='0; url=./$Version/'>"
Set-Content -Path "$TARGET_DIR\index.html" -Value $RedirectHtml

# Copy docs-versions.json into the built site as versions.json
Copy-Item -Path ".\docs-versions.json" -Destination "$TARGET_DIR/versions.json" -Force

# Push to gh-pages branch.
Write-Host "Pushing and forcing update to gh-pages..." -ForegroundColor Green
ghp-import "-n" "-p" "-f" "-s" $TARGET_DIR

# Display success message.
Write-Host "Deployment of version '$Version' completed successfully!" -ForegroundColor Green
Write-Host "The documentation should be up at https://shaurya-sharma-dev.github.io/pygame-topdownengine/ soon." -ForegroundColor Cyan
Write-Host "Visit https://github.com/shaurya-sharma-dev/pygame-topdownengine/actions/workflows/pages/pages-build-deployment for GitHub pages deployment runs." -ForegroundColor Cyan