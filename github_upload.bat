@echo off
set /p repo_url="Enter your GitHub Repository URL: "

echo.
echo [1/5] Setting up Git identity...
git config user.email "user@example.com"
git config user.name "StockBriefingUser"

echo.
echo [2/5] Initializing and fixing remote...
git init
git remote remove origin >nul 2>&1
git remote add origin %repo_url%

echo.
echo [3/5] Adding files...
git add .

echo.
echo [4/5] Committing...
git commit -m "Initial commit"

echo.
echo [5/5] Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ==========================================
echo 업로드가 완료되었습니다! 
echo 이제 깃허브 웹페이지를 새로고침해서 확인해 보세요.
echo ==========================================
pause
