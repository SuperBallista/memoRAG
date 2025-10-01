#!/usr/bin/env python
"""개발용 실행 스크립트"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# CLI 실행
from src.cli.main import main

if __name__ == '__main__':
    main()

