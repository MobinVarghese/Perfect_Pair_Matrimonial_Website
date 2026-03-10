# Test Feedback Feature
Write-Host "=== Testing Feedback Feature ===" -ForegroundColor Cyan

# Login
$loginBody = '{"username":"adminuser","password":"admin123"}'
$loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token/" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access
Write-Host "Logged in as adminuser" -ForegroundColor Green

$headers = @{ Authorization = "Bearer $token" }

# Submit feedback
Write-Host "`nSubmitting feedback..." -ForegroundColor Yellow
$feedbackBody = @{
    category = "suggestion"
    subject = "Great matrimonial site!"
    message = "I really love this platform. The profile matching is excellent. Keep up the good work!"
} | ConvertTo-Json

try {
    $feedback = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/feedback/" -Method POST -Headers $headers -Body $feedbackBody -ContentType "application/json"
    Write-Host "Feedback submitted successfully!" -ForegroundColor Green
    Write-Host "ID: $($feedback.id)" -ForegroundColor White
    Write-Host "Category: $($feedback.category_display)" -ForegroundColor White
    Write-Host "Subject: $($feedback.subject)" -ForegroundColor White
    Write-Host "Status: $($feedback.status_display)" -ForegroundColor White
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Get user's feedback
Write-Host "`nGetting feedback list..." -ForegroundColor Yellow
try {
    $feedbacks = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/feedback/" -Method GET -Headers $headers
    $count = if ($feedbacks.results) { $feedbacks.results.Count } else { $feedbacks.Count }
    Write-Host "Found $count feedback(s)" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Green
Write-Host "Visit http://localhost:3000/feedback to see the UI" -ForegroundColor Cyan
