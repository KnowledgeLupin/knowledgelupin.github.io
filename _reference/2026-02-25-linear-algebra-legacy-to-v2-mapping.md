---
title: "선형대수 교재 레거시 파일 -> v2 구조 매핑"
date: 2026-02-25 18:00:00 +0900
categories: [Mathematics, Linear Algebra]
tags: [선형대수학, 리팩토링, 마이그레이션]
math: true
toc: true
author: KnowledgeLupin
---

# 레거시 파일 -> v2 구조 매핑

이 문서는 구 체계(12장 + 군론 확장 부록) 파일을 v2 체계(5부 16장 + 부록 A/B/C)로 통합하면서 참고할 매핑 기록입니다.

## Chapters
- `ch01-vector-spaces.tex` -> `ch03-vector-spaces-and-subspaces.tex` + `ch04-basis-and-dimension.tex`
- `ch02-matrices.tex` -> `ch01-linear-systems-and-gauss.tex` + `ch02-matrix-operations-invertibility-rank.tex`
- `ch03-linear-maps.tex` -> `ch05-linear-maps-kernel-image.tex`
- `ch04-linear-maps-and-matrices.tex` -> `ch06-matrix-representation-and-similarity.tex`
- `ch05-inner-product-and-orthogonality.tex` -> `ch14-inner-product-and-orthogonalization.tex`
- `ch06-determinants.tex` -> `ch08-determinants.tex`
- `ch07-symmetric-hermitian-unitary.tex` -> `ch15-adjoint-normal-spectral.tex`
- `ch08-eigenvalues-eigenvectors.tex` -> `ch10-eigenvalues-and-diagonalization.tex`
- `ch09-polynomials-and-matrices.tex` -> `ch09-operator-polynomials.tex`
- `ch10-triangulation-and-cayley-hamilton.tex` -> `ch11-invariant-subspaces-and-triangularization.tex` (+ Ch9 일부)
- `ch11-primary-decomposition-and-jordan.tex` -> `ch12-primary-and-cyclic-decomposition.tex` + `ch13-jordan-canonical-form.tex`
- `ch12-convex-sets.tex` -> 본서 범위에서 제외

## Appendices
- `appendix-a-complex-numbers.tex` -> `appendix-b-field-and-complex.tex`
- `appendix-b-iwasawa-decomposition.tex` -> 본서 범위에서 제외

## 원칙
1. 군론/위상 확장은 v2 본문에서 제외한다.
2. 설명 문단은 경어체, 정의/정리/증명은 엄밀 문체로 유지한다.
3. 모든 신규 집필은 v2 파일에만 반영한다.
