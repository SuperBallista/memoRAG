# Contributing to memoRAG

memoRAG에 기여해주셔서 감사합니다! 🎉

## 기여 방법

### 버그 리포트

버그를 발견하셨나요?

1. [Issues](../../issues)에서 중복 확인
2. 새 이슈 생성
3. 다음 정보 포함:
   - 버그 설명
   - 재현 방법
   - 예상 동작 vs 실제 동작
   - 환경 정보 (OS, Python 버전 등)

### 기능 제안

새로운 기능을 제안하고 싶으신가요?

1. [Issues](../../issues)에서 제안
2. 왜 필요한지 설명
3. 사용 사례 제시
4. 토론 후 구현 검토

### Pull Request

코드를 기여하고 싶으신가요?

1. **Fork & Clone**
   ```bash
   git clone https://github.com/your-username/memorag.git
   cd memorag
   ```

2. **개발 환경 설정**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **브랜치 생성**
   ```bash
   git checkout -b feature/my-feature
   # 또는
   git checkout -b fix/bug-description
   ```

4. **코드 작성**
   - 코드 스타일: Black 포맷터 사용
   - 타입 힌트 사용
   - Docstring 작성

5. **테스트**
   ```bash
   # 테스트 실행
   pytest tests/
   
   # 린터 확인
   flake8 src/
   
   # 포맷터 적용
   black src/
   ```

6. **커밋**
   ```bash
   git add .
   git commit -m "feat: 새로운 기능 추가"
   ```

7. **Push & PR**
   ```bash
   git push origin feature/my-feature
   ```
   
   GitHub에서 Pull Request 생성

## 코드 스타일

### Python 스타일 가이드

- **포맷터**: Black (기본 설정)
- **최대 줄 길이**: 100자
- **Import 순서**: 표준 라이브러리 → 외부 패키지 → 로컬 모듈
- **타입 힌트**: 가능한 모든 곳에 사용

### 예시

```python
"""모듈 설명"""
from pathlib import Path
from typing import List, Optional
import logging

from ..core import DocumentParser

logger = logging.getLogger(__name__)


class MyService:
    """서비스 설명"""
    
    def __init__(self, parser: DocumentParser):
        """
        Args:
            parser: 문서 파서
        """
        self.parser = parser
    
    def process(self, file_path: Path) -> List[str]:
        """
        파일 처리
        
        Args:
            file_path: 파일 경로
            
        Returns:
            처리 결과 리스트
            
        Raises:
            ValueError: 잘못된 파일
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")
        
        return self.parser.parse(file_path)
```

## 커밋 메시지 규칙

### 형식

```
<type>: <subject>

<body> (선택)

<footer> (선택)
```

### Type 종류

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 등

### 예시

```
feat: PPTX 파일 파싱 기능 추가

python-pptx 라이브러리를 사용하여 PowerPoint 파일의
슬라이드별 텍스트를 추출합니다.

Closes #15
```

## 프로젝트 구조

새 기능을 추가할 때 적절한 위치:

```
src/
├── core/              # 핵심 엔진 (파서, 임베딩, 검색)
├── services/          # 비즈니스 로직
├── cli/               # CLI 인터페이스
└── utils/             # 유틸리티 (설정, 로깅)
```

## 테스트 작성

### 테스트 파일 위치

```
tests/
├── test_parser.py         # 파서 테스트
├── test_embedder.py       # 임베딩 테스트
├── test_vector_search.py  # 검색 테스트
└── test_services.py       # 서비스 테스트
```

### 테스트 예시

```python
import pytest
from pathlib import Path
from src.core.parser import DocumentParser

def test_pdf_parsing():
    """PDF 파싱 테스트"""
    parser = DocumentParser()
    chunks = parser.parse(Path("test_docs/sample.pdf"))
    
    assert len(chunks) > 0
    assert all(chunk.text for chunk in chunks)
    assert all(chunk.metadata for chunk in chunks)
```

## 문서 작성

### 개발자 문서

새 기능을 추가하면 다음 문서 업데이트:

- `docs/dev/아키텍처.md` - 구조 변경 시
- `docs/dev/API문서.md` - 새 API 추가 시
- `README.md` - 주요 기능 변경 시

### 사용자 문서

사용자 관련 변경 시:

- `docs/user/사용자_가이드.txt` - 사용법 변경
- `docs/user/명령어_치트시트.txt` - 새 명령어

## 개발 환경

### 권장 설정

**IDE**: VSCode, PyCharm
**Python**: 3.9 이상
**가상환경**: venv 또는 conda

### VSCode 설정 (.vscode/settings.json)

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": false,
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

## 릴리스 프로세스

### 버전 번호

Semantic Versioning 사용: `MAJOR.MINOR.PATCH`

- `MAJOR`: 호환성 깨지는 변경
- `MINOR`: 새 기능 추가
- `PATCH`: 버그 수정

### 릴리스 체크리스트

- [ ] 버전 번호 업데이트 (`src/__init__.py`)
- [ ] CHANGELOG 작성
- [ ] 모든 테스트 통과
- [ ] 문서 업데이트
- [ ] exe 빌드 테스트
- [ ] Git 태그 생성
- [ ] GitHub Release 생성

## 질문이 있으신가요?

- [Discussions](../../discussions)에서 질문
- [Issues](../../issues)에 문의
- 이메일: [연락처]

## 행동 강령

- 서로 존중하기
- 건설적인 피드백
- 초보자 환영
- 다양성 존중

---

**모든 기여자분들께 감사드립니다!** ❤️

