"""memoRAG CLI 메인 엔트리포인트"""
import click
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table

# 프로젝트 모듈
from ..core import DocumentParser, EmbeddingEngine, VectorSearch
from ..services import IndexingService, QueryService, ManagementService
from ..utils import Config, setup_logger

console = Console()


@click.group()
@click.option('--config', type=click.Path(), help='설정 파일 경로')
@click.option('--verbose', is_flag=True, help='상세 로그 출력')
@click.pass_context
def cli(ctx, config, verbose):
    """
    memoRAG - 개인/팀 문서 검색 시스템
    
    문서를 인덱싱하고 자연어로 검색할 수 있습니다.
    """
    # Context에 설정 저장
    ctx.ensure_object(dict)
    
    # 설정 로드
    config_path = Path(config) if config else None
    ctx.obj['config'] = Config(config_path)
    
    # 로거 설정
    log_level = "DEBUG" if verbose else ctx.obj['config'].get('logging.level', 'INFO')
    log_file = ctx.obj['config'].get('logging.file')
    
    logger = setup_logger(
        name="memoRAG",
        level=log_level,
        log_file=Path(log_file) if log_file else None,
        use_rich=True
    )
    
    ctx.obj['logger'] = logger


@cli.command()
@click.option('--folder', '-f', required=True, type=click.Path(exists=True), help='인덱싱할 폴더 경로')
@click.option('--output', '-o', help='인덱스 이름 (기본값: default)')
@click.option('--recursive/--no-recursive', default=True, help='하위 폴더 포함 여부')
@click.pass_context
def index(ctx, folder, output, recursive):
    """문서 폴더를 인덱싱합니다."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    console.print(f"\n[bold green]문서 인덱싱 시작[/bold green]")
    console.print(f"폴더: {folder}")
    console.print(f"인덱스: {output or 'default'}\n")
    
    try:
        # 컴포넌트 초기화
        parser = DocumentParser(
            chunk_size=config.get('parsing.chunk_size', 512),
            chunk_overlap=config.get('parsing.chunk_overlap', 50)
        )
        
        embedder = EmbeddingEngine(
            model_name=config.get('embedding.model_name'),
            device=config.get('embedding.device', 'cpu'),
            batch_size=config.get('embedding.batch_size', 32)
        )
        
        vector_db = VectorSearch(
            persist_directory=config.get('database.persist_directory', './chroma'),
            collection_name=output or config.get('database.default_collection', 'default')
        )
        
        indexing_service = IndexingService(parser, embedder, vector_db)
        
        # 인덱싱 실행
        stats = indexing_service.index_folder(
            folder_path=Path(folder),
            collection_name=output,
            recursive=recursive,
            show_progress=True
        )
        
        # 결과 출력
        console.print(f"\n[bold green]인덱싱 완료![/bold green]")
        console.print(f"처리 파일: {stats['total_files']}개")
        console.print(f"생성 청크: {stats['total_chunks']}개")
        
        if stats['errors'] > 0:
            console.print(f"[red]오류 파일: {stats['errors']}개[/red]")
            for error_file in stats.get('error_files', []):
                console.print(f"  - {error_file}")
        
    except Exception as e:
        console.print(f"\n[bold red]오류 발생: {e}[/bold red]")
        logger.exception("Indexing failed")
        sys.exit(1)


@cli.command()
@click.argument('query', required=True)
@click.option('--index', '-i', help='검색할 인덱스 이름')
@click.option('--top-k', '-k', type=int, help='결과 개수')
@click.option('--no-score', is_flag=True, help='점수 숨기기')
@click.option('--no-snippet', is_flag=True, help='스니펫 숨기기')
@click.pass_context
def query(ctx, query, index, top_k, no_score, no_snippet):
    """자연어로 문서를 검색합니다."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    console.print(f"\n[bold blue]검색 중...[/bold blue]")
    console.print(f"질의: {query}\n")
    
    try:
        # 컴포넌트 초기화
        embedder = EmbeddingEngine(
            model_name=config.get('embedding.model_name'),
            device=config.get('embedding.device', 'cpu'),
            batch_size=config.get('embedding.batch_size', 32)
        )
        
        vector_db = VectorSearch(
            persist_directory=config.get('database.persist_directory', './chroma'),
            collection_name=index or config.get('database.default_collection', 'default')
        )
        
        query_service = QueryService(
            embedder=embedder,
            vector_db=vector_db,
            top_k=top_k or config.get('search.top_k', 5),
            snippet_length=config.get('output.snippet_length', 200)
        )
        
        # 검색 실행
        results = query_service.search(
            query=query,
            collection_name=index
        )
        
        # 결과 출력
        if not results:
            console.print("[yellow]검색 결과가 없습니다.[/yellow]")
            return
        
        console.print(f"[bold green]총 {len(results)}개의 결과를 찾았습니다.[/bold green]\n")
        
        for idx, result in enumerate(results, 1):
            console.print(f"[bold cyan][{idx}] {result.metadata.get('file_name', 'Unknown')}[/bold cyan]")
            
            if not no_score:
                console.print(f"  유사도: [green]{result.score:.3f}[/green]")
            
            file_path = result.metadata.get('file_path', '')
            if file_path:
                console.print(f"  경로: {file_path}")
            
            page = result.metadata.get('page')
            if page:
                console.print(f"  페이지: {page}")
            
            if not no_snippet and result.snippet:
                console.print(f"  내용: [dim]{result.snippet}[/dim]")
            
            console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]✗ 오류 발생: {e}[/bold red]")
        logger.exception("Query failed")
        sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """모든 인덱스 목록을 표시합니다."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    try:
        vector_db = VectorSearch(
            persist_directory=config.get('database.persist_directory', './chroma')
        )
        
        management_service = ManagementService(vector_db)
        
        # 인덱스 정보 조회
        infos = management_service.list_all_info()
        
        if not infos:
            console.print("\n[yellow]인덱스가 없습니다.[/yellow]")
            return
        
        # 테이블로 출력
        table = Table(title=f"\n인덱스 목록 (총 {len(infos)}개)")
        table.add_column("이름", style="cyan")
        table.add_column("문서 수", justify="right", style="green")
        table.add_column("상태", style="yellow")
        
        for info in infos:
            table.add_row(
                info['name'],
                str(info['document_count']),
                info['status']
            )
        
        console.print(table)
        
        # 저장소 크기
        storage_size = management_service.get_storage_size()
        size_str = management_service.format_storage_size(storage_size)
        console.print(f"\n저장소 크기: {size_str}")
        console.print(f"저장 위치: {management_service.get_storage_path()}\n")
        
    except Exception as e:
        console.print(f"\n[bold red]✗ 오류 발생: {e}[/bold red]")
        logger.exception("List failed")
        sys.exit(1)


@cli.command()
@click.option('--index', '-i', help='삭제할 인덱스 이름 (없으면 전체 삭제)')
@click.option('--yes', '-y', is_flag=True, help='확인 없이 삭제')
@click.pass_context
def clean(ctx, index, yes):
    """인덱스를 삭제합니다."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    if not yes:
        if index:
            if not click.confirm(f"인덱스 '{index}'를 삭제하시겠습니까?"):
                console.print("[yellow]취소되었습니다.[/yellow]")
                return
        else:
            console.print("[bold red]주의: 모든 인덱스가 삭제됩니다![/bold red]")
            if not click.confirm("정말로 모든 데이터를 삭제하시겠습니까?"):
                console.print("[yellow]취소되었습니다.[/yellow]")
                return
    
    try:
        vector_db = VectorSearch(
            persist_directory=config.get('database.persist_directory', './chroma')
        )
        
        management_service = ManagementService(vector_db)
        
        if index:
            # 특정 인덱스 삭제
            success = management_service.delete_collection(index)
            if success:
                console.print(f"[green]인덱스 '{index}'를 삭제했습니다.[/green]")
            else:
                console.print(f"[red]인덱스 삭제 실패[/red]")
                sys.exit(1)
        else:
            # 전체 삭제
            success = management_service.clean_all(confirm=True)
            if success:
                console.print("[green]모든 데이터를 삭제했습니다.[/green]")
            else:
                console.print("[red]데이터 삭제 실패[/red]")
                sys.exit(1)
        
    except Exception as e:
        console.print(f"\n[bold red]오류 발생: {e}[/bold red]")
        logger.exception("Clean failed")
        sys.exit(1)


@cli.command()
def version():
    """버전 정보를 표시합니다."""
    from .. import __version__
    console.print(f"\nmemoRAG v{__version__}")
    console.print("개인/팀 문서 검색 시스템\n")


def main():
    """CLI 진입점"""
    cli(obj={})


if __name__ == '__main__':
    main()

