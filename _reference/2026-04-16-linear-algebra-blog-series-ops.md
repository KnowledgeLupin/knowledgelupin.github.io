---
title: "선형대수 블로그 연재 운영표"
date: 2026-04-16 09:10:00 +0200
categories: [Mathematics, Linear Algebra]
tags: [선형대수학, 블로그, 연재운영, 자동화]
math: true
toc: true
author: KnowledgeLupin
---

# 선형대수 블로그 연재 운영표

이 문서는 선형대수 연재 초안 자동화의 내부 기준표입니다.  
공개 게시용 색인으로 쓰지 않고, `_drafts/` 생성 순서와 검토 상태를 관리하기 위한 내부 문서로만 보관합니다.

## 운영 원칙
- 제목은 모두 교과서식 제목을 유지합니다.
- 초안 자동화는 `Europe/Berlin` 기준 `09:00`, `18:00`에 각각 1편씩 생성합니다.
- 자동화는 `_drafts/`에만 파일을 만들고 `_posts/` 승격은 사람이 수동으로 처리합니다.
- 상태 값은 `pending`, `drafted`, `reviewed`, `published` 네 단계로 봅니다.

## 기준 자료
- 1차 자료: `/Users/kwkwon/Desktop/Obsidian/Mathematician/_shared/my-library/2018Olver - Applied Linear Algebra.pdf`
- 2차 자료: `_reference/2026-02-24-linear-algebra-writing-style-guide.md`
- 기계용 manifest: `_reference/linear-algebra-series-manifest.yml`

## 연재 순서

| 번호 | 제목 | 핵심 개념 | 참고 절/쪽수 | 상태 |
| ---: | --- | --- | --- | --- |
| 1 | 선형대수의 대상과 응용 범위 | 선형성, 근사, 모델, 계산과 구조의 통일 | Preface pp. vii-ix, Ch.1 intro pp. 1-3 | pending |
| 2 | 연립일차방정식과 Gaussian elimination | 증강행렬, 기본 행연산, 해집합 보존, 소거 알고리듬 | Ch.1 §§1.1-1.3, pp. 1-22 | pending |
| 3 | `LU` 분해와 전진/후진 대입 | 소거와 인수분해, triangular system, 계산 절차 | Ch.1 §1.3, pp. 16-22 | pending |
| 4 | 역행렬과 행렬식의 계산적 의미 | inverse, determinant, 계산 비용, 이론과 실용의 차이 | Ch.1 §§1.5, 1.9, pp. 31-45, 69-74 | pending |
| 5 | Pivoting과 수치적 안정성 | permutation, pivoting, round-off, practical linear algebra | Ch.1 §§1.4, 1.7, pp. 22-27, 48-58 | pending |
| 6 | 벡터공간과 부분공간 | 공리, 부분공간 판정, 대표 예시 | Ch.2 §§2.1-2.2, pp. 76-86 | pending |
| 7 | 생성, 선형독립, 기저, 차원 | span, independence, basis, dimension | Ch.2 §§2.3-2.4, pp. 87-104 | pending |
| 8 | Kernel, image, rank-nullity | fundamental subspaces, 해의 구조, rank-nullity | Ch.2 §2.5, pp. 105-119 | pending |
| 9 | 그래프와 incidence matrix | graph, digraph, incidence matrix, 선형대수적 표현 | Ch.2 §2.6, pp. 120-127 | pending |
| 10 | Euler 공식과 독립 회로 | circuit, cokernel, Euler formula, combinatorial structure | Ch.2 §2.6, pp. 120-127 | pending |
| 11 | Inner product와 norm | 내적, 노름, 거리, 함수공간 관점 | Ch.3 §§3.1-3.3, pp. 129-155 | pending |
| 12 | Cauchy-Schwarz 부등식과 직교성 | inequality, orthogonality, triangle inequality | Ch.3 §§3.1-3.2, pp. 137-143; Ch.4 §4.1 | pending |
| 13 | Positive definite matrix와 Gram matrix | positive definiteness, Gram matrix, quadratic form | Ch.3 §§3.4-3.5, pp. 156-171 | pending |
| 14 | Completing the square와 Cholesky 분해 | quadratic minimization, completion of squares, Cholesky | Ch.3 §3.5, pp. 166-171 | pending |
| 15 | Orthogonal projection과 least squares | projection, closest point, least squares, compatibility | Ch.4 §4.4, pp. 212-225; Ch.5 §§5.1-5.4 | pending |
| 16 | Gram-Schmidt 과정과 `QR` 분해 | orthonormal basis, Gram-Schmidt, QR, Householder outlook | Ch.4 §§4.1-4.3, pp. 184-211 | pending |
| 17 | Fredholm alternative | orthogonal subspaces, compatibility, adjoint viewpoint | Ch.4 §4.4, pp. 221-225 | pending |
| 18 | Interpolation과 approximation | data fitting, polynomial interpolation, approximation | Ch.5 §5.5, pp. 254-278 | pending |
| 19 | Orthogonal polynomials와 최소제곱근사 | Legendre polynomials, least squares in function spaces | Ch.4 §4.5, pp. 226-234; Ch.5 §5.5, pp. 274-277 | pending |
| 20 | Spline과 piecewise polynomial approximation | spline, local control, approximation quality | Ch.5 §5.5, pp. 279-284 | pending |
| 21 | Discrete Fourier transform과 FFT | sampled data, Fourier coefficients, fast algorithm | Ch.5 §5.6, pp. 285-297 | pending |
| 22 | 압축과 잡음제거의 선형대수 | compression, denoising, frequency-domain viewpoint | Ch.5 §5.6, pp. 293-297 | pending |
| 23 | 스프링-질량계와 에너지 최소화 | equilibrium mechanics, minimization principle, modeling | Ch.5 §5.1, pp. 236-238; Ch.6 §6.1, pp. 301-310 | pending |
| 24 | 전기회로와 equilibrium | electrical network, Kirchhoff viewpoint, correspondence | Ch.6 §6.2, pp. 311-321 | pending |
| 25 | 선형사상, 기저변환, affine transformation | linear maps, change of basis, affine geometry | Ch.7 §§7.1-7.3, pp. 342-375 | pending |
| 26 | Eigenvalue와 spectral theorem | eigenvalue, diagonalization, symmetric matrices, spectral theorem | Ch.8 §§8.1-8.5, pp. 404-443 | pending |
| 27 | Singular value, pseudoinverse, condition number | singular values, pseudoinverse, conditioning | Ch.8 §8.7, pp. 454-466 | pending |
| 28 | Principal component analysis | variance, covariance, principal components | Ch.8 §8.8, pp. 467-474 | pending |
| 29 | Iteration, Markov process, iterative solver | iterative systems, stability, Markov process, Jacobi/Gauss-Seidel | Ch.9 §§9.1-9.4, pp. 476-521 | pending |
| 30 | Power method, `QR` algorithm, Krylov methods, matrix exponential, stability, resonance | eigenvalue algorithms, Krylov subspace, dynamics, resonance | Ch.9 §§9.5-9.6, pp. 522-546; Ch.10 §§10.1-10.6, pp. 565-630 | pending |
