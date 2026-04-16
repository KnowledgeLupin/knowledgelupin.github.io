#!/usr/bin/env python3
"""Check SEO readiness for a linear algebra blog draft or post."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "_site"
DEFAULT_IMAGE = "/assets/pdf/linear-algebra/linear-algebra-notes-latest-page1.png"
GENERIC_TITLE_PHRASES = {"대상과 응용 범위", "개요", "개관", "소개"}
GENERIC_SLUG_TOKENS = {"scope", "overview", "introduction", "applications"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, help="Markdown draft or post path.")
    parser.add_argument("--html", help="Optional built HTML path.")
    parser.add_argument("--require-html", action="store_true", help="Fail when built HTML is missing.")
    return parser.parse_args()


def normalize_text(text: str) -> str:
    lowered = text.replace("`", " ").lower()
    tokens = re.findall(r"[a-z0-9가-힣]+", lowered)
    return " ".join(tokens)


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        _, block, _ = text.split("---\n", 2)
    except ValueError:
        return {}
    result: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def strip_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def prose_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for chunk in re.split(r"\n\s*\n", strip_front_matter(text)):
        stripped = chunk.strip()
        if not stripped or stripped.startswith("#"):
            continue
        blocks.append(stripped)
    return blocks


def first_query(text: str) -> str:
    return text.strip()


def query_in_opening(text: str, query: str) -> bool:
    normalized_query = normalize_text(query)
    if not normalized_query:
        return False
    query_tokens = normalized_query.split()
    opening = " ".join(normalize_text(block) for block in prose_blocks(text)[:2])
    if normalized_query in opening:
        return True
    matched = sum(1 for token in query_tokens if token in opening)
    return matched >= max(1, len(query_tokens) - 1)


def query_in_heading(text: str, query: str) -> bool:
    normalized_query = normalize_text(query)
    if not normalized_query:
        return False
    query_tokens = normalized_query.split()
    for line in strip_front_matter(text).splitlines():
        if not (line.startswith("# ") or line.startswith("## ")):
            continue
        normalized_heading = normalize_text(line)
        if normalized_query in normalized_heading:
            return True
        matched = sum(1 for token in query_tokens if token in normalized_heading)
        if matched >= max(1, len(query_tokens) - 1):
            return True
    return False


def is_generic_title(title: str) -> bool:
    return any(phrase in title for phrase in GENERIC_TITLE_PHRASES)


def is_generic_slug(slug: str) -> bool:
    tokens = set(normalize_text(slug).split())
    return bool(tokens & GENERIC_SLUG_TOKENS)


def derive_html_path(markdown_path: Path) -> Path:
    stem = markdown_path.stem
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    return SITE_DIR / "posts" / stem / "index.html"


def inspect_html(path: Path, require_html: bool) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "issues": ["missing_built_html"] if require_html else []}
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    description = re.search(r'<meta name="description" content="([^"]*)"', text)
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', text)
    og_image = re.search(r'<meta property="og:image" content="([^"]*)"', text)
    if not description or not description.group(1).strip():
        issues.append("missing_html_description")
    if not canonical or not canonical.group(1).strip():
        issues.append("missing_canonical")
    if not og_image or not og_image.group(1).strip():
        issues.append("missing_og_image")
    return {
        "exists": True,
        "issues": issues,
        "description": description.group(1).strip() if description else "",
        "canonical": canonical.group(1).strip() if canonical else "",
        "og_image": og_image.group(1).strip() if og_image else "",
    }


def main() -> int:
    args = parse_args()
    markdown_path = Path(args.path).resolve()
    text = markdown_path.read_text(encoding="utf-8")
    front = parse_front_matter(text)
    html_path = Path(args.html).resolve() if args.html else derive_html_path(markdown_path)

    issues: list[str] = []
    title = front.get("title", "")
    slug = front.get("slug", "")
    description = front.get("description", "")
    excerpt = front.get("excerpt", "")
    image = front.get("image", "")
    query = first_query(title)

    if not title:
        issues.append("missing_title")
    if not slug:
        issues.append("missing_slug")
    if not description:
        issues.append("missing_description")
    if not excerpt:
        issues.append("missing_excerpt")
    if not image:
        issues.append("missing_image")
    if normalize_text(description) == normalize_text(title):
        issues.append("description_repeats_title")
    if normalize_text(excerpt) == normalize_text(title):
        issues.append("excerpt_repeats_title")
    if normalize_text(excerpt) == normalize_text(description):
        issues.append("excerpt_repeats_description")
    if is_generic_title(title):
        issues.append("weak_title")
    if is_generic_slug(slug):
        issues.append("weak_slug")
    if not query_in_opening(text, query):
        issues.append("missing_query_in_opening")
    if not query_in_heading(text, query):
        issues.append("missing_query_in_headings")
    html_report = inspect_html(html_path, args.require_html)
    issues.extend(html_report["issues"])

    result = {
        "passed": not issues,
        "path": str(markdown_path),
        "html_path": str(html_path),
        "issues": issues,
        "front_matter": {
            "title": title,
            "slug": slug,
            "description": description,
            "excerpt": excerpt,
            "image": image,
            "uses_default_image": image == DEFAULT_IMAGE,
        },
        "html": html_report,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
