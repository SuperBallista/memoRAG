"""인덱싱 서비스 - 문서 폴더를 스캔하여 벡터 DB에 저장"""
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime
import hashlib
from tqdm import tqdm

from ..core import DocumentParser, EmbeddingEngine, VectorSearch

logger = logging.getLogger(__name__)


class IndexingService:
    """문서 인덱싱 서비스"""
    
    def __init__(
        self,
        parser: DocumentParser,
        embedder: EmbeddingEngine,
        vector_db: VectorSearch
    ):
        """
        Args:
            parser: 문서 파서
            embedder: 임베딩 엔진
            vector_db: 벡터 검색 엔진
        """
        self.parser = parser
        self.embedder = embedder
        self.vector_db = vector_db
    
    def index_folder(
        self,
        folder_path: Path,
        collection_name: Optional[str] = None,
        recursive: bool = True,
        show_progress: bool = True
    ) -> dict:
        """
        폴더 내 모든 지원 문서를 인덱싱
        
        Args:
            folder_path: 인덱싱할 폴더 경로
            collection_name: 저장할 컬렉션 이름 (None이면 기본값)
            recursive: 하위 폴더 포함 여부
            show_progress: 진행률 표시 여부
            
        Returns:
            인덱싱 결과 통계
        """
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        logger.info(f"Starting indexing: {folder_path}")
        
        # 컬렉션 생성/가져오기
        self.vector_db.get_or_create_collection(collection_name)
        
        # 문서 파일 찾기
        file_list = self._scan_folder(folder_path, recursive)
        logger.info(f"Found {len(file_list)} supported documents")
        
        if not file_list:
            logger.warning("No supported files found")
            return {"total_files": 0, "total_chunks": 0, "errors": 0}
        
        # 통계
        stats = {
            "total_files": len(file_list),
            "total_chunks": 0,
            "errors": 0,
            "error_files": []
        }
        
        # 파일별 처리
        file_iterator = tqdm(file_list, desc="Indexing documents") if show_progress else file_list
        
        for file_path in file_iterator:
            try:
                chunks_count = self._index_file(file_path, collection_name)
                stats["total_chunks"] += chunks_count
                
            except Exception as e:
                logger.error(f"Failed to index {file_path}: {e}")
                stats["errors"] += 1
                stats["error_files"].append(str(file_path))
        
        logger.info(f"Indexing complete: {stats}")
        return stats
    
    def _scan_folder(self, folder_path: Path, recursive: bool) -> List[Path]:
        """폴더에서 지원 문서 찾기"""
        files = []
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in folder_path.glob(pattern):
            if file_path.is_file() and DocumentParser.is_supported(file_path):
                files.append(file_path)
        
        return sorted(files)
    
    def _index_file(self, file_path: Path, collection_name: Optional[str] = None) -> int:
        """
        단일 파일 인덱싱
        
        Args:
            file_path: 파일 경로
            collection_name: 컬렉션 이름
            
        Returns:
            생성된 청크 수
        """
        # 파일 파싱
        chunks = self.parser.parse(file_path)
        
        if not chunks:
            logger.warning(f"No content extracted from: {file_path}")
            return 0
        
        # 텍스트 추출
        texts = [chunk.text for chunk in chunks]
        
        # 임베딩 생성
        embeddings = self.embedder.embed_documents(texts)
        
        # ID 생성 (파일 경로 + 청크 인덱스의 해시)
        ids = []
        documents = []
        metadatas = []
        
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # 고유 ID 생성
            chunk_id = self._generate_chunk_id(file_path, idx)
            ids.append(chunk_id)
            documents.append(chunk.text)
            
            # 메타데이터 준비
            metadata = chunk.metadata.copy()
            metadata["indexed_at"] = datetime.now().isoformat()
            metadatas.append(metadata)
        
        # 벡터 DB에 저장
        self.vector_db.add_documents(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        logger.debug(f"Indexed {len(chunks)} chunks from {file_path.name}")
        return len(chunks)
    
    def _generate_chunk_id(self, file_path: Path, chunk_index: int) -> str:
        """청크 고유 ID 생성"""
        # 파일 경로 + 청크 인덱스를 해시화
        content = f"{file_path.absolute()}:{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def index_file(self, file_path: Path, collection_name: Optional[str] = None) -> int:
        """
        단일 파일 인덱싱 (공개 메서드)
        
        Args:
            file_path: 파일 경로
            collection_name: 컬렉션 이름
            
        Returns:
            생성된 청크 수
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not DocumentParser.is_supported(file_path):
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        logger.info(f"Indexing file: {file_path}")
        
        # 컬렉션 생성/가져오기
        self.vector_db.get_or_create_collection(collection_name)
        
        return self._index_file(file_path, collection_name)

