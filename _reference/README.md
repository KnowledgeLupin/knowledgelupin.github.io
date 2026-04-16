# 참고 문서 폴더

이 폴더는 웹사이트에 공개되지 않는 개인 참고 문서를 저장하는 공간입니다.

Jekyll은 언더스코어(_)로 시작하는 폴더를 자동으로 빌드에서 제외하므로, 이곳에 저장된 파일들은 블로그에 나타나지 않습니다.

## 사용 방법
- 개인 메모, 연구 노트, 참고 자료 등을 자유롭게 저장
- Markdown, PDF, 텍스트 파일 등 모든 형식 가능
- 폴더 내 하위 구조도 자유롭게 구성 가능

## 선형대수 교재 문서
- `2026-04-16-linear-algebra-independent-post-automation-design.md`: 독립 포스트 자동화 설계 정본
- `linear-algebra-post-manifest.yml`: 독립 포스트 후보 manifest
- `2026-02-25-linear-algebra-final-plan.md`: 최종 집필 계획안
- `2026-04-16-linear-algebra-blog-writing-spec.md`: 블로그 포스팅 집필 기준
- `2026-02-24-linear-algebra-korean-textbook-toc.md`: 최종 목차(5부 16장)
- `2026-02-25-linear-algebra-legacy-to-v2-mapping.md`: 레거시 파일 매핑 기록

현재 선형대수 포스트 설계는 수학적 엄밀성뿐 아니라 검색 가시성까지 함께 다룹니다.

1. 제목은 정확한 개념명을 유지하되 검색 의도와 만나는 한국어 표현을 포함합니다.
2. front matter에는 `description`, `excerpt`, `image`를 포함하는 방향으로 설계합니다.
3. 후보 선정과 게시 단계 모두에서 SEO 점검을 별도 단계로 둡니다.

## 자동화 스크립트
- `../tools/generate-linear-algebra-draft.py`: 독립 포스트 초안 생성기
- `../tools/review-linear-algebra-draft-with-claude.py`: Claude Code만을 이용해 초안을 3회 반복 교정하는 스크립트
- `../tools/check-linear-algebra-seo.py`: 초안이나 게시물의 front matter와 빌드된 HTML 메타 태그를 점검하는 SEO preflight 스크립트
