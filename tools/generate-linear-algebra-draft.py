#!/usr/bin/env python3
"""Generate the next independent linear algebra blog draft."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "_reference" / "linear-algebra-post-manifest.yml"
STATE_PATH = ROOT / "_reference" / ".automation" / "linear-algebra-post-state.json"
DEFAULT_OUTPUT_DIR = ROOT / "_drafts"
DEFAULT_POSTS_DIR = ROOT / "_posts"
SUPERSCEDED_DIRNAME = "_superseded"
DESIGN_PATH = ROOT / "_reference" / "2026-04-16-linear-algebra-independent-post-automation-design.md"
WRITING_SPEC_PATH = ROOT / "_reference" / "2026-04-16-linear-algebra-blog-writing-spec.md"
PRIMARY_SOURCE_PATH = Path(
    "/Users/kwkwon/Desktop/Obsidian/Mathematician/_shared/my-library/"
    "2018Olver - Applied Linear Algebra.pdf"
)
MASTER_BIB_PATH = Path("/Users/kwkwon/Desktop/Obsidian/Mathematician/_shared/my-library/master.bib")
SITE_TIMEZONE = ZoneInfo("Europe/Berlin")
AUTHOR = "KnowledgeLupin"
DEFAULT_CATEGORIES = ["Mathematics", "Linear Algebra"]
DEFAULT_SOCIAL_PREVIEW_IMAGE = "/assets/pdf/linear-algebra/linear-algebra-notes-latest-page1.png"
DEFAULT_WRITING_CONTRACT = {
    "min_words": 850,
    "min_characters": 3200,
    "min_blocks": 18,
    "min_sections": 5,
    "section_min_blocks": {
        "배경과 기본 정의": 5,
        "핵심 정리와 증명": 8,
        "간단한 예제로 보는 구조": 7,
        "응용에서 다시 나타나는 구조": 5,
        "마무리": 2,
    },
}
SEMANTIC_REQUIRED_FIELDS = [
    "title",
    "slug",
    "status",
    "source_refs",
    "core_concepts",
    "representative_theorem",
    "hand_example",
    "application_example_candidates",
    "visual_hint",
    "overlap_hint",
]
OPTIONAL_CANDIDATE_FIELDS = {
    "background_requirements": [],
    "proof_focus": "",
    "secondary_hand_example": "",
    "application_focus": [],
    "common_misunderstandings": [],
    "primary_query": "",
    "secondary_queries": [],
    "search_intent": "",
    "seo_title": "",
    "seo_slug": "",
    "meta_description_seed": "",
    "related_terms": [],
    "faq_queries": [],
    "internal_link_targets": [],
    "image_hint": "",
}
ACTIVE_STATUSES = {"selected", "drafting", "draft_ready", "needs_figure", "needs_revision", "review_ready"}
LEVEL_TO_SCORE = {"low": 0, "medium": 1, "high": 2}
APPLIED_KEYWORDS = (
    "데이터",
    "머신러닝",
    "회로",
    "신호",
    "그래프",
    "Markov",
    "PCA",
    "최소제곱",
    "근사",
    "압축",
    "필터링",
    "동역학",
    "에너지",
)
ESSENTIAL_IMPORTANCE_SLUGS = {
    "linear-systems-and-gaussian-elimination",
    "vector-spaces-and-subspaces",
    "span-independence-basis-dimension",
    "kernel-image-rank-nullity",
    "inner-products-and-norms",
    "orthogonal-projection-and-least-squares",
    "gram-schmidt-and-qr-factorization",
    "eigenvalues-and-the-spectral-theorem",
    "singular-values-pseudoinverse-and-condition-number",
    "principal-component-analysis",
}
HIGH_INDEPENDENCE_SLUGS = {
    "scope-and-applications",
    "linear-systems-and-gaussian-elimination",
    "inverse-and-determinant-in-computation",
    "pivoting-and-numerical-stability",
    "vector-spaces-and-subspaces",
    "span-independence-basis-dimension",
    "kernel-image-rank-nullity",
    "graphs-and-incidence-matrices",
    "inner-products-and-norms",
    "orthogonal-projection-and-least-squares",
    "gram-schmidt-and-qr-factorization",
    "interpolation-and-approximation",
    "discrete-fourier-transform-and-fft",
    "spring-mass-systems-and-energy-minimization",
    "electrical-networks-and-equilibrium",
    "principal-component-analysis",
}
LOW_INDEPENDENCE_SLUGS = {
    "power-method-qr-krylov-and-linear-dynamics",
    "iteration-markov-processes-and-iterative-solvers",
}
HIGH_APPLICABILITY_SLUGS = {
    "scope-and-applications",
    "linear-systems-and-gaussian-elimination",
    "pivoting-and-numerical-stability",
    "graphs-and-incidence-matrices",
    "orthogonal-projection-and-least-squares",
    "interpolation-and-approximation",
    "discrete-fourier-transform-and-fft",
    "compression-and-denoising",
    "spring-mass-systems-and-energy-minimization",
    "electrical-networks-and-equilibrium",
    "singular-values-pseudoinverse-and-condition-number",
    "principal-component-analysis",
    "iteration-markov-processes-and-iterative-solvers",
    "power-method-qr-krylov-and-linear-dynamics",
}
TAG_NORMALIZATION = {
    "gaussian elimination": "Gaussian elimination",
    "lu": "LU 분해",
    "pivoting": "Pivoting",
    "vector space": "벡터공간",
    "subspace": "부분공간",
    "basis": "기저",
    "dimension": "차원",
    "kernel": "Kernel",
    "image": "Image",
    "rank": "Rank",
    "nullity": "Nullity",
    "graph": "그래프",
    "incidence": "Incidence matrix",
    "inner product": "Inner product",
    "norm": "Norm",
    "cauchy": "Cauchy-Schwarz",
    "positive definite": "Positive definite matrix",
    "gram": "Gram matrix",
    "cholesky": "Cholesky 분해",
    "projection": "직교사영",
    "least squares": "Least squares",
    "gram schmidt": "Gram-Schmidt",
    "qr": "QR 분해",
    "fredholm": "Fredholm alternative",
    "interpolation": "보간",
    "approximation": "근사",
    "spline": "Spline",
    "fourier": "Fourier",
    "fft": "FFT",
    "compression": "압축",
    "denoising": "잡음제거",
    "spring": "스프링-질량계",
    "kirchhoff": "Kirchhoff 법칙",
    "eigenvalue": "고유값",
    "spectral": "Spectral theorem",
    "singular value": "특이값",
    "pseudoinverse": "의사역행렬",
    "condition": "조건수",
    "pca": "PCA",
    "markov": "Markov process",
    "krylov": "Krylov 방법",
}
TITLE_LOCALIZATION = {
    "Gaussian elimination": "가우스 소거법",
    "Pivoting": "피벗팅",
    "Kernel": "kernel",
    "image": "image",
    "rank-nullity": "rank nullity",
    "Inner product": "내적",
    "norm": "노름",
    "Positive definite matrix": "양의 정부호 행렬",
    "Gram matrix": "Gram 행렬",
    "Completing the square": "완전제곱",
    "Orthogonal projection": "직교사영",
    "least squares": "최소제곱",
    "Gram-Schmidt": "Gram Schmidt",
    "QR": "QR",
    "Discrete Fourier transform": "이산 푸리에 변환",
    "Fourier": "푸리에",
    "FFT": "FFT",
    "Eigenvalue": "고유값",
    "Singular value": "특이값",
    "Principal component analysis": "주성분분석",
    "Markov process": "마르코프 과정",
}
SEO_TITLE_OVERRIDES = {
    "scope-and-applications": "선형대수란 무엇인가와 주요 응용",
    "linear-systems-and-gaussian-elimination": "연립일차방정식과 가우스 소거법",
    "lu-factorization-and-triangular-solves": "LU 분해와 전진 대입, 후진 대입",
    "kernel-image-rank-nullity": "kernel과 image, rank nullity 정리",
    "inner-products-and-norms": "내적과 노름",
    "positive-definite-and-gram-matrices": "양의 정부호 행렬과 Gram 행렬",
    "completing-the-square-and-cholesky": "완전제곱과 Cholesky 분해",
    "orthogonal-projection-and-least-squares": "직교사영과 최소제곱",
    "gram-schmidt-and-qr-factorization": "Gram Schmidt 과정과 QR 분해",
    "discrete-fourier-transform-and-fft": "이산 푸리에 변환과 FFT",
    "eigenvalues-and-the-spectral-theorem": "고유값과 스펙트럴 정리",
    "singular-values-pseudoinverse-and-condition-number": "특이값, 의사역행렬, 조건수",
    "principal-component-analysis": "주성분분석",
}
GENERIC_TITLE_PHRASES = {
    "대상과 응용 범위",
    "개요",
    "개관",
    "소개",
}
GENERIC_SLUG_TOKENS = {
    "scope",
    "overview",
    "introduction",
    "applications",
}


TOPIC_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "scope-and-applications": {
        "intro": [
            "선형대수를 처음 배울 때 가장 먼저 생기는 오해는 이것이 행렬 계산의 기술 목록이라는 생각입니다. 실제로는 그 반대에 가깝습니다. 선형대수는 서로 전혀 달라 보이는 문제를 같은 문법으로 번역해 주는 언어이고, 계산은 그 언어가 실제로 작동한다는 가장 직접적인 증거입니다.",
            "이 글에서는 선형성이라는 말이 왜 연립일차방정식, 근사, 네트워크, 데이터 요약을 하나의 테이블에 올려놓는지를 정리합니다. 엄밀한 공리를 길게 나열하기보다는, 어떤 구조가 공통으로 반복되는지를 먼저 붙잡은 뒤 그 공통 구조가 수학적으로 무엇을 보장하는지 살펴보겠습니다.",
        ],
        "background": "선형성이라는 말은 보통 덧셈과 스칼라배를 보존한다는 뜻입니다. 이 보존 성질 하나 때문에 여러 문제를 좌표화할 수 있고, 좌표화된 문제는 다시 행렬과 벡터의 언어로 다룰 수 있습니다.",
        "definitions": [
            {
                "title": "선형사상 (linear map)",
                "body": "벡터공간 사이의 사상 $$T:V\\to W$$가 모든 $$u,v\\in V$$와 스칼라 $$a$$에 대하여 $$T(u+v)=T(u)+T(v)$$, $$T(av)=aT(v)$$를 만족하면 선형사상이라 한다.",
            },
            {
                "title": "선형모형",
                "body": "여러 변수 사이의 관계가 미지수의 선형결합으로 주어지면 그 관계를 선형모형이라 부른다. 좌표를 정하면 이런 관계는 행렬과 벡터의 곱으로 기록된다.",
            },
        ],
        "theorem_name": "합성과 선형결합의 안정성",
        "theorem_statement": "선형사상들의 합성과 선형결합은 다시 선형사상이다.",
        "proof": [
            "선형사상 $$S,T:V\\to W$$와 스칼라 $$\\alpha,\\beta$$를 잡자. 임의의 $$u,v\\in V$$에 대하여 $$\\alpha S+\\beta T$$를 적용하면",
            "$$((\\alpha S+\\beta T)(u+v))=\\alpha S(u+v)+\\beta T(u+v)=\\alpha(Su+Sv)+\\beta(Tu+Tv)=((\\alpha S+\\beta T)u)+((\\alpha S+\\beta T)v).$$",
            "같은 방식으로 $$((\\alpha S+\\beta T)(au))=\\alpha aS(u)+\\beta aT(u)=a((\\alpha S+\\beta T)u)$$이므로 선형결합은 선형이다. 합성 $$R\\circ T$$에 대해서도 $$R(T(u+v))=R(Tu+Tv)=RTu+RTv$$와 $$R(T(au))=R(aTu)=aRTu$$가 성립하므로 선형성이 보존된다. $$\\square$$",
        ],
        "hand_example_intro": "선형식과 비선형식을 구분하는 가장 빠른 방법은 실제로 선형성 조건을 대입해 보는 것입니다.",
        "hand_example_steps": [
            "$$f(x,y)=2x-3y$$에 대하여 $$f((x_1,y_1)+(x_2,y_2))=f(x_1,y_1)+f(x_2,y_2)$$와 $$f(a(x,y))=af(x,y)$$가 그대로 성립한다.",
            "반면 $$g(x,y)=x^2+y$$는 $$g((x_1,y_1)+(x_2,y_2))$$를 전개하면 교차항 $$2x_1x_2$$가 생기므로 덧셈을 보존하지 않는다.",
            "이 단순한 계산 하나가 선형대수가 어디까지 유효한 언어이고 어디서부터는 다른 도구가 필요한지를 가르는 출발점이다.",
        ],
        "application": [
            "선형회귀에서는 설명변수와 계수의 관계가 선형이기 때문에 데이터 적합 문제가 행렬식 언어로 바뀐다.",
            "회로 평형에서는 Kirchhoff 법칙이 전압과 전류의 선형 관계를 만들고, 그래프의 incidence matrix는 이를 압축된 형태로 기록한다.",
            "그래서 선형대수의 가치는 어떤 한 응용의 공식에 있지 않고, 전혀 다른 응용들이 같은 구조를 공유한다는 사실을 드러내는 데 있다.",
        ],
        "pitfalls": [
            "선형성을 단지 1차식이라는 뜻으로만 이해하면 함수공간이나 행렬공간으로 확장될 때 곧바로 막힌다.",
            "응용 사례를 모아 놓는다고 해서 자동으로 선형대수가 되는 것은 아니며, 실제로 덧셈과 스칼라배가 보존되는지를 확인해야 한다.",
        ],
        "closing": "선형대수의 첫 관문은 공식이 아니라 번역이다. 문제를 선형 구조로 번역할 수 있으면 계산, 분해, 근사, 스펙트럼 해석이 한 흐름으로 연결된다.",
        "visual_importance": "none",
    },
    "linear-systems-and-gaussian-elimination": {
        "intro": [
            "연립일차방정식은 선형대수가 행렬로 출발하는 이유를 가장 잘 보여 줍니다. 미지수가 여러 개여도 중요한 것은 각 방정식이 어떤 평면이나 초평면을 나타내는지, 그리고 그 교집합을 해집합으로 읽을 수 있는지입니다.",
            "Gaussian elimination의 핵심은 복잡한 식을 억지로 외워 푸는 데 있지 않습니다. 해를 바꾸지 않는 동치 변형만 허용하면서 문제를 점점 읽기 쉬운 형태로 바꾸는 데 있습니다. 그래서 이 절차를 이해하면 나중의 LU 분해, rank, least squares까지 한 번에 이어집니다.",
        ],
        "background": "증강행렬은 방정식의 계수와 우변을 한 표에 모아 적는 장치입니다. 이렇게 적으면 행연산이 해집합을 바꾸는지 아닌지를 식 전체 대신 행 단위로 추적할 수 있습니다.",
        "definitions": [
            {
                "title": "증강행렬 (augmented matrix)",
                "body": "연립일차방정식 $$A x=b$$의 계수행렬 $$A$$와 우변 $$b$$를 옆에 붙여 적은 행렬 $$[A\\mid b]$$를 증강행렬이라 한다.",
            },
            {
                "title": "기본 행연산",
                "body": "두 행을 교환하는 연산, 한 행에 0이 아닌 상수를 곱하는 연산, 한 행에 다른 행의 상수배를 더하는 연산을 기본 행연산이라 한다.",
            },
        ],
        "theorem_name": "기본 행연산과 해집합",
        "theorem_statement": "증강행렬에 가한 세 가지 기본 행연산은 대응하는 연립일차방정식의 해집합을 보존한다.",
        "proof": [
            "행 교환은 방정식의 순서만 바꾸는 것이므로 어떤 벡터가 한 시스템의 해이면 다른 시스템의 해이기도 하다.",
            "한 행에 0이 아닌 상수 $$c$$를 곱하는 것은 등식 $$r=0$$를 동치인 등식 $$cr=0$$로 바꾸는 것과 같다. 따라서 해집합은 변하지 않는다.",
            "한 행에 다른 행의 상수배를 더하는 경우를 보자. 어떤 벡터가 원래 시스템의 해이면 두 등식을 각각 만족하므로 그 선형결합도 만족한다. 반대로 바뀐 시스템의 해는 추가된 행과 원래 남겨둔 행을 이용해 이전 행을 복원할 수 있으므로 원래 시스템의 해이기도 하다. 세 연산 모두 양방향 동치 변형이므로 해집합이 보존된다. $$\\square$$",
        ],
        "hand_example_intro": "직접 한 번 소거를 해 보면 피벗, 자유변수, 해의 개수가 한꺼번에 읽힙니다.",
        "hand_example_steps": [
            "$$\\begin{aligned}x+y+z&=2\\\\ 2x+y-z&=1\\\\ x+2y+3z&=5\\end{aligned}$$를 증강행렬로 쓰면 $$\\left[\\begin{array}{ccc|c}1&1&1&2\\\\2&1&-1&1\\\\1&2&3&5\\end{array}\\right]$$가 된다.",
            "둘째 행에서 첫째 행의 두 배를 빼고, 셋째 행에서 첫째 행을 빼면 $$\\left[\\begin{array}{ccc|c}1&1&1&2\\\\0&-1&-3&-3\\\\0&1&2&3\\end{array}\\right]$$를 얻는다.",
            "다시 셋째 행과 둘째 행을 더하면 $$\\left[\\begin{array}{ccc|c}1&1&1&2\\\\0&-1&-3&-3\\\\0&0&-1&0\\end{array}\\right]$$이고, 여기서 바로 $$z=0$$, $$y=3$$, $$x=-1$$을 읽을 수 있다. 피벗이 세 개이므로 자유변수는 없다.",
        ],
        "application": [
            "회로의 전압과 전류, 질점계의 평형식, 마르코프 체인의 정상 상태 계산은 모두 결국 선형계로 정리된다.",
            "실제 데이터 적합 문제에서도 정규방정식을 세우는 순간 다시 선형계가 나온다. 따라서 Gaussian elimination은 단지 1장 내용이 아니라 선형대수 전체의 기본 계산 도구다.",
        ],
        "pitfalls": [
            "소거 결과만 읽고 각 행연산이 왜 동치 변형인지 잊어버리면, rank와 nullity를 배울 때 해석의 토대를 잃기 쉽다.",
            "기약행 사다리꼴만이 정답이라고 생각하면 실제 계산에서 불필요한 연산을 많이 하게 된다. 해를 읽는 데 필요한 최소한의 형태가 무엇인지 보는 편이 중요하다.",
        ],
        "closing": "Gaussian elimination은 문제를 더 간단한 동치 문제로 바꾸는 과정이다. 이 구조를 이해하면 뒤에서 LU 분해가 왜 자연스럽게 나오는지도 바로 보인다.",
        "visual_importance": "none",
    },
    "pivoting-and-numerical-stability": {
        "intro": [
            "종이에 적는 계산과 컴퓨터가 실제로 수행하는 계산은 다릅니다. 종이 위에서는 동치인 알고리듬이 부동소수점 환경에서는 전혀 다른 오차를 만들 수 있고, pivoting은 그 차이를 가장 먼저 보여 주는 장면입니다.",
            "수치적 안정성이라는 말은 답을 '대충' 얻는다는 뜻이 아닙니다. 입력의 작은 오차와 반올림 오차가 출력에서 통제 가능한 범위 안에 머무는지를 묻는 말입니다.",
        ],
        "background": "피벗은 소거 단계에서 나눗셈의 기준이 되는 원소입니다. 아주 작은 피벗을 나누기에 사용하면 상대오차가 크게 증폭될 수 있고, 행 교환은 이 문제를 줄이기 위한 가장 기본적인 처방입니다.",
        "definitions": [
            {
                "title": "pivot",
                "body": "사다리꼴을 만드는 각 단계에서 해당 열의 소거 기준이 되는 원소를 pivot이라 한다.",
            },
            {
                "title": "partial pivoting",
                "body": "현재 열에서 절댓값이 큰 원소를 피벗으로 택하도록 행을 교환하는 절차를 partial pivoting이라 한다.",
            },
        ],
        "theorem_name": "작은 피벗의 위험",
        "theorem_statement": "소거 과정에서 아주 작은 pivot을 그대로 사용하면 반올림 오차가 크게 증폭될 수 있으며, 행 교환은 그 위험을 줄인다.",
        "proof": [
            "$$\\begin{bmatrix}\\varepsilon &1\\\\1&1\\end{bmatrix}$$처럼 $$0<\\varepsilon\\ll1$$인 경우를 생각하자. 첫 번째 피벗을 $$\\varepsilon$$로 두고 둘째 행에서 $$\\varepsilon^{-1}$$배를 쓰면 계수의 크기가 급격히 커진다.",
            "유한 정밀도에서는 큰 수와 비슷한 큰 수를 빼는 과정에서 유효숫자가 급격히 손실된다. 따라서 해 자체는 존재해도 계산된 삼각행렬이 원래 문제를 제대로 대표하지 못할 수 있다.",
            "반대로 행을 교환해 1을 피벗으로 잡으면 소거 계수의 크기가 제한되고, 같은 반올림 환경에서도 훨씬 안정적으로 계산된다. 따라서 pivoting은 단순한 편의가 아니라 오차 제어 장치다. $$\\square$$",
        ],
        "hand_example_intro": "숫자가 작은 2x2 예제만으로도 작은 피벗이 얼마나 위험한지 보입니다.",
        "hand_example_steps": [
            "$$\\varepsilon=10^{-6}$$라고 두고 $$\\begin{aligned}10^{-6}x+y&=1\\\\ x+y&=2\\end{aligned}$$를 생각하자.",
            "행 교환 없이 소거하면 둘째 행에서 첫째 행의 $$10^6$$배를 빼야 하므로 중간 계수가 매우 커진다.",
            "행을 바꾸면 피벗이 1이 되고, 이후 소거 계수는 $$10^{-6}$$ 수준에 머문다. 실제 구현에서는 이런 차이가 결과 정확도를 좌우한다.",
        ],
        "application": [
            "큰 선형계를 푸는 과학 계산, 최적화, 미분방정식 시간 적분에서는 소거가 내부적으로 계속 나타난다.",
            "그래서 pivoting을 이해하는 것은 수치선형대수를 따로 배울 때까지 미루는 주제가 아니라, '왜 같은 공식인데 구현 결과가 다른가'를 설명하는 핵심 배경이다.",
        ],
        "pitfalls": [
            "안정성을 단순히 계산이 끝난다는 뜻으로 이해하면 안 된다. 중요한 것은 작은 입력 오차와 반올림 오차가 얼마나 증폭되는가이다.",
            "행 교환이 해를 바꾼다고 오해하는 경우가 있다. 해를 바꾸는 것이 아니라 표현을 더 안전한 동치 형태로 바꾸는 것이다.",
        ],
        "closing": "소거법은 대수적으로만 보면 끝난 이야기 같지만, 실제 계산에서는 어떤 피벗을 고르느냐가 결과의 신뢰도를 결정한다.",
        "visual_importance": "none",
    },
    "vector-spaces-and-subspaces": {
        "intro": [
            "벡터공간을 처음 만나면 공리가 너무 많아 보입니다. 그러나 실제로는 '덧셈과 스칼라배를 해도 같은 세계 안에 남는다'는 한 가지 감각을 정교하게 적어 놓은 것에 가깝습니다.",
            "부분공간은 선형대수 전체에서 반복해서 등장하는 무대입니다. 해집합, kernel, image, 고유공간, 직교여공간이 모두 부분공간이기 때문에 이 개념을 정확히 잡는 일이 가장 먼저 필요합니다.",
        ],
        "background": "벡터공간은 숫자 쌍만이 아니라 다항식, 함수, 행렬의 집합에도 나타납니다. 그래서 그림에만 기대기보다 공리가 무엇을 보장하는지를 보는 편이 중요합니다.",
        "definitions": [
            {
                "title": "벡터공간 (vector space)",
                "body": "체 $$K$$ 위의 집합 $$V$$가 벡터 덧셈과 스칼라배에 대해 공리를 만족하면 $$V$$를 $$K$$ 위의 벡터공간이라 한다.",
            },
            {
                "title": "부분공간 (subspace)",
                "body": "벡터공간 $$V$$의 부분집합 $$W$$가 영벡터를 포함하고 덧셈과 스칼라배에 대해 닫혀 있으면 $$W$$를 $$V$$의 부분공간이라 한다.",
            },
        ],
        "theorem_name": "부분공간의 교집합",
        "theorem_statement": "벡터공간 $$V$$의 임의의 부분공간족의 교집합은 다시 $$V$$의 부분공간이다.",
        "proof": [
            "부분공간족을 $$\\{W_i\\}_{i\\in I}$$라 하고 $$W=\\bigcap_{i\\in I}W_i$$라 두자. 각 $$W_i$$는 영벡터를 포함하므로 $$0\\in W$$이다.",
            "이제 $$u,v\\in W$$이면 모든 $$i$$에 대하여 $$u,v\\in W_i$$이고, 각 $$W_i$$가 부분공간이므로 $$u+v\\in W_i$$이다. 따라서 $$u+v\\in W$$이다.",
            "같은 방식으로 임의의 스칼라 $$a$$와 $$u\\in W$$에 대해 모든 $$i$$에 대하여 $$au\\in W_i$$이므로 $$au\\in W$$이다. 세 조건이 모두 성립하므로 $$W$$는 부분공간이다. $$\\square$$",
        ],
        "hand_example_intro": "부분공간 판정은 공리를 전부 다시 쓰는 일이 아니라 세 조건을 차례로 확인하는 일입니다.",
        "hand_example_steps": [
            "$$W=\\{(x,y,z)\\in\\mathbb R^3\\mid x+y+z=0\\}$$를 보자. $$0+0+0=0$$이므로 영벡터가 들어 있다.",
            "$$u=(x_1,y_1,z_1), v=(x_2,y_2,z_2)\\in W$$이면 $$(x_1+x_2)+(y_1+y_2)+(z_1+z_2)=0$$이므로 $$u+v\\in W$$다.",
            "또 $$a\\in\\mathbb R$$에 대해 $$a(x+y+z)=0$$이므로 $$au\\in W$$다. 따라서 $$W$$는 부분공간이다.",
        ],
        "application": [
            "동차 연립방정식의 해집합이 부분공간이라는 사실은 이후 kernel을 정의할 때 바로 쓰인다.",
            "다항식 공간이나 함수공간을 벡터공간으로 보는 순간, 선형대수는 유한차원 그림을 넘어서 훨씬 넓은 문제를 다루는 언어가 된다.",
        ],
        "pitfalls": [
            "덧셈 닫힘만 보고 부분공간이라고 결론 내리면 안 된다. 영벡터 포함과 스칼라배 닫힘도 반드시 확인해야 한다.",
            "벡터를 화살표 그림으로만 이해하면 다항식이나 함수가 벡터가 되는 순간 개념이 흔들린다.",
        ],
        "closing": "부분공간은 선형대수에서 계속 반복해 등장하는 '좋은 부분세계'다. 이후의 kernel, image, 직교여공간, 고유공간은 모두 이 언어로 정리된다.",
        "visual_importance": "none",
    },
    "span-independence-basis-dimension": {
        "intro": [
            "기저와 차원은 벡터공간의 자유도를 가장 압축된 방식으로 적는 언어입니다. 생성은 충분함을, 선형독립은 중복 없음 을 뜻하고, 기저는 이 둘이 정확히 만나는 자리입니다.",
            "그래서 기저를 배운다는 것은 좌표를 고르는 법을 배우는 것과 같습니다. 한 번 좌표가 정해지면 계산은 쉬워지고, 좌표가 달라도 변하지 않는 양으로 차원이 나타납니다.",
        ],
        "background": "생성집합은 모든 벡터를 만들 수 있을 만큼 커야 하고, 선형독립집합은 불필요한 중복이 없어야 합니다. 기저는 이 두 요구를 동시에 만족하는 최소의 좌표축입니다.",
        "definitions": [
            {
                "title": "생성 (span)",
                "body": "집합 $$S\\subset V$$의 모든 유한 선형결합으로 얻어지는 벡터들의 집합을 $$\\operatorname{span}(S)$$라 한다.",
            },
            {
                "title": "기저 (basis)",
                "body": "집합 $$B\\subset V$$가 $$V$$를 생성하고 동시에 선형독립이면 $$B$$를 $$V$$의 기저라 한다.",
            },
        ],
        "theorem_name": "기저의 원소 수",
        "theorem_statement": "유한차원 벡터공간의 임의의 두 기저는 같은 수의 원소를 가진다.",
        "proof": [
            "하나의 기저를 $$B=\\{v_1,\\dots,v_n\\}$$, 다른 기저를 $$C=\\{w_1,\\dots,w_m\\}$$라 하자. $$B$$는 생성집합이고 $$C$$는 선형독립이므로 교체정리에 의해 $$m\\le n$$이다.",
            "같은 논리를 반대로 적용하면 $$C$$는 생성집합이고 $$B$$는 선형독립이므로 $$n\\le m$$이다.",
            "따라서 $$m=n$$이다. 즉 기저 선택이 달라도 원소 수는 같고, 이 공통의 수를 차원이라 부른다. $$\\square$$",
        ],
        "hand_example_intro": "생성집합에서 중복을 지워 기저를 만드는 과정은 차원의 의미를 가장 직접적으로 보여 줍니다.",
        "hand_example_steps": [
            "$$\\mathbb R^3$$에서 $$v_1=(1,0,0), v_2=(0,1,0), v_3=(1,1,0), v_4=(0,0,1)$$을 보자.",
            "$$v_3=v_1+v_2$$이므로 $$\\{v_1,v_2,v_3,v_4\\}$$는 생성집합이지만 선형독립은 아니다.",
            "$$v_3$$를 빼도 나머지 세 벡터는 여전히 $$\\mathbb R^3$$를 생성하고 선형독립이므로 기저가 된다. 여기서 차원이 3이라는 사실이 다시 드러난다.",
        ],
        "application": [
            "데이터 표현에서는 기저를 바꾸는 일이 곧 좌표계를 바꾸는 일이다. 좋은 기저를 고르면 표현이 압축되거나 계산이 단순해진다.",
            "함수 근사나 신호 처리에서도 결국 어떤 기저를 쓰느냐가 해석과 계산의 품질을 좌우한다.",
        ],
        "pitfalls": [
            "생성과 선형독립을 서로 완전히 반대되는 성질이라고만 생각하면 기저의 의미를 놓치기 쉽다. 기저는 두 성질의 균형점이다.",
            "차원을 단지 벡터의 길이나 좌표 수로 이해하면 함수공간이나 추상 벡터공간으로 갈 때 바로 무너진다.",
        ],
        "closing": "기저는 좌표의 출발점이고, 차원은 좌표를 바꾸어도 변하지 않는 자유도의 수다. 선형대수의 많은 정리는 결국 이 두 문장을 다양한 방식으로 다시 쓰는 일이다.",
        "visual_importance": "none",
    },
    "kernel-image-rank-nullity": {
        "intro": [
            "선형사상을 이해하는 가장 빠른 방법은 '무엇이 0으로 가는가'와 '어디까지 도달할 수 있는가'를 동시에 보는 것입니다. kernel과 image는 바로 이 두 질문에 대한 답입니다.",
            "rank-nullity 정리는 입력 차원이 해의 자유도와 도달 가능한 출력의 차원으로 분해된다는 사실을 말합니다. 그래서 이 정리는 단순한 공식이 아니라 선형사상의 해석도입니다.",
        ],
        "background": "행렬로 보면 kernel은 동차방정식 $$Ax=0$$의 해공간이고, image는 열벡터들의 생성공간입니다. 선형사상의 언어로 보면 둘 다 좌표계에 의존하지 않는 부분공간입니다.",
        "definitions": [
            {
                "title": "kernel",
                "body": "선형사상 $$T:V\\to W$$에 대하여 $$\\ker T=\\{v\\in V\\mid T(v)=0\\}$$를 $$T$$의 kernel이라 한다.",
            },
            {
                "title": "image",
                "body": "선형사상 $$T:V\\to W$$에 대하여 $$\\operatorname{im}T=\\{T(v)\\mid v\\in V\\}$$를 $$T$$의 image라 한다.",
            },
        ],
        "theorem_name": "rank-nullity",
        "theorem_statement": "유한차원 벡터공간 $$V$$와 선형사상 $$T:V\\to W$$에 대하여 $$\\dim V=\\dim\\ker T+\\dim\\operatorname{im}T$$가 성립한다.",
        "proof": [
            "$$\\ker T$$의 기저를 $$\\{u_1,\\dots,u_k\\}$$라 하고 이를 $$V$$의 기저 $$\\{u_1,\\dots,u_k,v_1,\\dots,v_r\\}$$로 확장하자. 그러면 $$k=\\dim\\ker T$$이고 $$k+r=\\dim V$$이다.",
            "이제 $$\\{Tv_1,\\dots,Tv_r\\}$$가 $$\\operatorname{im}T$$의 기저임을 보이면 된다. 먼저 임의의 $$x\\in V$$는 위 기저로 전개되므로 $$Tx$$는 $$Tv_j$$들의 선형결합이다. 따라서 $$Tv_j$$들은 image를 생성한다.",
            "또 $$\\sum c_jTv_j=0$$이면 $$T(\\sum c_jv_j)=0$$이므로 $$\\sum c_jv_j\\in\\ker T$$이다. 그런데 $$u_i,v_j$$ 전체가 기저이므로 $$v_j$$ 부분의 계수는 모두 0이어야 한다. 따라서 $$Tv_j$$들은 선형독립이다. 결국 $$\\dim\\operatorname{im}T=r$$이고 $$\\dim V=k+r=\\dim\\ker T+\\dim\\operatorname{im}T$$가 된다. $$\\square$$",
        ],
        "hand_example_intro": "작은 행렬 하나만으로 kernel과 image, 그리고 차원 공식을 모두 확인할 수 있습니다.",
        "hand_example_steps": [
            "$$A=\\begin{bmatrix}1&2&0\\\\0&0&1\\end{bmatrix}$$를 보자. $$Ax=0$$을 풀면 $$x_1=-2x_2, x_3=0$$이므로 kernel은 $$(-2,1,0)$$ 하나로 생성되고 nullity는 1이다.",
            "image는 열벡터 $$ (1,0)^T, (2,0)^T, (0,1)^T$$의 생성공간이다. 첫째와 셋째 열이 독립이므로 rank는 2다.",
            "입력 차원은 3이고 $$3=1+2$$이므로 rank-nullity 정리가 정확히 맞아떨어진다.",
        ],
        "application": [
            "선형 회귀에서는 설계행렬의 kernel이 계수의 비식별성을 드러내고, image는 실제로 설명 가능한 출력의 공간을 뜻한다.",
            "미분방정식의 선형화나 제약 최적화에서도 '허용되는 방향'과 '관측 가능한 출력'을 구분하는 언어로 kernel과 image가 반복해서 등장한다.",
        ],
        "pitfalls": [
            "kernel을 단지 해공간이라고만 외우면 선형사상의 구조를 놓친다. kernel은 정보가 사라지는 방향 전체를 모아 놓은 부분공간이다.",
            "rank-nullity를 공식처럼만 기억하면 왜 자유변수의 수가 nullity와 같은지, 왜 열공간의 차원이 rank인지 연결이 약해진다.",
        ],
        "closing": "rank-nullity 정리는 입력 자유도가 어디로 사라지고 어디에 남는지를 보여 주는 균형식이다. 해석과 계산이 한 줄에 만나는 대표적인 정리다.",
        "visual_importance": "none",
    },
    "inner-products-and-norms": {
        "intro": [
            "벡터공간만으로는 방향을 더하고 스칼라배할 수 있을 뿐, 길이나 각도를 말할 수는 없습니다. 내적은 바로 그 기하학을 다시 불러오는 장치입니다.",
            "이 장에서 중요한 것은 단순히 점곱의 공식을 외우는 일이 아닙니다. 길이, 거리, 유사도, 직교성 같은 익숙한 개념이 추상 공간으로 어떻게 확장되는지를 보는 일입니다.",
        ],
        "background": "내적을 이해할 때 중요한 것은 대칭성, 선형성, 양의 정부호성이라는 말을 이름으로만 넘기지 않는 일입니다. 이 세 조건은 내적이 순서를 바꾸어도 같은 값을 주고, 선형결합을 안정적으로 전개하게 하며, 자기 자신과의 내적이 길이의 제곱처럼 작동하게 만든다는 뜻입니다.",
        "definitions": [
            {
                "title": "내적 (inner product)",
                "body": "벡터공간 $$V$$ 위의 함수 $$\\langle\\cdot,\\cdot\\rangle:V\\times V\\to\\mathbb R$$가 임의의 $$u,v,w\\in V$$와 $$a,b\\in\\mathbb R$$에 대하여 $$\\langle u,v\\rangle=\\langle v,u\\rangle$$, $$\\langle au+bv,w\\rangle=a\\langle u,w\\rangle+b\\langle v,w\\rangle$$, $$\\langle u,av+bw\\rangle=a\\langle u,v\\rangle+b\\langle u,w\\rangle$$, 그리고 $$\\langle v,v\\rangle\\ge0$$이며 $$\\langle v,v\\rangle=0$$일 때 그리고 그때에 한하여 $$v=0$$를 만족하면 inner product라 한다.",
            },
            {
                "title": "노름 (norm)",
                "body": "내적이 주어졌을 때 $$\\|v\\|=\\sqrt{\\langle v,v\\rangle}$$로 정의한 함수를 그 내적이 유도하는 norm이라 한다.",
            },
        ],
        "definition_bridge": [
            "첫째 조건 $$\\langle u,v\\rangle=\\langle v,u\\rangle$$는 두 벡터의 관계를 어느 쪽에서 읽어도 같은 수가 나온다는 뜻입니다. 둘째 조건은 선형결합이 각 변수에서 그대로 분배된다는 뜻이어서, 좌표를 바꾸거나 식을 전개할 때 계산이 흔들리지 않습니다.",
            "마지막 조건 $$\\langle v,v\\rangle\\ge0$$와 $$\\langle v,v\\rangle=0\\iff v=0$$는 내적이 실제 길이의 제곱 역할을 하게 만듭니다. 그래서 $$\\|v\\|=\\sqrt{\\langle v,v\\rangle}$$라는 정의가 자연스럽게 등장합니다.",
        ],
        "theorem_name": "내적이 유도하는 노름",
        "theorem_statement": "내적 $$\\langle\\cdot,\\cdot\\rangle$$가 주어지면 $$\\|v\\|=\\sqrt{\\langle v,v\\rangle}$$는 노름이 된다.",
        "proof": [
            "양의 정부호성에 의해 $$\\langle v,v\\rangle\\ge0$$이고, $$\\langle v,v\\rangle=0$$이면 $$v=0$$이므로 노름의 비음수성과 영벡터 판정이 성립한다.",
            "스칼라 $$a$$에 대해 $$\\|av\\|^2=\\langle av,av\\rangle=a^2\\langle v,v\\rangle$$이므로 $$\\|av\\|=|a|\\|v\\|$$이다.",
            "삼각부등식은 Cauchy-Schwarz를 쓰면 된다. 실제로 $$\\|u+v\\|^2=\\|u\\|^2+2\\langle u,v\\rangle+\\|v\\|^2\\le \\|u\\|^2+2\\|u\\|\\|v\\|+\\|v\\|^2=(\\|u\\|+\\|v\\|)^2$$이므로 $$\\|u+v\\|\\le\\|u\\|+\\|v\\|$$이다. 따라서 노름 공리가 모두 성립한다. $$\\square$$",
        ],
        "hand_example_intro": "좌표공간과 다항식 공간을 함께 보면 내적의 공리가 실제 계산에서 어떤 구조를 만드는지 훨씬 또렷하게 드러납니다.",
        "hand_example_steps": [
            "$$\\mathbb R^2$$에서는 $$\\langle (x_1,y_1),(x_2,y_2)\\rangle=x_1x_2+y_1y_2$$이고, 여기서 유도된 노름은 익숙한 유클리드 길이다.",
            "다항식 공간 $$P_1$$에서는 $$\\langle p,q\\rangle=\\int_0^1 p(x)q(x)\\,dx$$처럼 적분으로 내적을 줄 수 있다.",
            "예를 들어 $$p(x)=1+x$$이면 $$\\|p\\|^2=\\int_0^1(1+x)^2dx=\\frac73$$이다. 좌표가 아닌 함수도 내적공간의 벡터가 된다.",
        ],
        "application": [
            "데이터 분석에서는 두 벡터의 내적이 유사도나 상관성의 기본 측도로 쓰인다.",
            "최소제곱과 정사영은 결국 어떤 오차를 작게 본다는 문제인데, 그 오차의 크기를 재는 기준이 바로 내적이 유도하는 노름이다.",
            "끝으로 한 가지는 분명히 해 둘 필요가 있다. 모든 노름이 어떤 내적에서 오는 것은 아니며, 함수공간의 내적도 좌표공간 점곱의 단순한 변형으로만 보면 구조를 놓치기 쉽다.",
        ],
        "closing": "내적을 도입하면 벡터공간은 계산의 무대에서 기하의 무대로 바뀐다. 이후의 직교성, 정사영, least squares는 모두 여기서 출발한다.",
        "visual_importance": "none",
    },
    "orthogonal-projection-and-least-squares": {
        "intro": [
            "직교사영과 최소제곱은 '정확한 해가 없을 때 무엇을 해로 볼 것인가'라는 질문에 대한 선형대수의 대답입니다. 해가 아예 없다고 끝내지 않고, 가장 가까운 해를 구조적으로 찾아냅니다.",
            "이 주제는 기하와 계산이 가장 아름답게 만나는 장면이기도 합니다. 한 점을 직선에 내린 수선의 발이라는 그림이 곧바로 데이터 적합의 행렬식으로 이어지기 때문입니다.",
        ],
        "background": "부분공간 $$W$$에 대한 직교사영은 주어진 벡터 $$b$$를 $$W$$ 안의 벡터와 $$W$$에 직교한 오차로 나누는 과정입니다. least squares는 בדיוק 그 오차의 길이를 최소로 만드는 문제입니다.",
        "definitions": [
            {
                "title": "직교사영 (orthogonal projection)",
                "body": "내적공간의 부분공간 $$W$$에 대하여 $$b-p\\in W^\\perp$$를 만족하는 $$p\\in W$$를 $$b$$의 $$W$$ 위의 orthogonal projection이라 한다.",
            },
            {
                "title": "least squares 문제",
                "body": "계 $$Ax=b$$가 정확히 풀리지 않을 때 $$\\|Ax-b\\|$$를 최소화하는 $$x$$를 찾는 문제를 least squares 문제라 한다.",
            },
        ],
        "theorem_name": "정규방정식의 성격",
        "theorem_statement": "벡터 $$x_*$$가 $$\\|Ax-b\\|$$를 최소화할 필요충분조건은 잔차 $$r=b-Ax_*$$가 $$\\operatorname{im}A$$에 직교하는 것이다. 동치로 $$A^TAx_*=A^Tb$$가 성립한다.",
        "proof": [
            "$$Ax$$는 항상 $$\\operatorname{im}A$$에 속한다. 따라서 최소제곱 문제는 $$b$$를 $$\\operatorname{im}A$$ 위로 직교사영하는 문제와 같다.",
            "$$p=Ax_*$$가 직교사영이면 $$b-p\\in (\\operatorname{im}A)^\\perp$$이다. 이는 임의의 열벡터 $$a_j$$에 대해 $$a_j^T(b-Ax_*)=0$$임을 뜻하므로 행렬식으로 쓰면 $$A^T(b-Ax_*)=0$$, 즉 $$A^TAx_*=A^Tb$$이다.",
            "반대로 $$A^T(b-Ax_*)=0$$이면 잔차가 모든 열벡터에 직교하므로 $$\\operatorname{im}A$$ 전체에 직교한다. 직교사영의 성질에 의해 $$Ax_*$$는 $$b$$에 가장 가까운 $$\\operatorname{im}A$$의 원소이고, 따라서 $$x_*$$는 least squares 해다. $$\\square$$",
        ],
        "hand_example_intro": "가장 작은 예제는 직교사영과 least squares가 정말 같은 말인지 확인하게 해 줍니다.",
        "hand_example_steps": [
            "직선 $$W=\\operatorname{span}\\{(1,1)\\}$$ 위로 $$b=(2,0)$$를 사영해 보자. 사영벡터를 $$p=t(1,1)$$라 두면 잔차 $$b-p=(2-t,-t)$$가 $$(1,1)$$에 직교해야 한다.",
            "$$(2-t,-t)\\cdot(1,1)=2-2t=0$$이므로 $$t=1$$, 따라서 $$p=(1,1)$$이다.",
            "행렬로 보면 $$A=\\begin{bmatrix}1\\\\1\\end{bmatrix}$$, $$x=t$$이고 정규방정식은 $$A^TAx=A^Tb$$, 즉 $$2t=2$$가 된다. 그림과 행렬 계산이 정확히 같은 답을 준다.",
        ],
        "application": [
            "선형회귀는 데이터를 가장 잘 설명하는 직선을 찾는 문제인데, 결국 설계행렬의 열공간으로 데이터를 사영하는 문제다.",
            "그래서 least squares는 회귀분석, 잡음이 있는 측정의 보정, 과잉결정계의 해석에서 가장 기본적인 도구가 된다.",
        ],
        "pitfalls": [
            "최소제곱해는 원래 방정식의 정확한 해가 아닐 수 있다. 중요한 것은 잔차의 길이를 최소화한다는 점이다.",
            "정규방정식을 공식처럼 외우기보다, 왜 잔차가 열공간에 직교해야 하는지를 기하적으로 이해하는 편이 훨씬 오래 남는다.",
        ],
        "closing": "least squares의 핵심은 해가 없다는 사실을 포기하지 않는 데 있다. 대신 가장 가까운 설명을 찾고, 그 조건을 직교성과 정규방정식으로 정확하게 적어 낸다.",
        "visual_importance": "required",
        "visual_caption": "점 $$b$$를 부분공간 $$W$$ 위로 직교사영하는 그림은 least squares가 '가장 가까운 점' 문제라는 사실을 한눈에 보여 준다.",
    },
    "gram-schmidt-and-qr-factorization": {
        "intro": [
            "직교기저를 하나 가지고 있으면 좌표 계산과 사영 계산이 갑자기 쉬워집니다. Gram-Schmidt 과정은 일반적인 생성집합을 직교기저로 바꾸는 가장 직접적인 절차입니다.",
            "그리고 이 절차를 열벡터 전체에 적용해 모으면 QR 분해가 나옵니다. 즉, 추상적인 직교화와 실전 계산 알고리듬이 사실상 같은 이야기입니다.",
        ],
        "background": "이미 확보한 방향의 성분을 빼면 새로운 방향에서 중복이 사라집니다. Gram-Schmidt는 이 관찰을 반복해 독립 벡터열을 직교열로 바꿉니다.",
        "definitions": [
            {
                "title": "정규직교집합",
                "body": "벡터열 $$q_1,\\dots,q_k$$가 서로 직교하고 각 벡터의 길이가 1이면 이를 orthonormal set이라 한다.",
            },
            {
                "title": "QR 분해",
                "body": "열독립 행렬 $$A$$를 $$A=QR$$ 꼴로 쓰되, $$Q$$의 열들이 정규직교이고 $$R$$이 상삼각행렬이면 이를 QR factorization이라 한다.",
            },
        ],
        "theorem_name": "Gram-Schmidt의 span 보존",
        "theorem_statement": "선형독립 벡터열 $$v_1,\\dots,v_k$$에 Gram-Schmidt를 적용해 얻은 $$q_1,\\dots,q_k$$는 정규직교이며, 각 $$j$$에 대해 $$\\operatorname{span}\\{q_1,\\dots,q_j\\}=\\operatorname{span}\\{v_1,\\dots,v_j\\}$$가 성립한다.",
        "proof": [
            "$$j=1$$에서는 $$q_1=v_1/\\|v_1\\|$$이므로 자명하다. 이제 $$j-1$$까지 성립한다고 가정하자.",
            "$$u_j=v_j-\\sum_{i=1}^{j-1}\\langle v_j,q_i\\rangle q_i$$로 두면 $$u_j$$는 모든 $$q_i$$에 직교한다. 또한 $$u_j$$는 $$v_1,\\dots,v_j$$의 선형결합이므로 왼쪽 span에 속한다.",
            "반대로 $$v_j=u_j+\\sum_{i<j}\\langle v_j,q_i\\rangle q_i$$이므로 $$v_j$$도 $$q_1,\\dots,q_j$$의 span에 속한다. 따라서 두 span이 같다. $$u_j\\neq0$$는 $$v_j$$의 독립성에서 나오고, 정규화하여 $$q_j=u_j/\\|u_j\\|$$를 얻는다. 귀납이 끝난다. $$\\square$$",
        ],
        "hand_example_intro": "작은 벡터열 하나를 직접 직교화하면 QR 분해가 어떻게 읽히는지 바로 보입니다.",
        "hand_example_steps": [
            "$$v_1=(1,1,0), v_2=(1,0,1)$$를 보자. 먼저 $$q_1=\\frac1{\\sqrt2}(1,1,0)$$이다.",
            "$$v_2$$에서 $$q_1$$ 방향 성분을 빼면 $$u_2=v_2-\\langle v_2,q_1\\rangle q_1=(1,0,1)-\\frac12(1,1,0)=(\\frac12,-\\frac12,1)$$가 된다.",
            "$$u_2$$를 정규화하면 $$q_2$$를 얻고, $$A=[v_1\\ v_2]$$에 대해 $$Q=[q_1\\ q_2]$$, $$R=Q^TA$$를 계산하면 QR 분해가 완성된다.",
        ],
        "application": [
            "least squares를 직접 푸는 데에는 정규방정식보다 QR 분해가 더 안정적인 경우가 많다.",
            "또한 직교기저는 신호 분해, 함수 근사, 고유값 계산 알고리듬의 준비 단계로 반복해서 등장한다.",
        ],
        "pitfalls": [
            "Gram-Schmidt의 공식만 외우면 왜 span이 보존되는지, 왜 직교성이 얻어지는지 쉽게 잊게 된다.",
            "직교화는 이론적으로 단순하지만 실제 부동소수점 계산에서는 수정된 Gram-Schmidt나 Householder 방법이 더 안정적일 수 있다.",
        ],
        "closing": "Gram-Schmidt는 중복을 제거하면서 같은 공간을 보존하는 절차다. 그래서 직교성과 좌표 계산이 같은 흐름으로 묶이고, QR 분해라는 계산 도구로 바로 이어진다.",
        "visual_importance": "supporting",
    },
    "discrete-fourier-transform-and-fft": {
        "intro": [
            "DFT는 데이터를 다른 좌표계에서 다시 읽는 변환입니다. 시간 순서로 적힌 샘플을 주파수 기저에 대한 좌표로 바꾸는 순간, 주기성과 진동 구조가 훨씬 선명하게 드러납니다.",
            "FFT는 새로운 수학적 변환이 아니라 같은 DFT를 훨씬 빠르게 계산하는 알고리듬입니다. 그래서 이 글의 핵심은 변환과 계산을 분리해서 보는 것입니다.",
        ],
        "background": "길이 $$n$$의 데이터 벡터를 $$\\omega=e^{-2\\pi i/n}$$의 거듭제곱으로 이루어진 기저에 투영하면 Fourier 행렬이 등장합니다. 이 행렬의 직교성이 DFT의 안정성과 역변환 공식을 뒷받침합니다.",
        "definitions": [
            {
                "title": "DFT",
                "body": "길이 $$n$$ 벡터 $$x=(x_0,\\dots,x_{n-1})$$의 DFT는 $$\\hat x_k=\\sum_{j=0}^{n-1}x_j\\omega^{jk}$$로 정의한다. 여기서 $$\\omega=e^{-2\\pi i/n}$$이다.",
            },
            {
                "title": "Fourier 행렬",
                "body": "행렬 $$F_n=(\\omega^{jk})_{0\\le j,k\\le n-1}$$를 Fourier matrix라 한다. DFT는 행렬식으로는 $$\\hat x=F_nx$$이다.",
            },
        ],
        "theorem_name": "Fourier 행렬의 직교성",
        "theorem_statement": "Fourier 행렬 $$F_n$$에 대하여 $$\\frac1{\\sqrt n}F_n$$은 unitary이다.",
        "proof": [
            "$$F_n$$의 서로 다른 두 열 $$c_r,c_s$$의 내적을 계산하면 $$\\sum_{j=0}^{n-1}\\omega^{j(r-s)}$$가 된다.",
            "$$r\\neq s$$이면 $$\\omega^{r-s}\\neq1$$이고 이는 공비가 1이 아닌 등비수열의 합이므로 0이다. $$r=s$$이면 각 항의 절댓값이 1이므로 합은 $$n$$이다.",
            "따라서 $$F_n^*F_n=nI$$이고, 곧 $$\\left(\\frac1{\\sqrt n}F_n\\right)^*\\left(\\frac1{\\sqrt n}F_n\\right)=I$$이다. 즉 $$\\frac1{\\sqrt n}F_n$$은 unitary이다. $$\\square$$",
        ],
        "hand_example_intro": "길이 4 데이터는 손으로도 DFT를 계산할 수 있는 가장 좋은 연습장입니다.",
        "hand_example_steps": [
            "$$x=(1,0,1,0)$$와 $$\\omega=e^{-2\\pi i/4}=-i$$를 잡자.",
            "$$\\hat x_0=1+0+1+0=2$$, $$\\hat x_1=1+0\\cdot(-i)+1\\cdot(-1)+0\\cdot i=0$$, $$\\hat x_2=1+1=2$$, $$\\hat x_3=0$$이다.",
            "즉 원래 데이터는 시간축에서는 두 개의 1로 보이지만, 주파수축에서는 특정 계수 두 개가 살아 있는 벡터로 읽힌다.",
        ],
        "application": [
            "신호 처리에서는 특정 주파수 대역만 남기거나 지우는 작업이 시간 영역보다 주파수 영역에서 훨씬 쉽다.",
            "또한 FFT 덕분에 큰 데이터에서도 DFT를 반복해서 계산할 수 있어, 압축과 필터링이 실전 알고리듬으로 작동한다.",
        ],
        "pitfalls": [
            "FFT를 DFT와 다른 변환이라고 생각하면 안 된다. FFT는 같은 DFT를 빠르게 계산하는 절차다.",
            "연속 Fourier transform과 DFT를 그대로 동일시하면 샘플링과 주기화의 차이를 놓치게 된다.",
        ],
        "closing": "DFT는 좌표계를 바꾸는 선형변환이고, FFT는 그 좌표변환을 현실적인 시간 안에 수행하게 해 주는 계산 전략이다.",
        "visual_importance": "supporting",
    },
    "eigenvalues-and-the-spectral-theorem": {
        "intro": [
            "고유값 이론은 선형변환을 가장 잘 보이는 좌표계에서 읽으려는 시도입니다. 변환 뒤에도 방향이 바뀌지 않는 특별한 축을 찾으면, 복잡한 변환이 훨씬 단순한 스칼라배로 분해됩니다.",
            "모든 행렬이 그렇게 단순해지는 것은 아니지만, 대칭행렬에서는 놀라울 정도로 강한 구조가 성립합니다. 이 대칭성 때문에 spectral theorem이 가능해집니다.",
        ],
        "background": "고유벡터는 선형변환이 방향을 보존하는 벡터이고, 고유값은 그 방향에서의 확대축소 비율입니다. 서로 다른 고유값이 많을수록 변환을 좌표별로 분해하기 쉬워집니다.",
        "definitions": [
            {
                "title": "고유값과 고유벡터",
                "body": "선형사상 $$T:V\\to V$$에 대하여 $$T(v)=\\lambda v$$를 만족하는 0이 아닌 벡터 $$v$$를 고유벡터, 그때의 스칼라 $$\\lambda$$를 고유값이라 한다.",
            },
            {
                "title": "대각화",
                "body": "기저를 적절히 택해 선형사상의 행렬표현이 대각행렬이 되면 그 선형사상 또는 행렬을 diagonalizable하다고 한다.",
            },
        ],
        "theorem_name": "서로 다른 고유값과 선형독립성",
        "theorem_statement": "서로 다른 고유값에 대응하는 고유벡터들은 선형독립이다.",
        "proof": [
            "고유벡터 $$v_1,\\dots,v_k$$가 각각 서로 다른 고유값 $$\\lambda_1,\\dots,\\lambda_k$$에 대응한다고 하자. 선형독립이 아니라고 가정하고, 가장 짧은 관계식 $$c_1v_1+\\cdots+c_kv_k=0$$를 잡는다.",
            "여기에 선형사상 $$T$$를 적용하면 $$c_1\\lambda_1v_1+\\cdots+c_k\\lambda_kv_k=0$$을 얻는다. 원래 식에 $$\\lambda_k$$를 곱해 빼면 $$c_1(\\lambda_1-\\lambda_k)v_1+\\cdots+c_{k-1}(\\lambda_{k-1}-\\lambda_k)v_{k-1}=0$$이 된다.",
            "고유값들이 서로 다르므로 계수 $$\\lambda_j-\\lambda_k$$는 0이 아니다. 따라서 더 짧은 비자명 관계식이 생겨 최소성에 모순이다. 결국 모든 $$c_j$$가 0이고, 고유벡터들은 선형독립이다. $$\\square$$",
        ],
        "hand_example_intro": "대칭행렬에서는 고유벡터들의 직교성까지 자연스럽게 보입니다.",
        "hand_example_steps": [
            "$$A=\\begin{bmatrix}2&1\\\\1&2\\end{bmatrix}$$의 특성방정식은 $$(2-\\lambda)^2-1=0$$이므로 고유값은 3과 1이다.",
            "$$\\lambda=3$$에 대한 고유벡터는 $$(1,1)$$, $$\\lambda=1$$에 대한 고유벡터는 $$(1,-1)$$로 잡을 수 있다.",
            "이 둘은 서로 직교한다. 대칭행렬에서는 이런 현상이 일반적으로 일어나고, 그것이 spectral theorem의 핵심 정서다.",
        ],
        "application": [
            "선형 동역학에서는 반복이나 미분방정식의 장기 거동이 고유값의 크기와 부호에 의해 크게 좌우된다.",
            "PCA에서는 공분산 행렬의 고유벡터가 데이터의 주된 방향을 주므로, 고유값 이론이 곧 데이터 해석 도구가 된다.",
        ],
        "pitfalls": [
            "모든 행렬이 대각화 가능하다고 생각하면 Jordan 형식을 배울 때 큰 혼란이 온다.",
            "고유값 계산만 강조하고 왜 대칭행렬에서 직교기저가 가능한지 보지 않으면 spectral theorem의 핵심을 놓친다.",
        ],
        "closing": "고유값 이론은 복잡한 변환을 가능한 한 좌표별 현상으로 분해하려는 시도다. 그 시도가 가장 아름답게 완성되는 경우가 바로 대칭행렬의 spectral theorem이다.",
        "visual_importance": "supporting",
    },
    "principal-component-analysis": {
        "intro": [
            "PCA는 데이터를 가장 잘 설명하는 방향을 찾는 절차입니다. 눈으로 보면 기울어진 구름처럼 보이는 데이터가, 수학적으로는 공분산 행렬의 고유값 문제로 바뀝니다.",
            "그래서 PCA는 통계 기법이면서 동시에 아주 전형적인 선형대수의 응용입니다. 분산을 가장 크게 만드는 방향을 고르는 문제와 고유벡터를 찾는 문제가 정확히 같은 문제이기 때문입니다.",
        ],
        "background": "데이터를 평균 중심화하면 각 방향으로 얼마나 퍼져 있는지가 공분산 행렬에 기록됩니다. 이때 분산을 많이 설명하는 방향일수록 차원 축소에서도 더 많은 정보를 남깁니다.",
        "definitions": [
            {
                "title": "공분산 행렬 (covariance matrix)",
                "body": "중심화된 데이터 행렬 $$X\\in\\mathbb R^{m\\times n}$$에 대하여 $$C=\\frac1m X^TX$$를 공분산 행렬이라 한다.",
            },
            {
                "title": "주성분",
                "body": "단위벡터 $$u$$ 중에서 사영된 데이터의 분산 $$u^TCu$$를 최대화하는 방향을 첫 번째 주성분이라 한다.",
            },
        ],
        "theorem_name": "첫 주성분의 성격",
        "theorem_statement": "공분산 행렬 $$C$$의 최대 고유값에 대응하는 단위 고유벡터는 데이터 분산 $$u^TCu$$를 최대화하는 방향이다.",
        "proof": [
            "$$C$$는 대칭행렬이므로 직교대각화 가능하다. 즉 정규직교기저 $$q_1,\\dots,q_n$$와 고유값 $$\\lambda_1\\ge\\cdots\\ge\\lambda_n$$가 존재하여 $$C=Q\\Lambda Q^T$$라 쓸 수 있다.",
            "임의의 단위벡터 $$u$$를 $$u=\\sum_j c_j q_j$$라 쓰면 $$\\sum_j c_j^2=1$$이고 $$u^TCu=\\sum_j \\lambda_j c_j^2$$이다.",
            "이 값은 가중평균이므로 최대값은 $$\\lambda_1$$이고, 그 최대는 $$u=q_1$$일 때 달성된다. 따라서 최대 고유값의 고유벡터가 첫 주성분이다. $$\\square$$",
        ],
        "hand_example_intro": "작은 2차원 데이터만으로도 PCA의 핵심을 손으로 계산할 수 있습니다.",
        "hand_example_steps": [
            "중심화된 데이터 점을 $$(1,1),(2,2),(-1,-1),(-2,-2)$$처럼 잡으면 모든 점이 직선 $$y=x$$ 위에 놓여 있다.",
            "이 경우 공분산 행렬은 $$\\begin{bmatrix}a&a\\\\a&a\\end{bmatrix}$$ 꼴이 되고, 최대 고유벡터는 $$\\frac1{\\sqrt2}(1,1)$$이다.",
            "즉 데이터가 가장 많이 퍼지는 방향이 바로 대각선 방향이라는 직관이 고유벡터 계산으로 정확히 확인된다.",
        ],
        "application": [
            "PCA는 고차원 데이터를 2차원이나 3차원으로 눌러 시각화할 때 가장 널리 쓰인다.",
            "또한 노이즈가 많은 데이터에서 분산이 작은 방향을 버리면 차원 축소와 잡음 완화가 동시에 일어나기도 한다.",
        ],
        "pitfalls": [
            "평균 중심화를 하지 않으면 PCA는 데이터의 퍼짐이 아니라 원점으로부터의 위치까지 함께 반영해 버린다.",
            "주성분의 수를 정할 때 고유값 크기만 기계적으로 자르면 해석 가능한 구조를 놓칠 수 있다.",
        ],
        "closing": "PCA는 '데이터가 가장 길게 뻗은 방향을 찾자'는 직관을 고유값 문제로 번역한 것이다. 그래서 선형대수의 스펙트럼 이론이 곧 데이터 해석 도구가 된다.",
        "visual_importance": "required",
        "visual_caption": "산점도 위에 첫 주성분 축을 그리면 PCA가 분산을 최대화하는 방향을 고르는 절차라는 사실이 즉시 드러난다.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slot", choices=("am", "pm"), required=True, help="Automation slot label.")
    parser.add_argument("--now", help="Override the current timestamp with an ISO-8601 string.")
    parser.add_argument("--dry-run", action="store_true", help="Render without writing drafts or state.")
    parser.add_argument("--index", type=int, help="Force a specific candidate order without advancing selection logic.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where drafts will be written. Defaults to _drafts/.",
    )
    return parser.parse_args()


def parse_now(raw: str | None) -> datetime:
    if not raw:
        return datetime.now(SITE_TIMEZONE)
    cleaned = raw.replace("Z", "+00:00")
    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=SITE_TIMEZONE)
    return dt.astimezone(SITE_TIMEZONE)


def normalize_text(text: str) -> str:
    lowered = text.replace("`", " ").lower()
    tokens = re.findall(r"[a-z0-9가-힣]+", lowered)
    return " ".join(tokens)


def localized_title(text: str) -> str:
    localized = text
    for source, target in TITLE_LOCALIZATION.items():
        localized = localized.replace(source, target)
    return localized.replace("  ", " ").strip()


def public_title_for(candidate: dict[str, Any]) -> str:
    explicit = str(candidate.get("seo_title", "")).strip()
    if explicit:
        return explicit
    slug = candidate["slug"]
    if slug in SEO_TITLE_OVERRIDES:
        return SEO_TITLE_OVERRIDES[slug]
    return localized_title(candidate["title"])


def public_slug_for(candidate: dict[str, Any]) -> str:
    explicit = str(candidate.get("seo_slug", "")).strip()
    if explicit:
        return explicit
    return candidate["slug"]


def primary_query_for(candidate: dict[str, Any]) -> str:
    explicit = str(candidate.get("primary_query", "")).strip()
    if explicit:
        return explicit
    return public_title_for(candidate)


def secondary_queries_for(candidate: dict[str, Any]) -> list[str]:
    explicit = ensure_list(candidate.get("secondary_queries"))
    if explicit:
        return explicit
    title = public_title_for(candidate)
    concepts = [localized_title(item) for item in ensure_list(candidate.get("core_concepts"))[:3]]
    applications = [localized_title(item) for item in ensure_list(candidate.get("application_example_candidates"))[:2]]
    related = [localized_title(item) for item in ensure_list(candidate.get("related_terms"))[:3]]
    bag = [title] + concepts + applications + related
    return dedupe_preserve([item for item in bag if item and normalize_text(item) != normalize_text(primary_query_for(candidate))])[:6]


def meta_description_for(candidate: dict[str, Any]) -> str:
    seed = str(candidate.get("meta_description_seed", "")).strip()
    if seed:
        return seed
    title = public_title_for(candidate)
    first = localized_title(ensure_list(candidate.get("core_concepts"))[0]) if ensure_list(candidate.get("core_concepts")) else title
    second = localized_title(ensure_list(candidate.get("core_concepts"))[1]) if len(ensure_list(candidate.get("core_concepts"))) > 1 else first
    application = localized_title(ensure_list(candidate.get("application_example_candidates"))[0]) if ensure_list(candidate.get("application_example_candidates")) else "응용"
    return f"이 글은 {title}를 중심으로 {first}과 {second}의 구조를 설명하고, 작은 예제와 {application} 장면에서 이 개념이 어떻게 나타나는지 정리합니다."


def excerpt_for(candidate: dict[str, Any]) -> str:
    title = public_title_for(candidate)
    application = localized_title(ensure_list(candidate.get("application_example_candidates"))[0]) if ensure_list(candidate.get("application_example_candidates")) else "현실적 응용"
    return f"{title}의 핵심 정의와 정리를 엄밀하게 설명하고, 작은 예제와 {application} 맥락을 통해 이 주제가 왜 중요한지 정리합니다."


def image_for(candidate: dict[str, Any], blueprint: dict[str, Any] | None = None) -> str:
    hint = str(candidate.get("image_hint", "")).strip()
    if hint.startswith("/"):
        return hint
    if blueprint and blueprint.get("visual_importance") in {"required", "supporting"}:
        return DEFAULT_SOCIAL_PREVIEW_IMAGE
    return DEFAULT_SOCIAL_PREVIEW_IMAGE


def is_generic_title(title: str) -> bool:
    return any(phrase in title for phrase in GENERIC_TITLE_PHRASES)


def is_generic_slug(slug: str) -> bool:
    tokens = set(normalize_text(slug).split())
    return bool(tokens & GENERIC_SLUG_TOKENS)


def headings(text: str) -> list[str]:
    items: list[str] = []
    for line in strip_front_matter(text).splitlines():
        if line.startswith("# "):
            items.append(line[2:].strip())
        elif line.startswith("## "):
            items.append(line[3:].strip())
    return items


def query_in_blocks(text: str, query: str, block_limit: int = 2) -> bool:
    normalized_query = normalize_text(query)
    if not normalized_query:
        return False
    query_tokens = normalized_query.split()
    blocks = prose_blocks(text)[:block_limit]
    normalized_blocks = " ".join(normalize_text(block) for block in blocks)
    if normalized_query in normalized_blocks:
        return True
    if not query_tokens:
        return False
    matched = sum(1 for token in query_tokens if token in normalized_blocks)
    return matched >= max(1, len(query_tokens) - 1)


def query_in_heading(text: str, query: str) -> bool:
    normalized_query = normalize_text(query)
    if not normalized_query:
        return False
    query_tokens = normalized_query.split()
    for item in headings(text):
        normalized_heading = normalize_text(item)
        if normalized_query in normalized_heading:
            return True
        matched = sum(1 for token in query_tokens if token in normalized_heading)
        if matched >= max(1, len(query_tokens) - 1):
            return True
    return False


def yaml_quote(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_inline_list(items: list[str]) -> str:
    return "[" + ", ".join(yaml_quote(item) for item in items) + "]"


def format_offset(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S %z")


def dedupe_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def load_manifest() -> dict[str, Any]:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest must contain a JSON object.")
    if data.get("kind") != "linear_algebra_independent_posts":
        raise ValueError("Unexpected manifest kind.")
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("Manifest candidates must be a list.")
    contract = deepcopy(DEFAULT_WRITING_CONTRACT)
    manifest_contract = data.get("writing_contract")
    if isinstance(manifest_contract, dict):
        contract.update({key: value for key, value in manifest_contract.items() if key != "section_min_blocks"})
        if isinstance(manifest_contract.get("section_min_blocks"), dict):
            contract["section_min_blocks"] = {
                **DEFAULT_WRITING_CONTRACT["section_min_blocks"],
                **manifest_contract["section_min_blocks"],
            }
    data["writing_contract"] = contract
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Manifest candidate entries must be objects.")
        for field in SEMANTIC_REQUIRED_FIELDS + ["order"]:
            if field not in candidate:
                raise ValueError(f"Missing candidate field: {field}")
        for field_name, default_value in OPTIONAL_CANDIDATE_FIELDS.items():
            candidate.setdefault(field_name, deepcopy(default_value))
    data["candidates"] = sorted(candidates, key=lambda item: int(item["order"]))
    return data


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {
            "schema_version": 1,
            "updated_at": None,
            "runs": [],
            "candidates": {},
        }
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("State file must be a JSON object.")
    data.setdefault("schema_version", 1)
    data.setdefault("updated_at", None)
    data.setdefault("runs", [])
    data.setdefault("candidates", {})
    return data


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def runtime_for(state: dict[str, Any], slug: str) -> dict[str, Any]:
    candidates = state.setdefault("candidates", {})
    return candidates.setdefault(
        slug,
        {
            "status": "candidate",
            "selected_at": None,
            "last_checked_at": None,
            "skip_reason": None,
            "draft_path": None,
            "revision_attempts": 0,
            "failure_reason": None,
            "history": [],
        },
    )


def append_history(runtime: dict[str, Any], now: datetime, status: str, note: str) -> None:
    runtime.setdefault("history", []).append(
        {
            "at": now.isoformat(),
            "status": status,
            "note": note,
        }
    )


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


def collect_markdown_entries(directory: Path, *, recursive: bool = False) -> list[dict[str, Any]]:
    if not directory.exists():
        return []
    pattern = "**/*.md" if recursive else "*.md"
    entries: list[dict[str, Any]] = []
    for path in sorted(directory.glob(pattern)):
        if path.is_dir():
            continue
        if SUPERSCEDED_DIRNAME in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        front_matter = parse_front_matter(text)
        entries.append(
            {
                "path": path,
                "title": front_matter.get("title", ""),
                "slug": front_matter.get("slug", ""),
                "text": text,
            }
        )
    return entries


def same_topic(candidate: dict[str, Any], entry: dict[str, Any]) -> bool:
    candidate_slugs = {candidate["slug"], public_slug_for(candidate)}
    candidate_titles = {normalize_text(candidate["title"]), normalize_text(public_title_for(candidate))}
    entry_slug = entry.get("slug", "")
    entry_title = normalize_text(entry.get("title", ""))
    if entry_slug and entry_slug in candidate_slugs:
        return True
    if entry_title and entry_title in candidate_titles:
        return True
    return False


def count_headings(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("## "))


def strip_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def prose_text(text: str) -> str:
    body = strip_front_matter(text)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return body


def prose_blocks(text: str) -> list[str]:
    body = prose_text(text)
    blocks: list[str] = []
    for chunk in re.split(r"\n\s*\n", body):
        stripped = chunk.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        blocks.append(stripped)
    return blocks


def count_words(text: str) -> int:
    return len(prose_text(text).split())


def count_characters(text: str) -> int:
    return len(prose_text(text))


def extract_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_title: str | None = None
    buffer: list[str] = []
    for line in strip_front_matter(text).splitlines():
        if line.startswith("## "):
            if current_title is not None:
                sections[current_title] = "\n".join(buffer).strip()
            current_title = line[3:].strip()
            buffer = []
            continue
        if current_title is not None:
            buffer.append(line)
    if current_title is not None:
        sections[current_title] = "\n".join(buffer).strip()
    return sections


def count_blocks(body: str) -> int:
    return len([chunk for chunk in re.split(r"\n\s*\n", body) if chunk.strip()])


def writing_contract(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    if manifest is None:
        return deepcopy(DEFAULT_WRITING_CONTRACT)
    contract = deepcopy(DEFAULT_WRITING_CONTRACT)
    manifest_contract = manifest.get("writing_contract")
    if isinstance(manifest_contract, dict):
        contract.update({key: value for key, value in manifest_contract.items() if key != "section_min_blocks"})
        if isinstance(manifest_contract.get("section_min_blocks"), dict):
            contract["section_min_blocks"] = {
                **DEFAULT_WRITING_CONTRACT["section_min_blocks"],
                **manifest_contract["section_min_blocks"],
            }
    return contract


def low_quality_report(text: str) -> dict[str, Any]:
    contract = writing_contract()
    issues: list[str] = []
    front = parse_front_matter(text)
    if "> **정리 1" not in text:
        issues.append("missing_theorem_block")
    if "**증명.**" not in text:
        issues.append("missing_direct_proof")
    if "## 참고문헌" not in text:
        issues.append("missing_references")
    if "## 간단한 예제로 보는 구조" not in text:
        issues.append("missing_hand_example")
    if "## 응용에서 다시 나타나는 구조" not in text:
        issues.append("missing_application_section")
    if any(heading in text for heading in ("## 손으로 따라가는 계산", "## 응용으로 보는 이유", "## 자주 헷갈리는 점", "## 정리하며")):
        issues.append("legacy_section_headings")
    if "손계산" in text:
        issues.append("legacy_hand_calculation_language")
    if count_headings(text) < contract["min_sections"]:
        issues.append("too_few_sections")
    if count_words(text) < contract["min_words"]:
        issues.append("too_few_words")
    if count_characters(text) < contract["min_characters"]:
        issues.append("too_few_characters")
    if len(prose_blocks(text)) < contract["min_blocks"]:
        issues.append("too_few_blocks")
    sections = extract_sections(text)
    for title, min_blocks in contract["section_min_blocks"].items():
        body = sections.get(title)
        if body and count_blocks(body) < int(min_blocks):
            issues.append(f"thin_section:{title}")
    if "연재" in text or "다음 글" in text:
        issues.append("series_style_language")
    if not front.get("description"):
        issues.append("missing_description")
    if not front.get("excerpt"):
        issues.append("missing_excerpt")
    if not front.get("image"):
        issues.append("missing_image")
    if "inner-products-and-norms" in text:
        formula_markers = (
            "\\langle u,v\\rangle=\\langle v,u\\rangle",
            "\\langle au+bv,w\\rangle",
            "\\langle v,v\\rangle\\ge0",
        )
        if not all(marker in text for marker in formula_markers):
            issues.append("inner_product_axioms_not_explicit")
    return {
        "low_quality": bool(issues),
        "issues": issues,
    }


def reference_titles_from_refs(refs: list[str]) -> list[str]:
    titles: list[str] = []
    for ref in refs:
        title = ref.split(",", 1)[0].strip()
        if title:
            titles.append(title)
    if PRIMARY_SOURCE_PATH.name not in titles and "Applied Linear Algebra" not in titles:
        titles.append("Applied Linear Algebra")
    return dedupe_preserve(titles)


def parse_bibtex_entries(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    pattern = re.compile(r"@(?P<kind>\w+)\{(?P<key>[^,]+),(?P<body>.*?)\n\}", re.DOTALL)
    field_pattern = re.compile(r"^\s*(\w+)\s*=\s*\{(.*)\}\s*,?\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        body = match.group("body")
        fields: dict[str, str] = {"ENTRYTYPE": match.group("kind"), "ID": match.group("key").strip()}
        for field_match in field_pattern.finditer(body):
            field_name = field_match.group(1).strip().lower()
            field_value = field_match.group(2).strip()
            fields[field_name] = field_value
        title = fields.get("title")
        if title:
            entries[normalize_text(title)] = fields
    return entries


def format_author_list(author_field: str) -> str:
    authors = [part.strip() for part in author_field.split(" and ") if part.strip()]
    pretty_names: list[str] = []
    for author in authors:
        if "," in author:
            family, given = [piece.strip() for piece in author.split(",", 1)]
            pretty_names.append(f"{given} {family}".strip())
        else:
            pretty_names.append(author)
    if len(pretty_names) <= 2:
        return " and ".join(pretty_names)
    return ", ".join(pretty_names[:-1]) + f", and {pretty_names[-1]}"


def bibliography_entries_from_refs(refs: list[str]) -> list[str]:
    titles = reference_titles_from_refs(refs)
    catalog = parse_bibtex_entries(MASTER_BIB_PATH)
    formatted: list[str] = []
    for title in titles:
        record = catalog.get(normalize_text(title))
        if not record:
            formatted.append(title)
            continue
        authors = format_author_list(record.get("author", "")).strip()
        year = record.get("year", "").strip()
        publisher = record.get("publisher", "").strip()
        book_title = record.get("title", title).strip()
        parts = []
        if authors:
            parts.append(authors)
        if year:
            parts.append(f"({year})")
        parts.append(book_title)
        if publisher:
            parts.append(publisher)
        formatted.append(". ".join(part for part in parts if part) + ".")
    return dedupe_preserve(formatted)


def generate_tags(candidate: dict[str, Any]) -> list[str]:
    bag = " ".join(
        [public_title_for(candidate), primary_query_for(candidate)]
        + candidate.get("core_concepts", [])
        + candidate.get("application_example_candidates", [])
        + ensure_list(candidate.get("secondary_queries"))
    ).lower()
    tags = ["선형대수학"]
    tags.append(primary_query_for(candidate))
    normalized_bag = normalize_text(bag)
    for key, pretty in TAG_NORMALIZATION.items():
        if key in normalized_bag:
            tags.append(pretty)
    for concept in candidate.get("core_concepts", [])[:3]:
        pretty = localized_title(concept.strip())
        if pretty and pretty not in tags:
            tags.append(pretty)
    for query in secondary_queries_for(candidate)[:3]:
        if query:
            tags.append(query)
    return dedupe_preserve(tags[:8])


def importance_level(candidate: dict[str, Any]) -> tuple[str, str]:
    slug = candidate["slug"]
    if slug in ESSENTIAL_IMPORTANCE_SLUGS:
        return "high", "이 주제는 기저, 선형계, 직교성, 스펙트럼처럼 이후 많은 글의 기반을 이루므로 중요도를 높게 둔다."
    if int(candidate["order"]) <= 12:
        return "medium", "선형대수의 기본 구조를 이루지만 다른 핵심 주제의 준비 단계로도 읽히므로 중요도는 중간으로 둔다."
    return "medium", "응용이나 확장 측면에서 중요하지만 전체 뼈대를 이루는 핵심 축보다 한 단계 뒤에 놓인다."


def independence_level(candidate: dict[str, Any]) -> tuple[str, str]:
    slug = candidate["slug"]
    if slug in HIGH_INDEPENDENCE_SLUGS:
        return "high", "앞선 글을 읽지 않아도 필요한 배경을 짧게 다시 설명하면 독립 포스트로 충분히 완결될 수 있다."
    if slug in LOW_INDEPENDENCE_SLUGS:
        return "low", "스펙트럼, 반복, 동역학 등 여러 선행 개념이 함께 필요해 독립성이 상대적으로 낮다."
    return "medium", "독립적으로 읽을 수는 있지만 핵심 개념 몇 개를 본문 안에서 다시 설명해야 한다."


def applicability_level(candidate: dict[str, Any]) -> tuple[str, str]:
    slug = candidate["slug"]
    if slug in HIGH_APPLICABILITY_SLUGS:
        return "high", "데이터, 회로, 신호, 최적화처럼 독자가 바로 떠올릴 수 있는 응용 맥락이 분명하다."
    joined = " ".join(candidate.get("application_example_candidates", []))
    if any(keyword.lower() in joined.lower() for keyword in APPLIED_KEYWORDS):
        return "high", "응용 맥락이 구체적으로 확보되어 있어 학습 동기를 강하게 줄 수 있다."
    return "medium", "응용 연결은 가능하지만 개념 구조 자체가 먼저 강조되는 편이다."


def searchability_level(candidate: dict[str, Any]) -> tuple[str, str]:
    title = public_title_for(candidate)
    slug = public_slug_for(candidate)
    primary_query = primary_query_for(candidate)
    secondaries = secondary_queries_for(candidate)
    if candidate.get("primary_query") or candidate.get("seo_title"):
        return "high", "주 검색어와 공개 제목이 명시되어 있어 제목, 설명문, 태그를 검색 의도에 맞게 설계하기 쉽다."
    if is_generic_title(title) or is_generic_slug(slug):
        return "low", "현재 제목이나 slug가 다소 추상적이어서 검색 의도를 직접 드러내기 어렵다."
    if primary_query and secondaries:
        return "high", "핵심 검색어와 보조 검색어를 함께 구성할 수 있어 검색 스니펫과 태그 설계가 수월하다."
    return "medium", "검색 가능한 개념명은 분명하지만 별도의 검색어 설계 정보가 아직 충분히 구체적이지 않다."


def evaluate_candidate(
    candidate: dict[str, Any],
    state: dict[str, Any],
    draft_entries: list[dict[str, Any]],
    post_entries: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    runtime = runtime_for(state, candidate["slug"])
    importance, importance_reason = importance_level(candidate)
    independence, independence_reason = independence_level(candidate)
    applicability, applicability_reason = applicability_level(candidate)
    searchability, searchability_reason = searchability_level(candidate)
    total_score = (
        3 * LEVEL_TO_SCORE[importance]
        + 3 * LEVEL_TO_SCORE[independence]
        + 2 * LEVEL_TO_SCORE[applicability]
        + 2 * LEVEL_TO_SCORE[searchability]
    )

    evaluation: dict[str, Any] = {
        "slug": candidate["slug"],
        "title": public_title_for(candidate),
        "internal_title": candidate["title"],
        "order": int(candidate["order"]),
        "status_before": runtime.get("status", candidate.get("status", "candidate")),
        "importance": {"level": importance, "score": LEVEL_TO_SCORE[importance], "reason": importance_reason},
        "independence": {
            "level": independence,
            "score": LEVEL_TO_SCORE[independence],
            "reason": independence_reason,
        },
        "applicability": {
            "level": applicability,
            "score": LEVEL_TO_SCORE[applicability],
            "reason": applicability_reason,
        },
        "searchability": {
            "level": searchability,
            "score": LEVEL_TO_SCORE[searchability],
            "reason": searchability_reason,
        },
        "total_score": total_score,
        "eligible": True,
        "decision": None,
        "decision_reason": None,
        "existing_draft": None,
    }

    missing = [field for field in SEMANTIC_REQUIRED_FIELDS if not candidate.get(field)]
    if missing:
        evaluation["eligible"] = False
        evaluation["decision"] = "missing_semantics"
        evaluation["decision_reason"] = f"Manifest semantic fields are incomplete: {', '.join(missing)}"
        return evaluation

    for entry in post_entries:
        if same_topic(candidate, entry):
            evaluation["eligible"] = False
            evaluation["decision"] = "published_duplicate"
            evaluation["decision_reason"] = f"Published post already exists at {entry['path']}"
            return evaluation

    for entry in draft_entries:
        if same_topic(candidate, entry):
            report = low_quality_report(entry["text"])
            evaluation["existing_draft"] = {
                "path": str(entry["path"]),
                "title": entry["title"],
                "low_quality": report["low_quality"],
                "issues": report["issues"],
            }
            if report["low_quality"]:
                evaluation["decision"] = "supersede_existing_draft"
                evaluation["decision_reason"] = "Existing draft does not meet the independent-post quality bar and can be superseded."
            else:
                evaluation["eligible"] = False
                evaluation["decision"] = "active_draft_exists"
                evaluation["decision_reason"] = f"Usable draft already exists at {entry['path']}"
            return evaluation

    return evaluation


def pick_selected_candidate(
    evaluations: list[dict[str, Any]],
    manifest_candidates: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, Any]]]:
    lookup = {candidate["slug"]: candidate for candidate in manifest_candidates}
    eligible = [item for item in evaluations if item["eligible"]]
    if not eligible:
        return None, None, evaluations

    eligible.sort(
        key=lambda item: (
            -item["total_score"],
            -item["importance"]["score"],
            -item["independence"]["score"],
            -item["searchability"]["score"],
            -item["applicability"]["score"],
            item["order"],
        )
    )
    selected_eval = eligible[0]
    ties = [
        item
        for item in eligible
        if item["total_score"] == selected_eval["total_score"]
        and item["importance"]["score"] == selected_eval["importance"]["score"]
        and item["independence"]["score"] == selected_eval["independence"]["score"]
        and item["searchability"]["score"] == selected_eval["searchability"]["score"]
        and item["applicability"]["score"] == selected_eval["applicability"]["score"]
    ]
    if len(ties) > 1:
        selected_eval["decision_reason"] = (
            "Multiple candidates tied on the published rubric; the earliest internal order was used as the operational fallback."
        )
        selected_eval["tie_candidates"] = [item["slug"] for item in ties]
    else:
        selected_eval["decision_reason"] = "Selected by rubric score and tie-break order."
    selected_eval["decision"] = "selected"
    return lookup[selected_eval["slug"]], selected_eval, evaluations


def target_draft_path(output_dir: Path, slug: str) -> Path:
    return output_dir / f"linear-algebra-{slug}.md"


def superseded_path(output_dir: Path, original: Path, now: datetime) -> Path:
    stamp = now.strftime("%Y%m%d-%H%M%S")
    dest_dir = output_dir / SUPERSCEDED_DIRNAME
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir / f"{stamp}-{original.name}"


def block_definition(title: str, body: str) -> str:
    return f"> **정의 ({title})**  \n> {body}"


def block_theorem(name: str, statement: str) -> str:
    return f"> **정리 1 ({name})**  \n> {statement}"


def fallback_blueprint(candidate: dict[str, Any]) -> dict[str, Any]:
    first, second = candidate["core_concepts"][:2]
    application = candidate["application_example_candidates"][0]
    return {
        "intro": [
            f"이 글에서는 {candidate['title']}를 독립된 하나의 주제로 다룹니다. 핵심은 {first}과 {second}이 어떤 방식으로 연결되고, 그 연결이 계산과 응용에서 왜 중요한지 분명히 하는 데 있습니다.",
            "세부 공식보다 먼저 구조를 붙잡고, 이어서 작은 예제를 직접 전개하며 실제 응용 장면과 연결하겠습니다.",
        ],
        "background": f"본문 이해에 필요한 배경은 글 안에서 다시 설명하겠지만, 중심 질문은 {candidate['representative_theorem']}라는 진술이 왜 자연스럽고 어떤 계산에서 드러나는가에 있다.",
        "definitions": [
            {
                "title": f"{first}",
                "body": f"이 글에서는 {first}을(를) 중심 개념으로 두고, 그것이 {second}와 맺는 구조적 관계를 살핀다.",
            },
            {
                "title": f"{second}",
                "body": f"{second}은(는) {first}의 계산적 또는 기하적 해석을 정리해 주는 보조 언어로 작동한다.",
            },
        ],
        "theorem_name": candidate["title"],
        "theorem_statement": candidate["representative_theorem"],
        "proof": [
            f"{candidate['representative_theorem']}라는 진술을 볼 때 가장 먼저 확인할 것은 정의가 실제로 선형성 조건과 어떻게 맞물리는가이다.",
            f"{first}의 정의를 그대로 전개하면 {second}가 등장하는 이유가 계산 안에서 드러난다. 즉, 임의의 선형결합을 취했을 때 필요한 닫힘성과 동치 조건이 유지된다.",
            f"따라서 문제의 핵심 구조는 좌표 표현을 바꾸어도 유지되고, 그 결과 {candidate['representative_theorem']}가 성립한다. $$\\square$$",
        ],
        "hand_example_intro": "작은 예제 하나를 직접 전개해 보면 정의와 정리가 서로 어떻게 맞물리는지 더 선명해집니다.",
        "hand_example_steps": [
            candidate["hand_example"],
            f"이 계산에서 중요한 것은 숫자 자체보다 {first}이(가) 어떤 제약을 만들고, 그 제약이 {second}를 어떻게 결정하는지 읽는 것이다.",
            "같은 절차를 조금 더 큰 문제에 적용하면 알고리듬이나 근사 문제로 자연스럽게 확장된다.",
        ],
        "application": [
            f"응용 쪽에서는 {application}이(가) 가장 자연스러운 예다. 문제를 이 언어로 옮기면 개념적 설명과 계산 절차가 한 번에 정리된다.",
            f"그래서 {candidate['title']}는 교재 안의 한 절에 머물지 않고, 실제 데이터나 물리 모형을 해석하는 기본 틀로 반복해서 나타난다.",
        ],
        "pitfalls": [
            f"{first}과(와) {second}를 각각 따로 외우면 왜 이 주제가 하나의 독립 포스트가 되어야 하는지 보이지 않는다.",
            candidate["overlap_hint"],
        ],
        "closing": f"{candidate['title']}의 핵심은 {first}과(와) {second}을(를) 따로 배우는 것이 아니라, 하나의 구조로 읽는 데 있다.",
        "visual_importance": "supporting" if "그림" in candidate["visual_hint"] or "도식" in candidate["visual_hint"] else "none",
        "visual_caption": candidate["visual_hint"],
    }


def blueprint_for(candidate: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(TOPIC_BLUEPRINTS.get(candidate["slug"], fallback_blueprint(candidate)))


def ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def dedupe_text(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = normalize_text(item)
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def pad_to_minimum(seed: list[str], extras: list[str], minimum: int) -> list[str]:
    merged = dedupe_text(seed)
    for item in extras:
        if len(merged) >= minimum:
            break
        if normalize_text(item) not in {normalize_text(existing) for existing in merged}:
            merged.append(item)
    return merged


def concept_labels(candidate: dict[str, Any]) -> tuple[str, str, str]:
    concepts = [item for item in candidate.get("core_concepts", []) if item]
    first = concepts[0] if concepts else candidate["title"]
    second = concepts[1] if len(concepts) > 1 else first
    third = concepts[2] if len(concepts) > 2 else second
    return first, second, third


def long_form_blueprint(candidate: dict[str, Any], depth_boost: int = 0) -> dict[str, Any]:
    seed = blueprint_for(candidate)
    first, second, third = concept_labels(candidate)
    application_examples = candidate.get("application_example_candidates", [])
    leading_application = application_examples[0] if application_examples else candidate["title"]
    secondary_application = application_examples[1] if len(application_examples) > 1 else leading_application
    public_title = public_title_for(candidate)
    background_requirements = ensure_list(candidate.get("background_requirements"))
    application_focus = ensure_list(candidate.get("application_focus"))
    common_misunderstandings = ensure_list(candidate.get("common_misunderstandings"))
    proof_focus = candidate.get("proof_focus", "").strip()
    secondary_hand_example = candidate.get("secondary_hand_example", "").strip()
    intro_target = 4 + min(depth_boost, 1)
    example_step_target = 5 + depth_boost
    application_target = 4 + min(depth_boost, 1)

    intro = pad_to_minimum(
        ensure_list(seed.get("intro")),
        [
            f"{public_title}는 {leading_application} 같은 응용에서 갑자기 등장하는 계산 규칙이 아니라, {first}과 {second}을(를) 같은 구조로 읽게 해 주는 출발점이기도 합니다.",
            f"따라서 아래에서는 정의를 적는 데서 멈추지 않고, 정리의 논리 전개와 간단한 예제, 그리고 {secondary_application}으로 이어지는 해석까지 한 번에 묶어 보겠습니다.",
        ],
        intro_target,
    )

    background_opening = pad_to_minimum(
        [seed.get("background", "").strip()] + background_requirements,
        [
            f"특히 {first}과 {second}은(는) 서로 다른 개념처럼 보이지만, 실제 계산에서는 같은 조건을 다른 언어로 적어 놓은 경우가 많습니다.",
            f"이 글에서 필요한 선수 내용은 본문 안에서 다시 짚겠지만, 핵심은 {third}이(가) 정의의 부속물이 아니라 정리와 계산을 연결하는 매개라는 점입니다.",
        ],
        3 + min(depth_boost, 1),
    )

    definition_bridge = pad_to_minimum(
        ensure_list(seed.get("definition_bridge")),
        [
            f"이제 정의를 하나씩 적어 놓고 나면, 왜 같은 문제를 {first}의 언어와 {second}의 언어로 동시에 읽을 수 있는지가 조금 더 분명해집니다.",
            f"이런 배경 위에서 대표 정리를 보면, 추상적인 진술처럼 보이던 명제가 실제 계산 절차와 정확히 맞물린다는 사실을 확인할 수 있습니다.",
        ],
        2,
    )

    theorem_context = pad_to_minimum(
        ensure_list(seed.get("theorem_context")),
        [
            f"이 글의 대표 정리는 {candidate['representative_theorem']}라는 문장을 중심으로 잡습니다. 중요한 이유는 이 진술 하나가 {first}의 정의와 {second}의 계산 규칙을 동시에 정리해 주기 때문입니다.",
            f"정리의 이름만 외우면 공식처럼 보일 수 있지만, 실제로는 어떤 정보가 보존되고 어떤 정보가 새로 드러나는지를 분명히 설명하는 문장입니다.",
            f"따라서 증명에서는 단순히 결론을 확인하는 데 그치지 않고, 왜 이 정리가 이후의 {leading_application} 같은 응용으로 자연스럽게 이어지는지도 함께 드러내겠습니다.",
        ],
        2 + min(depth_boost, 1),
    )

    proof_seed = ensure_list(seed.get("proof"))
    proof_paragraphs = proof_seed or [
        proof_focus or f"증명에서는 {first}의 정의를 직접 전개하면서 {second}이(가) 어디에서 필연적으로 나타나는지를 확인합니다. $$\\square$$"
    ]

    theorem_consequences = ensure_list(seed.get("theorem_consequences"))

    hand_example_intro = pad_to_minimum(
        ensure_list(seed.get("hand_example_intro")),
        [
            f"작은 예제를 직접 전개해 보는 이유는, 정리의 각 문장이 실제로 어떤 계산 단계에 대응하는지를 눈으로 확인하기 위해서입니다.",
            f"작은 예제라고 해서 중요도가 낮은 것은 아닙니다. 오히려 작은 예제에서는 {first}과 {second}이(가) 서로 어떻게 물리는지가 가장 선명하게 드러납니다.",
        ],
        2,
    )

    hand_example_steps = pad_to_minimum(
        ensure_list(seed.get("hand_example_steps")),
        [
            secondary_hand_example or f"같은 예제를 다른 좌표나 표현으로 다시 써 보면, 계산 절차가 달라져도 결국 읽어 내는 구조는 동일하다는 사실을 확인할 수 있습니다.",
            f"이 단계에서 중요한 것은 숫자를 끝까지 정리하는 것만이 아닙니다. 어떤 항이 {second}에 해당하고, 그 항이 왜 해석의 기준점이 되는지를 함께 읽어야 합니다.",
            f"마지막으로 결과를 다시 원래 문제의 언어로 번역하면, 계산된 값이 단순한 수가 아니라 {leading_application}에서 의미 있는 양이라는 점도 확인할 수 있습니다.",
        ],
        example_step_target,
    )

    hand_example_takeaways = pad_to_minimum(
        ensure_list(seed.get("hand_example_takeaways")),
        [
            f"이 예제에서 얻은 결론은 더 큰 문제에서도 그대로 유지됩니다. 규모가 커지면 계산은 길어지지만, 정리의 적용 방식과 해석의 논리는 달라지지 않습니다.",
            f"그래서 작은 예제를 직접 전개해 보면, 실제 응용 문제를 볼 때도 어떤 단계를 먼저 확인해야 하는지 자연스럽게 감이 잡힙니다.",
        ],
        2,
    )

    application = pad_to_minimum(
        ensure_list(seed.get("application")) + application_focus,
        [
            f"{leading_application}에서는 문제의 표면적 모습이 달라도, 핵심 계산은 결국 지금 본 구조로 환원됩니다. 그래서 추상적인 정의를 정확히 이해해 두면 응용의 세부 공식이 훨씬 덜 낯설게 느껴집니다.",
            f"또한 {secondary_application}처럼 겉보기에는 다른 분야에서도 같은 정리와 같은 계산이 반복됩니다. 선형대수가 여러 분야를 잇는 공통 언어라고 하는 이유가 바로 여기에 있습니다.",
            f"이 응용 관점은 단순한 동기 부여에 그치지 않습니다. 어떤 양이 실제로 관측 가능하고, 어떤 양이 계산의 편의를 위해 도입된 표현인지를 구분하게 해 준다는 점에서도 중요합니다.",
        ],
        application_target,
    )

    pitfalls = pad_to_minimum(
        ensure_list(seed.get("pitfalls")) + common_misunderstandings,
        [
            candidate["overlap_hint"],
            f"또 하나 흔한 오해는 {first}과 {second}을(를) 각각 따로 외워 두면 충분하다고 생각하는 것입니다. 그러나 실제로는 두 개념 사이의 대응을 읽지 못하면 계산과 해석이 금세 분리됩니다.",
        ],
        2,
    )

    closing = pad_to_minimum(
        ensure_list(seed.get("closing")),
        [
            f"결국 {candidate['title']}의 핵심은 정의, 정리, 계산, 응용이 따로 놀지 않는다는 데 있습니다. 이 흐름이 잡히면 다음 주제의 새로운 공식들도 훨씬 적은 부담으로 받아들일 수 있습니다.",
            f"이제 다음 단계에서는 지금 확인한 구조를 조금 더 복잡한 문제로 옮겨 가면서, 같은 논리가 어떻게 분해와 근사, 스펙트럼 해석으로 이어지는지 보게 됩니다.",
            f"따라서 이 글을 읽은 뒤에는 결과만 기억하기보다, 어떤 정의가 어떤 계산과 응용으로 이어졌는지를 한 번 더 연결해 보는 것이 좋습니다.",
        ],
        3,
    )

    return {
        "intro": intro,
        "background_opening": background_opening,
        "definitions": deepcopy(seed.get("definitions", [])),
        "definition_bridge": definition_bridge,
        "theorem_name": seed["theorem_name"],
        "theorem_statement": seed["theorem_statement"],
        "theorem_context": theorem_context,
        "proof_paragraphs": proof_paragraphs,
        "theorem_consequences": theorem_consequences,
        "hand_example_intro": hand_example_intro,
        "hand_example_steps": hand_example_steps,
        "hand_example_takeaways": hand_example_takeaways,
        "application": application,
        "pitfalls": pitfalls,
        "closing": closing,
        "visual_importance": seed.get("visual_importance", "none"),
        "visual_caption": seed.get("visual_caption", candidate["visual_hint"]),
    }


def automation_meta_block(candidate: dict[str, Any], slot: str) -> str:
    lines = [
        "<!--",
        f"automation-slot: {slot}",
        f"manifest: {MANIFEST_PATH}",
        f"state-file: {STATE_PATH}",
        f"primary-source: {PRIMARY_SOURCE_PATH}",
        f"design-doc: {DESIGN_PATH}",
        f"writing-spec: {WRITING_SPEC_PATH}",
        f"public-title: {public_title_for(candidate)}",
        f"public-slug: {public_slug_for(candidate)}",
        f"primary-query: {primary_query_for(candidate)}",
    ]
    lines.extend(f"source-ref: {ref}" for ref in candidate["source_refs"])
    lines.append("-->")
    return "\n".join(lines)


def render_front_matter(
    candidate: dict[str, Any],
    dt: datetime,
    tags: list[str],
    categories: list[str],
    blueprint: dict[str, Any],
) -> str:
    title = public_title_for(candidate)
    slug = public_slug_for(candidate)
    description = meta_description_for(candidate)
    excerpt = excerpt_for(candidate)
    image = image_for(candidate, blueprint)
    return "\n".join(
        [
            "---",
            f"title: {yaml_quote(title)}",
            f"date: {format_offset(dt)}",
            f"slug: {yaml_quote(slug)}",
            f"categories: {yaml_inline_list(categories)}",
            f"tags: {yaml_inline_list(tags)}",
            f"description: {yaml_quote(description)}",
            f"excerpt: {yaml_quote(excerpt)}",
            f"image: {yaml_quote(image)}",
            f"author: {yaml_quote(AUTHOR)}",
            "math: true",
            "toc: true",
            "---",
            "",
        ]
    )


def render_section(title: str, paragraphs: list[str]) -> str:
    body = "\n\n".join(paragraphs)
    return f"## {title}\n{body}"


def render_draft(candidate: dict[str, Any], manifest: dict[str, Any], slot: str, now: datetime, depth_boost: int = 0) -> tuple[str, dict[str, Any]]:
    blueprint = long_form_blueprint(candidate, depth_boost=depth_boost)
    tags = generate_tags(candidate)
    categories = manifest.get("defaults", {}).get("categories", DEFAULT_CATEGORIES)
    public_title = public_title_for(candidate)
    application_paragraphs = blueprint["application"] + [
        f"여기서 함께 짚어 둘 점은 {point}" if index == 1 else f"또한 {point}"
        for index, point in enumerate(blueprint["pitfalls"], start=1)
    ]
    parts: list[str] = [
        render_front_matter(candidate, now, tags, categories, blueprint).rstrip(),
        automation_meta_block(candidate, slot),
        "",
        f"# {public_title}",
        "",
        "\n\n".join(blueprint["intro"]),
        "",
        render_section(
            "배경과 기본 정의",
            blueprint["background_opening"]
            + [block_definition(item["title"], item["body"]) for item in blueprint["definitions"]]
            + blueprint["definition_bridge"],
        ),
        "",
        render_section(
            "핵심 정리와 증명",
            blueprint["theorem_context"]
            + [block_theorem(blueprint["theorem_name"], blueprint["theorem_statement"]), "**증명.** " + blueprint["proof_paragraphs"][0]]
            + blueprint["proof_paragraphs"][1:],
        ),
        "",
        render_section(
            "간단한 예제로 보는 구조",
            blueprint["hand_example_intro"]
            + [f"{index}. {step}" for index, step in enumerate(blueprint["hand_example_steps"], start=1)]
            + blueprint["hand_example_takeaways"],
        ),
        "",
        render_section("응용에서 다시 나타나는 구조", application_paragraphs),
    ]

    if blueprint.get("visual_importance") == "required":
        parts.extend(
            [
                "",
                render_section(
                    "그림 메모",
                    [
                        f"> **그림 메모.** {blueprint.get('visual_caption', candidate['visual_hint'])}",
                        "> 실제 게시 전에는 이 자리표시를 SVG 또는 PNG 시각자료로 대체해야 한다.",
                    ],
                ),
            ]
        )

    parts.extend(
        [
            "",
            render_section("마무리", blueprint["closing"]),
            "",
            render_section("참고문헌", [f"- {entry}" for entry in bibliography_entries_from_refs(candidate["source_refs"])]),
            "",
        ]
    )
    return "\n".join(parts), blueprint


def quality_report(text: str, candidate: dict[str, Any], blueprint: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    contract = writing_contract(manifest)
    issues: list[str] = []
    front = parse_front_matter(text)
    public_title = public_title_for(candidate)
    public_slug = public_slug_for(candidate)
    primary_query = primary_query_for(candidate)
    secondary_queries = secondary_queries_for(candidate)
    required_checks = {
        "theorem_block": "> **정리 1",
        "proof_block": "**증명.**",
        "hand_example": "## 간단한 예제로 보는 구조",
        "application": "## 응용에서 다시 나타나는 구조",
        "references": "## 참고문헌",
        "closing": "## 마무리",
    }
    for key, needle in required_checks.items():
        if needle not in text:
            issues.append(key)
    if any(heading in text for heading in ("## 손으로 따라가는 계산", "## 응용으로 보는 이유", "## 자주 헷갈리는 점", "## 정리하며")):
        issues.append("legacy_section_headings")
    if "손계산" in text:
        issues.append("legacy_hand_calculation_language")
    if normalize_text(front.get("title", "")) != normalize_text(public_title):
        issues.append("front_matter_title")
    if normalize_text(front.get("slug", "")) != normalize_text(public_slug):
        issues.append("front_matter_slug")
    if not front.get("description"):
        issues.append("missing_description")
    if not front.get("excerpt"):
        issues.append("missing_excerpt")
    if not front.get("image"):
        issues.append("missing_image")
    if normalize_text(front.get("description", "")) == normalize_text(front.get("title", "")):
        issues.append("description_repeats_title")
    if normalize_text(front.get("excerpt", "")) == normalize_text(front.get("title", "")):
        issues.append("excerpt_repeats_title")
    if normalize_text(front.get("excerpt", "")) == normalize_text(front.get("description", "")):
        issues.append("excerpt_repeats_description")
    if count_headings(text) < contract["min_sections"]:
        issues.append("too_few_sections")
    words = count_words(text)
    characters = count_characters(text)
    block_total = len(prose_blocks(text))
    if words < contract["min_words"]:
        issues.append("too_few_words")
    if characters < contract["min_characters"]:
        issues.append("too_few_characters")
    if block_total < contract["min_blocks"]:
        issues.append("too_few_blocks")
    if "다음 글" in text or "연재" in text:
        issues.append("series_style_language")
    if blueprint.get("visual_importance") == "required" and "## 그림 메모" not in text:
        issues.append("missing_required_figure_placeholder")
    if is_generic_title(front.get("title", "")):
        issues.append("weak_seo_title")
    if is_generic_slug(front.get("slug", "")):
        issues.append("weak_seo_slug")
    if not query_in_blocks(text, primary_query):
        issues.append("missing_primary_query_in_opening")
    if not query_in_heading(text, primary_query):
        matched_secondary = any(query_in_heading(text, query) for query in secondary_queries[:3])
        if not matched_secondary:
            issues.append("missing_query_in_headings")
    tag_blob = normalize_text(front.get("tags", ""))
    search_terms = [primary_query] + secondary_queries[:3]
    if not any(normalize_text(term) in tag_blob for term in search_terms if term):
        issues.append("weak_search_tags")
    if candidate.get("slug") == "inner-products-and-norms":
        formula_markers = (
            "\\langle u,v\\rangle=\\langle v,u\\rangle",
            "\\langle au+bv,w\\rangle",
            "\\langle v,v\\rangle\\ge0",
        )
        if not all(marker in text for marker in formula_markers):
            issues.append("inner_product_axioms_not_explicit")
    sections = extract_sections(text)
    for title, min_blocks in contract["section_min_blocks"].items():
        body = sections.get(title, "")
        if not body:
            continue
        if count_blocks(body) < int(min_blocks):
            issues.append(f"thin_section:{title}")
    return {
        "passed": not issues,
        "issues": issues,
        "metrics": {
            "words": words,
            "characters": characters,
            "blocks": block_total,
            "headings": count_headings(text),
            "primary_query": primary_query,
            "public_title": public_title,
            "public_slug": public_slug,
        },
    }


def build_and_check(candidate: dict[str, Any], manifest: dict[str, Any], slot: str, now: datetime) -> tuple[str, dict[str, Any], int]:
    attempts = 0
    text, blueprint = render_draft(candidate, manifest, slot, now, depth_boost=attempts)
    report = quality_report(text, candidate, blueprint, manifest)
    while not report["passed"] and attempts < 3:
        attempts += 1
        text, blueprint = render_draft(candidate, manifest, slot, now, depth_boost=attempts)
        report = quality_report(text, candidate, blueprint, manifest)
    return text, report, attempts


def final_status(candidate: dict[str, Any], report: dict[str, Any]) -> str:
    blueprint = blueprint_for(candidate)
    if not report["passed"]:
        return "needs_revision"
    if blueprint.get("visual_importance") == "required":
        return "needs_figure"
    return "review_ready"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    now = parse_now(args.now)
    output_dir = Path(args.output_dir).resolve()
    manifest = load_manifest()
    state = load_state()
    draft_entries = collect_markdown_entries(output_dir, recursive=True)
    post_entries = collect_markdown_entries(DEFAULT_POSTS_DIR, recursive=False)

    if args.index is not None:
        selected_candidate = next((item for item in manifest["candidates"] if int(item["order"]) == args.index), None)
        if selected_candidate is None:
            raise SystemExit(f"No manifest candidate with order {args.index}.")
        evaluations = [
            evaluate_candidate(selected_candidate, state, draft_entries, post_entries, now),
        ]
        selected_eval = evaluations[0] if evaluations[0]["eligible"] else None
        if selected_eval:
            selected_eval["decision"] = "selected"
            selected_eval["decision_reason"] = "Selected by explicit --index override."
    else:
        evaluations = [evaluate_candidate(item, state, draft_entries, post_entries, now) for item in manifest["candidates"]]
        selected_candidate, selected_eval, evaluations = pick_selected_candidate(evaluations, manifest["candidates"])

    for evaluation in evaluations:
        runtime = runtime_for(state, evaluation["slug"])
        runtime["last_checked_at"] = now.isoformat()
        if evaluation["decision"] and evaluation["decision"] != "selected":
            runtime["skip_reason"] = evaluation["decision_reason"]

    if not selected_candidate or not selected_eval:
        if not args.dry_run:
            state["updated_at"] = now.isoformat()
            state.setdefault("runs", []).append(
                {
                    "run_at": now.isoformat(),
                    "slot": args.slot,
                    "selected_slug": None,
                    "selected_title": None,
                    "draft_path": None,
                    "status": "no_candidate",
                    "superseded": [],
                    "evaluations": evaluations,
                }
            )
            write_state(state)
        result = {
            "status": "no_candidate",
            "reason": "No eligible independent-post candidate is currently available.",
            "evaluations": evaluations,
            "state_path": str(STATE_PATH),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    runtime = runtime_for(state, selected_candidate["slug"])
    draft_path = target_draft_path(output_dir, public_slug_for(selected_candidate))
    superseded: list[dict[str, str]] = []

    runtime["selected_at"] = now.isoformat()
    runtime["last_checked_at"] = now.isoformat()
    runtime["skip_reason"] = None
    runtime["failure_reason"] = None
    runtime["status"] = "selected"
    append_history(runtime, now, "selected", selected_eval["decision_reason"])

    existing_draft = selected_eval.get("existing_draft")
    if existing_draft and existing_draft.get("low_quality"):
        original = Path(existing_draft["path"])
        destination = superseded_path(output_dir, original, now)
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(original), str(destination))
        superseded.append({"from": str(original), "to": str(destination)})
        append_history(runtime, now, "superseded", f"Superseded low-quality draft at {original}")

    runtime["status"] = "drafting"
    append_history(runtime, now, "drafting", f"Draft generation started for {draft_path}")
    draft_text, report, attempts = build_and_check(selected_candidate, manifest, args.slot, now)
    status = final_status(selected_candidate, report)
    runtime["revision_attempts"] = attempts
    runtime["status"] = status
    runtime["draft_path"] = str(draft_path)
    if status == "needs_revision":
        runtime["failure_reason"] = ", ".join(report["issues"])
        append_history(runtime, now, "needs_revision", runtime["failure_reason"])
    else:
        append_history(runtime, now, "draft_ready", "Draft satisfies structure and content checks.")
        append_history(runtime, now, status, f"Draft finalized with status {status}.")

    if not args.dry_run:
        write_text(draft_path, draft_text)
        state["updated_at"] = now.isoformat()
        state.setdefault("runs", []).append(
            {
                "run_at": now.isoformat(),
                "slot": args.slot,
                "selected_slug": selected_candidate["slug"],
                "selected_title": public_title_for(selected_candidate),
                "draft_path": str(draft_path),
                "status": status,
                "superseded": superseded,
                "evaluations": evaluations,
            }
        )
        write_state(state)

    result = {
        "status": status,
        "slug": selected_candidate["slug"],
        "title": public_title_for(selected_candidate),
        "draft_path": str(draft_path),
        "superseded": superseded,
        "revision_attempts": attempts,
        "quality_issues": report["issues"],
        "quality_metrics": report.get("metrics", {}),
        "selected_reason": selected_eval["decision_reason"],
        "state_path": str(STATE_PATH),
        "manifest_path": str(MANIFEST_PATH),
        "dry_run": args.dry_run,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
