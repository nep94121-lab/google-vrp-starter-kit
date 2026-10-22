# ==============================================================================
# SCRIPT TỰ ĐỘNG CÀI ĐẶT TÀI NGUYÊN & CÔNG CỤ SĂN BUG GOOGLE VRP (WINDOWS)
# Cách chạy: Mở PowerShell tại thư mục gốc GOOGLE_VRP_STARTER_KIT và chạy:
#   powershell -ExecutionPolicy Bypass -File .\01_SETUP_AND_INSTALL\install_tools.ps1
# ==============================================================================

Write-Host "=== [1/5] Kiểm tra và cài đặt Git & GitHub CLI (gh) ===" -ForegroundColor Cyan
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Đang cài đặt Git qua winget..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
} else {
    git --version
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Đang cài đặt GitHub CLI (gh) qua winget..." -ForegroundColor Yellow
    winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements
} else {
    gh --version
}

Write-Host "`n=== [2/5] Kiểm tra Python 3.10+ ===" -ForegroundColor Cyan
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Đang cài đặt Python 3.12 qua winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.12 -e --source winget --accept-package-agreements --accept-source-agreements
} else {
    python --version
}

Write-Host "`n=== [3/5] Cài đặt các thư viện Python & Máy quét tĩnh (zizmor, requests, pyyaml) ===" -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install requests pyyaml zizmor

Write-Host "`n=== [4/5] Kiểm tra đăng nhập GitHub CLI (gh auth status) ===" -ForegroundColor Cyan
gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Bạn chưa đăng nhập GitHub CLI! Hãy chạy lệnh: gh auth login" -ForegroundColor Yellow
}

Write-Host "`n=== [5/5] Chạy kiểm thử tự động toàn bộ môi trường (check_environment.py) ===" -ForegroundColor Cyan
python "$PSScriptRoot\check_environment.py"
