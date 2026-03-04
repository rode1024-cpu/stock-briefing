@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo 🚀 GitHub Actions 즉시 실행 도구 (간편 버전)
echo ==========================================
echo.

:: 1. 기존 리모트 주소에서 정보 추출
for /f "tokens=*" %%i in ('git remote get-url origin 2^>nul') do (
    set "raw_url=%%i"
)

if "!raw_url!"=="" (
    echo [!] 깃허브 주소를 찾을 수 없습니다. 
    echo 먼저 github_upload.bat을 실행해서 업로드를 완료해 주세요.
    pause
    exit /b
)

:: URL에서 아이디/저장소명 추출 (https://github.com/userid/repo.git -> userid/repo)
set "temp_url=!raw_url:https://github.com/=!"
set "full_name=!temp_url:.git=!"

echo 연결된 저장소: !full_name!
echo.
set /p choice="지금 즉시 깃허브에서 브리핑을 발송할까요? (Y/N): "

if /i "!choice!"=="Y" (
    echo.
    echo 깃허브 서버로 명령을 전달하는 중...
    gh workflow run daily_briefing.yml --repo !full_name!
    
    if !errorlevel! equ 0 (
        echo.
        echo ✅ 명령 전송 성공!
        echo 약 1~2분 뒤에 메일함을 확인해 보세요. 😊
    ) else (
        echo.
        echo [!] 오류가 발생했습니다.
        echo 1. GitHub CLI가 설치되어 있는지 확인해 주세요.
        echo 2. 또는 웹사이트 Actions 탭에서 직접 [Run workflow]를 눌러주세요.
    )
) else (
    echo 작업을 취소했습니다.
)

echo.
echo ==========================================
pause
