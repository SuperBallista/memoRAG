"""문서 파서 테스트"""
import pytest
from pathlib import Path
from src.core.parser import DocumentParser, DocumentChunk


def test_parser_initialization():
    """파서 초기화 테스트"""
    parser = DocumentParser(chunk_size=512, chunk_overlap=50)
    assert parser.chunk_size == 512
    assert parser.chunk_overlap == 50


def test_is_supported():
    """지원 파일 형식 확인 테스트"""
    assert DocumentParser.is_supported(Path("test.pdf"))
    assert DocumentParser.is_supported(Path("test.docx"))
    assert DocumentParser.is_supported(Path("test.hwpx"))
    assert DocumentParser.is_supported(Path("test.txt"))
    assert DocumentParser.is_supported(Path("test.md"))
    assert not DocumentParser.is_supported(Path("test.xlsx"))


def test_split_text():
    """텍스트 분할 테스트"""
    parser = DocumentParser(chunk_size=20, chunk_overlap=5)
    text = "This is a test sentence for chunking."
    
    chunks = parser._split_text(text)
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


# 실제 파일 테스트는 테스트 문서가 필요
# TODO: 테스트용 샘플 문서 추가

