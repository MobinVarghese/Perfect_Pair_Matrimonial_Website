# Export Data Script - Generate PDF and Excel files
# This script exports user data and saves files to the exports folder

Write-Host "=== Matrimonial Site Data Export Tool ===" -ForegroundColor Cyan
Write-Host ""

# Configuration
$baseUrl = "http://127.0.0.1:8000/api"
$username = "adminuser"
$password = "admin123"
$exportFolder = "D:\Matrimonial_Site\exports"

# Create exports folder if it doesn't exist
if (-not (Test-Path $exportFolder)) {
    New-Item -ItemType Directory -Path $exportFolder | Out-Null
    Write-Host "Created exports folder: $exportFolder" -ForegroundColor Green
}

# Step 1: Login and get token
Write-Host "Step 1: Logging in as admin..." -ForegroundColor Yellow
$loginBody = @{
    username = $username
    password = $password
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/token/" -Method POST -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.access
    Write-Host "✓ Login successful!" -ForegroundColor Green
} catch {
    Write-Host "✗ Login failed: $_" -ForegroundColor Red
    exit 1
}

# Headers with authentication
$headers = @{
    Authorization = "Bearer $token"
}

# Step 2: Export to PDF
Write-Host ""
Write-Host "Step 2: Exporting profiles to PDF..." -ForegroundColor Yellow
$pdfBody = @{
    file_type = "pdf"
    export_type = "profiles"
} | ConvertTo-Json

try {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $pdfFileName = "profiles_$timestamp.pdf"
    $pdfPath = Join-Path $exportFolder $pdfFileName
    
    Invoke-WebRequest -Uri "$baseUrl/export-logs/export-data/" `
        -Method POST `
        -Headers $headers `
        -Body $pdfBody `
        -ContentType "application/json" `
        -OutFile $pdfPath
    
    Write-Host "✓ PDF exported successfully!" -ForegroundColor Green
    Write-Host "  Location: $pdfPath" -ForegroundColor Cyan
    
    # Get file size
    $pdfSize = (Get-Item $pdfPath).Length / 1KB
    Write-Host "  Size: $([math]::Round($pdfSize, 2)) KB" -ForegroundColor Gray
} catch {
    Write-Host "✗ PDF export failed: $_" -ForegroundColor Red
}

# Step 3: Export to Excel
Write-Host ""
Write-Host "Step 3: Exporting profiles to Excel..." -ForegroundColor Yellow
$excelBody = @{
    file_type = "excel"
    export_type = "profiles"
} | ConvertTo-Json

try {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $excelFileName = "profiles_$timestamp.xlsx"
    $excelPath = Join-Path $exportFolder $excelFileName
    
    Invoke-WebRequest -Uri "$baseUrl/export-logs/export-data/" `
        -Method POST `
        -Headers $headers `
        -Body $excelBody `
        -ContentType "application/json" `
        -OutFile $excelPath
    
    Write-Host "✓ Excel exported successfully!" -ForegroundColor Green
    Write-Host "  Location: $excelPath" -ForegroundColor Cyan
    
    # Get file size
    $excelSize = (Get-Item $excelPath).Length / 1KB
    Write-Host "  Size: $([math]::Round($excelSize, 2)) KB" -ForegroundColor Gray
} catch {
    Write-Host "✗ Excel export failed: $_" -ForegroundColor Red
}

# Step 4: List all exported files
Write-Host ""
Write-Host "Step 4: Listing all exports in folder..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $exportFolder -File | Sort-Object LastWriteTime -Descending
if ($files.Count -eq 0) {
    Write-Host "  No files found in exports folder" -ForegroundColor Gray
} else {
    foreach ($file in $files) {
        $fileSize = [math]::Round($file.Length / 1KB, 2)
        $fileName = $file.Name
        $fileTime = $file.LastWriteTime
        Write-Host "  - $fileName (${fileSize} KB) - $fileTime" -ForegroundColor White
    }
}

# Step 5: Open exports folder
Write-Host ""
Write-Host "Opening exports folder..." -ForegroundColor Yellow
Start-Process explorer.exe $exportFolder

Write-Host ""
Write-Host "=== Export Complete ===" -ForegroundColor Green
Write-Host "All files saved to: $exportFolder" -ForegroundColor Cyan
