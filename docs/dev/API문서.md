# memoRAG API 문서

Python 코드에서 memoRAG를 라이브러리로 사용하는 방법입니다.

## 설치

```bash
pip install -e .
```

---

## 빠른 시작

```python
from pathlib import Path
from src.core import DocumentParser, EmbeddingEngine, VectorSearch
from src.services import IndexingService, QueryService

# 1. 컴포넌트 초기화
parser = DocumentParser(chunk_size=512, chunk_overlap=50)
embedder = EmbeddingEngine(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu"
)
vector_db = VectorSearch(
    persist_directory="./my_chroma",
    collection_name="my_docs"
)

# 2. 인덱싱
indexing_service = IndexingService(parser, embedder, vector_db)
stats = indexing_service.index_folder(
    folder_path=Path("./documents"),
    show_progress=True
)
print(f"인덱싱 완료: {stats['total_chunks']}개 청크")

# 3. 검색
query_service = QueryService(embedder, vector_db, top_k=5)
results = query_service.search("찾고싶은 내용")

for result in results:
    print(f"{result.metadata['file_name']}: {result.score:.3f}")
    print(result.snippet)
```

---

## Core API

### DocumentParser

문서 파싱 클래스

#### 초기화

```python
parser = DocumentParser(
    chunk_size=512,        # 청크 크기 (문자 수)
    chunk_overlap=50       # 청크 중복 (문자 수)
)
```

#### 메서드

**parse(file_path: Path) -> List[DocumentChunk]**

파일을 파싱하여 청크 리스트 반환

```python
from pathlib import Path

chunks = parser.parse(Path("document.pdf"))

for chunk in chunks:
    print(chunk.text)           # 텍스트 내용
    print(chunk.metadata)       # 메타데이터
    print(chunk.page)           # 페이지 번호
```

**is_supported(file_path: Path) -> bool**

지원 형식 확인

```python
if DocumentParser.is_supported(Path("file.pdf")):
    chunks = parser.parse(Path("file.pdf"))
```

#### DocumentChunk

```python
@dataclass
class DocumentChunk:
    text: str                    # 텍스트 내용
    metadata: Dict[str, any]     # 메타데이터
    page: Optional[int]          # 페이지/슬라이드 번호
    section: Optional[str]       # 섹션/시트 이름
```

---

### EmbeddingEngine

임베딩 엔진 클래스

#### 초기화

```python
embedder = EmbeddingEngine(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu",           # or "cuda"
    batch_size=32
)
```

#### 메서드

**embed_documents(texts: List[str]) -> List[List[float]]**

문서 텍스트를 벡터로 변환

```python
texts = ["문서 1", "문서 2", "문서 3"]
embeddings = embedder.embed_documents(texts)
# [[0.1, 0.2, ...], [0.3, 0.4, ...], ...]
```

**embed_query(text: str) -> List[float]**

쿼리 텍스트를 벡터로 변환

```python
query_vector = embedder.embed_query("검색어")
# [0.1, 0.2, 0.3, ...]
```

**get_dimension() -> int**

임베딩 차원 반환

```python
dim = embedder.get_dimension()  # 384 또는 768
```

---

### VectorSearch

벡터 검색 엔진 클래스

#### 초기화

```python
vector_db = VectorSearch(
    persist_directory="./chroma",
    collection_name="default"
)
```

#### 메서드

**get_or_create_collection(collection_name: str)**

컬렉션 가져오기 또는 생성

```python
collection = vector_db.get_or_create_collection("my_collection")
```

**add_documents(ids, embeddings, documents, metadatas)**

문서 추가

```python
vector_db.add_documents(
    ids=["doc1", "doc2"],
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    documents=["텍스트 1", "텍스트 2"],
    metadatas=[{"file": "a.txt"}, {"file": "b.txt"}]
)
```

**search(query_embedding, top_k, where) -> Dict**

벡터 검색

```python
results = vector_db.search(
    query_embedding=[0.1, 0.2, ...],
    top_k=5,
    where={"file_type": "pdf"}  # 필터 (선택)
)
```

**delete_collection(collection_name: str)**

컬렉션 삭제

```python
vector_db.delete_collection("old_collection")
```

**list_collections() -> List[str]**

모든 컬렉션 이름 반환

```python
collections = vector_db.list_collections()
# ["collection1", "collection2", ...]
```

---

## Services API

### IndexingService

인덱싱 서비스

#### 초기화

```python
from src.services import IndexingService

indexing_service = IndexingService(parser, embedder, vector_db)
```

#### 메서드

**index_folder(folder_path, collection_name, recursive, show_progress) -> dict**

폴더 인덱싱

```python
stats = indexing_service.index_folder(
    folder_path=Path("./documents"),
    collection_name="my_docs",
    recursive=True,
    show_progress=True
)

print(stats)
# {
#     "total_files": 10,
#     "total_chunks": 50,
#     "errors": 0,
#     "error_files": []
# }
```

**index_file(file_path, collection_name) -> int**

단일 파일 인덱싱

```python
count = indexing_service.index_file(
    file_path=Path("document.pdf"),
    collection_name="my_docs"
)
print(f"{count}개 청크 생성")
```

---

### QueryService

쿼리 서비스

#### 초기화

```python
from src.services import QueryService

query_service = QueryService(
    embedder=embedder,
    vector_db=vector_db,
    top_k=5,
    snippet_length=200
)
```

#### 메서드

**search(query, collection_name, top_k, filters) -> List[QueryResult]**

자연어 검색

```python
results = query_service.search(
    query="체육대회 준비물",
    collection_name="my_docs",
    top_k=5,
    filters={"file_type": "pdf"}  # 선택
)

for result in results:
    print(f"파일: {result.metadata['file_name']}")
    print(f"점수: {result.score}")
    print(f"내용: {result.snippet}")
```

**format_results(results, show_score, show_snippet) -> str**

결과 포맷팅

```python
formatted = query_service.format_results(
    results=results,
    show_score=True,
    show_snippet=True
)
print(formatted)
```

#### QueryResult

```python
class QueryResult:
    text: str               # 원본 텍스트
    metadata: Dict          # 메타데이터
    score: float            # 유사도 점수 (0~1)
    snippet: str            # 짧은 미리보기
```

---

### ManagementService

관리 서비스

#### 초기화

```python
from src.services import ManagementService

management_service = ManagementService(vector_db)
```

#### 메서드

**list_collections() -> List[str]**

컬렉션 목록

```python
collections = management_service.list_collections()
```

**get_collection_info(collection_name) -> Dict**

컬렉션 정보

```python
info = management_service.get_collection_info("my_docs")
print(info['document_count'])
```

**delete_collection(collection_name) -> bool**

컬렉션 삭제

```python
success = management_service.delete_collection("old_docs")
```

**get_storage_size() -> int**

저장소 크기 (바이트)

```python
size = management_service.get_storage_size()
size_str = management_service.format_storage_size(size)
print(f"크기: {size_str}")
```

---

## Utils API

### Config

설정 관리

```python
from src.utils import Config

# 설정 로드
config = Config(Path("config.yaml"))

# 값 가져오기
model = config.get("embedding.model_name")
top_k = config.get("search.top_k", default=5)

# 값 설정
config.set("search.top_k", 10)

# 저장
config.save(Path("config.yaml"))
```

### Logger

로깅 설정

```python
from src.utils import setup_logger

logger = setup_logger(
    name="my_app",
    level="INFO",
    log_file=Path("./logs/app.log"),
    use_rich=True
)

logger.info("정보 메시지")
logger.error("오류 메시지")
```

---

## 고급 사용 예시

### 예시 1: 커스텀 파이프라인

```python
from pathlib import Path
from src.core import DocumentParser, EmbeddingEngine, VectorSearch

def custom_pipeline(folder: Path, query: str):
    """커스텀 검색 파이프라인"""
    
    # 초기화
    parser = DocumentParser()
    embedder = EmbeddingEngine()
    vector_db = VectorSearch()
    
    # 파일 파싱
    all_chunks = []
    for file_path in folder.glob("*.pdf"):
        chunks = parser.parse(file_path)
        all_chunks.extend(chunks)
    
    # 임베딩 & 저장
    texts = [c.text for c in all_chunks]
    embeddings = embedder.embed_documents(texts)
    
    vector_db.add_documents(
        ids=[f"chunk_{i}" for i in range(len(texts))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[c.metadata for c in all_chunks]
    )
    
    # 검색
    query_vector = embedder.embed_query(query)
    results = vector_db.search(query_vector, top_k=3)
    
    return results
```

### 예시 2: 배치 인덱싱

```python
def batch_index_multiple_folders(folders: List[Path]):
    """여러 폴더를 배치 인덱싱"""
    
    # 공통 컴포넌트
    parser = DocumentParser()
    embedder = EmbeddingEngine()
    
    for folder in folders:
        # 폴더별로 별도 컬렉션 생성
        collection_name = folder.name
        vector_db = VectorSearch(collection_name=collection_name)
        
        indexing_service = IndexingService(parser, embedder, vector_db)
        stats = indexing_service.index_folder(folder)
        
        print(f"{collection_name}: {stats['total_chunks']}개 청크")
```

### 예시 3: 통합 검색 (여러 컬렉션)

```python
def search_all_collections(query: str) -> List[QueryResult]:
    """모든 컬렉션에서 검색"""
    
    embedder = EmbeddingEngine()
    vector_db = VectorSearch()
    
    all_results = []
    
    for collection in vector_db.list_collections():
        query_service = QueryService(embedder, vector_db, top_k=3)
        results = query_service.search(query, collection_name=collection)
        all_results.extend(results)
    
    # 점수순 정렬
    all_results.sort(key=lambda r: r.score, reverse=True)
    
    return all_results[:10]  # 상위 10개
```

---

## 타입 힌트

모든 API는 타입 힌트를 제공합니다:

```python
from typing import List, Dict, Optional
from pathlib import Path

def my_function(
    file_path: Path,
    options: Optional[Dict] = None
) -> List[str]:
    """타입이 명확한 함수"""
    pass
```

---

## 에러 처리

### 일반적인 예외

```python
from src.core import DocumentParser

try:
    chunks = parser.parse(Path("file.pdf"))
except FileNotFoundError:
    print("파일이 없습니다")
except ValueError as e:
    print(f"지원하지 않는 형식: {e}")
except ImportError as e:
    print(f"라이브러리 필요: {e}")
```

### 권장 패턴

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = process_document(file_path)
except Exception as e:
    logger.error(f"처리 실패: {e}")
    raise  # 또는 적절히 처리
```

---

## 성능 최적화

### 배치 처리

```python
# 나쁜 예: 하나씩 처리
for text in texts:
    embedding = embedder.embed_documents([text])

# 좋은 예: 배치 처리
embeddings = embedder.embed_documents(texts)
```

### 재사용

```python
# 나쁜 예: 매번 새로 생성
for query in queries:
    embedder = EmbeddingEngine()  # 느림!
    result = embedder.embed_query(query)

# 좋은 예: 한 번만 생성
embedder = EmbeddingEngine()
for query in queries:
    result = embedder.embed_query(query)
```

---

## 참고

더 많은 예시는 다음 파일 참고:

- `src/cli/main.py` - CLI 구현 예시
- `test_simple.py` - 통합 테스트 예시
- `tests/test_*.py` - 유닛 테스트 예시

---

**Happy Coding!** 🚀

