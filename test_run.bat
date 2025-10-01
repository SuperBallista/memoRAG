@echo off
REM memoRAG 테스트 스크립트

echo ========================================
echo memoRAG 테스트 시작
echo ========================================
echo.

echo [1단계] CLI 도움말 확인
call .\venv\Scripts\activate.bat
python run.py --help
echo.

echo [2단계] 버전 확인
python run.py version
echo.

echo [3단계] 문서 인덱싱
python run.py index --folder test_documents
echo.

echo [4단계] 인덱스 목록 확인
python run.py list
echo.

echo [5단계] 검색 테스트 1 - 체육대회 준비물
python run.py query "체육대회 준비물"
echo.

echo [6단계] 검색 테스트 2 - 수련활동 일정
python run.py query "수련활동 일정"
echo.

echo [7단계] 검색 테스트 3 - 학부모 공개수업
python run.py query "학부모 공개수업 언제"
echo.

echo ========================================
echo 테스트 완료!
echo ========================================

