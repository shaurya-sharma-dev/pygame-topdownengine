# Configuration
param (
    [Parameter(Mandatory = $true, HelpMessage = "Enter the version name")]
    [string]$Version
)

$TARGET_DIR = "built-docs" # Build directory
$REMOTE_URL = (git remote get-url origin) # Automatically grabs repo URL

python "$PSScriptRoot\check_latest.py" "$Version" > $null
$latest = ($LASTEXITCODE -eq 0)

if ($latest){
    Write-Host "Auto-detected that this is the latest version." -ForegroundColor Cyan
} else {
    Write-Host "Auto-detected that this is NOT the latest version." -ForegroundColor Cyan
}

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
    If ((Test-Path "$TARGET_DIR/latest")) { 
        Remove-Item -Path "$TARGET_DIR/latest" -Recurse -Force # Wipe latest folder
        New-Item -Path "$TARGET_DIR/latest" -ItemType Directory | Out-Null
    }
    Copy-Item -Path "site/*" -Destination "$TARGET_DIR/latest" -Recurse -Force
}
Remove-Item -Path "site" -Recurse -Force # Clean up old build folder

# Remove changelog copy from docs folder and copy the changelog folder generated for the deploy into the root site.
Remove-Item -Path ".\docs\changelog.md"
Remove-Item -Path "$TARGET_DIR/changelog" -Recurse
if ($latest) {
    Remove-Item -Path "$TARGET_DIR/latest/changelog" -Recurse
}
Write-Host "Moving changelog to $TARGET_DIR/changelog..." -ForegroundColor Cyan
if (-not (Test-Path -Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force
}
Move-Item -Path "$DestinationPath/changelog" -Destination $TARGET_DIR -Force

# For the changelog file, replace all url references of the version to latest.
$CHANGELOG_FILE = "$TARGET_DIR/changelog/index.html"
(Get-Content -Path $CHANGELOG_FILE) -replace 'href="../', 'href="../latest/' | Set-Content -Path $CHANGELOG_FILE

# Remove scripts from build
Remove-Item -Path "$DestinationPath/deploy.ps1"
Remove-Item -Path "$DestinationPath/build.ps1"
Remove-Item -Path "$DestinationPath/check_latest.py"

if ($latest) {
    Remove-Item -Path "$TARGET_DIR/latest/deploy.ps1"
    Remove-Item -Path "$TARGET_DIR/latest/build.ps1"
    Remove-Item -Path "$TARGET_DIR/latest/check_latest.py"
}

# Make root redirect.
Write-Host "Setting root index.html redirect to /latest/..." -ForegroundColor Gray
$RedirectHtml = "<meta http-equiv='refresh' content='0; url=./latest/'>"
Set-Content -Path "$TARGET_DIR\index.html" -Value $RedirectHtml

# Make 404 page
Write-Host "Creating 404 page..." -ForegroundColor Gray
Copy-Item -Path "$TARGET_DIR\latest\404.html" -Destination "$TARGET_DIR\404.html"
(Get-Content -Path "$TARGET_DIR\404.html") -replace '/pygame-topdownengine/assets', '/pygame-topdownengine/latest/assets' | Set-Content -Path "$TARGET_DIR\404.html"

# Copy docs-versions.json into the built site as versions.json
Copy-Item -Path ".\docs-versions.json" -Destination "$TARGET_DIR/versions.json" -Force