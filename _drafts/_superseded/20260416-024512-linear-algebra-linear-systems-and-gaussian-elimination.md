---
title: "연립일차방정식과 Gaussian elimination"
date: 2026-04-16 02:09:25 +0200
slug: "linear-systems-and-gaussian-elimination"
categories: ["Mathematics", "Linear Algebra"]
tags: ["선형대수학", "Gaussian elimination", "증강행렬", "기본 행연산", "피벗"]
author: "KnowledgeLupin"
math: true
toc: true
---
<!--
automation-slot: am
manifest: /Users/kwkwon/Desktop/Obsidian/Mathematician/_active/github-blog/_reference/linear-algebra-post-manifest.yml
state-file: /Users/kwkwon/Desktop/Obsidian/Mathematician/_active/github-blog/_reference/.automation/linear-algebra-post-state.json
primary-source: /Users/kwkwon/Desktop/Obsidian/Mathematician/_shared/my-library/2018Olver - Applied Linear Algebra.pdf
design-doc: /Users/kwkwon/Desktop/Obsidian/Mathematician/_active/github-blog/_reference/2026-04-16-linear-algebra-independent-post-automation-design.md
writing-spec: /Users/kwkwon/Desktop/Obsidian/Mathematician/_active/github-blog/_reference/2026-04-16-linear-algebra-blog-writing-spec.md
source-ref: Applied Linear Algebra, Chapter 1 §§1.1-1.3, pp. 1-22
-->

# 연립일차방정식과 Gaussian elimination

연립일차방정식은 선형대수가 행렬로 출발하는 이유를 가장 잘 보여 줍니다. 미지수가 여러 개여도 핵심은 각 방정식이 어떤 평면 또는 초평면을 나타내는지, 그리고 그 교집합을 해집합으로 읽을 수 있는지에 있습니다.

Gaussian elimination은 복잡한 식을 억지로 외워 푸는 방법이 아닙니다. 해를 바꾸지 않는 동치 변형만 허용하면서 문제를 점점 읽기 쉬운 형태로 바꾸는 절차입니다. 이 구조를 이해하면 이후의 LU 분해, rank, least squares까지 자연스럽게 연결됩니다.

## 기본 정의

증강행렬은 방정식의 계수와 우변을 한 표에 모아 적는 장치입니다. 이렇게 표현하면 행연산이 해집합을 바꾸는지 여부를 식 전체 대신 행 단위로 추적할 수 있습니다.

> **정의 (증강행렬 (augmented matrix))**  
> 연립일차방정식 $$Ax = b$$의 계수행렬 $$A$$와 우변 $$b$$를 옆에 붙여 적은 행렬 $$[A \mid b]$$를 증강행렬이라 한다.

> **정의 (기본 행연산)**  
> 두 행을 교환하는 연산, 한 행에 0이 아닌 상수를 곱하는 연산, 한 행에 다른 행의 상수배를 더하는 연산을 기본 행연산이라 한다.

## 기본 행연산과 해집합

> **정리 1 (기본 행연산과 해집합)**  
> 증강행렬에 가한 세 가지 기본 행연산은 대응하는 연립일차방정식의 해집합을 보존한다.

**증명.** 행 교환은 방정식의 순서만 바꾸는 것이므로, 어떤 벡터가 한 시스템의 해이면 순서를 바꾼 시스템의 해이기도 하다.

한 행에 0이 아닌 상수 $$c$$를 곱하는 것은 등식 $$r = 0$$을 동치인 등식 $$cr = 0$$으로 바꾸는 것과 같으므로 해집합은 변하지 않는다.

한 행에 다른 행의 상수배를 더하는 경우, 원래 시스템의 해는 두 등식을 각각 만족하므로 그 선형결합도 만족한다. 반대로, 바뀐 시스템의 해는 추가된 행과 남겨둔 행을 이용해 이전 행을 복원할 수 있으므로 원래 시스템의 해이기도 하다. 세 연산 모두 양방향 동치 변형이므로 해집합이 보존된다. $$\square$$

## 계산 예시

소거 과정을 직접 따라가 보면 피벗, 자유변수, 해의 개수가 한꺼번에 눈에 들어옵니다.

1. 연립방정식

   $$\begin{aligned} x + y + z &= 2 \\ 2x + y - z &= 1 \\ x + 2y + 3z &= 5 \end{aligned}$$

   을 증강행렬로 쓰면 $$\left[\begin{array}{ccc|c}1&1&1&2\\2&1&-1&1\\1&2&3&5\end{array}\right]$$가 된다.

2. 둘째 행에서 첫째 행의 두 배를 빼고, 셋째 행에서 첫째 행을 빼면

   $$\left[\begin{array}{ccc|c}1&1&1&2\\0&-1&-3&-3\\0&1&2&3\end{array}\right]$$

   을 얻는다.

3. 셋째 행에 둘째 행을 더하면

   $$\left[\begin{array}{ccc|c}1&1&1&2\\0&-1&-3&-3\\0&0&-1&0\end{array}\right]$$

   이 되고, 여기서 바로 $$z = 0$$, $$y = 3$$, $$x = -1$$을 읽을 수 있습니다. 피벗이 세 개이므로 자유변수는 없습니다.

## 응용

회로의 전압과 전류, 질점계의 평형식, 마르코프 체인의 정상 상태 계산은 모두 결국 선형계로 정리됩니다. 데이터 적합 문제에서도 정규방정식을 세우는 순간 다시 선형계가 등장합니다. Gaussian elimination이 단지 1장의 계산 절차가 아니라 선형대수 전체를 관통하는 기본 도구인 이유가 여기에 있습니다.

## 주의할 점

소거 결과만 읽고 각 행연산이 왜 동치 변형인지 잊어버리면, 이후에 rank와 nullity를 다룰 때 해석의 토대를 잃기 쉽습니다. 또한 기약행 사다리꼴만이 정답이라고 생각하면 실제 계산에서 불필요한 연산이 늘어납니다. 해를 읽는 데 필요한 최소한의 형태가 무엇인지 파악하는 것이 더 중요합니다.

## 마치며

Gaussian elimination의 본질은 문제를 더 간단한 동치 문제로 바꾸는 과정에 있습니다. 이 구조를 명확히 이해해 두면, 다음 주제인 LU 분해가 왜 자연스럽게 등장하는지도 어렵지 않게 파악할 수 있습니다.

## 참고문헌

- Peter J. Olver and Chehrzad Shakiban. (2018). *Applied Linear Algebra*. Springer Cham.
