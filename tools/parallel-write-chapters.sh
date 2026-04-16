#!/usr/bin/env bash

set -euo pipefail
shopt -s nullglob

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHAPTER_DIR="$ROOT_DIR/latex/linear-algebra/chapters"
WRITING_REFERENCE_PATH="$ROOT_DIR/_reference/2026-04-16-linear-algebra-blog-writing-spec.md"
PLAN_PATH="$ROOT_DIR/_reference/2026-02-25-linear-algebra-final-plan.md"
PREAMBLE_PATH="$ROOT_DIR/latex/linear-algebra/preamble.tex"
VALIDATOR_SCRIPT="$ROOT_DIR/tools/validate-chapter-draft.sh"
MERGE_SCRIPT="$ROOT_DIR/tools/merge-chapter-drafts.sh"
SCRIPT_PATH="$ROOT_DIR/tools/parallel-write-chapters.sh"

DEFAULT_SCOPE="ch1-ch16"
DEFAULT_CONCURRENCY=4
DEFAULT_GATE="strict"
DEFAULT_PROOF_POLICY="full"
DEFAULT_REFERENCE_MODE="three-books"
DEFAULT_REFERENCE_CACHE_MODE="reuse"
MAX_ATTEMPTS=3
SKILL_NAME="linear-algebra-chapter-writer"

PDF_KOREAN_PATH="/Users/kwkwon/Library/Mobile Documents/com~apple~CloudDocs/Documents/전공/대수학/선형대수와 군 - OCR-TOC.pdf"
PDF_HK_PATH="/Users/kwkwon/Library/Mobile Documents/com~apple~CloudDocs/Documents/전공/대수학/Linear Algebra, 2nd ed - Kenneth Hoffman, Ray Kunze, 1971.pdf"
PDF_LANG_PATH="/Users/kwkwon/Library/Mobile Documents/com~apple~CloudDocs/Documents/전공/대수학/serge-lang-linear-algebra.pdf"

SCOPE="$DEFAULT_SCOPE"
CONCURRENCY="$DEFAULT_CONCURRENCY"
GATE="$DEFAULT_GATE"
PROOF_POLICY="$DEFAULT_PROOF_POLICY"
REFERENCE_MODE="$DEFAULT_REFERENCE_MODE"
REFERENCE_CACHE_MODE="$DEFAULT_REFERENCE_CACHE_MODE"
RUN_ID=""
CHAPTER_FILTER=""
CHAPTER_FILTER_NORMALIZED=""

RUN_DIR=""
REFERENCE_DIR=""
REFERENCE_CACHE_DIR=""
WORKER_RESULT_PATH=""

REFERENCE_CONTEXT_PATH=""
REFERENCE_STATUS="off"
REFERENCE_REASON="mode_off"
REFERENCE_SOURCE_PRIORITY="off"
REFERENCE_SOURCES_USED="none"
REFERENCE_HIT_SUMMARY=""

usage() {
  cat <<'USAGE'
Usage:
  bash tools/parallel-write-chapters.sh \
    --scope ch1-ch16 \
    --concurrency 4 \
    --gate strict \
    --proof-policy full \
    --reference-mode three-books|off \
    --reference-cache refresh|reuse \
    [--run-id <run_id>] \
    [--chapters ch01,ch10]

Notes:
  - Uses fixed worker map W1..W4.
  - Runs each chapter up to 3 attempts (1 + 2 retries).
  - Writes run artifacts to _reference/parallel-drafts/<run_id>/.
USAGE
}

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

append_csv_unique() {
  local csv="$1"
  local item="$2"

  if [[ -z "$item" ]]; then
    echo "$csv"
    return 0
  fi

  if [[ -z "$csv" ]]; then
    echo "$item"
    return 0
  fi

  if [[ ",$csv," == *",$item,"* ]]; then
    echo "$csv"
  else
    echo "$csv,$item"
  fi
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

worker_chapters() {
  local worker_id="$1"
  case "$worker_id" in
    W1) echo "01 05 09 13" ;;
    W2) echo "02 06 10 14" ;;
    W3) echo "03 07 11 15" ;;
    W4) echo "04 08 12 16" ;;
    *)
      return 1
      ;;
  esac
}

is_selected_chapter() {
  local chapter_id="$1"
  if [[ -z "$CHAPTER_FILTER_NORMALIZED" ]]; then
    return 0
  fi
  if [[ ",$CHAPTER_FILTER_NORMALIZED," == *",$chapter_id,"* ]]; then
    return 0
  fi
  return 1
}

first_failed_rule() {
  local report_path="$1"
  if [[ ! -f "$report_path" ]]; then
    echo ""
    return 0
  fi
  awk -F'"' '
    /"failed_rules": \[/ { in_rules = 1; next }
    in_rules && /\]/ { in_rules = 0 }
    in_rules && /"/ { print $2; exit }
  ' "$report_path"
}

source_pdf_path() {
  local source="$1"
  case "$source" in
    hk) echo "$PDF_HK_PATH" ;;
    lang) echo "$PDF_LANG_PATH" ;;
    korean-ocr) echo "$PDF_KOREAN_PATH" ;;
    *)
      return 1
      ;;
  esac
}

chapter_source_priority_for_id() {
  local chapter_num="$((10#$1))"

  if [[ "$chapter_num" -eq 16 ]]; then
    echo "hk,lang,korean-ocr"
    return 0
  fi

  if [[ "$chapter_num" -ge 9 && "$chapter_num" -le 15 ]]; then
    echo "lang,hk,korean-ocr"
    return 0
  fi

  if [[ "$chapter_num" -ge 7 && "$chapter_num" -le 13 ]]; then
    echo "hk,korean-ocr,lang"
    return 0
  fi

  if [[ "$chapter_num" -ge 1 && "$chapter_num" -le 8 ]]; then
    echo "korean-ocr,hk,lang"
    return 0
  fi

  echo "hk,lang,korean-ocr"
}

chapter_keyword_pattern_for_id() {
  local chapter_id="$1"
  case "$chapter_id" in
    01) echo 'gauss|elimination|row[- ]?reduction|rref|linear systems|증강행렬|소거법|연립일차' ;;
    02) echo 'matrix operations|invertible|inverse matrix|rank|column space|가역|역행렬|랭크' ;;
    03) echo 'vector space|subspace|span|linear independence|벡터공간|부분공간|생성|일차독립' ;;
    04) echo 'basis|dimension|exchange theorem|coordinate vector|기저|차원|교체정리|좌표' ;;
    05) echo 'linear map|kernel|image|rank[- ]?nullity|선형사상|핵|상|랭크-널리티' ;;
    06) echo 'matrix representation|change of basis|similarity|기저변환|유사|행렬표현' ;;
    07) echo 'dual space|dual map|transpose|annihilator|쌍대공간|쌍대사상|전치|소멸자' ;;
    08) echo 'determinant|leibniz|cofactor|adjugate|행렬식|여인수|수반행렬' ;;
    09) echo 'operator polynomial|minimal polynomial|characteristic polynomial|cayley|최소다항식|특성다항식|케일리-해밀턴' ;;
    10) echo 'eigenvalue|eigenvector|eigenspace|diagonalization|고유값|고유벡터|대각화' ;;
    11) echo 'invariant subspace|triangularization|nilpotent|generalized eigenvector|불변부분공간|삼각화|멱영|일반화 고유벡터' ;;
    12) echo 'primary decomposition|cyclic decomposition|annihilator|프라이머리 분해|순환 분해|소멸다항식' ;;
    13) echo 'jordan|jordan block|jordan canonical form|조르당|조르당 표준형' ;;
    14) echo 'inner product|gram[- ]?schmidt|orthogonal projection|least squares|내적|직교화|직교투영|최소제곱' ;;
    15) echo 'adjoint|normal operator|self[- ]adjoint|unitary|spectral theorem|수반|정규연산자|유니터리|스펙트럴' ;;
    16) echo 'bilinear form|hermitian form|quadratic form|쌍선형형식|에르미트형식|이차형식' ;;
    *)
      echo 'linear algebra|vector space|matrix|선형대수|벡터공간|행렬'
      ;;
  esac
}

sanitize_reference_snippet() {
  sed 's/\r//g; s/\f/ /g' |
    sed 's/[[:space:]]\+/ /g; s/^[[:space:]]*//; s/[[:space:]]*$//' |
    awk 'length($0) >= 8'
}

sanitize_ocr_snippet() {
  sed 's/\r//g; s/\f/ /g' |
    sed 's/[[:space:]]\+/ /g; s/^[[:space:]]*//; s/[[:space:]]*$//' |
    awk '
      length($0) < 10 { next }
      $0 ~ /^[[:digit:][:space:][:punct:]]+$/ { next }
      {
        n = split($0, parts, " ")
        if (n < 2) { next }
        print
      }
    '
}

emit_json_array_from_csv() {
  local csv="$1"
  local indent="$2"

  if [[ -z "$csv" || "$csv" == "none" ]]; then
    return 0
  fi

  IFS=',' read -r -a items <<< "$csv"
  local i
  for i in "${!items[@]}"; do
    local comma=","
    if [[ "$i" -eq "$(( ${#items[@]} - 1 ))" ]]; then
      comma=""
    fi
    echo "${indent}\"$(json_escape "${items[$i]}")\"$comma"
  done
}

probe_reference_sources() {
  local probe_file="$RUN_DIR/reports/reference-probe.txt"
  : > "$probe_file"

  if [[ "$REFERENCE_MODE" != "three-books" ]]; then
    echo "reference_mode=off" >> "$probe_file"
    return 0
  fi

  local source path
  for source in korean-ocr hk lang; do
    path="$(source_pdf_path "$source")"
    if pdfinfo "$path" >/dev/null 2>&1; then
      echo "$source=ok" >> "$probe_file"
    else
      echo "$source=warn_unreadable" >> "$probe_file"
      echo "Warning: reference source probe failed for $source: $path" >&2
    fi
  done
}

ensure_reference_cache() {
  if [[ "$REFERENCE_MODE" != "three-books" ]]; then
    return 0
  fi

  mkdir -p "$REFERENCE_CACHE_DIR"

  local rc=0
  local source path cache_file tmp_file
  for source in hk lang korean-ocr; do
    path="$(source_pdf_path "$source")"
    cache_file="$REFERENCE_CACHE_DIR/$source.txt"

    if [[ "$REFERENCE_CACHE_MODE" == "refresh" || ! -s "$cache_file" ]]; then
      if ! pdfinfo "$path" >/dev/null 2>&1; then
        echo "Warning: pdfinfo failed for $source ($path)" >&2
        rc=1
        continue
      fi

      tmp_file="$cache_file.tmp"
      if ! pdftotext "$path" - > "$tmp_file" 2>/dev/null; then
        echo "Warning: pdftotext failed for $source ($path)" >&2
        rc=1
        rm -f "$tmp_file"
        continue
      fi

      tr -d '\r' < "$tmp_file" > "$cache_file"
      rm -f "$tmp_file"
    fi
  done

  return "$rc"
}

extract_context_from_source() {
  local source="$1"
  local cache_file="$2"
  local pattern="$3"
  local context_file="$4"
  local chapter_tag="$5"

  local line_file="$RUN_DIR/tmp/${chapter_tag}-${source}-hits.txt"
  local hit_count=0

  rg -n -i "$pattern" "$cache_file" | head -n 30 > "$line_file" || true

  if [[ ! -s "$line_file" ]]; then
    echo "0"
    return 1
  fi

  echo "## Source: $source" >> "$context_file"

  while IFS=: read -r line_no _rest; do
    [[ -z "$line_no" ]] && continue

    local start_line=1
    if [[ "$line_no" -gt 2 ]]; then
      start_line=$((line_no - 2))
    fi
    local end_line=$((line_no + 2))
    local snippet_file="$RUN_DIR/tmp/${chapter_tag}-${source}-${line_no}.txt"

    awk -v s="$start_line" -v e="$end_line" 'NR>=s && NR<=e {print}' "$cache_file" > "$snippet_file"

    echo "### Hit line $line_no" >> "$context_file"
    if [[ "$source" == "korean-ocr" ]]; then
      sanitize_ocr_snippet < "$snippet_file" >> "$context_file" || true
    else
      sanitize_reference_snippet < "$snippet_file" >> "$context_file" || true
    fi
    echo "" >> "$context_file"

    hit_count=$((hit_count + 1))
    if [[ "$hit_count" -ge 8 ]]; then
      break
    fi
  done < "$line_file"

  echo "$hit_count"
  if [[ "$hit_count" -gt 0 ]]; then
    return 0
  fi
  return 1
}

write_reference_report() {
  local chapter_tag="$1"
  local status="$2"
  local reason="$3"
  local attempt="$4"
  local retry_count="$5"
  local context_path="$6"
  local source_priority="$7"
  local sources_used="$8"
  local hit_summary="$9"

  local report_path="$RUN_DIR/reports/${chapter_tag}-reference.json"

  {
    echo "{"
    echo "  \"chapter\": \"$(json_escape "$chapter_tag")\","
    echo "  \"reference_mode\": \"$(json_escape "$REFERENCE_MODE")\","
    echo "  \"status\": \"$(json_escape "$status")\","
    echo "  \"reason\": \"$(json_escape "$reason")\","
    echo "  \"attempt\": $attempt,"
    echo "  \"reference_retry_count\": $retry_count,"
    echo "  \"context_path\": \"$(json_escape "$context_path")\","
    echo "  \"source_priority\": \"$(json_escape "$source_priority")\","
    echo "  \"sources_used\": ["
    emit_json_array_from_csv "$sources_used" "    "
    echo "  ],"
    echo "  \"hit_summary\": \"$(json_escape "$hit_summary")\""
    echo "}"
  } > "$report_path"
}

prepare_reference_context_for_chapter() {
  local chapter_id="$1"
  local chapter_tag="$2"
  local attempt="$3"
  local reference_retry_count="$4"

  REFERENCE_CONTEXT_PATH="$REFERENCE_DIR/${chapter_tag}-context.md"
  REFERENCE_STATUS="off"
  REFERENCE_REASON="mode_off"
  REFERENCE_SOURCE_PRIORITY="off"
  REFERENCE_SOURCES_USED="none"
  REFERENCE_HIT_SUMMARY=""

  if [[ "$REFERENCE_MODE" == "off" ]]; then
    cat > "$REFERENCE_CONTEXT_PATH" <<EOF_CTX
# Reference Context for ${chapter_tag}

- reference_mode: off
- note: external three-book references are disabled for this run.
EOF_CTX
    write_reference_report "$chapter_tag" "$REFERENCE_STATUS" "$REFERENCE_REASON" "$attempt" "$reference_retry_count" "$REFERENCE_CONTEXT_PATH" "$REFERENCE_SOURCE_PRIORITY" "$REFERENCE_SOURCES_USED" "$REFERENCE_HIT_SUMMARY"
    return 0
  fi

  if ! ensure_reference_cache; then
    echo "Warning: reference cache preparation had partial failures (chapter $chapter_tag, attempt $attempt)." >&2
  fi

  local source_priority
  local keyword_pattern
  source_priority="$(chapter_source_priority_for_id "$chapter_id")"
  keyword_pattern="$(chapter_keyword_pattern_for_id "$chapter_id")"

  REFERENCE_SOURCE_PRIORITY="$source_priority"

  local tmp_context="$RUN_DIR/tmp/${chapter_tag}-context-attempt${attempt}.md"
  {
    echo "# Reference Context for ${chapter_tag}"
    echo ""
    echo "- source_priority: $source_priority"
    echo "- keyword_pattern: $keyword_pattern"
    echo "- generated_at: $(date '+%Y-%m-%d %H:%M:%S %z')"
    echo ""
  } > "$tmp_context"

  local total_hits=0
  local sources_used=""
  local hit_summary=""

  IFS=',' read -r -a priority_sources <<< "$source_priority"
  local source
  for source in "${priority_sources[@]}"; do
    local cache_file="$REFERENCE_CACHE_DIR/$source.txt"
    if [[ ! -s "$cache_file" ]]; then
      hit_summary="${hit_summary}${source}:cache_missing;"
      continue
    fi

    local hits
    hits="$(extract_context_from_source "$source" "$cache_file" "$keyword_pattern" "$tmp_context" "$chapter_tag")"
    if [[ "$hits" -gt 0 ]]; then
      total_hits=$((total_hits + hits))
      sources_used="$(append_csv_unique "$sources_used" "$source")"
    fi
    hit_summary="${hit_summary}${source}:${hits};"
  done

  if [[ "$total_hits" -eq 0 ]]; then
    cp "$tmp_context" "$REFERENCE_CONTEXT_PATH" || true
    REFERENCE_STATUS="failed"
    REFERENCE_REASON="no_keyword_hits_or_cache_missing"
    REFERENCE_SOURCES_USED="${sources_used:-none}"
    REFERENCE_HIT_SUMMARY="$hit_summary"
    write_reference_report "$chapter_tag" "$REFERENCE_STATUS" "$REFERENCE_REASON" "$attempt" "$reference_retry_count" "$REFERENCE_CONTEXT_PATH" "$REFERENCE_SOURCE_PRIORITY" "$REFERENCE_SOURCES_USED" "$REFERENCE_HIT_SUMMARY"
    return 1
  fi

  local context_lines
  context_lines="$(wc -l < "$tmp_context" | tr -d ' ')"
  if [[ "$context_lines" -lt 12 ]]; then
    cp "$tmp_context" "$REFERENCE_CONTEXT_PATH" || true
    REFERENCE_STATUS="failed"
    REFERENCE_REASON="context_too_short_after_filter"
    REFERENCE_SOURCES_USED="${sources_used:-none}"
    REFERENCE_HIT_SUMMARY="$hit_summary"
    write_reference_report "$chapter_tag" "$REFERENCE_STATUS" "$REFERENCE_REASON" "$attempt" "$reference_retry_count" "$REFERENCE_CONTEXT_PATH" "$REFERENCE_SOURCE_PRIORITY" "$REFERENCE_SOURCES_USED" "$REFERENCE_HIT_SUMMARY"
    return 1
  fi

  mv "$tmp_context" "$REFERENCE_CONTEXT_PATH"
  REFERENCE_STATUS="ready"
  REFERENCE_REASON="ok"
  REFERENCE_SOURCES_USED="${sources_used:-none}"
  REFERENCE_HIT_SUMMARY="$hit_summary"

  write_reference_report "$chapter_tag" "$REFERENCE_STATUS" "$REFERENCE_REASON" "$attempt" "$reference_retry_count" "$REFERENCE_CONTEXT_PATH" "$REFERENCE_SOURCE_PRIORITY" "$REFERENCE_SOURCES_USED" "$REFERENCE_HIT_SUMMARY"
  return 0
}

build_prompt_file() {
  local prompt_path="$1"
  local chapter_id="$2"
  local chapter_file="$3"
  local chapter_path="$4"
  local reference_context_path="$5"
  local source_priority="$6"
  local reference_mode="$7"

  cat > "$prompt_path" <<EOF
Use \$${SKILL_NAME}.

Task:
Rewrite and complete chapter ch${chapter_id} in file ${chapter_file}.

Strict requirements:
1. Output raw LaTeX chapter content only.
2. Do not include markdown code fences or commentary.
3. Keep Korean textbook voice with polite explanatory paragraphs.
4. Keep formal blocks (\`정의\`, \`정리\`, \`증명\`) rigorous.
5. Use full proof policy for every theorem.
6. Include proof-strategy paragraph before each proof.
7. Include interpretation paragraph after each proof.
8. Include at least two warning blocks.
9. Include at least one self-diagnosis quiz block with three or more items.
10. Include graded exercises A/B/C with minimum counts A>=6, B>=4, C>=2.
11. Keep chapter macros and templates compatible with preamble macros.
12. Never copy textbook sentences verbatim.
13. Never include visible citation tags, reference notes, or footnotes in chapter body.

Repository context:
- Chapter file: ${chapter_path}
- Writing reference: ${WRITING_REFERENCE_PATH}
- Project plan: ${PLAN_PATH}
- Preamble/macros: ${PREAMBLE_PATH}
- Proof policy: ${PROOF_POLICY}
- Reference mode: ${reference_mode}
- Source priority: ${source_priority}
EOF

  if [[ "$reference_mode" == "three-books" ]]; then
    {
      echo "- Reference context path (required): ${reference_context_path}"
      echo ""
      echo "Reference usage policy:"
      echo "- Use reference context for concept flow, theorem order, and proof strategy only."
      echo "- Rewrite all content in fresh wording."
      echo "- Do not copy textbook phrasing."
      echo "- Do not expose source citations in the chapter output."
      echo ""
      echo "Reference context excerpt:"
      sed -n '1,220p' "$reference_context_path"
    } >> "$prompt_path"
  fi

  cat >> "$prompt_path" <<'EOF'

Output:
- Return final chapter content only.
- Do not wrap output in code fences.
EOF
}

detect_long_english_sequence() {
  local draft_path="$1"
  if rg -n -i '([A-Za-z]{3,}[[:space:]]+){18,}[A-Za-z]{3,}' "$draft_path" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

write_generation_failure_report() {
  local report_path="$1"
  local chapter_tag="$2"
  local draft_path="$3"
  local reason="$4"
  local attempt_count="$5"
  mkdir -p "$(dirname "$report_path")"
  {
    echo "{"
    echo "  \"chapter\": \"$(json_escape "$chapter_tag")\","
    echo "  \"draft\": \"$(json_escape "$draft_path")\","
    echo "  \"gate\": \"$(json_escape "$GATE")\","
    echo "  \"status\": \"fail\","
    echo "  \"checks\": [],"
    echo "  \"failed_rules\": [\"$(json_escape "$reason")\"],"
    echo "  \"attempts\": $attempt_count"
    echo "}"
  } > "$report_path"
}

run_single_chapter() {
  local worker_id="$1"
  local chapter_id="$2"

  local chapter_file
  local chapter_path
  local chapter_tag="ch${chapter_id}"
  local draft_path
  local report_path

  local attempt=1
  local final_reason="unknown_failure"
  local generation_status="fail"
  local generation_reason="unknown_failure"

  local reference_status="off"
  local reference_reason="mode_off"
  local reference_source_priority="off"
  local reference_sources_used="none"
  local reference_retry_count=0

  if ! chapter_file="$(chapter_file_by_id "$chapter_id")"; then
    echo "${chapter_tag}|unknown|0|fail|missing_source_file|failed|missing_source_file|0|none|off" >> "$WORKER_RESULT_PATH"
    return 0
  fi

  chapter_path="$CHAPTER_DIR/$chapter_file"
  draft_path="$RUN_DIR/chapters/$chapter_file"
  report_path="$RUN_DIR/reports/${chapter_tag}-validation.json"

  while [[ "$attempt" -le "$MAX_ATTEMPTS" ]]; do
    local prompt_path="$RUN_DIR/tmp/${chapter_tag}-prompt.txt"
    local attempt_draft="$RUN_DIR/tmp/${chapter_file}.attempt${attempt}.txt"
    local attempt_log="$RUN_DIR/logs/${chapter_tag}-attempt${attempt}.jsonl"
    local latest_log="$RUN_DIR/logs/${chapter_tag}.jsonl"

    if ! prepare_reference_context_for_chapter "$chapter_id" "$chapter_tag" "$attempt" "$reference_retry_count"; then
      reference_status="$REFERENCE_STATUS"
      reference_reason="$REFERENCE_REASON"
      reference_source_priority="$REFERENCE_SOURCE_PRIORITY"
      reference_sources_used="$REFERENCE_SOURCES_USED"
      if [[ "$attempt" -lt "$MAX_ATTEMPTS" ]]; then
        reference_retry_count=$((reference_retry_count + 1))
      fi

      final_reason="reference_failed:${reference_reason}"
      generation_reason="$final_reason"
      attempt=$((attempt + 1))
      continue
    fi

    reference_status="$REFERENCE_STATUS"
    reference_reason="$REFERENCE_REASON"
    reference_source_priority="$REFERENCE_SOURCE_PRIORITY"
    reference_sources_used="$REFERENCE_SOURCES_USED"

    build_prompt_file "$prompt_path" "$chapter_id" "$chapter_file" "$chapter_path" "$REFERENCE_CONTEXT_PATH" "$reference_source_priority" "$REFERENCE_MODE"

    if codex exec \
      --ephemeral \
      -s read-only \
      -C "$ROOT_DIR" \
      --json \
      -o "$attempt_draft" \
      - < "$prompt_path" > "$attempt_log" 2>&1; then

      cp "$attempt_log" "$latest_log"

      if [[ -s "$attempt_draft" ]]; then
        cp "$attempt_draft" "$draft_path"

        if bash "$VALIDATOR_SCRIPT" --draft "$draft_path" --report "$report_path" --gate "$GATE" --chapter "$chapter_tag" >/dev/null 2>&1; then
          if detect_long_english_sequence "$draft_path"; then
            final_reason="anti_copy_suspected"
            generation_reason="$final_reason"
          else
            generation_status="success"
            generation_reason="ok"
            echo "${chapter_tag}|${chapter_file}|${attempt}|${generation_status}|${generation_reason}|${reference_status}|${reference_reason}|${reference_retry_count}|${reference_sources_used}|${reference_source_priority}" >> "$WORKER_RESULT_PATH"
            return 0
          fi
        else
          local failed_rule
          failed_rule="$(first_failed_rule "$report_path")"
          if [[ -n "$failed_rule" ]]; then
            final_reason="validation_failed:${failed_rule}"
          else
            final_reason="validation_failed"
          fi
          generation_reason="$final_reason"
        fi
      else
        final_reason="empty_output"
        generation_reason="$final_reason"
      fi
    else
      cp "$attempt_log" "$latest_log"
      final_reason="codex_exec_failed"
      generation_reason="$final_reason"
    fi

    attempt=$((attempt + 1))
  done

  write_generation_failure_report "$report_path" "$chapter_tag" "$draft_path" "$final_reason" "$((attempt - 1))"
  echo "${chapter_tag}|${chapter_file}|$((attempt - 1))|fail|${generation_reason}|${reference_status}|${reference_reason}|${reference_retry_count}|${reference_sources_used}|${reference_source_priority}" >> "$WORKER_RESULT_PATH"
  return 0
}

run_worker() {
  local worker_id="$1"
  local chapters
  chapters="$(worker_chapters "$worker_id")"
  : > "$WORKER_RESULT_PATH"

  local chapter_id
  for chapter_id in $chapters; do
    if is_selected_chapter "$chapter_id"; then
      run_single_chapter "$worker_id" "$chapter_id"
    fi
  done
}

run_internal_worker_mode() {
  local worker_id="$1"
  RUN_DIR="$2"
  GATE="$3"
  PROOF_POLICY="$4"
  CHAPTER_FILTER_NORMALIZED="$5"
  REFERENCE_MODE="$6"
  REFERENCE_CACHE_MODE="$7"

  REFERENCE_DIR="$RUN_DIR/references"
  REFERENCE_CACHE_DIR="$REFERENCE_DIR/cache"
  WORKER_RESULT_PATH="$RUN_DIR/attempts/${worker_id}.tsv"

  run_worker "$worker_id"
}

if [[ "${1:-}" == "__run_worker" ]]; then
  if [[ $# -ne 8 ]]; then
    echo "Internal worker mode argument mismatch." >&2
    exit 1
  fi
  run_internal_worker_mode "$2" "$3" "$4" "$5" "$6" "$7" "$8"
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)
      SCOPE="${2:-}"
      shift 2
      ;;
    --concurrency)
      CONCURRENCY="${2:-}"
      shift 2
      ;;
    --gate)
      GATE="${2:-}"
      shift 2
      ;;
    --proof-policy)
      PROOF_POLICY="${2:-}"
      shift 2
      ;;
    --reference-mode)
      REFERENCE_MODE="${2:-}"
      shift 2
      ;;
    --reference-cache)
      REFERENCE_CACHE_MODE="${2:-}"
      shift 2
      ;;
    --run-id)
      RUN_ID="${2:-}"
      shift 2
      ;;
    --chapters)
      CHAPTER_FILTER="${2:-}"
      shift 2
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

if [[ "$SCOPE" != "ch1-ch16" ]]; then
  echo "Unsupported scope: $SCOPE (only ch1-ch16 is supported)." >&2
  exit 1
fi

if [[ ! "$CONCURRENCY" =~ ^[0-9]+$ ]] || [[ "$CONCURRENCY" -lt 1 ]]; then
  echo "Invalid concurrency: $CONCURRENCY" >&2
  exit 1
fi

if [[ "$GATE" != "strict" && "$GATE" != "balanced" && "$GATE" != "draft-first" ]]; then
  echo "Unsupported gate: $GATE" >&2
  exit 1
fi

if [[ "$REFERENCE_MODE" != "three-books" && "$REFERENCE_MODE" != "off" ]]; then
  echo "Unsupported reference mode: $REFERENCE_MODE" >&2
  exit 1
fi

if [[ "$REFERENCE_CACHE_MODE" != "refresh" && "$REFERENCE_CACHE_MODE" != "reuse" ]]; then
  echo "Unsupported reference cache mode: $REFERENCE_CACHE_MODE" >&2
  exit 1
fi

if [[ -z "$RUN_ID" ]]; then
  RUN_ID="$(date +%Y%m%d-%H%M%S)"
fi

if [[ -n "$CHAPTER_FILTER" ]]; then
  IFS=',' read -r -a chapter_tokens <<< "$CHAPTER_FILTER"
  normalized_tokens=()
  for raw_token in "${chapter_tokens[@]}"; do
    token="$(echo "$raw_token" | tr -d '[:space:]')"
    if [[ -z "$token" ]]; then
      continue
    fi
    if ! norm="$(normalize_chapter_id "$token")"; then
      echo "Invalid chapter token in --chapters: $token" >&2
      exit 1
    fi
    normalized_tokens+=("$norm")
  done
  if [[ "${#normalized_tokens[@]}" -eq 0 ]]; then
    echo "--chapters was provided but no valid chapter token was found." >&2
    exit 1
  fi
  CHAPTER_FILTER_NORMALIZED="$(IFS=','; echo "${normalized_tokens[*]}")"
fi

for required in "$VALIDATOR_SCRIPT" "$MERGE_SCRIPT" "$WRITING_REFERENCE_PATH" "$PLAN_PATH" "$PREAMBLE_PATH"; do
  if [[ ! -f "$required" ]]; then
    echo "Required file not found: $required" >&2
    exit 1
  fi
done

if [[ "$REFERENCE_MODE" == "three-books" ]]; then
  for cmd in pdfinfo pdftotext rg; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Required command not found for reference mode: $cmd" >&2
      exit 1
    fi
  done
fi

RUN_DIR="$ROOT_DIR/_reference/parallel-drafts/$RUN_ID"
REFERENCE_DIR="$RUN_DIR/references"
REFERENCE_CACHE_DIR="$REFERENCE_DIR/cache"

mkdir -p "$RUN_DIR/chapters" "$RUN_DIR/logs" "$RUN_DIR/reports" "$RUN_DIR/attempts" "$RUN_DIR/tmp" "$REFERENCE_DIR" "$REFERENCE_CACHE_DIR"

{
  echo "scope=$SCOPE"
  echo "concurrency=$CONCURRENCY"
  echo "gate=$GATE"
  echo "proof_policy=$PROOF_POLICY"
  echo "reference_mode=$REFERENCE_MODE"
  echo "reference_cache_mode=$REFERENCE_CACHE_MODE"
  echo "chapters_filter=${CHAPTER_FILTER_NORMALIZED:-all}"
  echo "pdf_korean=$PDF_KOREAN_PATH"
  echo "pdf_hk=$PDF_HK_PATH"
  echo "pdf_lang=$PDF_LANG_PATH"
} > "$RUN_DIR/reports/run-config.txt"

probe_reference_sources
if [[ "$REFERENCE_MODE" == "three-books" ]]; then
  if ! ensure_reference_cache; then
    echo "Warning: initial reference cache warmup had partial failures; worker retries will handle per chapter." >&2
  fi
fi

printf '%s\n' W1 W2 W3 W4 | \
  xargs -P "$CONCURRENCY" -I{} bash "$SCRIPT_PATH" __run_worker "{}" "$RUN_DIR" "$GATE" "$PROOF_POLICY" "${CHAPTER_FILTER_NORMALIZED:-}" "$REFERENCE_MODE" "$REFERENCE_CACHE_MODE"

ALL_RESULTS="$RUN_DIR/attempts/all-results.tsv"
: > "$ALL_RESULTS"
for worker_file in "$RUN_DIR"/attempts/W*.tsv; do
  if [[ -f "$worker_file" ]]; then
    cat "$worker_file" >> "$ALL_RESULTS"
  fi
done

if [[ ! -s "$ALL_RESULTS" ]]; then
  echo "No chapter task was executed. Check chapter filter settings." >&2
  exit 1
fi

SUCCESS_COUNT=0
FAILURE_COUNT=0
RETRY_TOTAL=0
FAILED_CHAPTERS=()

REFERENCE_READY_CHAPTERS=()
REFERENCE_FAILED_CHAPTERS=()
REFERENCE_RETRY_TOTAL=0
REFERENCE_SOURCES_UNION=""

SORTED_RESULTS="$RUN_DIR/attempts/all-results.sorted.tsv"
sort -t'|' -k1,1 "$ALL_RESULTS" > "$SORTED_RESULTS"

while IFS='|' read -r chapter_tag chapter_file attempts generation_status generation_reason reference_status reference_reason reference_retry_count reference_sources_used source_priority; do
  retries=$((attempts - 1))
  RETRY_TOTAL=$((RETRY_TOTAL + retries))
  REFERENCE_RETRY_TOTAL=$((REFERENCE_RETRY_TOTAL + reference_retry_count))

  if [[ "$generation_status" == "success" ]]; then
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  else
    FAILURE_COUNT=$((FAILURE_COUNT + 1))
    FAILED_CHAPTERS+=("$chapter_tag")
  fi

  if [[ "$reference_status" == "ready" ]]; then
    REFERENCE_READY_CHAPTERS+=("$chapter_tag")
  fi
  if [[ "$reference_status" == "failed" ]]; then
    REFERENCE_FAILED_CHAPTERS+=("$chapter_tag")
  fi

  if [[ -n "$reference_sources_used" && "$reference_sources_used" != "none" ]]; then
    IFS=',' read -r -a source_arr <<< "$reference_sources_used"
    for source in "${source_arr[@]}"; do
      REFERENCE_SOURCES_UNION="$(append_csv_unique "$REFERENCE_SOURCES_UNION" "$source")"
    done
  fi
done < "$SORTED_RESULTS"

REFERENCE_STATUS_SUMMARY="pass"
if [[ "$REFERENCE_MODE" == "off" ]]; then
  REFERENCE_STATUS_SUMMARY="off"
elif [[ "${#REFERENCE_FAILED_CHAPTERS[@]}" -gt 0 ]]; then
  REFERENCE_STATUS_SUMMARY="fail"
fi

BUILD_STATUS="skipped"
MERGE_STATUS="skipped"
BUILD_LOG="$RUN_DIR/logs/latex-build.log"
MERGE_LOG="$RUN_DIR/logs/merge.log"

if [[ "$FAILURE_COUNT" -eq 0 ]]; then
  if [[ "$GATE" == "strict" ]]; then
    if bash "$ROOT_DIR/tools/latex-build.sh" all > "$BUILD_LOG" 2>&1; then
      BUILD_STATUS="pass"
    else
      BUILD_STATUS="fail"
    fi
  else
    BUILD_STATUS="not_required"
  fi
else
  BUILD_STATUS="skipped_due_chapter_failures"
fi

READY_TO_MERGE="false"
if [[ "$FAILURE_COUNT" -eq 0 ]]; then
  if [[ "$GATE" == "strict" && "$BUILD_STATUS" == "pass" ]]; then
    READY_TO_MERGE="true"
  fi
  if [[ "$GATE" != "strict" ]]; then
    READY_TO_MERGE="true"
  fi
fi

echo "$READY_TO_MERGE" > "$RUN_DIR/reports/ready-to-merge"

if [[ "$READY_TO_MERGE" == "true" ]]; then
  merge_cmd=(bash "$MERGE_SCRIPT" --run-dir "$RUN_DIR")
  if [[ -n "$CHAPTER_FILTER_NORMALIZED" ]]; then
    merge_cmd+=(--chapters "$CHAPTER_FILTER_NORMALIZED")
  fi
  if "${merge_cmd[@]}" > "$MERGE_LOG" 2>&1; then
    MERGE_STATUS="pass"
  else
    MERGE_STATUS="fail"
  fi
fi

SUMMARY_PATH="$RUN_DIR/reports/summary.json"

{
  echo "{"
  echo "  \"run_id\": \"$(json_escape "$RUN_ID")\","
  echo "  \"run_dir\": \"$(json_escape "$RUN_DIR")\","
  echo "  \"scope\": \"$(json_escape "$SCOPE")\","
  echo "  \"concurrency\": $CONCURRENCY,"
  echo "  \"gate\": \"$(json_escape "$GATE")\","
  echo "  \"proof_policy\": \"$(json_escape "$PROOF_POLICY")\","
  echo "  \"reference_mode\": \"$(json_escape "$REFERENCE_MODE")\","
  echo "  \"reference_cache_mode\": \"$(json_escape "$REFERENCE_CACHE_MODE")\","
  echo "  \"reference_status\": \"$(json_escape "$REFERENCE_STATUS_SUMMARY")\","
  echo "  \"reference_retry_count\": $REFERENCE_RETRY_TOTAL,"
  echo "  \"reference_retry_total\": $REFERENCE_RETRY_TOTAL,"
  echo "  \"reference_sources_used\": ["
  emit_json_array_from_csv "$REFERENCE_SOURCES_UNION" "    "
  echo "  ],"
  echo "  \"reference_ready_chapters\": ["
  for i in "${!REFERENCE_READY_CHAPTERS[@]}"; do
    comma=","
    if [[ "$i" -eq "$(( ${#REFERENCE_READY_CHAPTERS[@]} - 1 ))" ]]; then
      comma=""
    fi
    echo "    \"$(json_escape "${REFERENCE_READY_CHAPTERS[$i]}")\"$comma"
  done
  echo "  ],"
  echo "  \"reference_failed_chapters\": ["
  for i in "${!REFERENCE_FAILED_CHAPTERS[@]}"; do
    comma=","
    if [[ "$i" -eq "$(( ${#REFERENCE_FAILED_CHAPTERS[@]} - 1 ))" ]]; then
      comma=""
    fi
    echo "    \"$(json_escape "${REFERENCE_FAILED_CHAPTERS[$i]}")\"$comma"
  done
  echo "  ],"
  echo "  \"result\": {"
  echo "    \"success_count\": $SUCCESS_COUNT,"
  echo "    \"failure_count\": $FAILURE_COUNT,"
  echo "    \"retry_total\": $RETRY_TOTAL,"
  echo "    \"reference_ready_count\": ${#REFERENCE_READY_CHAPTERS[@]},"
  echo "    \"reference_failed_count\": ${#REFERENCE_FAILED_CHAPTERS[@]},"
  echo "    \"build_status\": \"$(json_escape "$BUILD_STATUS")\","
  echo "    \"merge_status\": \"$(json_escape "$MERGE_STATUS")\""
  echo "  },"
  echo "  \"chapters\": ["

  line_no=0
  total_lines="$(wc -l < "$SORTED_RESULTS" | tr -d ' ')"
  while IFS='|' read -r chapter_tag chapter_file attempts generation_status generation_reason reference_status reference_reason reference_retry_count reference_sources_used source_priority; do
    retries=$((attempts - 1))
    line_no=$((line_no + 1))
    comma=","
    if [[ "$line_no" -eq "$total_lines" ]]; then
      comma=""
    fi
    echo "    {\"chapter\":\"$(json_escape "$chapter_tag")\",\"file\":\"$(json_escape "$chapter_file")\",\"attempts\":$attempts,\"retries\":$retries,\"generation_status\":\"$(json_escape "$generation_status")\",\"generation_reason\":\"$(json_escape "$generation_reason")\",\"reference_status\":\"$(json_escape "$reference_status")\",\"reference_reason\":\"$(json_escape "$reference_reason")\",\"reference_retry_count\":$reference_retry_count,\"reference_sources_used\":\"$(json_escape "$reference_sources_used")\",\"source_priority\":\"$(json_escape "$source_priority")\"}$comma"
  done < "$SORTED_RESULTS"

  echo "  ],"
  echo "  \"failed_chapters\": ["
  for i in "${!FAILED_CHAPTERS[@]}"; do
    comma=","
    if [[ "$i" -eq "$(( ${#FAILED_CHAPTERS[@]} - 1 ))" ]]; then
      comma=""
    fi
    echo "    \"$(json_escape "${FAILED_CHAPTERS[$i]}")\"$comma"
  done
  echo "  ],"
  echo "  \"next_actions\": ["
  if [[ "$FAILURE_COUNT" -gt 0 ]]; then
    failed_joined="$(IFS=','; echo "${FAILED_CHAPTERS[*]}")"
    echo "    \"Rerun failed chapters only: bash tools/parallel-write-chapters.sh --scope $SCOPE --concurrency $CONCURRENCY --gate $GATE --proof-policy $PROOF_POLICY --reference-mode $REFERENCE_MODE --reference-cache $REFERENCE_CACHE_MODE --chapters $failed_joined\","
    echo "    \"Inspect generation logs in _reference/parallel-drafts/$RUN_ID/logs/, validation reports in _reference/parallel-drafts/$RUN_ID/reports/, and reference reports chXX-reference.json.\""
  elif [[ "$GATE" == "strict" && "$BUILD_STATUS" != "pass" ]]; then
    echo "    \"Fix LaTeX build failures and rerun strict gate using a new run id.\","
    echo "    \"Review build log at _reference/parallel-drafts/$RUN_ID/logs/latex-build.log\""
  else
    echo "    \"Merged chapters are ready. Run manual editorial review for mathematical clarity and anti-copy compliance.\","
    echo "    \"Optionally run bash tools/test.sh for site-level checks.\""
  fi
  echo "  ]"
  echo "}"
} > "$SUMMARY_PATH"

echo "Run completed: $RUN_ID"
echo "Summary: $SUMMARY_PATH"

if [[ "$FAILURE_COUNT" -gt 0 ]]; then
  exit 2
fi

if [[ "$GATE" == "strict" && "$BUILD_STATUS" != "pass" ]]; then
  exit 3
fi

if [[ "$READY_TO_MERGE" == "true" && "$MERGE_STATUS" != "pass" ]]; then
  exit 4
fi

exit 0
