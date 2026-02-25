#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LATEX_DIR="$ROOT_DIR/latex/linear-algebra"
OUT_DIR="$ROOT_DIR/assets/pdf/linear-algebra"

VERSIONED_PDF="$OUT_DIR/linear-algebra-notes-v0.1.pdf"
LATEST_PDF="$OUT_DIR/linear-algebra-notes-latest.pdf"
CH1_PREVIEW_PDF="$OUT_DIR/linear-algebra-notes-ch1-preview.pdf"

ensure_env() {
  if command -v xcrun >/dev/null 2>&1; then
    local sdk
    sdk="$(xcrun --show-sdk-path 2>/dev/null || true)"
    if [[ -n "$sdk" ]]; then
      export SDKROOT="$sdk"
      export CPLUS_INCLUDE_PATH="$sdk/usr/include/c++/v1${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}"
      export CPATH="$sdk/usr/include${CPATH:+:$CPATH}"
    fi
  fi
}

check_dependencies() {
  command -v latexmk >/dev/null 2>&1 || {
    echo "Error: latexmk is not installed." >&2
    exit 1
  }
  command -v xelatex >/dev/null 2>&1 || {
    echo "Error: xelatex is not installed." >&2
    exit 1
  }
}

build_all() {
  mkdir -p "$OUT_DIR"
  (cd "$LATEX_DIR" && latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex)
  cp "$LATEX_DIR/main.pdf" "$VERSIONED_PDF"
  cp "$LATEX_DIR/main.pdf" "$LATEST_PDF"
  echo "Built: $VERSIONED_PDF"
  echo "Built: $LATEST_PDF"
}

build_ch1() {
  mkdir -p "$OUT_DIR"
  (cd "$LATEX_DIR" && latexmk -xelatex -interaction=nonstopmode -halt-on-error main-ch1.tex)
  cp "$LATEX_DIR/main-ch1.pdf" "$CH1_PREVIEW_PDF"
  echo "Built: $CH1_PREVIEW_PDF"
}

clean_all() {
  (cd "$LATEX_DIR" && latexmk -C main.tex && latexmk -C main-ch1.tex)
  rm -f "$CH1_PREVIEW_PDF"
  echo "Cleaned LaTeX artifacts."
}

usage() {
  cat <<USAGE
Usage: bash tools/latex-build.sh [all|ch1|clean]

  all   Build full notes PDF and copy to:
        - assets/pdf/linear-algebra/linear-algebra-notes-v0.1.pdf
        - assets/pdf/linear-algebra/linear-algebra-notes-latest.pdf

  ch1   Build Chapter 1 preview PDF and copy to:
        - assets/pdf/linear-algebra/linear-algebra-notes-ch1-preview.pdf

  clean Remove LaTeX build artifacts.
USAGE
}

main() {
  local mode="${1:-all}"
  check_dependencies
  ensure_env

  case "$mode" in
    all)
      build_all
      ;;
    ch1)
      build_ch1
      ;;
    clean)
      clean_all
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"
