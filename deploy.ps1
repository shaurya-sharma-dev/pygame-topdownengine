Write-Host "Starting build + deployment of docs..." -ForegroundColor Cyan
zensical build --clean
ghp-import -n -p -f site