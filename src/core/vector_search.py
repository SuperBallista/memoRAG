"""벡터 검색 엔진 - ChromaDB 기반"""
from typing import List, Dict, Optional
from pathlib import Path
import logging
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class VectorSearch:
    """ChromaDB를 사용한 벡터 검색 엔진"""
    
    def __init__(
        self,
        persist_directory: str = "./chroma",
        collection_name: str = "default"
    ):
        """
        Args:
            persist_directory: ChromaDB 저장 디렉토리
            collection_name: 컬렉션 이름
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """ChromaDB 클라이언트 초기화"""
        try:
            # 저장 디렉토리 생성
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            # ChromaDB 클라이언트 생성
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            logger.info(f"ChromaDB initialized at {self.persist_directory}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def get_or_create_collection(self, collection_name: Optional[str] = None) -> chromadb.Collection:
        """
        컬렉션 가져오기 또는 생성
        
        Args:
            collection_name: 컬렉션 이름 (None이면 기본값 사용)
            
        Returns:
            ChromaDB 컬렉션
        """
        name = collection_name or self.collection_name
        
        try:
            self.collection = self.client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}  # 코사인 유사도 사용
            )
            logger.info(f"Using collection: {name}")
            return self.collection
            
        except Exception as e:
            logger.error(f"Failed to get/create collection: {e}")
            raise
    
    def add_documents(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict]
    ):
        """
        문서 임베딩 추가
        
        Args:
            ids: 문서 ID 리스트
            embeddings: 임베딩 벡터 리스트
            documents: 원본 텍스트 리스트
            metadatas: 메타데이터 리스트
        """
        if not self.collection:
            self.get_or_create_collection()
        
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Added {len(ids)} documents to collection")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """
        벡터 검색
        
        Args:
            query_embedding: 쿼리 임베딩 벡터
            top_k: 반환할 결과 수
            where: 메타데이터 필터 조건
            
        Returns:
            검색 결과 딕셔너리
        """
        if not self.collection:
            self.get_or_create_collection()
        
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=["documents", "metadatas", "distances"]
            )
            
            logger.debug(f"Search returned {len(results.get('ids', [[]])[0])} results")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def delete_collection(self, collection_name: Optional[str] = None):
        """
        컬렉션 삭제
        
        Args:
            collection_name: 삭제할 컬렉션 이름 (None이면 현재 컬렉션)
        """
        name = collection_name or self.collection_name
        
        try:
            self.client.delete_collection(name=name)
            logger.info(f"Deleted collection: {name}")
            
            if name == self.collection_name:
                self.collection = None
                
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
    
    def list_collections(self) -> List[str]:
        """모든 컬렉션 이름 반환"""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            return []
    
    def get_collection_count(self, collection_name: Optional[str] = None) -> int:
        """
        컬렉션의 문서 개수 반환
        
        Args:
            collection_name: 컬렉션 이름 (None이면 현재 컬렉션)
            
        Returns:
            문서 개수
        """
        if collection_name:
            collection = self.client.get_collection(collection_name)
        else:
            if not self.collection:
                return 0
            collection = self.collection
        
        try:
            return collection.count()
        except Exception as e:
            logger.error(f"Failed to get count: {e}")
            return 0
    
    def reset(self):
        """모든 데이터 초기화 (주의: 복구 불가능)"""
        try:
            self.client.reset()
            self.collection = None
            logger.warning("All data has been reset!")
        except Exception as e:
            logger.error(f"Failed to reset: {e}")
            raise
    
    def __repr__(self) -> str:
        return f"VectorSearch(persist_directory={self.persist_directory}, collection={self.collection_name})"

