"""설정 관리 모듈"""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import logging

logger = logging.getLogger(__name__)


class Config:
    """설정 파일 관리 클래스"""
    
    DEFAULT_CONFIG = {
        "embedding": {
            "model_name": "intfloat/multilingual-e5-base",
            "batch_size": 32,
            "device": "cpu"
        },
        "database": {
            "persist_directory": "./chroma",
            "default_collection": "default"
        },
        "parsing": {
            "chunk_size": 512,
            "chunk_overlap": 50,
            "supported_extensions": [".pdf", ".docx", ".hwpx", ".txt", ".md"]
        },
        "search": {
            "top_k": 5,
            "similarity_threshold": 0.5
        },
        "output": {
            "show_score": True,
            "show_snippet": True,
            "snippet_length": 200,
            "verbose": False
        },
        "logging": {
            "level": "INFO",
            "file": "./logs/memoRAG.log"
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Args:
            config_path: 설정 파일 경로 (None이면 기본값 사용)
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and config_path.exists():
            self.load(config_path)
    
    def load(self, config_path: Path):
        """
        YAML 설정 파일 로드
        
        Args:
            config_path: 설정 파일 경로
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
            
            # 기본 설정과 병합
            self._merge_config(self.config, user_config)
            logger.info(f"Loaded config from: {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            logger.info("Using default configuration")
    
    def _merge_config(self, base: Dict, update: Dict):
        """재귀적으로 설정 병합"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        점(.) 표기법으로 설정 값 가져오기
        
        Args:
            key_path: 설정 키 경로 (예: "embedding.model_name")
            default: 키가 없을 때 반환할 기본값
            
        Returns:
            설정 값
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        점(.) 표기법으로 설정 값 변경
        
        Args:
            key_path: 설정 키 경로 (예: "embedding.device")
            value: 설정할 값
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self, config_path: Optional[Path] = None):
        """
        설정을 YAML 파일로 저장
        
        Args:
            config_path: 저장할 경로 (None이면 로드한 경로 사용)
        """
        path = config_path or self.config_path
        if not path:
            raise ValueError("No config path specified")
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
            logger.info(f"Saved config to: {path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            raise
    
    def to_dict(self) -> Dict:
        """설정을 딕셔너리로 반환"""
        return self.config.copy()
    
    def __repr__(self) -> str:
        return f"Config(path={self.config_path})"

