#!/usr/bin/env python
"""간단한 통합 테스트 스크립트"""
import sys
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent))

from src.core import DocumentParser, EmbeddingEngine, VectorSearch
from src.services import IndexingService, QueryService, ManagementService
from src.utils import Config, setup_logger

def test_full_workflow():
    """전체 워크플로우 테스트"""
    print("\n" + "="*50)
    print("memoRAG 통합 테스트 시작")
    print("="*50 + "\n")
    
    # 로거 설정
    logger = setup_logger(name="test", level="INFO", use_rich=True)
    
    # 설정
    config = Config()
    
    print("[1단계] 컴포넌트 초기화 중...")
    try:
        # 파서
        parser = DocumentParser(
            chunk_size=config.get('parsing.chunk_size', 512),
            chunk_overlap=config.get('parsing.chunk_overlap', 50)
        )
        print("  [OK] DocumentParser 초기화 완료")
        
        # 임베딩 엔진 (처음엔 모델 다운로드 시간 소요)
        print("  [진행중] EmbeddingEngine 초기화 중... (모델 다운로드 시간이 걸릴 수 있습니다)")
        embedder = EmbeddingEngine(
            model_name=config.get('embedding.model_name'),
            device=config.get('embedding.device', 'cpu'),
            batch_size=config.get('embedding.batch_size', 32)
        )
        print(f"  [OK] EmbeddingEngine 초기화 완료 (차원: {embedder.get_dimension()})")
        
        # 벡터 DB
        vector_db = VectorSearch(
            persist_directory="./chroma_test",
            collection_name="test_collection"
        )
        print("  [OK] VectorSearch 초기화 완료")
        
    except Exception as e:
        print(f"  [ERROR] 초기화 실패: {e}")
        return False
    
    print("\n[2단계] 문서 인덱싱 중...")
    try:
        indexing_service = IndexingService(parser, embedder, vector_db)
        
        test_folder = Path("test_documents")
        if not test_folder.exists():
            print(f"  [ERROR] 테스트 폴더가 없습니다: {test_folder}")
            return False
        
        stats = indexing_service.index_folder(
            folder_path=test_folder,
            collection_name="test_collection",
            recursive=True,
            show_progress=True
        )
        
        print(f"\n  [OK] 인덱싱 완료!")
        print(f"    - 파일 수: {stats['total_files']}개")
        print(f"    - 청크 수: {stats['total_chunks']}개")
        print(f"    - 오류: {stats['errors']}개")
        
    except Exception as e:
        print(f"  [ERROR] 인덱싱 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n[3단계] 검색 테스트 중...")
    try:
        query_service = QueryService(
            embedder=embedder,
            vector_db=vector_db,
            top_k=3,
            snippet_length=200
        )
        
        test_queries = [
            "체육대회 준비물은 뭐야?",
            "수련활동 일정 알려줘",
            "학부모 공개수업 언제야?"
        ]
        
        for idx, query in enumerate(test_queries, 1):
            print(f"\n  [질문 {idx}] {query}")
            results = query_service.search(
                query=query,
                collection_name="test_collection",
                top_k=3
            )
            
            if results:
                print(f"    [OK] {len(results)}개 결과 발견")
                for i, result in enumerate(results[:2], 1):  # 상위 2개만 표시
                    print(f"      [{i}] {result.metadata.get('file_name')} (점수: {result.score:.3f})")
                    print(f"          {result.snippet[:100]}...")
            else:
                print("    [ERROR] 결과 없음")
        
    except Exception as e:
        print(f"  [ERROR] 검색 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n[4단계] 관리 기능 테스트 중...")
    try:
        management_service = ManagementService(vector_db)
        
        # 인덱스 목록
        collections = management_service.list_collections()
        print(f"  [OK] 컬렉션 목록: {collections}")
        
        # 컬렉션 정보
        info = management_service.get_collection_info("test_collection")
        print(f"  [OK] 문서 수: {info['document_count']}개")
        
        # 저장소 크기
        size = management_service.get_storage_size()
        size_str = management_service.format_storage_size(size)
        print(f"  [OK] 저장소 크기: {size_str}")
        
    except Exception as e:
        print(f"  [ERROR] 관리 기능 실패: {e}")
        return False
    
    print("\n" + "="*50)
    print("[SUCCESS] 모든 테스트 통과!")
    print("="*50 + "\n")
    
    # 정리
    print("[정리] 테스트 데이터 삭제 중...")
    try:
        management_service.delete_collection("test_collection")
        print("  [OK] 테스트 컬렉션 삭제 완료")
    except:
        pass
    
    return True


if __name__ == '__main__':
    success = test_full_workflow()
    sys.exit(0 if success else 1)

