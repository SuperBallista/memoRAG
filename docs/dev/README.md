# 개발자 문서

memoRAG 개발에 필요한 모든 문서가 여기 있습니다.

## 📖 문서 목록

### 필수 문서

1. **[개발_가이드.md](개발_가이드.md)** - 개발 환경 설정 및 워크플로우
2. **[아키텍처.md](아키텍처.md)** - 시스템 설계 및 구조
3. **[API문서.md](API문서.md)** - Python API 레퍼런스

### 심화 문서

4. **[배포_가이드.md](배포_가이드.md)** - exe 빌드 및 배포
5. **[모델_선택_가이드.md](모델_선택_가이드.md)** - 임베딩 모델 가이드
6. **[향후_확장_계획.md](향후_확장_계획.md)** - 로드맵 및 계획

---

## 🚀 빠른 시작 (개발자용)

### 1단계: 환경 설정

```bash
# 클론
git clone https://github.com/your-username/memorag.git
cd memorag

# 가상환경
python -m venv venv
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 개발 서버 실행

```bash
# CLI 테스트
python run.py --help
python run.py version

# 샘플로 테스트
python run.py index --folder test_documents
python run.py query "테스트"
```

### 3단계: 테스트

```bash
# 유닛 테스트
pytest tests/

# 통합 테스트
python test_simple.py
```

---

## 📚 읽기 순서

### 신규 기여자

1. `개발_가이드.md` - 환경 설정
2. `아키텍처.md` - 구조 파악
3. `../../CONTRIBUTING.md` - 기여 방법

### 새 기능 개발

1. `아키텍처.md` - 어디에 추가할지 결정
2. `API문서.md` - API 디자인 참고
3. `향후_확장_계획.md` - 로드맵 확인

### 배포 담당

1. `배포_가이드.md` - 빌드 방법
2. `../../최종_배포_체크리스트.txt` - 배포 절차

---

## 🔗 관련 링크

- [프로젝트 README](../../README.md)
- [Contributing Guide](../../CONTRIBUTING.md)
- [Changelog](../../CHANGELOG.md)
- [사용자 문서](../user/)

---

**개발에 참여해주셔서 감사합니다!** 🙏

