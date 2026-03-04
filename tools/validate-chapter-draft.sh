#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash tools/validate-chapter-draft.sh --draft <path> --report <path> [--gate strict|balanced|draft-first] [--chapter chXX]
USAGE
}

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

count_literal() {
  local needle="$1"
  local file="$2"
  NEEDLE="$needle" awk 'index($0, ENVIRON["NEEDLE"]) { c++ } END { print c + 0 }' "$file"
}

count_items_between() {
  local file="$1"
  local start_pat="$2"
  local end_pat="${3:-}"

  awk -v start_pat="$start_pat" -v end_pat="$end_pat" '
    $0 ~ start_pat { in_block = 1; next }
    in_block && end_pat != "" && $0 ~ end_pat { in_block = 0 }
    in_block && /\\item/ { count++ }
    END { print count + 0 }
  ' "$file"
}

count_quiz_items() {
  local file="$1"
  awk '
    /\\subsection\*\{자가진단퀴즈\}/ { in_quiz = 1; next }
    in_quiz && /^\\section\{/ { in_quiz = 0 }
    in_quiz && /^\\sectiontemplate\{/ { in_quiz = 0 }
    in_quiz && /\\subsection\*\{/ && $0 !~ /자가진단퀴즈/ { in_quiz = 0 }
    in_quiz && /\\item/ { count++ }
    END { print count + 0 }
  ' "$file"
}

add_check() {
  local id="$1"
  local pass="$2"
  local detail="$3"

  CHECK_IDS+=("$id")
  CHECK_PASSES+=("$pass")
  CHECK_DETAILS+=("$detail")
  if [[ "$pass" == "false" ]]; then
    FAILED_RULES+=("$id")
    OVERALL_PASS="false"
  fi
}

DRAFT_PATH=""
REPORT_PATH=""
GATE="strict"
CHAPTER_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --draft)
      DRAFT_PATH="${2:-}"
      shift 2
      ;;
    --report)
      REPORT_PATH="${2:-}"
      shift 2
      ;;
    --gate)
      GATE="${2:-}"
      shift 2
      ;;
    --chapter)
      CHAPTER_ID="${2:-}"
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

if [[ -z "$DRAFT_PATH" || -z "$REPORT_PATH" ]]; then
  usage >&2
  exit 1
fi

if [[ ! -f "$DRAFT_PATH" ]]; then
  echo "Draft file not found: $DRAFT_PATH" >&2
  exit 1
fi

if [[ "$GATE" != "strict" && "$GATE" != "balanced" && "$GATE" != "draft-first" ]]; then
  echo "Unsupported gate: $GATE" >&2
  exit 1
fi

mkdir -p "$(dirname "$REPORT_PATH")"

CHECK_IDS=()
CHECK_PASSES=()
CHECK_DETAILS=()
FAILED_RULES=()
OVERALL_PASS="true"

THEOREM_COUNT="$(count_literal '\begin{theorem}' "$DRAFT_PATH")"
PROOF_COUNT="$(count_literal '\begin{proof}' "$DRAFT_PATH")"
DEFINITION_COUNT="$(count_literal '\begin{definition}' "$DRAFT_PATH")"
EXAMPLE_COUNT="$(count_literal '\begin{example}' "$DRAFT_PATH")"
WARNING_COUNT="$(count_literal '\begin{warning}' "$DRAFT_PATH")"
QUIZ_HEADING_COUNT="$(count_literal '\subsection*{자가진단퀴즈}' "$DRAFT_PATH")"
QUIZ_ITEM_COUNT="$(count_quiz_items "$DRAFT_PATH")"
SECTION_TEMPLATE_COUNT="$(count_literal '\sectiontemplate{' "$DRAFT_PATH")"
CODE_FENCE_COUNT="$(count_literal '```' "$DRAFT_PATH")"

HAS_CHAPTER="$( [[ "$(count_literal '\chapter{' "$DRAFT_PATH")" -ge 1 ]] && echo true || echo false )"
HAS_INTRO="$( [[ "$(count_literal '\chapterintro{' "$DRAFT_PATH")" -ge 1 ]] && echo true || echo false )"
HAS_GOALS="$( [[ "$(count_literal '\chaptergoals{' "$DRAFT_PATH")" -ge 1 ]] && echo true || echo false )"
HAS_APPLICATION="$( [[ "$(count_literal '\chapterapplicationtemplate{' "$DRAFT_PATH")" -ge 1 || "$(count_literal '\section{응용}' "$DRAFT_PATH")" -ge 1 ]] && echo true || echo false )"
HAS_SUMMARY="$( [[ "$(count_literal '\chaptersummarytemplate' "$DRAFT_PATH")" -ge 1 || "$(count_literal '\section*{장 요약}' "$DRAFT_PATH")" -ge 1 ]] && echo true || echo false )"

EX_A_ITEMS="$(count_items_between "$DRAFT_PATH" '연습문제 A' '연습문제 B')"
EX_B_ITEMS="$(count_items_between "$DRAFT_PATH" '연습문제 B' '연습문제 C')"
EX_C_ITEMS="$(count_items_between "$DRAFT_PATH" '연습문제 C' '')"

if [[ "$GATE" == "draft-first" ]]; then
  if [[ -s "$DRAFT_PATH" ]]; then
    add_check "non_empty_draft" "true" "Draft is not empty."
  else
    add_check "non_empty_draft" "false" "Draft is empty."
  fi
else
  if [[ "$HAS_CHAPTER" == "true" && "$HAS_INTRO" == "true" && "$HAS_GOALS" == "true" ]]; then
    add_check "required_chapter_macros" "true" "Found chapter, intro, and goals macros."
  else
    add_check "required_chapter_macros" "false" "Missing one or more chapter macros."
  fi

  if [[ "$SECTION_TEMPLATE_COUNT" -ge 1 ]]; then
    add_check "section_templates_present" "true" "Found $SECTION_TEMPLATE_COUNT section template blocks."
  else
    add_check "section_templates_present" "false" "No section template block found."
  fi

  if [[ "$DEFINITION_COUNT" -ge 1 && "$EXAMPLE_COUNT" -ge 1 ]]; then
    add_check "definition_and_example_present" "true" "Definitions and examples exist."
  else
    add_check "definition_and_example_present" "false" "Missing definition or example blocks."
  fi

  if [[ "$THEOREM_COUNT" -ge 1 ]]; then
    add_check "theorem_present" "true" "Found $THEOREM_COUNT theorem blocks."
  else
    add_check "theorem_present" "false" "No theorem block found."
  fi

  if [[ "$THEOREM_COUNT" -eq "$PROOF_COUNT" && "$THEOREM_COUNT" -ge 1 ]]; then
    add_check "theorem_proof_parity" "true" "Theorem/proof counts match ($THEOREM_COUNT)."
  else
    add_check "theorem_proof_parity" "false" "Theorem/proof counts mismatch (theorem=$THEOREM_COUNT, proof=$PROOF_COUNT)."
  fi

  if [[ "$WARNING_COUNT" -ge 2 ]]; then
    add_check "warning_minimum" "true" "Found $WARNING_COUNT warning blocks."
  else
    add_check "warning_minimum" "false" "Need at least 2 warning blocks (found $WARNING_COUNT)."
  fi

  if [[ "$QUIZ_HEADING_COUNT" -ge 1 && "$QUIZ_ITEM_COUNT" -ge 3 ]]; then
    add_check "quiz_minimum" "true" "Quiz heading found with $QUIZ_ITEM_COUNT quiz items."
  else
    add_check "quiz_minimum" "false" "Need quiz heading and at least 3 items (heading=$QUIZ_HEADING_COUNT, items=$QUIZ_ITEM_COUNT)."
  fi

  if [[ "$HAS_APPLICATION" == "true" && "$HAS_SUMMARY" == "true" ]]; then
    add_check "chapter_tail_blocks" "true" "Application and summary blocks found."
  else
    add_check "chapter_tail_blocks" "false" "Missing application or summary block."
  fi

  if [[ "$CODE_FENCE_COUNT" -eq 0 ]]; then
    add_check "no_markdown_code_fence" "true" "No markdown code fence found."
  else
    add_check "no_markdown_code_fence" "false" "Markdown code fences are not allowed."
  fi

  if [[ "$GATE" == "strict" ]]; then
    if [[ "$EX_A_ITEMS" -ge 6 && "$EX_B_ITEMS" -ge 4 && "$EX_C_ITEMS" -ge 2 ]]; then
      add_check "graded_exercise_minimum" "true" "Exercise counts satisfy A/B/C minimums ($EX_A_ITEMS/$EX_B_ITEMS/$EX_C_ITEMS)."
    else
      add_check "graded_exercise_minimum" "false" "Need A>=6, B>=4, C>=2 (found $EX_A_ITEMS/$EX_B_ITEMS/$EX_C_ITEMS)."
    fi
  else
    if [[ "$EX_A_ITEMS" -ge 1 && "$EX_B_ITEMS" -ge 1 && "$EX_C_ITEMS" -ge 1 ]]; then
      add_check "graded_exercise_presence" "true" "Exercise tiers A/B/C are present."
    else
      add_check "graded_exercise_presence" "false" "Exercise tiers A/B/C are missing."
    fi
  fi
fi

STATUS="pass"
if [[ "$OVERALL_PASS" == "false" ]]; then
  STATUS="fail"
fi

{
  echo "{"
  echo "  \"chapter\": \"$(json_escape "$CHAPTER_ID")\","
  echo "  \"draft\": \"$(json_escape "$DRAFT_PATH")\","
  echo "  \"gate\": \"$(json_escape "$GATE")\","
  echo "  \"status\": \"$(json_escape "$STATUS")\","
  echo "  \"counts\": {"
  echo "    \"theorem\": $THEOREM_COUNT,"
  echo "    \"proof\": $PROOF_COUNT,"
  echo "    \"definition\": $DEFINITION_COUNT,"
  echo "    \"example\": $EXAMPLE_COUNT,"
  echo "    \"warning\": $WARNING_COUNT,"
  echo "    \"quiz_heading\": $QUIZ_HEADING_COUNT,"
  echo "    \"quiz_item\": $QUIZ_ITEM_COUNT,"
  echo "    \"exercise_a\": $EX_A_ITEMS,"
  echo "    \"exercise_b\": $EX_B_ITEMS,"
  echo "    \"exercise_c\": $EX_C_ITEMS"
  echo "  },"
  echo "  \"checks\": ["
  for i in "${!CHECK_IDS[@]}"; do
    comma=","
    if [[ "$i" -eq "$((${#CHECK_IDS[@]} - 1))" ]]; then
      comma=""
    fi
    echo "    {\"id\":\"$(json_escape "${CHECK_IDS[$i]}")\",\"pass\":${CHECK_PASSES[$i]},\"detail\":\"$(json_escape "${CHECK_DETAILS[$i]}")\"}$comma"
  done
  echo "  ],"
  echo "  \"failed_rules\": ["
  for i in "${!FAILED_RULES[@]}"; do
    comma=","
    if [[ "$i" -eq "$((${#FAILED_RULES[@]} - 1))" ]]; then
      comma=""
    fi
    echo "    \"$(json_escape "${FAILED_RULES[$i]}")\"$comma"
  done
  echo "  ]"
  echo "}"
} > "$REPORT_PATH"

if [[ "$STATUS" == "pass" ]]; then
  exit 0
fi
exit 1
