# Simple Export Script
Write-Host "=== Exporting Data ===" -ForegroundColor Cyan

# Login
$loginBody = '{"username":"adminuser","password":"admin123"}'
$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access
Write-Host "Logged in successfully" -ForegroundColor Green

# Create exports folder
$exportFolder = "D:\Matrimonial_Site\exports"
if (-not (Test-Path $exportFolder)) {
    New-Item -ItemType Directory -Path $exportFolder | Out-Null
}

# Export PDF
Write-Host "Exporting PDF..." -ForegroundColor Yellow
$headers = @{ Authorization = "Bearer $token" }
$pdfBody = '{"file_type":"pdf","export_type":"profiles"}'
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$pdfFile = "$exportFolder\profiles_$timestamp.pdf"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/export-logs/export-data/" -Method POST -Headers $headers -Body $pdfBody -ContentType "application/json" -OutFile $pdfFile
Write-Host "PDF saved: $pdfFile" -ForegroundColor Green

# Export Excel
Write-Host "Exporting Excel..." -ForegroundColor Yellow
$excelBody = '{"file_type":"excel","export_type":"profiles"}'
$excelFile = "$exportFolder\profiles_$timestamp.xlsx"
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/export-logs/export-data/" -Method POST -Headers $headers -Body $excelBody -ContentType "application/json" -OutFile $excelFile
Write-Host "Excel saved: $excelFile" -ForegroundColor Green

# Open folder
Write-Host "`nOpening exports folder..." -ForegroundColor Yellow
Start-Process explorer.exe $exportFolder
Write-Host "Done!" -ForegroundColor Green
