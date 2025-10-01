@echo off
REM memoRAG CPU 버전 설치 스크립트

echo ========================================
echo memoRAG CPU 버전 설치
echo ========================================
echo.

echo [1단계] 가상환경 생성
python -m venv venv
echo.

echo [2단계] 가상환경 활성화
call .\venv\Scripts\activate.bat
echo.

echo [3단계] pip 업그레이드
python -m pip install --upgrade pip
echo.

echo [4단계] PyTorch CPU 버전 설치
echo (GPU 미사용, 크기 절약)
pip install torch --index-url https://download.pytorch.org/whl/cpu
echo.

echo [5단계] 나머지 패키지 설치
pip install sentence-transformers chromadb pypdf python-docx lxml python-pptx openpyxl
pip install click pyyaml rich tqdm
pip install pytest black flake8
pip install pyinstaller
echo.

echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo 다음 명령어로 테스트:
echo   python run.py version
echo   python test_simple.py
echo.

pause

