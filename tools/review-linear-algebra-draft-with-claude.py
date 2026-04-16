#!/usr/bin/env python3
"""Review and polish a linear algebra blog draft with Claude CLI only."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "_reference" / ".automation" / "linear-algebra-post-state.json"
MANIFEST_PATH = ROOT / "_reference" / "linear-algebra-post-manifest.yml"
AGENTS_PATH = ROOT / "AGENTS.md"
SITE_TIMEZONE = ZoneInfo("Europe/Berlin")
DEFAULT_MODEL = "sonnet"
CLAUDE_TIMEOUT_SECONDS = 420
DEFAULT_PASSES = 3
DEFAULT_REVIEW_CONTRACT = {
    "min_words": 850,
    "min_characters": 3200,
    "min_blocks": 18,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", help="Explicit draft path to review.")
    parser.add_argument("--latest", action="store_true", help="Review the latest draft path recorded in the automation state.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write the revised draft back to disk.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model alias or name.")
    parser.add_argument("--passes", type=int, default=DEFAULT_PASSES, help="Number of full Claude review passes.")
    return parser.parse_args()


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"runs": [], "candidates": {}, "updated_at": None}
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("State file must be a JSON object.")
    data.setdefault("runs", [])
    data.setdefault("candidates", {})
    data.setdefault("updated_at", None)
    return data


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(SITE_TIMEZONE).isoformat()


def load_review_contract() -> dict[str, Any]:
    contract = dict(DEFAULT_REVIEW_CONTRACT)
    if not MANIFEST_PATH.exists():
        return contract
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return contract
    writing_contract = manifest.get("writing_contract")
    if isinstance(writing_contract, dict):
        for key in DEFAULT_REVIEW_CONTRACT:
            if key in writing_contract:
                contract[key] = writing_contract[key]
    return contract


def resolve_target_path(args: argparse.Namespace, state: dict[str, Any]) -> tuple[Path | None, dict[str, Any] | None]:
    if args.path:
        return Path(args.path).resolve(), None
    if args.latest:
        for run in reversed(state.get("runs", [])):
            draft_path = run.get("draft_path")
            if not draft_path:
                continue
            path = Path(draft_path)
            if path.exists():
                return path.resolve(), run
        return None, None
    raise SystemExit("Use --path or --latest.")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return "", text
    _, middle, rest = parts
    return f"---\n{middle}---\n", rest


def split_document_chunks(text: str) -> tuple[str, list[str]]:
    frontmatter, body = split_frontmatter(text)
    matches = list(re.finditer(r"^## .*$", body, flags=re.MULTILINE))
    if not matches:
        stripped = body.strip()
        return frontmatter, [stripped] if stripped else []

    chunks: list[str] = []
    preamble = body[: matches[0].start()].strip()
    if preamble:
        chunks.append(preamble)

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        chunk = body[start:end].strip()
        if chunk:
            chunks.append(chunk)
    return frontmatter, chunks


def strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def read_agents_excerpt() -> str:
    if not AGENTS_PATH.exists():
        return ""
    return AGENTS_PATH.read_text(encoding="utf-8")


def build_chunk_prompt(path: Path, chunk: str, chunk_index: int, total_chunks: int) -> str:
    agents = read_agents_excerpt()
    contract = load_review_contract()
    return f"""다음 Markdown 블로그 초안의 일부 구간을 최종 게시 가능한 수준으로 다듬어라.

중요 규칙:
1. 출력은 수정된 Markdown 구간 전체만 내보내라.
2. 현재 구간 밖의 내용은 재구성하지 말고, 이 구간만 자연스럽게 다듬어라.
3. 수식 표기($$...$$, inline math), 코드, 링크, HTML comment, 파일 경로는 보존하라.
4. 수학적 진술의 의미를 바꾸거나 새로운 정리와 결론을 발명하지 말라. 다만 기존 초안에 이미 들어 있는 정의, 정리, 증명, 예제, 응용을 더 충분한 문단으로 풀어 써도 된다.
5. `정의`, `정리`, `증명` 블록에서는 수학 교재식 평서체(`...라 한다.`, `성립한다.`)를 유지해도 된다.
6. 그 밖의 설명 문단은 모두 경어체/설명체(`...입니다.`, `...합니다.`)로 일관되게 써라.
7. 설명 문단에서 반말이나 평서체(`...이다.`, `...한다.`)가 섞이면 안 된다.
8. 문장 사이 연결이 부자연스러운 부분, 단락 전환이 갑작스러운 부분, 소제목이 불필요하게 잘게 나뉘어 있거나 어색한 부분을 고쳐라.
9. 필요하면 현재 구간의 소제목 이름도 조금 더 자연스럽게 고쳐라.
10. 글이 너무 짧거나 설명이 성기면, 같은 수학 내용을 유지한 채 배경 설명, 증명 해설, 계산 예제 해석, 응용 연결을 보강해 독립 포스트다운 밀도를 갖추게 하라.
11. ChatGPT스럽게 들리는 어색한 표현, 과하게 틀에 박힌 연결 문장, 불필요하게 번들거리는 요약 문구, 지나치게 교과서적이거나 기계적으로 반복되는 표현이 있으면 모두 자연스러운 한국어 문장으로 고쳐라.
12. 이 단계의 문장 교정은 Claude Code만 담당한다. 현재 구간에서 고칠 점이 없다면 원문을 거의 그대로 유지하고, 불확실한 수정을 추측해서 추가하지 말라.

특별 점검 항목:
- 문장 간 전환이 자연스러운가
- 문체가 일관적인가
- 정리/증명 밖에서 반말이나 과한 평서체가 남아 있지 않은가
- 소제목 구조가 과도하거나 부자연스럽지 않은가
- 설명이 지나치게 짧거나 끊겨 있지 않은가
- ChatGPT스럽거나 기계적으로 반복되는 표현이 남아 있지 않은가
- 적어도 대략 {contract["min_words"]}단어, {contract["min_characters"]}자, {contract["min_blocks"]}개 안팎의 prose block을 가진 독립 포스트다운 밀도를 향해 가고 있는가

로컬 AGENTS.md 요약:
{agents}

대상 파일: {path}
현재 구간: {chunk_index}/{total_chunks}

검토 대상 구간:
```markdown
{chunk}
```"""


def run_claude_review(prompt: str, model: str) -> str:
    command = [
        "claude",
        "-p",
        "--output-format",
        "text",
        "--tools",
        "",
        "--model",
        model,
        "--effort",
        "low",
    ]
    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        timeout=CLAUDE_TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Claude review failed: {stderr}")
    return completed.stdout


def normalize_chunk_output(original_chunk: str, revised_chunk: str) -> str:
    cleaned = strip_code_fence(revised_chunk).strip()
    if not cleaned:
        raise ValueError("Claude output is empty.")
    if len(cleaned) < len(original_chunk.strip()) * 0.45:
        raise ValueError("Claude output is unexpectedly short for the reviewed chunk.")
    return cleaned


def review_document_once(path: Path, text: str, model: str) -> str:
    frontmatter, chunks = split_document_chunks(text)
    if not chunks:
        return text

    revised_chunks: list[str] = []
    total_chunks = len(chunks)
    for index, chunk in enumerate(chunks, start=1):
        if len(chunk.split()) < 20:
            revised_chunks.append(chunk.strip())
            continue
        revised = run_claude_review(build_chunk_prompt(path, chunk, index, total_chunks), model)
        revised_chunks.append(normalize_chunk_output(chunk, revised))

    body = "\n\n".join(revised_chunks).rstrip() + "\n"
    if frontmatter:
        return frontmatter + "\n" + body
    return body


def review_document(path: Path, text: str, model: str, passes: int) -> str:
    revised = text
    for _ in range(max(1, passes)):
        revised = review_document_once(path, revised, model)
    return revised


def update_state_with_review(
    state: dict[str, Any],
    path: Path,
    changed: bool,
    model: str,
    run_record: dict[str, Any] | None,
) -> None:
    reviewed_at = now_iso()
    slug = None
    for run in reversed(state.get("runs", [])):
        if run.get("draft_path") == str(path):
            slug = run.get("selected_slug")
            run["claude_review"] = {
                "reviewed_at": reviewed_at,
                "changed": changed,
                "model": model,
                "path": str(path),
            }
            break
    if run_record is not None and "claude_review" not in run_record:
        run_record["claude_review"] = {
            "reviewed_at": reviewed_at,
            "changed": changed,
            "model": model,
            "path": str(path),
        }
    if slug:
        runtime = state.setdefault("candidates", {}).setdefault(slug, {})
        runtime["claude_reviewed_at"] = reviewed_at
        runtime["claude_review_changed"] = changed
        runtime["claude_review_model"] = model
    state["updated_at"] = reviewed_at


def main() -> int:
    args = parse_args()
    state = load_state()
    target_path, run_record = resolve_target_path(args, state)
    if target_path is None or not target_path.exists():
        result = {
            "status": "skipped",
            "reason": "No draft path available for Claude review.",
            "path": None,
            "changed": False,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    original = target_path.read_text(encoding="utf-8")
    revised = review_document(target_path, original, args.model, args.passes)
    changed = revised != original

    if changed and not args.dry_run:
        target_path.write_text(revised, encoding="utf-8")
    if not args.dry_run:
        update_state_with_review(state, target_path, changed, args.model, run_record)
        write_state(state)

    result = {
        "status": "reviewed",
        "path": str(target_path),
        "changed": changed,
        "model": args.model,
        "passes": args.passes,
        "review_engine": "claude_code_only",
        "dry_run": args.dry_run,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
