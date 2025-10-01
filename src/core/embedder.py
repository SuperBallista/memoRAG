"""임베딩 엔진 - 텍스트를 벡터로 변환"""
from typing import List, Union
import logging
import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingEngine:
    """텍스트를 벡터로 변환하는 임베딩 엔진"""
    
    def __init__(
        self,
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        device: str = "cpu",
        batch_size: int = 32
    ):
        """
        Args:
            model_name: 사용할 임베딩 모델 이름
            device: 연산 디바이스 ("cpu" or "cuda")
            batch_size: 배치 처리 크기
        """
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.model = None
        
        logger.info(f"Initializing embedding engine with model: {model_name}")
        self._load_model()
    
    def _load_model(self):
        """모델 로드"""
        try:
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def embed(self, texts: Union[str, List[str]], prefix: str = "") -> List[List[float]]:
        """
        텍스트를 벡터로 변환
        
        Args:
            texts: 임베딩할 텍스트 (문자열 또는 리스트)
            prefix: 텍스트 앞에 붙일 접두사 (일부 모델에서 사용)
            
        Returns:
            임베딩 벡터 리스트 (각 벡터는 float 리스트)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        if not texts:
            return []
        
        # multilingual-e5 모델은 query와 passage에 다른 접두사 사용
        if prefix:
            texts = [f"{prefix}: {text}" for text in texts]
        
        try:
            logger.debug(f"Embedding {len(texts)} texts...")
            
            # 배치 처리
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            # numpy array를 리스트로 변환
            embeddings_list = embeddings.tolist()
            
            logger.debug(f"Generated {len(embeddings_list)} embeddings")
            return embeddings_list
            
        except Exception as e:
            logger.error(f"Error during embedding: {e}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        문서 텍스트를 임베딩 (passage용)
        
        Args:
            texts: 문서 텍스트 리스트
            
        Returns:
            임베딩 벡터 리스트
        """
        # multilingual-e5 모델의 경우 passage 접두사 사용
        if "e5" in self.model_name.lower():
            return self.embed(texts, prefix="passage")
        return self.embed(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        쿼리 텍스트를 임베딩 (query용)
        
        Args:
            text: 쿼리 텍스트
            
        Returns:
            임베딩 벡터
        """
        # multilingual-e5 모델의 경우 query 접두사 사용
        if "e5" in self.model_name.lower():
            embeddings = self.embed([text], prefix="query")
        else:
            embeddings = self.embed([text])
        
        return embeddings[0] if embeddings else []
    
    def get_dimension(self) -> int:
        """임베딩 벡터 차원 반환"""
        if self.model is None:
            return 0
        return self.model.get_sentence_embedding_dimension()
    
    def __repr__(self) -> str:
        return f"EmbeddingEngine(model={self.model_name}, device={self.device}, dim={self.get_dimension()})"

