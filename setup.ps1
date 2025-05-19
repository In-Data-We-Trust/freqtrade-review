# PowerShell script to set up Freqtrade environment
# Run this script to prepare your environment and start Freqtrade

Write-Host "Setting up Freqtrade environment..." -ForegroundColor Green

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is installed: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker is not installed or not in PATH. Please install Docker first." -ForegroundColor Red
    Write-Host "  Download Docker from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if docker-compose is installed
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose is installed: $composeVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker Compose is not installed or not in PATH." -ForegroundColor Red
    Write-Host "  Docker Compose should be included with Docker Desktop for Windows." -ForegroundColor Yellow
    exit 1
}

# Pull the Freqtrade image
Write-Host "Pulling latest Freqtrade Docker image..." -ForegroundColor Cyan
docker pull freqtradeorg/freqtrade:stable

# Ask user if they want to configure API keys
$configureAPI = Read-Host "Do you want to configure your exchange API keys now? (y/n)"
if ($configureAPI -eq "y") {
    $apiKey = Read-Host "Enter your exchange API key"
    $apiSecret = Read-Host "Enter your exchange API secret"
    
    # Update the config file with API keys
    $configPath = ".\user_data\config\config.json"
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $config.exchange.key = $apiKey
    $config.exchange.secret = $apiSecret
    $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
    
    Write-Host "API keys have been updated in the configuration file." -ForegroundColor Green
}

# Ask if user wants to enable dry run or live trading
$tradingMode = Read-Host "Do you want to use dry run mode (paper trading)? (y/n)"
if ($tradingMode -eq "n") {
    # Update the config file for live trading
    $configPath = ".\user_data\config\config.json"
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $config.dry_run = $false
    $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
    
    Write-Host "Warning: Live trading enabled! Real funds will be used." -ForegroundColor Red
}
else {
    Write-Host "Dry run mode enabled. No real funds will be used." -ForegroundColor Green
}

# Start Freqtrade with docker-compose
Write-Host "Starting Freqtrade..." -ForegroundColor Cyan
docker-compose up -d

# Display information
Write-Host "`nFreqtrade is now running!" -ForegroundColor Green
Write-Host "Web UI available at: http://localhost:8080" -ForegroundColor Cyan
Write-Host "Username: freqtrader" -ForegroundColor Cyan
Write-Host "Password: SuperSecretPassword" -ForegroundColor Cyan
Write-Host "`nUseful commands:" -ForegroundColor Yellow
Write-Host "  - View logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "  - Stop Freqtrade: docker-compose down" -ForegroundColor Gray
Write-Host "  - Run backtesting: docker-compose run --rm freqtrade backtesting --strategy SimpleProfit" -ForegroundColor Gray
Write-Host "`nCheck the documentation for more details:" -ForegroundColor Yellow
Write-Host "  - Quick Start Guide: .\user_data\docs\QuickStart.md" -ForegroundColor Gray
Write-Host "  - DCA Strategy Guide: .\user_data\docs\DCA_Strategy.md" -ForegroundColor Gray
