"""로깅 설정 모듈"""
import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console


def setup_logger(
    name: str = "memorag",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    use_rich: bool = True
) -> logging.Logger:
    """
    로거 설정
    
    Args:
        name: 로거 이름
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 로그 파일 경로 (None이면 파일 로깅 안 함)
        use_rich: Rich 핸들러 사용 여부 (예쁜 콘솔 출력)
        
    Returns:
        설정된 로거
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 기존 핸들러 제거
    logger.handlers.clear()
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러
    if use_rich:
        # Rich 핸들러 (예쁜 콘솔 출력)
        console_handler = RichHandler(
            console=Console(stderr=True),
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=False
        )
    else:
        # 기본 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # 파일 핸들러
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "memorag") -> logging.Logger:
    """
    로거 가져오기
    
    Args:
        name: 로거 이름
        
    Returns:
        로거 인스턴스
    """
    return logging.getLogger(name)

