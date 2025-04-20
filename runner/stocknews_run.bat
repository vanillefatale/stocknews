@echo off
setlocal

:: 🕒 날짜+시간
set datetime=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set datetime=%datetime: =0%

:: 📁 로그 저장 위치
set LOG_DIR=C:\Users\user\Desktop\inv\stocknews\runner\logs
set LOG_FILE=%LOG_DIR%\log_fetch_%datetime%.txt

:: 📁 로그 폴더가 없으면 생성
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [%DATE% %TIME%] Fetch Start > "%LOG_FILE%"

:: 📍 프로젝트 디렉토리로 이동
cd /d C:\Users\user\Desktop\inv\stocknews

:: 💡 가상환경 활성화
call venv\Scripts\activate

:: ✅ 파이썬 실행
set PYTHONIOENCODING=utf-8
python run.py >> "%LOG_FILE%" 2>&1

echo [%DATE% %TIME%] Fetch Done >> "%LOG_FILE%"

endlocal
exit
