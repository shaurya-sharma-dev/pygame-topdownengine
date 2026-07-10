# Configuration
param (
    [Parameter(Mandatory = $true, HelpMessage = "Enter the version name")]
    [string]$Version,
    [Parameter(Mandatory = $true, HelpMessage = "Enter the finished build path")]
    [string]$TARGET_DIR
)

$REMOTE_URL = (git remote get-url origin) # Automatically grabs repo URL

python "$PSScriptRoot\check_latest.py" "$Version" > $null
$latest = ($LASTEXITCODE -eq 0)

if ($latest) {
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
Remove-Item -Path "site" -Recurse -Force # Clean up old build folder

# Remove changelog copy from docs folder and move the built changelog folder to the site root.
Remove-Item -Path ".\docs\changelog.md"
Remove-Item -Path "$TARGET_DIR/changelog" -Recurse -ErrorAction SilentlyContinue
Write-Host "Moving changelog to $TARGET_DIR/changelog..." -ForegroundColor Cyan
if (-not (Test-Path -Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}
Move-Item -Path "$DestinationPath/changelog" -Destination $TARGET_DIR -Force

# Patch the changelog index.html
Write-Host "Patching changelog index.html..." -ForegroundColor Gray
$ChangelogFile = "$TARGET_DIR/changelog/index.html"
$ChangelogScriptInjectionMarker = '<title>Changelog - pygame-topdownengine Documentation</title>'
$ChangelogXhrRerouteScript = @'
<script>
    (function() {
        const originalOpen = window.XMLHttpRequest.prototype.open;
        const routeTable = {
            "/search.json": "/search-changelog.json",
            "/versions.json": "/pygame-topdownengine/versions-404.json"
        };

        window.XMLHttpRequest.prototype.open = function(method, url, ...args) {
            let finalUrl = url;
            for (const originalPath in routeTable) {
                if (url.includes(originalPath)) {
                    finalUrl = url.replaceAll(originalPath, routeTable[originalPath]);
                    console.log(`[Rerouted]: ${url} -> ${finalUrl}`);
                    break;
                }
            }
            return originalOpen.apply(this, [method, finalUrl, ...args]);
        };
    })();
</script>
'@
(Get-Content -Path $ChangelogFile) -replace '<a href="/pygame-topdownengine/latest/..', '<a href="/pygame-topdownengine' | Set-Content -Path $ChangelogFile
(Get-Content -Path $ChangelogFile) -replace '<a href="/pygame-topdownengine(?!/latest)', "<a href=`"/pygame-topdownengine/$Version" | Set-Content -Path $ChangelogFile
(Get-Content -Path $ChangelogFile) -replace 'href="../', "href=`"../$Version/" | Set-Content -Path $ChangelogFile
(Get-Content -Path $ChangelogFile) -replace $ChangelogScriptInjectionMarker, "$ChangelogScriptInjectionMarker $ChangelogXhrRerouteScript" | Set-Content -Path $ChangelogFile

# Remove build/deploy scripts and version metadata from the versioned output.
Remove-Item -Path "$DestinationPath/deploy.ps1"
Remove-Item -Path "$DestinationPath/build.ps1"
Remove-Item -Path "$DestinationPath/check_latest.py"
Remove-Item -Path "$DestinationPath/build_static_assets.py"
Remove-Item -Path "$DestinationPath/versions.json"

# Make root index.html redirect to /latest/.
Write-Host "Setting root index.html redirect to /latest/..." -ForegroundColor Gray
$RootRedirectHtml = "<meta http-equiv='refresh' content='0; url=./latest/'>"
Set-Content -Path "$TARGET_DIR\index.html" -Value $RootRedirectHtml

# Update /latest/ redirect to point to this version (only when deploying latest).
if ($latest) {
    Remove-Item -Path "$TARGET_DIR\latest\*" -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -Path "$TARGET_DIR\latest\index.html" -ItemType File -Force | Out-Null
    $LatestRedirectHtml = "<meta http-equiv='refresh' content='0; url=/pygame-topdownengine/$Version/'>"
    Set-Content -Path "$TARGET_DIR\latest\index.html" -Value $LatestRedirectHtml
}

# Patch the versioned 404.html.
Write-Host "Creating 404 page..." -ForegroundColor Gray
$NotFoundScriptInjectionMarker = '<title>pygame-topdownengine Documentation</title>'
$NotFoundXhrRerouteScript = @'
<script>
    (function() {
        const originalOpen = window.XMLHttpRequest.prototype.open;
        const routeTable = {
            "/search.json": "/pygame-topdownengine/search-404.json",
            "/versions.json": "/pygame-topdownengine/versions-404.json"
        };

        window.XMLHttpRequest.prototype.open = function(method, url, ...args) {
            let finalUrl = url;
            for (const originalPath in routeTable) {
                if (url.includes(originalPath)) {
                    finalUrl = url.replaceAll(originalPath, routeTable[originalPath]);
                    console.log(`[Rerouted]: ${url} -> ${finalUrl}`);
                    break;
                }
            }
            return originalOpen.apply(this, [method, finalUrl, ...args]);
        };
    })();
</script>
'@
$NotFoundRedirectHtml = "<meta http-equiv='refresh' content='0; url=/pygame-topdownengine/$Version/404.html'>"
Set-Content -Path "$TARGET_DIR\404.html" -Value $NotFoundRedirectHtml

(Get-Content -Path "$TARGET_DIR\$Version\404.html") -replace '<a href="/pygame-topdownengine/latest/..', '<a href="/pygame-topdownengine' | Set-Content -Path "$TARGET_DIR\$Version\404.html"
(Get-Content -Path "$TARGET_DIR\$Version\404.html") -replace '<a href="/pygame-topdownengine(?!/latest)', "<a href=`"/pygame-topdownengine/$Version" | Set-Content -Path "$TARGET_DIR\$Version\404.html"
(Get-Content -Path "$TARGET_DIR\$Version\404.html") -replace $NotFoundScriptInjectionMarker, "$NotFoundScriptInjectionMarker $NotFoundXhrRerouteScript" | Set-Content -Path "$TARGET_DIR\$Version\404.html"

# Patch search.json for this version and (if latest) build root search-404.json and versions-404.json.
python "$PSScriptRoot\build_static_assets.py" "$TARGET_DIR" "$Version" "$latest"

# Copy assets folder to site root so the 404 and changelog pages can reference them.
Copy-Item -Path "$TARGET_DIR\$Version\assets" -Destination "$TARGET_DIR\assets" -Recurse -Force

# Copy versions.json into the built site root.
Copy-Item -Path ".\docs\versions.json" -Destination "$TARGET_DIR/versions.json" -Force