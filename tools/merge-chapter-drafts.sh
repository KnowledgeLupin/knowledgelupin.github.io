#!/usr/bin/env bash

set -euo pipefail
shopt -s nullglob

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHAPTER_DIR="$ROOT_DIR/latex/linear-algebra/chapters"

usage() {
  cat <<'USAGE'
Usage: bash tools/merge-chapter-drafts.sh --run-id <run_id> [--run-dir <path>] [--chapters ch01,ch10] [--force]
USAGE
}

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

normalize_chapter_id() {
  local raw="$1"
  local body="${raw#ch}"
  body="${body#CH}"
  body="${body#Ch}"
  if [[ ! "$body" =~ ^[0-9]+$ ]]; then
    return 1
  fi
  printf '%02d' "$((10#$body))"
}

chapter_file_by_id() {
  local chapter_id="$1"
  local matches=("$CHAPTER_DIR/ch${chapter_id}-"*.tex)
  if [[ "${#matches[@]}" -ne 1 ]]; then
    return 1
  fi
  basename "${matches[0]}"
}

RUN_ID=""
RUN_DIR=""
FORCE="false"
CHAPTER_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-id)
      RUN_ID="${2:-}"
      shift 2
      ;;
    --run-dir)
      RUN_DIR="${2:-}"
      shift 2
      ;;
    --chapters)
      CHAPTER_FILTER="${2:-}"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$RUN_DIR" ]]; then
  if [[ -z "$RUN_ID" ]]; then
    echo "Either --run-id or --run-dir is required." >&2
    exit 1
  fi
  RUN_DIR="$ROOT_DIR/_reference/parallel-drafts/$RUN_ID"
fi

if [[ ! -d "$RUN_DIR" ]]; then
  echo "Run directory not found: $RUN_DIR" >&2
  exit 1
fi

REPORT_DIR="$RUN_DIR/reports"
READY_FILE="$REPORT_DIR/ready-to-merge"
MERGE_REPORT="$REPORT_DIR/merge-report.json"

if [[ "$FORCE" != "true" ]]; then
  if [[ ! -f "$READY_FILE" ]]; then
    echo "ready-to-merge marker not found: $READY_FILE" >&2
    exit 1
  fi
  if [[ "$(tr -d '[:space:]' < "$READY_FILE")" != "true" ]]; then
    echo "Merge gate is closed. Run did not pass strict checks." >&2
    exit 1
  fi
fi

missing=()
merged=()
targets=()

if [[ -n "$CHAPTER_FILTER" ]]; then
  IFS=',' read -r -a raw_tokens <<< "$CHAPTER_FILTER"
  for token in "${raw_tokens[@]}"; do
    trimmed="$(echo "$token" | tr -d '[:space:]')"
    if [[ -z "$trimmed" ]]; then
      continue
    fi
    if ! chapter_id="$(normalize_chapter_id "$trimmed")"; then
      echo "Invalid chapter token: $trimmed" >&2
      exit 1
    fi
    if ! chapter_file="$(chapter_file_by_id "$chapter_id")"; then
      echo "No chapter file found for token: $trimmed" >&2
      exit 1
    fi
    targets+=("$chapter_file")
  done
  if [[ "${#targets[@]}" -eq 0 ]]; then
    echo "No valid chapter target was resolved from --chapters." >&2
    exit 1
  fi
else
  for chapter_path in "$CHAPTER_DIR"/*.tex; do
    targets+=("$(basename "$chapter_path")")
  done
fi

for chapter_file in "${targets[@]}"; do
  draft_path="$RUN_DIR/chapters/$chapter_file"
  if [[ ! -f "$draft_path" ]]; then
    missing+=("$chapter_file")
  fi
done

if [[ "${#missing[@]}" -gt 0 ]]; then
  echo "Missing draft files:" >&2
  printf ' - %s\n' "${missing[@]}" >&2
  exit 1
fi

for chapter_file in "${targets[@]}"; do
  chapter_path="$CHAPTER_DIR/$chapter_file"
  draft_path="$RUN_DIR/chapters/$chapter_file"
  cp "$draft_path" "$chapter_path"
  merged+=("$chapter_file")
done

mkdir -p "$REPORT_DIR"

{
  echo "{"
  echo "  \"run_dir\": \"$(json_escape "$RUN_DIR")\","
  echo "  \"merged_count\": ${#merged[@]},"
  echo "  \"forced\": $FORCE,"
  echo "  \"chapter_filter\": \"$(json_escape "${CHAPTER_FILTER:-all}")\","
  echo "  \"merged_files\": ["
  for i in "${!merged[@]}"; do
    comma=","
    if [[ "$i" -eq "$((${#merged[@]} - 1))" ]]; then
      comma=""
    fi
    echo "    \"$(json_escape "${merged[$i]}")\"$comma"
  done
  echo "  ]"
  echo "}"
} > "$MERGE_REPORT"

echo "Merged ${#merged[@]} chapter drafts into $CHAPTER_DIR"
echo "Report: $MERGE_REPORT"
