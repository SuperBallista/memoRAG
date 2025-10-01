"""쿼리 서비스 - 자연어 질의 처리"""
from typing import List, Dict, Optional
import logging

from ..core import EmbeddingEngine, VectorSearch

logger = logging.getLogger(__name__)


class QueryResult:
    """검색 결과 데이터 클래스"""
    
    def __init__(
        self,
        text: str,
        metadata: Dict,
        score: float,
        snippet: Optional[str] = None
    ):
        self.text = text
        self.metadata = metadata
        self.score = score
        self.snippet = snippet
    
    def __repr__(self) -> str:
        return f"QueryResult(score={self.score:.3f}, file={self.metadata.get('file_name', 'unknown')})"


class QueryService:
    """자연어 질의 처리 서비스"""
    
    def __init__(
        self,
        embedder: EmbeddingEngine,
        vector_db: VectorSearch,
        top_k: int = 5,
        snippet_length: int = 200
    ):
        """
        Args:
            embedder: 임베딩 엔진
            vector_db: 벡터 검색 엔진
            top_k: 반환할 결과 수
            snippet_length: 스니펫 길이 (문자 수)
        """
        self.embedder = embedder
        self.vector_db = vector_db
        self.top_k = top_k
        self.snippet_length = snippet_length
    
    def search(
        self,
        query: str,
        collection_name: Optional[str] = None,
        top_k: Optional[int] = None,
        filters: Optional[Dict] = None
    ) -> List[QueryResult]:
        """
        자연어 쿼리로 검색
        
        Args:
            query: 검색 쿼리 (자연어)
            collection_name: 검색할 컬렉션 이름
            top_k: 반환할 결과 수 (None이면 기본값)
            filters: 메타데이터 필터 (예: {"file_type": "pdf"})
            
        Returns:
            검색 결과 리스트
        """
        if not query.strip():
            logger.warning("Empty query")
            return []
        
        logger.info(f"Searching for: {query}")
        
        # 컬렉션 설정
        if collection_name:
            self.vector_db.get_or_create_collection(collection_name)
        
        # 쿼리 임베딩
        query_embedding = self.embedder.embed_query(query)
        
        # 벡터 검색
        k = top_k or self.top_k
        results = self.vector_db.search(
            query_embedding=query_embedding,
            top_k=k,
            where=filters
        )
        
        # 결과 변환
        query_results = self._parse_results(results)
        
        logger.info(f"Found {len(query_results)} results")
        return query_results
    
    def _parse_results(self, raw_results: Dict) -> List[QueryResult]:
        """
        ChromaDB 결과를 QueryResult로 변환
        
        Args:
            raw_results: ChromaDB 검색 결과
            
        Returns:
            QueryResult 리스트
        """
        results = []
        
        # ChromaDB 결과 구조: {'ids': [[...]], 'documents': [[...]], 'metadatas': [[...]], 'distances': [[...]]}
        if not raw_results.get('ids') or not raw_results['ids'][0]:
            return results
        
        ids = raw_results['ids'][0]
        documents = raw_results['documents'][0]
        metadatas = raw_results['metadatas'][0]
        distances = raw_results['distances'][0]
        
        for doc_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            # 거리를 유사도 점수로 변환 (코사인 거리: 0=완전일치, 2=완전반대)
            # 점수: 1 - (distance / 2) -> 0~1 범위
            score = 1.0 - (distance / 2.0)
            
            # 스니펫 생성
            snippet = self._create_snippet(document)
            
            results.append(QueryResult(
                text=document,
                metadata=metadata,
                score=score,
                snippet=snippet
            ))
        
        return results
    
    def _create_snippet(self, text: str) -> str:
        """
        텍스트에서 스니펫 생성
        
        Args:
            text: 원본 텍스트
            
        Returns:
            스니펫 (제한된 길이)
        """
        if len(text) <= self.snippet_length:
            return text
        
        # 단어 경계에서 자르기
        snippet = text[:self.snippet_length]
        last_space = snippet.rfind(' ')
        
        if last_space > 0:
            snippet = snippet[:last_space]
        
        return snippet + "..."
    
    def format_results(
        self,
        results: List[QueryResult],
        show_score: bool = True,
        show_snippet: bool = True
    ) -> str:
        """
        검색 결과를 보기 좋게 포맷팅
        
        Args:
            results: 검색 결과 리스트
            show_score: 점수 표시 여부
            show_snippet: 스니펫 표시 여부
            
        Returns:
            포맷된 결과 문자열
        """
        if not results:
            return "검색 결과가 없습니다."
        
        output = []
        output.append(f"\n총 {len(results)}개의 결과를 찾았습니다.\n")
        
        for idx, result in enumerate(results, 1):
            output.append(f"[{idx}] {result.metadata.get('file_name', 'Unknown')}")
            
            if show_score:
                output.append(f"    유사도: {result.score:.3f}")
            
            # 파일 정보
            file_path = result.metadata.get('file_path', '')
            if file_path:
                output.append(f"    경로: {file_path}")
            
            page = result.metadata.get('page')
            if page:
                output.append(f"    페이지: {page}")
            
            # 스니펫
            if show_snippet and result.snippet:
                output.append(f"    내용: {result.snippet}")
            
            output.append("")  # 빈 줄
        
        return "\n".join(output)

