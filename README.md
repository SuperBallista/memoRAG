# memoRAG - 개인/팀 문서 검색 시스템

> 업무 문서, 공문, 회의록, 기획서 등을 **자연어 질의로 빠르게 검색**하는 RAG 기반 시스템  
> 교사, 직장인, 연구자 누구나 사용 가능!

## 🎯 주요 특징

- 📁 **다양한 문서 포맷 지원**: PDF, DOCX, HWPX(한글), PPTX, XLSX, TXT, MD
- 🔍 **자연어 검색**: "체육대회 준비물은 뭐였지?" 같은 문장으로 검색
- 💾 **로컬 처리**: 모든 데이터는 내 PC에서만 처리 (보안)
- 📤 **인덱스 파일 공유**: 부서 인덱스를 메신저로 간편하게 공유
- 🚀 **단일 실행 파일**: Python 설치 없이 exe로 바로 실행

## 🏗️ 시스템 구조

```
사용자 → CLI → [검색엔진 + 임베딩] → ChromaDB → 검색 결과
```

상세 아키텍처는 [docs/아키텍처.md](docs/아키텍처.md) 참고

## 📦 설치

### 방법 1: 실행 파일 다운로드 (일반 사용자 권장 ⭐)

**Python 설치 불필요!**

1. [Release 페이지](https://github.com/user/memorag/releases)에서 `memorag.exe` 다운로드
2. 원하는 폴더에 저장
3. 바로 실행!

```bash
# 샘플로 테스트
memorag.exe index --folder 샘플문서
memorag.exe query "검색어"
```

**참고**: 첫 실행 시 임베딩 모델 자동 다운로드 (~420MB, 인터넷 필요)

**최적화**: CPU 전용 + 경량 모델로 빠르고 효율적!

### 방법 2: Python 환경 설정 (개발자용)

```bash
# Python 3.9 이상 필요
python --version

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 방법 3: 직접 빌드 (개발자용)

```bash
# 의존성 설치 후
python build_exe.py

# 또는
build.bat

# 결과: dist/memorag.exe
```

자세한 내용은 [배포 가이드](docs/배포_가이드.md) 참고

## 🚀 사용법

### 개인 모드 (기본)

```bash
# 1. 내 문서 폴더 인덱싱
python src/cli/main.py index --folder ./내문서

# 2. 검색
python src/cli/main.py query "체육대회 준비물"

# 3. 인덱스 삭제
python src/cli/main.py clean
```

### 부서 모드 (인덱스 파일 공유)

#### 담당자 (인덱스 생성)
```bash
# 부서 문서 폴더를 특정 이름으로 인덱싱
python src/cli/main.py index --folder ./5학년_문서 --output 5학년부_2025_09

# 생성된 파일(5학년부_2025_09.db)을 팀원에게 공유
# → 카카오톡 워크, 슬랙 등으로 전송
```

#### 팀원 (인덱스 사용)
```bash
# 받은 인덱스 파일을 ./chroma/ 폴더에 저장

# 검색
python src/cli/main.py query "수련활동 일정" --index 5학년부_2025_09

# 여러 인덱스 동시 검색
python src/cli/main.py query "학부모 안내문" --index 5학년부_2025_09,교무부_공지

# 인덱스 목록 확인
python src/cli/main.py list

# 업무 종료 후 삭제
python src/cli/main.py clean --index 5학년부_2025_09
```

## 📋 주요 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `index` | 문서 폴더 인덱싱 | `--folder ./문서 --output 인덱스명` |
| `query` | 자연어 검색 | `"검색어" --index 인덱스명` |
| `list` | 인덱스 목록 조회 | |
| `clean` | 인덱스 삭제 | `--index 인덱스명` (전체 삭제 시 생략) |

## 🔐 보안

- ✅ **로컬 처리**: 모든 데이터는 로컬 PC에서만 처리, 외부 업로드 없음
- ✅ **직관적 삭제**: 인덱스 파일 삭제 = 모든 데이터 제거
- ⚠️ **주의사항**: 인덱스 파일에 원본 텍스트가 포함되므로, 민감한 문서는 별도 관리

## 🛠️ 개발

### 프로젝트 구조 (예정)

```
jobqa/
├── src/
│   ├── core/           # 핵심 엔진 (임베딩, 파서, 검색)
│   ├── services/       # 비즈니스 로직
│   ├── cli/            # CLI 인터페이스
│   └── utils/          # 유틸리티
├── tests/              # 테스트
├── docs/               # 문서
└── requirements.txt
```

### 테스트 실행

```bash
pytest tests/
```

### 배포 (exe 빌드)

```bash
pyinstaller --onefile --name rag_local src/cli/main.py
# → dist/rag_local.exe 생성
```

## 🗺️ 로드맵

- [x] Phase 1: CLI 기본 기능 (현재)
- [ ] Phase 2: Tkinter GUI
- [ ] Phase 3: FastAPI WebUI
- [ ] Phase 4: LLM 연동 (요약, 생성형 답변)

## 📚 문서

- [기획 문서](docs/기획문서.txt)
- [아키텍처 문서](docs/아키텍처.md)

## 📄 라이선스

Apache-2.0

---

**Made for Everyone - 교사, 직장인, 연구자 모두를 위해**

