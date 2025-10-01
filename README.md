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

상세 아키텍처는 [docs/dev/아키텍처.md](docs/dev/아키텍처.md) 참고

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

자세한 내용은 [배포 가이드](docs/dev/배포_가이드.md) 참고

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

### 프로젝트 구조

```
memoRAG/
├── src/                 # 소스 코드
│   ├── core/           # 핵심 엔진 (파서, 임베딩, 검색)
│   ├── services/       # 비즈니스 로직
│   ├── cli/            # CLI 인터페이스
│   └── utils/          # 유틸리티
├── tests/              # 테스트
├── docs/               # 문서
│   ├── dev/           # 개발자 문서
│   └── user/          # 사용자 문서
├── dist/               # 빌드 결과
│   └── memorag.exe    # 실행 파일
└── requirements.txt
```

### 개발 시작

```bash
# 저장소 클론
git clone https://github.com/SuperBallista/memoRAG.git
cd memoRAG

# 가상환경 설정
python -m venv venv
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 실행
python run.py --help
```

### 테스트

```bash
# 유닛 테스트
pytest tests/

# 통합 테스트
python test_simple.py
```

### 배포 (exe 빌드)

```bash
# 빌드
python build_exe.py

# 결과
dist/memorag.exe
```

자세한 개발 가이드는 [docs/dev/개발_가이드.md](docs/dev/개발_가이드.md) 참고

## 🗺️ 로드맵

- ✅ **v0.1.0** (완료): CLI 기본 기능, 7가지 파일 형식, exe 배포
- 🔥 **v0.2.0** (최우선): **GUI + 모던 UX/UI 디자인**
- 🌐 **v0.3.0** (높음): **클라우드 연동** (Notion, Google Drive, OneNote)
- 🤖 **v0.4.0** (중기): LLM 요약 답변
- 🌍 **v0.5.0+** (장기): WebUI, 고급 기능

자세한 로드맵: [향후 확장 계획](docs/dev/향후_확장_계획.md)

## 📚 문서

### 👤 사용자용
- [빠른 시작 (5분)](docs/user/빠른_시작_가이드.txt)
- [사용자 가이드](docs/user/사용자_가이드.txt)
- [부서 공유 방법](docs/user/부서_공유_가이드.txt)
- [명령어 치트시트](docs/user/명령어_치트시트.txt)

### 💻 개발자용
- [아키텍처](docs/dev/아키텍처.md)
- [개발 가이드](docs/dev/개발_가이드.md)
- [API 문서](docs/dev/API문서.md)
- [배포 가이드](docs/dev/배포_가이드.md)

### 🤝 기여
- [CONTRIBUTING.md](CONTRIBUTING.md) - 기여 방법
- [CHANGELOG.md](CHANGELOG.md) - 변경 이력

## 🌟 특별한 기능

### 인덱스 파일 공유
원본 문서 없이 **인덱스 파일만 공유**하면 팀원들이 검색 가능!
- 메신저로 간편하게 전달
- 직관적인 보안 (파일 삭제 = 데이터 삭제)
- 버전 관리 용이

## 📄 라이선스

Apache-2.0

## 🙏 기여

버그 리포트, 기능 제안, Pull Request 모두 환영합니다!

- [Issues](https://github.com/SuperBallista/memoRAG/issues) - 버그/제안
- [Pull Requests](https://github.com/SuperBallista/memoRAG/pulls) - 코드 기여
- [CONTRIBUTING.md](CONTRIBUTING.md) - 기여 가이드

---

**Made for Everyone - 교사, 직장인, 연구자 모두를 위해** 🌟

_memoRAG - 메모처럼 저장하고, AI처럼 검색하세요_

