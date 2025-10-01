"""관리 서비스 - 인덱스 관리, 통계, 삭제 등"""
from typing import List, Dict, Optional
from pathlib import Path
import logging

from ..core import VectorSearch

logger = logging.getLogger(__name__)


class ManagementService:
    """시스템 관리 서비스"""
    
    def __init__(self, vector_db: VectorSearch):
        """
        Args:
            vector_db: 벡터 검색 엔진
        """
        self.vector_db = vector_db
    
    def list_collections(self) -> List[str]:
        """
        모든 컬렉션(인덱스) 목록 반환
        
        Returns:
            컬렉션 이름 리스트
        """
        collections = self.vector_db.list_collections()
        logger.info(f"Found {len(collections)} collections")
        return collections
    
    def get_collection_info(self, collection_name: str) -> Dict:
        """
        컬렉션 정보 조회
        
        Args:
            collection_name: 컬렉션 이름
            
        Returns:
            컬렉션 정보 딕셔너리
        """
        try:
            count = self.vector_db.get_collection_count(collection_name)
            
            info = {
                "name": collection_name,
                "document_count": count,
                "status": "active"
            }
            
            logger.debug(f"Collection info: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {
                "name": collection_name,
                "document_count": 0,
                "status": "error",
                "error": str(e)
            }
    
    def list_all_info(self) -> List[Dict]:
        """
        모든 컬렉션의 정보 반환
        
        Returns:
            컬렉션 정보 리스트
        """
        collections = self.list_collections()
        
        infos = []
        for collection_name in collections:
            info = self.get_collection_info(collection_name)
            infos.append(info)
        
        return infos
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        컬렉션 삭제
        
        Args:
            collection_name: 삭제할 컬렉션 이름
            
        Returns:
            성공 여부
        """
        try:
            self.vector_db.delete_collection(collection_name)
            logger.info(f"Deleted collection: {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return False
    
    def clean_all(self, confirm: bool = False) -> bool:
        """
        모든 데이터 삭제 (주의: 복구 불가능)
        
        Args:
            confirm: 삭제 확인 (안전장치)
            
        Returns:
            성공 여부
        """
        if not confirm:
            logger.warning("Clean all requires confirmation")
            return False
        
        try:
            self.vector_db.reset()
            logger.warning("All data has been cleaned!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clean all: {e}")
            return False
    
    def format_collection_list(self, infos: List[Dict]) -> str:
        """
        컬렉션 목록을 보기 좋게 포맷팅
        
        Args:
            infos: 컬렉션 정보 리스트
            
        Returns:
            포맷된 문자열
        """
        if not infos:
            return "인덱스가 없습니다."
        
        output = []
        output.append(f"\n총 {len(infos)}개의 인덱스가 있습니다.\n")
        
        for idx, info in enumerate(infos, 1):
            output.append(f"[{idx}] {info['name']}")
            output.append(f"    문서 수: {info['document_count']}")
            output.append(f"    상태: {info['status']}")
            
            if info.get('error'):
                output.append(f"    오류: {info['error']}")
            
            output.append("")  # 빈 줄
        
        return "\n".join(output)
    
    def get_storage_path(self) -> Path:
        """벡터 DB 저장 경로 반환"""
        return self.vector_db.persist_directory
    
    def get_storage_size(self) -> int:
        """
        벡터 DB 저장소 크기 계산 (바이트)
        
        Returns:
            저장소 크기 (bytes)
        """
        storage_path = self.get_storage_path()
        
        if not storage_path.exists():
            return 0
        
        total_size = 0
        for file_path in storage_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size
    
    def format_storage_size(self, size_bytes: int) -> str:
        """
        저장소 크기를 읽기 좋은 형식으로 변환
        
        Args:
            size_bytes: 크기 (바이트)
            
        Returns:
            포맷된 크기 문자열 (예: "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.2f} PB"

