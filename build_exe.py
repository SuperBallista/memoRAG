#!/usr/bin/env python
"""PyInstaller를 사용하여 memoRAG를 단일 exe 파일로 빌드"""
import PyInstaller.__main__
import sys
from pathlib import Path

def build_exe():
    """exe 파일 빌드"""
    
    # 프로젝트 루트
    project_root = Path(__file__).parent
    
    # PyInstaller 옵션
    options = [
        'run.py',                                    # 진입점
        '--name=memorag',                            # 실행 파일 이름
        '--onefile',                                 # 단일 파일로 생성
        '--clean',                                   # 빌드 전 캐시 정리
        '--noconfirm',                               # 확인 없이 덮어쓰기
        
        # 콘솔 표시 (CLI 앱이므로)
        '--console',
        
        # 아이콘 (있으면)
        # '--icon=icon.ico',
        
        # 데이터 파일 포함
        '--add-data=config.yaml.example;.',          # 설정 예시 파일
        
        # 임베딩 모델 캐시 경로 (상대 경로로)
        '--hidden-import=sentence_transformers',
        '--hidden-import=torch',
        '--hidden-import=transformers',
        '--hidden-import=chromadb',
        '--hidden-import=pptx',
        '--hidden-import=openpyxl',
        
        # 제외할 모듈 (크기 줄이기)
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=numpy.distutils',
        
        # 빌드 디렉토리
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ]
    
    print("="*60)
    print("memoRAG 빌드 시작")
    print("="*60)
    print(f"프로젝트 루트: {project_root}")
    print(f"출력 경로: dist/memorag.exe")
    print()
    
    try:
        PyInstaller.__main__.run(options)
        
        print()
        print("="*60)
        print("빌드 완료!")
        print("="*60)
        print(f"실행 파일: {project_root / 'dist' / 'memorag.exe'}")
        print()
        print("사용법:")
        print("  dist\\memorag.exe --help")
        print("  dist\\memorag.exe version")
        print("  dist\\memorag.exe index --folder 문서폴더")
        print("  dist\\memorag.exe query \"검색어\"")
        print()
        
    except Exception as e:
        print(f"\n빌드 실패: {e}")
        sys.exit(1)


if __name__ == '__main__':
    build_exe()

