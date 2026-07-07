Write-Host "Starting build + deployment of docs..." -ForegroundColor Cyan
zensical build --clean
ghp-import -n -p -f site
Write-Host "Deployment finished. The documentation should be up at https://shaurya-sharma-dev.github.io/pygame-topdownengine/ soon." -ForegroundColor Green
Write-Host "Visit https://github.com/shaurya-sharma-dev/pygame-topdownengine/actions/workflows/pages/pages-build-deployment for GitHub pages deployment runs."