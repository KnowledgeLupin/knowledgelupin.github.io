#!/usr/bin/env python3
"""Generate the next draft in the linear algebra blog series."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "_reference" / "linear-algebra-series-manifest.yml"
STATE_PATH = ROOT / "_reference" / ".automation" / "linear-algebra-series-state.json"
DEFAULT_OUTPUT_DIR = ROOT / "_drafts"
STYLE_GUIDE_PATH = ROOT / "_reference" / "2026-02-24-linear-algebra-writing-style-guide.md"
OPS_DOC_PATH = ROOT / "_reference" / "2026-04-16-linear-algebra-blog-series-ops.md"
PRIMARY_SOURCE_PATH = Path(
    "/Users/kwkwon/Desktop/Obsidian/Mathematician/_shared/my-library/"
    "2018Olver - Applied Linear Algebra.pdf"
)
SITE_TIMEZONE = ZoneInfo("Europe/Berlin")
AUTHOR = "KnowledgeLupin"
CATEGORIES = ["Mathematics", "Linear Algebra"]


TOPIC_SPECS: dict[int, dict[str, Any]] = {
    1: {
        "intro": (
            "선형대수를 단지 행렬 계산의 모음으로 읽으면 뒤로 갈수록 장들의 연결이 약해집니다. "
            "이 글에서는 선형대수가 어떤 종류의 문제를 다루며, 왜 계산과 구조와 응용을 하나의 언어로 묶는지를 먼저 정리합니다."
        ),
        "prereqs": ["고등학교 수준의 일차식과 함수", "행렬과 벡터 표기법", "모형과 근사의 기본 생각"],
        "key_points": [
            {
                "title": "선형대수가 다루는 문제군",
                "note": "연립방정식, 미분방정식, 데이터 분석, 회로 모형이 모두 선형 결합과 선형 근사의 공통 문법으로 연결된다는 점을 강조합니다.",
            },
            {
                "title": "선형성과 근사의 관점",
                "note": "복잡한 비선형 현상을 직접 다루지 못하더라도 국소 선형화와 반복 계산이 강력한 출발점이 된다는 사실을 설명합니다.",
            },
            {
                "title": "연재 전체의 흐름",
                "note": "계산에서 시작해 벡터공간, 직교성, 스펙트럼, 동역학으로 나아가는 전체 흐름을 미리 보여 줍니다.",
            },
        ],
        "cautions": [
            "선형대수를 단지 연립일차방정식 풀이 기술로 축소하면 이후의 구조 이론이 왜 필요한지 놓치기 쉽습니다.",
            "응용 사례를 장식적인 예시로만 읽지 말고, 서로 다른 문제들이 어떤 공통 구조를 갖는지 확인해야 합니다.",
        ],
    },
    2: {
        "intro": (
            "선형대수의 첫 번째 작업은 연립일차방정식을 체계적으로 푸는 것입니다. "
            "이 글에서는 Gaussian elimination이 해집합을 보존하면서 문제를 어떻게 단순한 형태로 바꾸는지 단계별로 정리합니다."
        ),
        "prereqs": ["행렬의 기본 표기", "연립일차방정식의 해 개념", "덧셈과 스칼라배의 기초"],
        "key_points": [
            {
                "title": "증강행렬과 기본 행연산",
                "note": "방정식 자체 대신 증강행렬을 다루면 계산 절차와 해집합 보존 원리를 한눈에 볼 수 있습니다.",
            },
            {
                "title": "피벗과 자유변수",
                "note": "사다리꼴 형태에서 어떤 열이 선도변수를 결정하고 어떤 열이 자유도를 남기는지 분명히 설명합니다.",
            },
            {
                "title": "소거 알고리듬의 논리",
                "note": "앞에서부터 미지수를 제거해 뒤쪽의 triangular structure를 얻는 것이 왜 효율적인지 강조합니다.",
            },
        ],
        "cautions": [
            "행연산을 기계적으로 적용하기 전에 각 연산이 해집합을 보존하는 이유를 먼저 확인해야 합니다.",
            "기약행 사다리꼴만을 목표로 잡으면 실제 계산에서는 불필요하게 많은 연산을 하게 될 수 있습니다.",
        ],
    },
    3: {
        "intro": (
            "소거법은 단순히 미지수를 없애는 계산이 아니라 행렬을 곱의 형태로 분해하는 과정이기도 합니다. "
            "이 글에서는 소거법과 `LU` 분해, 그리고 전진/후진 대입이 하나의 계산 구조라는 점을 정리합니다."
        ),
        "prereqs": ["Gaussian elimination의 기본 절차", "삼각행렬의 형태", "행렬곱의 의미"],
        "key_points": [
            {
                "title": "소거와 인수분해의 대응",
                "note": "소거 단계마다 누적되는 계수를 lower triangular matrix에 모으면 `LU` 분해가 자연스럽게 드러납니다.",
            },
            {
                "title": "전진/후진 대입의 역할",
                "note": "분해 이후에는 두 개의 단순한 triangular system을 순서대로 푸는 문제로 바뀐다는 점을 설명합니다.",
            },
            {
                "title": "반복 사용에서의 이점",
                "note": "같은 계수행렬에 대해 여러 우변을 처리할 때 분해를 한 번만 계산하는 것이 얼마나 큰 이점인지 보여 줍니다.",
            },
        ],
        "cautions": [
            "`LU` 분해는 항상 가능한 것이 아니며 피벗 선택 조건을 점검해야 합니다.",
            "분해 공식을 외우는 것보다 소거 단계가 어떤 방식으로 `L`과 `U`에 기록되는지 이해하는 편이 중요합니다.",
        ],
    },
    4: {
        "intro": (
            "역행렬과 행렬식은 선형대수에서 매우 상징적인 대상이지만, 실제 계산의 주인공은 아닙니다. "
            "이 글에서는 왜 이 두 개념이 중요하면서도 직접 계산의 중심에 놓이지 않는지 설명합니다."
        ),
        "prereqs": ["행렬곱과 항등행렬", "Gaussian elimination의 기본 아이디어", "정사각행렬의 기초"],
        "key_points": [
            {
                "title": "역행렬의 이론적 의미",
                "note": "가역성, 해의 유일성, 선형사상의 동형성 같은 구조적 의미를 통해 역행렬의 중요성을 설명합니다.",
            },
            {
                "title": "행렬식의 판정 도구 역할",
                "note": "행렬식은 면적·부피의 스케일과 가역성 판정에 유용하지만 실제 해법으로 직접 쓰기에는 비효율적입니다.",
            },
            {
                "title": "계산 비용의 관점",
                "note": "역행렬 전체를 구하는 것보다 필요한 선형계를 직접 푸는 편이 훨씬 경제적이라는 점을 비교합니다.",
            },
        ],
        "cautions": [
            "`A^{-1}b`라는 공식이 있다고 해서 언제나 먼저 역행렬을 계산해야 한다고 생각하면 안 됩니다.",
            "행렬식을 0이냐 아니냐의 판정 도구로만 쓰고 끝내면 그 기하학적 의미를 놓치기 쉽습니다.",
        ],
    },
    5: {
        "intro": (
            "실제 계산에서는 정확한 대수 공식보다 반올림 오차에 얼마나 버티는지가 더 중요할 때가 많습니다. "
            "이 글에서는 pivoting이 왜 필요한지, 그리고 수치적 안정성이라는 말이 무엇을 뜻하는지 설명합니다."
        ),
        "prereqs": ["Gaussian elimination", "부동소수점 오차의 직관", "절댓값과 상대오차의 기본 개념"],
        "key_points": [
            {
                "title": "pivoting의 기본 아이디어",
                "note": "작은 피벗을 피하고 계산 중 계수의 폭주를 줄이기 위해 행 또는 열을 재배열하는 이유를 설명합니다.",
            },
            {
                "title": "round-off error의 증폭",
                "note": "정확한 공식이라도 유한 정밀도 환경에서는 오차가 누적되고 증폭될 수 있다는 점을 구체적으로 짚습니다.",
            },
            {
                "title": "practical linear algebra의 시선",
                "note": "이론적으로는 같은 해를 주는 알고리듬도 실제 계산 환경에서는 전혀 다른 품질을 낼 수 있음을 강조합니다.",
            },
        ],
        "cautions": [
            "수치적 안정성은 단순히 계산이 끝난다는 뜻이 아니라 오차가 통제 가능한 범위에 머무른다는 뜻입니다.",
            "pivoting을 예외적인 보정 절차로 보면 안 되고, 실제 구현에서는 기본 선택지로 보는 편이 자연스럽습니다.",
        ],
    },
    6: {
        "intro": (
            "벡터공간과 부분공간은 선형대수 전체의 문법을 정하는 가장 기본적인 개념입니다. "
            "이 글에서는 공리의 나열을 넘어서, 어떤 집합이 왜 선형적이라고 불릴 수 있는지 설명합니다."
        ),
        "prereqs": ["집합과 함수의 기본 개념", "실수벡터의 표기", "덧셈과 스칼라배의 연산 규칙"],
        "key_points": [
            {
                "title": "벡터공간 공리의 역할",
                "note": "공리는 계산이 가능한 최소 문법을 고정해 주며 이후 모든 정리의 출발점이 됩니다.",
            },
            {
                "title": "부분공간 판정 기준",
                "note": "영벡터 포함, 덧셈 닫힘, 스칼라배 닫힘이라는 세 조건이 실제 판정에서 어떻게 쓰이는지 정리합니다.",
            },
            {
                "title": "대표 예시의 폭",
                "note": "유클리드 공간뿐 아니라 다항식 공간과 함수공간까지 함께 보아야 개념의 추상성이 살아납니다.",
            },
        ],
        "cautions": [
            "부분공간 여부를 볼 때 닫힘성만 확인하고 영벡터 포함 여부를 빠뜨리는 실수가 자주 생깁니다.",
            "벡터를 화살표 그림으로만 이해하면 함수공간이나 행렬공간으로 자연스럽게 확장하기 어렵습니다.",
        ],
    },
    7: {
        "intro": (
            "기저와 차원은 벡터공간의 자유도를 가장 압축된 방식으로 기록하는 언어입니다. "
            "이 글에서는 생성과 선형독립이 어떻게 만나 기저를 이루고, 차원이 왜 구조적 불변량이 되는지 정리합니다."
        ),
        "prereqs": ["벡터공간과 부분공간", "유한 집합의 기초", "행렬의 열벡터 관점"],
        "key_points": [
            {
                "title": "span과 선형독립의 긴장",
                "note": "많이 생성하려면 중복이 생기기 쉽고, 중복을 없애면 생성력이 약해지기 쉬운 두 요구가 기저에서 균형을 이룹니다.",
            },
            {
                "title": "기저의 존재와 교체 원리",
                "note": "기저는 우연한 예시가 아니라 벡터공간의 핵심 구조이며, 교체 정리는 그 안정성을 보여 줍니다.",
            },
            {
                "title": "차원의 불변성",
                "note": "기저 선택이 달라져도 기저의 원소 수는 같다는 사실이 차원을 구조적 수치로 만들어 줍니다.",
            },
        ],
        "cautions": [
            "생성과 선형독립을 서로 반대되는 성질로만 보면 기저의 의미를 놓치기 쉽습니다.",
            "차원을 단지 원소의 개수처럼 오해하면 무한차원 공간이나 함수공간을 이해하기 어려워집니다.",
        ],
    },
    8: {
        "intro": (
            "Kernel, image, rank-nullity는 선형사상이 해를 어떻게 압축하고 남기는지를 동시에 보여 줍니다. "
            "이 글에서는 해의 자유도와 출력의 차원을 연결하는 가장 중요한 정리 하나를 중심으로 설명합니다."
        ),
        "prereqs": ["기저와 차원", "선형결합", "행렬의 열공간 직관"],
        "key_points": [
            {
                "title": "kernel과 해의 자유도",
                "note": "동차방정식의 해공간이 왜 kernel로 나타나고, 자유변수의 수가 nullity와 맞물리는지 설명합니다.",
            },
            {
                "title": "image와 도달 가능한 출력",
                "note": "선형사상이 실제로 만들어 낼 수 있는 값들의 집합을 image로 보고, 그 차원이 rank가 되는 이유를 봅니다.",
            },
            {
                "title": "rank-nullity의 균형식",
                "note": "입력 차원이 kernel과 image의 차원으로 분해된다는 사실이 선형대수의 핵심 구조를 드러냅니다.",
            },
        ],
        "cautions": [
            "kernel과 image를 각각 해공간과 열공간으로만 외우면 선형사상 전체의 언어로 확장하기 어렵습니다.",
            "rank-nullity를 공식으로만 기억하지 말고 입력 자유도의 분해로 읽어야 응용에서 힘을 발휘합니다.",
        ],
    },
    9: {
        "intro": (
            "그래프는 조합론적 대상처럼 보이지만 incidence matrix를 도입하는 순간 선형대수의 문제로 바뀝니다. "
            "이 글에서는 꼭짓점과 변의 정보를 행렬로 옮기는 방식이 어떤 구조를 드러내는지 설명합니다."
        ),
        "prereqs": ["행렬과 벡터의 표기", "기저와 차원", "그래프의 기초 용어"],
        "key_points": [
            {
                "title": "incidence matrix의 정의",
                "note": "각 변이 어떤 꼭짓점에 들어오고 나가는지를 부호 있는 열벡터로 기록하는 방식이 핵심입니다.",
            },
            {
                "title": "그래프 정보의 선형화",
                "note": "연결성, 흐름, 회로 같은 조합적 정보가 행렬의 kernel과 cokernel 언어로 옮겨집니다.",
            },
            {
                "title": "응용을 위한 준비",
                "note": "이 관점은 이후 Markov process, spectral graph theory, 네트워크 문제로 이어지는 기반이 됩니다.",
            },
        ],
        "cautions": [
            "incidence matrix는 adjacency matrix와 역할이 다르므로 둘을 섞어 쓰지 않도록 주의해야 합니다.",
            "그래프의 방향 부호는 임의로 정해도 되지만, 정한 뒤에는 끝까지 일관되게 유지해야 합니다.",
        ],
    },
    10: {
        "intro": (
            "그래프 위의 회로를 선형대수로 보면 단순한 그림이 차원 공식으로 바뀝니다. "
            "이 글에서는 독립 회로의 수와 Euler 공식이 어떻게 cokernel 관점에서 나타나는지 정리합니다."
        ),
        "prereqs": ["그래프와 incidence matrix", "kernel과 cokernel의 기본 생각", "차원의 계산"],
        "key_points": [
            {
                "title": "회로의 벡터 표현",
                "note": "회로를 edge vector로 표현하면 서로 다른 회로의 독립성을 선형독립성으로 읽을 수 있습니다.",
            },
            {
                "title": "cokernel과 독립 회로 수",
                "note": "incidence matrix의 cokernel 차원이 독립 회로의 개수와 맞물린다는 점을 강조합니다.",
            },
            {
                "title": "Euler 공식의 선형대수적 증명",
                "note": "정점 수, 변 수, 독립 회로 수 사이의 관계가 rank 계산 하나로 자연스럽게 도출됩니다.",
            },
        ],
        "cautions": [
            "Euler 공식을 단순 암기식으로만 보면 왜 회로의 수와 연결되는지 이해하기 어렵습니다.",
            "그래프의 평면성 여부와 독립 회로의 선형대수적 차원을 같은 개념으로 혼동하지 말아야 합니다.",
        ],
    },
    11: {
        "intro": (
            "내적과 노름은 길이와 각도를 추상적인 공간으로 옮기는 장치입니다. "
            "이 글에서는 유클리드 공간의 익숙한 기하학이 함수공간으로 확장되는 과정을 중심으로 설명합니다."
        ),
        "prereqs": ["벡터공간", "절댓값과 거리", "적분의 기초 직관"],
        "key_points": [
            {
                "title": "inner product의 구조",
                "note": "대칭성, 선형성, 양의 정부호성이라는 세 조건이 길이와 각도의 기반을 이룬다는 점을 정리합니다.",
            },
            {
                "title": "norm과 거리",
                "note": "내적에서 노름과 거리가 어떻게 유도되며, 이것이 계산과 수렴 논의에 어떤 의미를 주는지 설명합니다.",
            },
            {
                "title": "함수공간으로의 확장",
                "note": "벡터가 수열이나 함수일 때도 동일한 개념틀이 작동한다는 사실이 추상화의 힘을 보여 줍니다.",
            },
        ],
        "cautions": [
            "모든 노름이 반드시 어떤 내적에서 오는 것은 아니므로 두 개념을 동일시하면 안 됩니다.",
            "함수공간의 내적은 적분으로 정의되지만, 그 의미를 좌표공간의 점곱과 단순 동일시하면 세부 구조를 놓칩니다.",
        ],
    },
    12: {
        "intro": (
            "Cauchy-Schwarz 부등식은 내적공간에서 가능한 거의 모든 기하학적 논의의 출발점입니다. "
            "이 글에서는 이 부등식이 왜 직교성, 삼각부등식, 투영 논의로 이어지는지 정리합니다."
        ),
        "prereqs": ["inner product와 norm", "기본적인 대수 전개", "직교의 직관"],
        "key_points": [
            {
                "title": "Cauchy-Schwarz 부등식의 의미",
                "note": "내적이 길이의 곱보다 클 수 없다는 제약이 각도와 직교의 개념을 가능하게 합니다.",
            },
            {
                "title": "직교성과 최소화",
                "note": "직교는 단지 각이 90도인 상태가 아니라 오차를 최소화하는 방향이라는 사실을 강조합니다.",
            },
            {
                "title": "삼각부등식으로의 연결",
                "note": "노름의 기본 성질도 결국 Cauchy-Schwarz에서 나온다는 흐름을 보여 줍니다.",
            },
        ],
        "cautions": [
            "부등식의 증명을 외우는 데 그치면 왜 equality case가 중요한지 놓치기 쉽습니다.",
            "직교를 좌표축이 서로 수직인 그림으로만 이해하면 함수공간이나 추상공간에서 막히기 쉽습니다.",
        ],
    },
    13: {
        "intro": (
            "양의 정부호 행렬은 이차형식, 에너지, 최소화 문제를 묶어 주는 중심 개념입니다. "
            "이 글에서는 Gram matrix와 positive definite matrix가 왜 자주 함께 등장하는지 설명합니다."
        ),
        "prereqs": ["inner product와 norm", "대칭행렬의 기초", "이차식 전개"],
        "key_points": [
            {
                "title": "positive definite의 판정 의미",
                "note": "벡터를 0이 아닌 방향으로 움직였을 때 언제나 양의 값을 주는 이차형식이 안정성과 최소화의 기반이 됩니다.",
            },
            {
                "title": "Gram matrix의 자연스러움",
                "note": "내적을 행렬로 모으면 positive semidefinite 구조가 자동으로 생긴다는 점을 보여 줍니다.",
            },
            {
                "title": "에너지와 최소화의 연결",
                "note": "양의 정부호성은 최소값 존재와 유일성, 그리고 수치 알고리듬의 안정성까지 이어집니다.",
            },
        ],
        "cautions": [
            "모든 대칭행렬이 양의 정부호인 것은 아니며, 고유값 정보와 함께 봐야 합니다.",
            "Gram matrix는 단순한 계산 보조물이 아니라 내적 구조를 좌표로 끌어온 핵심 표현이라는 점을 잊지 말아야 합니다.",
        ],
    },
    14: {
        "intro": (
            "완전제곱과 Cholesky 분해는 이차형식을 가장 잘 보이는 좌표로 바꾸는 방법입니다. "
            "이 글에서는 대칭 양의 정부호 행렬의 구조가 왜 triangular factorization으로 떨어지는지 설명합니다."
        ),
        "prereqs": ["positive definite matrix", "삼각행렬", "이차형식의 기초"],
        "key_points": [
            {
                "title": "completing the square의 관점",
                "note": "복잡한 이차식을 반복적으로 정리하면 독립적인 제곱합 형태에 가까워지는 과정을 설명합니다.",
            },
            {
                "title": "Cholesky 분해의 구조",
                "note": "대칭 양의 정부호 행렬을 `LL^T` 꼴로 쓰는 것이 계산과 해석 모두에서 왜 편리한지 다룹니다.",
            },
            {
                "title": "최소화 문제와의 연결",
                "note": "분해된 형태는 에너지 함수의 양의 성질과 유일한 최소점을 훨씬 투명하게 보여 줍니다.",
            },
        ],
        "cautions": [
            "Cholesky 분해는 일반 행렬이 아니라 대칭 양의 정부호 행렬에서만 자연스럽게 작동합니다.",
            "완전제곱을 단순한 대수 기술로만 보면 최소화와 안정성으로 이어지는 의미를 놓치기 쉽습니다.",
        ],
    },
    15: {
        "intro": (
            "직교투영과 최소제곱은 정확히 풀 수 없는 문제를 가장 잘 근사하는 방법을 제공합니다. "
            "이 글에서는 기하학적 투영 그림과 행렬 계산이 같은 내용을 말하고 있음을 설명합니다."
        ),
        "prereqs": ["직교성", "positive definite matrix", "연립방정식의 해 구조"],
        "key_points": [
            {
                "title": "closest point 문제",
                "note": "주어진 점에서 부분공간으로 내린 수선의 발이 최소제곱 문제의 기하학적 핵심입니다.",
            },
            {
                "title": "normal equation의 해석",
                "note": "오차가 부분공간에 직교해야 한다는 조건이 곧 최소제곱의 정상 방정식으로 이어집니다.",
            },
            {
                "title": "근사와 데이터 적합",
                "note": "정확한 해가 없더라도 가장 작은 오차를 주는 해를 찾는다는 관점이 실제 응용에서 얼마나 중요한지 보여 줍니다.",
            },
        ],
        "cautions": [
            "최소제곱해는 원래 문제의 정확한 해가 아니라 오차를 최소화한 근사해라는 점을 분명히 해야 합니다.",
            "정상 방정식을 공식처럼 쓰기 전에 왜 오차가 직교해야 하는지 기하학적으로 이해하는 편이 좋습니다.",
        ],
    },
    16: {
        "intro": (
            "직교기저를 만들면 계산이 급격히 단순해집니다. "
            "이 글에서는 Gram-Schmidt 과정과 `QR` 분해가 왜 직교화와 수치 계산의 기본 도구가 되는지 설명합니다."
        ),
        "prereqs": ["직교성", "기저와 차원", "삼각행렬과 행렬곱"],
        "key_points": [
            {
                "title": "Gram-Schmidt의 아이디어",
                "note": "기존 벡터에서 이미 확보한 방향의 성분을 빼면 새로운 직교 방향을 얻는다는 단순한 원리를 강조합니다.",
            },
            {
                "title": "orthonormal basis의 계산 이점",
                "note": "직교정규기저에서는 좌표 추출과 투영 계산이 내적 하나로 정리된다는 점을 보여 줍니다.",
            },
            {
                "title": "`QR` 분해로의 연결",
                "note": "열벡터를 직교화한 결과를 모으면 자연스럽게 `A = QR` 구조가 나오며, 이는 수치해석의 핵심 도구가 됩니다.",
            },
        ],
        "cautions": [
            "직교화 과정은 이론적으로 단순해 보여도 실제 수치 계산에서는 수정된 알고리듬이 필요할 수 있습니다.",
            "`Q`와 `R`을 기호로만 기억하지 말고, 각각 직교 기저와 좌표 변환 정보를 담는다는 점을 이해해야 합니다.",
        ],
    },
    17: {
        "intro": (
            "Fredholm alternative는 선형계가 언제 풀리고 언제 막히는지에 대한 구조적 답을 줍니다. "
            "이 글에서는 직교여공간과 적합성 조건이 만나는 지점을 중심으로 설명합니다."
        ),
        "prereqs": ["kernel과 image", "직교성과 직교여공간", "선형계의 해 구조"],
        "key_points": [
            {
                "title": "compatibility 조건",
                "note": "우변이 어떤 부분공간에 직교해야만 해가 존재한다는 구조적 조건을 분명히 합니다.",
            },
            {
                "title": "adjoint 관점",
                "note": "적합성 조건은 원래 행렬이 아니라 그 수반 또는 전치가 만드는 공간과 자연스럽게 연결됩니다.",
            },
            {
                "title": "해의 존재와 자유도",
                "note": "해가 존재할 때도 유일할 수 있고 무한히 많을 수 있으며, 그 차이가 kernel 구조에서 나온다는 점을 봅니다.",
            },
        ],
        "cautions": [
            "Fredholm alternative를 추상적인 정리로만 보면 실제 연립방정식의 적합성 판정과 연결되지 않습니다.",
            "해의 존재 조건과 해의 유일성 조건은 서로 다른 층위의 문제라는 점을 분리해서 보아야 합니다.",
        ],
    },
    18: {
        "intro": (
            "보간과 근사는 주어진 데이터를 함수나 다항식으로 바꾸는 두 가지 서로 다른 전략입니다. "
            "이 글에서는 정확히 맞추는 것과 잘 맞추는 것의 차이를 선형대수 언어로 설명합니다."
        ),
        "prereqs": ["least squares", "다항식의 기초", "행렬과 계수 벡터의 대응"],
        "key_points": [
            {
                "title": "interpolation의 조건",
                "note": "주어진 점들을 정확히 통과하는 함수를 찾는 문제는 선형계 하나로 정리할 수 있습니다.",
            },
            {
                "title": "approximation의 관점",
                "note": "데이터가 많거나 잡음이 있을 때는 정확한 일치보다 오차 제어가 더 중요한 목표가 됩니다.",
            },
            {
                "title": "선형대수적 통일",
                "note": "둘 다 결국 기저 선택, 계수행렬, 오차 측정 방식의 차이로 설명할 수 있다는 점이 핵심입니다.",
            },
        ],
        "cautions": [
            "모든 데이터에 대해 높은 차수 다항식 보간을 하는 것이 좋은 근사라고 생각하면 안 됩니다.",
            "정확히 맞춘다는 사실과 안정적으로 예측한다는 사실은 서로 다른 평가 기준이라는 점을 기억해야 합니다.",
        ],
    },
    19: {
        "intro": (
            "직교다항식은 함수공간에서의 직교기저라는 관점을 가장 잘 보여 주는 예시입니다. "
            "이 글에서는 직교다항식과 최소제곱근사가 왜 자연스럽게 만나게 되는지 설명합니다."
        ),
        "prereqs": ["inner product와 함수공간", "least squares", "다항식의 기초"],
        "key_points": [
            {
                "title": "직교다항식의 구조",
                "note": "Legendre 다항식처럼 서로 직교하는 다항식족은 함수공간의 좌표계를 제공해 줍니다.",
            },
            {
                "title": "함수공간의 최소제곱근사",
                "note": "함수를 직교기저로 전개하면 근사 계수 계산이 유한차원 벡터와 거의 같은 방식으로 진행됩니다.",
            },
            {
                "title": "기저 선택의 효과",
                "note": "표준 단항식 기저보다 직교기저가 계산과 해석에서 얼마나 유리한지를 비교합니다.",
            },
        ],
        "cautions": [
            "직교다항식은 단지 특별한 함수족이 아니라 내적과 가중치 선택이 만들어 낸 구조라는 점을 봐야 합니다.",
            "최소제곱근사에서 기저만 바꾸면 문제가 끝난다고 생각하면 오차 해석과 수치 안정성을 놓치기 쉽습니다.",
        ],
    },
    20: {
        "intro": (
            "Spline은 보간과 근사 문제를 전역 고차다항식 대신 구간별 다항식으로 푸는 방법입니다. "
            "이 글에서는 spline이 왜 국소성, 매끄러움, 계산 효율을 동시에 확보하는지 설명합니다."
        ),
        "prereqs": ["보간과 근사", "다항식의 기초", "연속성과 매끄러움의 기본 개념"],
        "key_points": [
            {
                "title": "piecewise polynomial의 관점",
                "note": "전체 구간을 한 번에 다루는 대신 작은 구간마다 다항식을 두는 것이 안정성에 어떤 도움을 주는지 설명합니다.",
            },
            {
                "title": "연결 조건의 역할",
                "note": "각 구간을 이어 붙일 때 함수값과 도함수 조건을 어떻게 맞추는지가 spline의 핵심입니다.",
            },
            {
                "title": "국소 제어와 계산성",
                "note": "데이터 일부를 바꾸었을 때 전체 해가 흔들리지 않는다는 국소성이 spline의 큰 장점입니다.",
            },
        ],
        "cautions": [
            "spline을 단순히 보간 다항식의 한 종류로만 보면 국소성과 계산 효율이라는 핵심 장점을 놓칩니다.",
            "연속성 조건을 너무 약하게 두거나 너무 강하게 두면 원하는 근사 성질을 잃을 수 있습니다.",
        ],
    },
    21: {
        "intro": (
            "이산 푸리에 변환은 샘플 데이터를 주파수 성분으로 다시 읽는 방법입니다. "
            "이 글에서는 DFT의 선형대수적 구조와 FFT가 계산량을 어떻게 줄이는지를 설명합니다."
        ),
        "prereqs": ["복소수의 기본 성질", "행렬벡터 곱", "주기함수와 삼각함수의 기초"],
        "key_points": [
            {
                "title": "DFT의 행렬 구조",
                "note": "샘플 벡터를 복소 지수 기저에 대한 좌표로 바꾸는 선형변환으로 DFT를 해석합니다.",
            },
            {
                "title": "주파수 해석의 의미",
                "note": "시간 영역의 데이터를 주파수 성분으로 바꾸면 압축과 필터링이 훨씬 자연스러워집니다.",
            },
            {
                "title": "FFT의 계산 절감",
                "note": "대칭성과 분할 정복을 이용하면 계산량이 급격히 줄어든다는 점을 구조적으로 설명합니다.",
            },
        ],
        "cautions": [
            "DFT와 연속 푸리에 변환은 밀접하지만 같은 대상이 아니므로 샘플링 맥락을 분명히 해야 합니다.",
            "FFT는 새로운 수학적 변환이 아니라 DFT를 빠르게 계산하는 알고리듬이라는 점을 구분해야 합니다.",
        ],
    },
    22: {
        "intro": (
            "주파수 관점에서 보면 압축과 잡음제거는 선형변환 뒤의 좌표 선택 문제로 바뀝니다. "
            "이 글에서는 선형대수가 디지털 데이터 처리에서 어떤 실질적 힘을 갖는지 설명합니다."
        ),
        "prereqs": ["DFT와 FFT", "벡터의 좌표 표현", "오차와 근사의 기초 개념"],
        "key_points": [
            {
                "title": "중요한 성분만 남기는 압축",
                "note": "대부분의 에너지가 소수의 계수에 몰릴 때 좌표를 잘 선택하면 데이터 표현을 크게 줄일 수 있습니다.",
            },
            {
                "title": "고주파 성분과 잡음",
                "note": "주파수 영역에서는 잡음이 특정 패턴으로 드러나기 때문에 필터링 전략이 명확해집니다.",
            },
            {
                "title": "선형변환 선택의 중요성",
                "note": "무엇을 기준으로 좋은 기저를 고를 것인지가 압축률과 복원 품질을 좌우합니다.",
            },
        ],
        "cautions": [
            "계수를 많이 지운다고 해서 항상 좋은 압축이 되는 것은 아니며, 복원 오류를 함께 봐야 합니다.",
            "잡음제거는 데이터의 진짜 고주파 성분까지 함께 깎아낼 수 있으므로 해석 기준이 필요합니다.",
        ],
    },
    23: {
        "intro": (
            "스프링-질량계는 선형대수가 물리적 모형으로 어떻게 들어가는지 보여 주는 대표적인 예입니다. "
            "이 글에서는 힘의 평형과 에너지 최소화가 왜 같은 내용을 말하는지 설명합니다."
        ),
        "prereqs": ["least squares와 최소화의 기초", "양의 정부호 행렬", "힘과 에너지의 물리 직관"],
        "key_points": [
            {
                "title": "스프링-질량계의 선형 모형",
                "note": "Hooke 법칙 아래에서는 힘의 관계가 선형계로 정리되어 행렬 모델이 자연스럽게 등장합니다.",
            },
            {
                "title": "에너지 최소화 원리",
                "note": "평형 상태는 힘의 합이 0인 상태이면서 동시에 퍼텐셜 에너지가 최소가 되는 상태로 읽을 수 있습니다.",
            },
            {
                "title": "모형과 계산의 결합",
                "note": "선형대수는 단지 해를 계산하는 역할뿐 아니라 물리적 해석의 구조를 드러내는 역할도 맡습니다.",
            },
        ],
        "cautions": [
            "힘의 평형식과 에너지 최소화식을 별개의 원리처럼 보면 두 접근의 일치가 주는 통찰을 놓칩니다.",
            "선형 모델은 작은 변형이나 이상화 조건에 기대고 있으므로 모형의 적용 범위를 항상 함께 봐야 합니다.",
        ],
    },
    24: {
        "intro": (
            "전기회로는 선형 방정식이 실제 세계에서 얼마나 자연스럽게 등장하는지 보여 주는 또 하나의 예입니다. "
            "이 글에서는 회로의 평형과 스프링-질량계 사이의 대응까지 함께 설명합니다."
        ),
        "prereqs": ["연립일차방정식", "그래프와 incidence matrix", "기본적인 전압·전류 개념"],
        "key_points": [
            {
                "title": "회로 방정식의 선형 구조",
                "note": "Kirchhoff 법칙과 저항 관계를 정리하면 미지 전압과 전류에 대한 선형계가 자연스럽게 나타납니다.",
            },
            {
                "title": "그래프 관점의 회로 해석",
                "note": "회로를 그래프로 보면 incidence matrix와 회로 공간의 언어가 곧바로 들어옵니다.",
            },
            {
                "title": "기계-전기 대응",
                "note": "스프링-질량계와 전기회로가 서로 다른 현상처럼 보여도 같은 선형 구조를 공유한다는 점을 보여 줍니다.",
            },
        ],
        "cautions": [
            "회로 문제를 단순한 공식 대입 문제로만 보면 왜 그래프와 선형대수가 자연스럽게 연결되는지 보이지 않습니다.",
            "물리량의 단위와 부호 규약을 무시하면 선형계는 맞아 보여도 해석이 틀릴 수 있습니다.",
        ],
    },
    25: {
        "intro": (
            "행렬은 선형사상을 좌표계 안에서 기록한 모습입니다. "
            "이 글에서는 선형사상, 기저변환, affine transformation이 서로 어떻게 연결되는지 설명합니다."
        ),
        "prereqs": ["기저와 차원", "kernel과 image", "행렬과 벡터 곱"],
        "key_points": [
            {
                "title": "선형사상의 본질",
                "note": "선형사상은 벡터공간 사이의 구조 보존 규칙이며, 행렬은 그 규칙을 특정 기저에서 본 좌표 표현입니다.",
            },
            {
                "title": "기저변환과 similarity",
                "note": "같은 사상이라도 기저를 바꾸면 행렬은 달라지며, similarity는 이러한 좌표 변화의 흔적입니다.",
            },
            {
                "title": "affine transformation의 기하학",
                "note": "선형 변환에 평행이동을 더하면 실제 기하학적 변형과 그래픽스에서 쓰이는 affine structure가 나타납니다.",
            },
        ],
        "cautions": [
            "행렬이 곧 사상이라고 생각하면 기저를 바꿨을 때 무엇이 본질이고 무엇이 표현인지 흐려집니다.",
            "affine transformation은 선형성이 완전히 사라진 경우가 아니라 선형 부분과 평행이동이 결합된 구조입니다.",
        ],
    },
    26: {
        "intro": (
            "고유값 이론은 복잡한 선형변환을 가장 잘 보이는 좌표계에서 읽으려는 시도입니다. "
            "이 글에서는 eigenvalue, diagonalization, spectral theorem이 만드는 큰 흐름을 설명합니다."
        ),
        "prereqs": ["선형사상과 행렬표현", "기저변환", "대칭행렬의 기초"],
        "key_points": [
            {
                "title": "eigenvalue 문제의 의미",
                "note": "어떤 방향은 변환 뒤에도 방향을 유지하며 크기만 바뀌는데, 이것이 고유값 문제의 출발점입니다.",
            },
            {
                "title": "대각화의 힘",
                "note": "적절한 기저를 찾으면 복잡한 변환이 좌표별 스칼라배로 분해되어 계산과 해석이 급격히 단순해집니다.",
            },
            {
                "title": "spectral theorem의 구조",
                "note": "대칭행렬이나 self-adjoint operator에서는 직교기저로 대각화가 가능하다는 점이 핵심입니다.",
            },
        ],
        "cautions": [
            "모든 행렬이 대각화 가능한 것은 아니므로 eigenvector가 충분히 모인다는 가정을 자동으로 두면 안 됩니다.",
            "고유값을 찾는 계산과 스펙트럴 정리의 구조적 의미를 분리해서 봐야 전체 그림이 선명해집니다.",
        ],
    },
    27: {
        "intro": (
            "특이값 이론은 정사각행렬과 대칭행렬 바깥에서도 행렬의 크기와 방향 왜곡을 읽게 해 줍니다. "
            "이 글에서는 singular value, pseudoinverse, condition number를 한 흐름으로 설명합니다."
        ),
        "prereqs": ["inner product", "spectral theorem의 기초", "least squares"],
        "key_points": [
            {
                "title": "singular value의 해석",
                "note": "행렬이 단위구를 타원체로 보내는 방식에서 각 축의 길이가 singular value로 읽힌다는 점을 강조합니다.",
            },
            {
                "title": "pseudoinverse와 최소제곱",
                "note": "정사각이 아니거나 가역이 아닌 경우에도 가장 자연스러운 역연산이 최소제곱 관점에서 정의됩니다.",
            },
            {
                "title": "condition number와 민감도",
                "note": "입력의 작은 오차가 출력에서 얼마나 증폭되는지를 singular value가 정량화해 줍니다.",
            },
        ],
        "cautions": [
            "특이값은 고유값의 대체물이 아니라 일반 행렬에서의 왜곡 크기를 보여 주는 별도의 구조입니다.",
            "condition number를 단지 큰 수치 하나로만 보면 어떤 방향이 문제를 일으키는지 보이지 않습니다.",
        ],
    },
    28: {
        "intro": (
            "PCA는 데이터의 분산을 가장 잘 설명하는 방향을 찾는 선형대수적 절차입니다. "
            "이 글에서는 공분산 행렬과 특이값/고유값 이론이 데이터 분석으로 이어지는 과정을 설명합니다."
        ),
        "prereqs": ["특이값 또는 고유값의 기초", "평균과 분산의 기본 개념", "행렬 데이터 표기"],
        "key_points": [
            {
                "title": "variance와 covariance",
                "note": "데이터의 퍼짐과 변수 간 상관 구조를 행렬 하나로 요약하는 것이 PCA의 출발점입니다.",
            },
            {
                "title": "주성분 방향의 선택",
                "note": "분산을 최대화하는 방향을 찾는 문제가 결국 고유값 문제로 바뀐다는 점을 설명합니다.",
            },
            {
                "title": "차원 축소의 해석",
                "note": "적은 수의 주성분으로 데이터를 설명하면 정보 손실과 단순화 사이의 균형을 볼 수 있습니다.",
            },
        ],
        "cautions": [
            "PCA는 지도학습 기법이 아니라 데이터의 선형 구조를 요약하는 비지도적 방법입니다.",
            "공분산 기반 분석은 스케일과 중심화에 민감하므로 전처리를 빼고 논의하면 결과 해석이 왜곡됩니다.",
        ],
    },
    29: {
        "intro": (
            "반복은 큰 행렬을 직접 다루기 어려울 때 선형대수가 택하는 기본 전략입니다. "
            "이 글에서는 iterative system, Markov process, iterative solver가 왜 같은 장에서 만나는지 설명합니다."
        ),
        "prereqs": ["행렬곱의 반복", "수열의 수렴 직관", "선형계와 고정점의 기본 개념"],
        "key_points": [
            {
                "title": "iteration의 기본 구조",
                "note": "한 번의 선형 변환을 계속 반복할 때 어떤 성분이 살아남고 어떤 성분이 사라지는지가 핵심입니다.",
            },
            {
                "title": "Markov process의 선형성",
                "note": "확률 벡터의 진화도 전이행렬의 반복으로 표현되므로 선형대수의 도구가 그대로 들어갑니다.",
            },
            {
                "title": "iterative solver의 필요",
                "note": "대규모 문제에서는 직접법보다 반복법이 현실적이며, 수렴 조건을 아는 것이 중요합니다.",
            },
        ],
        "cautions": [
            "반복법은 계산을 덜 하는 대신 수렴 보장이 자동으로 따라오는 것이 아니므로 안정성 분석이 필요합니다.",
            "Markov process를 단지 확률론의 예시로만 보면 행렬 반복과의 구조적 공통점을 놓치게 됩니다.",
        ],
    },
    30: {
        "intro": (
            "스펙트럼 계산과 선형 동역학의 마지막 주제들은 선형대수가 계산과 해석을 얼마나 깊게 결합하는지 보여 줍니다. "
            "이 글에서는 power method, `QR` algorithm, Krylov methods, matrix exponential, stability, resonance를 한 흐름으로 묶어 설명합니다."
        ),
        "prereqs": ["eigenvalue와 spectral theorem", "iteration의 기초", "미분방정식의 가장 기본적인 직관"],
        "key_points": [
            {
                "title": "고유값 계산 알고리듬",
                "note": "power method와 `QR` algorithm은 행렬의 스펙트럼을 직접 계산하기 위한 대표적 절차입니다.",
            },
            {
                "title": "Krylov 부분공간의 아이디어",
                "note": "큰 문제에서 필요한 정보만 부분공간에 모아 계산하는 전략이 현대 반복법의 중심을 이룹니다.",
            },
            {
                "title": "matrix exponential과 동역학",
                "note": "선형 미분방정식의 해, 안정성, 공명 현상은 결국 스펙트럼과 행렬지수의 언어로 정리됩니다.",
            },
        ],
        "cautions": [
            "고유값 알고리듬은 단지 계산 절차가 아니라 어떤 스펙트럼 정보가 반복에서 드러나는지를 이해해야 제대로 보입니다.",
            "선형 동역학의 안정성과 공명은 공식 대입보다 스펙트럼 구조를 먼저 보는 편이 훨씬 선명합니다.",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slot", choices=("am", "pm"), required=True, help="Automation slot label.")
    parser.add_argument("--now", help="Override the current timestamp with an ISO-8601 string.")
    parser.add_argument("--dry-run", action="store_true", help="Render metadata without writing files or state.")
    parser.add_argument("--index", type=int, help="Generate a specific manifest order without advancing state.")
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


def load_manifest() -> list[dict[str, Any]]:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Manifest must be a JSON list stored in YAML-compatible form.")

    validated: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Manifest entries must be objects.")
        for field in ("order", "title", "slug", "tags", "source_refs", "status"):
            if field not in item:
                raise ValueError(f"Missing required manifest field: {field}")
        validated.append(item)
    return sorted(validated, key=lambda item: int(item["order"]))


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"next_order": 1, "updated_at": None, "history": []}

    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("State file must contain a JSON object.")
    data.setdefault("next_order", 1)
    data.setdefault("updated_at", None)
    data.setdefault("history", [])
    return data


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def format_offset(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S %z")


def build_goals(spec: dict[str, Any]) -> list[str]:
    points = spec["key_points"]
    return [
        f"{points[0]['title']}이 이 주제에서 왜 먼저 등장하는지 설명할 수 있습니다.",
        f"`{points[1]['title']}`와 `{points[2]['title']}`가 이 글 안에서 어떻게 이어지는지 자신의 언어로 정리할 수 있습니다.",
        "대표 예시나 계산 절차에 이 관점을 적용해 다음 글과의 연결 고리를 만들 수 있습니다.",
    ]


def build_quiz(spec: dict[str, Any]) -> list[str]:
    points = spec["key_points"]
    return [
        f"`{points[0]['title']}`의 뜻을 오늘 글의 맥락에서 한 문단으로 설명하여라.",
        f"`{points[1]['title']}`가 왜 필요한지 간단한 예시와 함께 서술하여라.",
        f"`{points[2]['title']}`가 다음 단계의 이론이나 계산에 어떤 역할을 하는지 정리하여라.",
    ]


def build_summary(spec: dict[str, Any]) -> list[str]:
    return [point["note"] for point in spec["key_points"]]


def prompt_info_block(item: dict[str, Any], slot: str) -> str:
    source_lines = "\n".join([f"> - {ref}" for ref in item["source_refs"]])
    return (
        f"> 자동 생성 슬롯: `{slot}`\n"
        f"> 1차 자료: `{PRIMARY_SOURCE_PATH}`\n"
        f"> 2차 자료: `{STYLE_GUIDE_PATH.name}`, `{OPS_DOC_PATH.name}`\n"
        f"> 참고 위치:\n{source_lines}\n"
        "{: .prompt-info }"
    )


def render_front_matter(item: dict[str, Any], dt: datetime) -> str:
    tag_list = ", ".join(item["tags"])
    categories = ", ".join(CATEGORIES)
    return "\n".join(
        [
            "---",
            f'title: "{item["title"]}"',
            f"date: {format_offset(dt)}",
            f"categories: [{categories}]",
            f"tags: [{tag_list}]",
            "math: true",
            "toc: true",
            f"author: {AUTHOR}",
            "---",
            "",
        ]
    )


def render_body(item: dict[str, Any], spec: dict[str, Any], slot: str) -> str:
    goals = build_goals(spec)
    quiz = build_quiz(spec)
    summary = build_summary(spec)
    sections = spec["key_points"]

    lines = [
        prompt_info_block(item, slot),
        "",
        f"# {item['title']}",
        "",
        "## 도입 설명",
        spec["intro"],
        "",
        "## 학습목표",
        *(f"- {goal}" for goal in goals),
        "",
        "## 선수개념 체크",
        *(f"- {prereq}" for prereq in spec["prereqs"]),
        "",
        "## 핵심 내용",
    ]

    for index, section in enumerate(sections, start=1):
        lines.extend(
            [
                f"### {index}. {section['title']}",
                (
                    f"이 부분의 초점은 `{section['title']}`입니다. "
                    f"{section['note']}"
                ),
                (
                    "정의와 계산 절차를 따로 외우기보다는, 이 개념이 어떤 문제를 단순화하고 "
                    "어떤 다음 주제로 이어지는지 함께 정리하는 방식으로 읽는 것이 좋습니다."
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## 주의",
            "1. " + spec["cautions"][0],
            "2. " + spec["cautions"][1],
            "",
            "## 자가진단퀴즈",
            "1. " + quiz[0],
            "2. " + quiz[1],
            "3. " + quiz[2],
            "",
            "## 요약",
            "1. " + summary[0],
            "2. " + summary[1],
            "3. " + summary[2],
            "",
        ]
    )

    return "\n".join(lines)


def render_post(item: dict[str, Any], slot: str, dt: datetime) -> str:
    order = int(item["order"])
    spec = TOPIC_SPECS.get(order)
    if spec is None:
        raise KeyError(f"Missing topic spec for order {order}")
    return render_front_matter(item, dt) + render_body(item, spec, slot)


def draft_name(item: dict[str, Any]) -> str:
    return f"linear-algebra-{int(item['order']):02d}-{item['slug']}.md"


def make_result(
    *,
    status: str,
    item: dict[str, Any] | None,
    draft_path: Path | None,
    timestamp: datetime,
    skipped_orders: list[int] | None = None,
    message: str | None = None,
    preview: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": status,
        "timestamp": timestamp.isoformat(),
        "skipped_orders": skipped_orders or [],
    }
    if item is not None:
        result["order"] = int(item["order"])
        result["title"] = item["title"]
        result["slug"] = item["slug"]
        result["tags"] = item["tags"]
    if draft_path is not None:
        result["draft_path"] = str(draft_path)
    if message:
        result["message"] = message
    if preview:
        result["preview"] = preview
    return result


def save_draft(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def next_item_from_state(
    manifest: list[dict[str, Any]], output_dir: Path, start_order: int
) -> tuple[dict[str, Any] | None, list[int], int]:
    skipped_orders: list[int] = []
    for item in manifest:
        order = int(item["order"])
        if order < start_order:
            continue
        if item["status"] == "published":
            skipped_orders.append(order)
            continue

        expected_path = output_dir / draft_name(item)
        if expected_path.exists():
            skipped_orders.append(order)
            continue
        return item, skipped_orders, order
    return None, skipped_orders, len(manifest) + 1


def handle_dry_run(
    *, manifest: list[dict[str, Any]], output_dir: Path, args: argparse.Namespace, now: datetime, state: dict[str, Any]
) -> dict[str, Any]:
    if args.index is not None:
        item = next((entry for entry in manifest if int(entry["order"]) == args.index), None)
        if item is None:
            raise ValueError(f"No manifest entry with order {args.index}")
        draft_path = output_dir / draft_name(item)
        preview = render_post(item, args.slot, now)
        return make_result(
            status="dry_run",
            item=item,
            draft_path=draft_path,
            timestamp=now,
            preview=preview,
        )

    item, skipped_orders, next_order = next_item_from_state(
        manifest, output_dir, int(state.get("next_order", 1))
    )
    if item is None:
        return make_result(
            status="complete",
            item=None,
            draft_path=None,
            timestamp=now,
            skipped_orders=skipped_orders,
            message=f"All drafts are already present. Next order would be {next_order}.",
        )

    preview = render_post(item, args.slot, now)
    return make_result(
        status="dry_run",
        item=item,
        draft_path=output_dir / draft_name(item),
        timestamp=now,
        skipped_orders=skipped_orders,
        preview=preview,
    )


def handle_write(
    *, manifest: list[dict[str, Any]], output_dir: Path, args: argparse.Namespace, now: datetime, state: dict[str, Any]
) -> dict[str, Any]:
    if args.index is not None:
        item = next((entry for entry in manifest if int(entry["order"]) == args.index), None)
        if item is None:
            raise ValueError(f"No manifest entry with order {args.index}")
        path = output_dir / draft_name(item)
        if path.exists():
            return make_result(
                status="existing",
                item=item,
                draft_path=path,
                timestamp=now,
                message="Draft already exists for the requested order.",
            )
        save_draft(path, render_post(item, args.slot, now))
        return make_result(status="created", item=item, draft_path=path, timestamp=now)

    next_order = int(state.get("next_order", 1))
    item, skipped_orders, resolved_next_order = next_item_from_state(manifest, output_dir, next_order)
    if item is None:
        state["next_order"] = resolved_next_order
        state["updated_at"] = now.isoformat()
        write_state(state)
        return make_result(
            status="complete",
            item=None,
            draft_path=None,
            timestamp=now,
            skipped_orders=skipped_orders,
            message="No remaining pending draft to generate.",
        )

    path = output_dir / draft_name(item)
    content = render_post(item, args.slot, now)
    save_draft(path, content)

    state["next_order"] = int(item["order"]) + 1
    state["updated_at"] = now.isoformat()
    history = state.setdefault("history", [])
    history.append(
        {
            "order": int(item["order"]),
            "title": item["title"],
            "slot": args.slot,
            "draft_path": str(path),
            "created_at": now.isoformat(),
            "skipped_orders": skipped_orders,
        }
    )
    write_state(state)

    return make_result(
        status="created",
        item=item,
        draft_path=path,
        timestamp=now,
        skipped_orders=skipped_orders,
        message="Draft created and state advanced.",
    )


def main() -> int:
    args = parse_args()
    now = parse_now(args.now)
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = (ROOT / output_dir).resolve()

    manifest = load_manifest()
    state = load_state()

    if args.index is not None and args.index < 1:
        raise ValueError("--index must be a positive order number.")

    if args.dry_run:
        result = handle_dry_run(manifest=manifest, output_dir=output_dir, args=args, now=now, state=state)
    else:
        result = handle_write(manifest=manifest, output_dir=output_dir, args=args, now=now, state=state)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - surfaced to automation logs
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
