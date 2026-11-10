@echo off
echo ========================================================
echo Pushing Hospital Management System to GitHub (harshtn)
echo ========================================================
git branch -M main
git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo SUCCESS! Repository uploaded to GitHub:
    echo https://github.com/harshtn/Hospital-Management-System
    echo ========================================================
) else (
    echo.
    echo [NOTE] If you received a "Repository not found" error:
    echo 1. Go to https://github.com/new
    echo 2. Repository name: Hospital-Management-System
    echo 3. Keep it Public or Private (do NOT check Initialize with README)
    echo 4. Click 'Create repository'
    echo 5. Run this script again!
)
pause
