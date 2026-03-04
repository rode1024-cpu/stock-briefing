@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo 🚀 GitHub 업로드 도구 (간편 버전)
echo ==========================================
echo.

:: 1. 기존 리모트 주소 확인
for /f "tokens=*" %%i in ('git remote get-url origin 2^>nul') do (
    set "repo_url=%%i"
)

if "!repo_url!"=="" (
    echo [!] 등록된 깃허브 주소가 없습니다.
    set /p repo_url="내 깃허브 저장소 주소를 입력하세요: "
    git init
    git remote add origin !repo_url!
) else (
    echo 현재 연결된 주소: !repo_url!
    set /p choice="이 주소로 코드를 올리시겠습니까? (Y/N): "
    if /i "!choice!" neq "Y" (
        echo 작업을 취소합니다.
        pause
        exit /b
    )
)

echo.
echo [1/4] 사용자 정보 설정...
git config user.email "user@example.com"
git config user.name "StockBriefingUser"

echo [2/4] 파일 준비 중...
git add .

echo [3/4] 기록 남기는 중 (Commit)...
git commit -m "Update: %date% %time%" >nul 2>&1

echo [4/4] 깃허브로 전송 중...
git branch -M main
git push -u origin main --force

echo.
echo ==========================================
echo ✅ 업로드가 완료되었습니다!
echo ==========================================
pause
