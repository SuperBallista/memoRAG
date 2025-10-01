@echo off
REM memoRAG 빌드 스크립트 (Windows)

echo ========================================
echo memoRAG exe 빌드
echo ========================================
echo.

REM 가상환경 활성화
call .\venv\Scripts\activate.bat

REM 빌드 실행
python build_exe.py

echo.
echo ========================================
echo 빌드 완료!
echo ========================================
echo.
echo 실행 파일: dist\memoRAG.exe
echo.
echo 테스트:
echo   dist\memoRAG.exe version
echo   dist\memoRAG.exe --help
echo.

pause

