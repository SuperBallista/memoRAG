# Changelog

memoRAG 프로젝트의 모든 주요 변경 사항을 기록합니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따르며,
버전 관리는 [Semantic Versioning](https://semver.org/lang/ko/)을 따릅니다.

## [Unreleased]

### 계획된 기능
- Tkinter GUI
- LLM 요약 답변
- 클라우드 연동 (Notion, Google Drive)

## [0.1.0] - 2025-10-01

### 추가됨 (Added)
- 문서 파싱 기능 (PDF, DOCX, HWPX, PPTX, XLSX, TXT, MD)
- 벡터 검색 엔진 (ChromaDB 기반)
- 의미 기반 검색 (multilingual-e5 임베딩)
- CLI 인터페이스 (index, query, list, clean 명령어)
- 인덱스 파일 공유 기능
- CPU 최적화 (일반 PC 환경)
- 경량 모델 옵션 (MiniLM-L12-v2)
- PyInstaller 단일 exe 빌드
- 사용자 가이드 (6종)
- 개발자 문서 (아키텍처, 배포 가이드 등)

### 보안 (Security)
- 로컬 전용 처리 (외부 서버 업로드 없음)
- 개인정보 보호 강화

---

## 버전 비교

[Unreleased]: https://github.com/user/memorag/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/user/memorag/releases/tag/v0.1.0

