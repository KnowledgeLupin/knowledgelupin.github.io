---
title: "선형대수학 제1장 1.1: 체(Field)와 벡터공간의 공리"
date: 2026-02-24 23:50:00 +0900
categories: [Mathematics, Linear Algebra]
tags: [선형대수학, 벡터공간, 체, 공리]
math: true
toc: true
author: KnowledgeLupin
---

# 제1장 벡터공간
## 1.1 체(Field)와 벡터공간의 공리

## 동기: 왜 공리부터 시작할까?
선형대수에서 우리가 하고 싶은 일은 크게 두 가지입니다.
1. 벡터를 더한다.
2. 벡터를 숫자로 늘리거나 줄인다.

그런데 "숫자"가 무엇인지, "더한다"는 것이 어떤 규칙을 따라야 하는지 먼저 정해 두지 않으면, 이후의 정리(기저, 차원, 고유값)가 전부 흔들립니다.  
그래서 선형대수는 계산 기술보다 먼저, 계산이 안전하게 작동하는 규칙부터 세웁니다. 이 절의 핵심은 바로 그 규칙입니다.

## 1. 체(Field): 스칼라의 세계
벡터를 늘리고 줄일 때 쓰는 숫자를 **스칼라(scalar)**라고 부릅니다.  
스칼라들의 집합은 보통 $\mathbb{Q}, \mathbb{R}, \mathbb{C}$ 중 하나를 씁니다.

> **정의 1.1 (체, Field)**  
집합 $K$와 두 연산 $+$, $\cdot$가 다음을 만족하면 $K$를 체라 한다.
1. $(K,+)$는 아벨군이다.  
2. $(K\setminus\{0\},\cdot)$는 아벨군이다.  
3. 분배법칙 $a(b+c)=ab+ac$가 성립한다.

말로 풀면 다음과 같습니다.
- 덧셈은 자유롭고(항등원/역원 있음),
- 0이 아닌 원소는 곱셈으로도 나눌 수 있으며,
- 곱셈과 덧셈이 잘 호환됩니다.

### 예시와 비예시
- $\mathbb{Q}, \mathbb{R}, \mathbb{C}$는 체입니다.
- $\mathbb{Z}$는 체가 아닙니다. 예를 들어 $2$의 곱셈 역원 $\frac{1}{2}$가 $\mathbb{Z}$에 없기 때문입니다.

## 2. 벡터공간: 벡터의 세계
이제 스칼라 체 $K$ 위에서 벡터들의 집합 $V$를 생각합니다.

> **정의 1.2 (벡터공간, Vector Space)**  
집합 $V$에 대해
1. 벡터 덧셈 $V\times V\to V$, $(\mathbf{u},\mathbf{v})\mapsto \mathbf{u}+\mathbf{v}$  
2. 스칼라곱 $K\times V\to V$, $(a,\mathbf{v})\mapsto a\mathbf{v}$  
가 정의되어 있고, 임의의 $a,b\in K$, $\mathbf{u},\mathbf{v},\mathbf{w}\in V$에 대해 아래 공리가 성립하면 $V$를 $K$ 위의 벡터공간이라 한다.

1. $(\mathbf{u}+\mathbf{v})+\mathbf{w}=\mathbf{u}+(\mathbf{v}+\mathbf{w})$
2. $\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}$
3. 영벡터 $\mathbf{0}\in V$가 존재하여 $\mathbf{v}+\mathbf{0}=\mathbf{v}$
4. 각 $\mathbf{v}\in V$에 대해 $\mathbf{v}+(-\mathbf{v})=\mathbf{0}$인 $-\mathbf{v}$가 존재
5. $a(\mathbf{u}+\mathbf{v})=a\mathbf{u}+a\mathbf{v}$
6. $(a+b)\mathbf{v}=a\mathbf{v}+b\mathbf{v}$
7. $(ab)\mathbf{v}=a(b\mathbf{v})$
8. $1\mathbf{v}=\mathbf{v}$

> 💡 **핵심 관찰**  
> 벡터공간 공리는 "벡터 덧셈의 군 구조 + 스칼라곱의 호환성"으로 요약됩니다.
{: .prompt-tip }

## 3. 첫 정리들: 공리에서 바로 나오는 성질
공리를 외우는 것보다, 공리로 무엇을 증명할 수 있는지 보는 편이 훨씬 중요합니다.

> **정리 1.1.3 (영벡터와 역벡터의 유일성)**  
$K$ 위의 벡터공간 $V$에서 영벡터는 유일하고, 각 벡터의 덧셈 역벡터도 유일하다.

**증명.**  
(영벡터 유일성) $\mathbf{0},\mathbf{0}'$가 둘 다 영벡터라고 하자.  
그러면 $\mathbf{0}+\mathbf{0}'=\mathbf{0}'$ (왜냐하면 $\mathbf{0}$은 영벡터),  
또 $\mathbf{0}+\mathbf{0}'=\mathbf{0}$ (왜냐하면 $\mathbf{0}'$은 영벡터).  
따라서 $\mathbf{0}=\mathbf{0}'$.

(역벡터 유일성) $\mathbf{w},\mathbf{w}'$가 모두 $\mathbf{v}$의 역벡터라고 하자.  
즉 $\mathbf{v}+\mathbf{w}=\mathbf{0}$, $\mathbf{v}+\mathbf{w}'=\mathbf{0}$.  
그러면
$$
\mathbf{w}
=\mathbf{w}+\mathbf{0}
=\mathbf{w}+(\mathbf{v}+\mathbf{w}')
=(\mathbf{w}+\mathbf{v})+\mathbf{w}'
=(\mathbf{v}+\mathbf{w})+\mathbf{w}'
=\mathbf{0}+\mathbf{w}'
=\mathbf{w}'.
$$
따라서 역벡터도 유일하다. $\square$

> **정리 1.1.4 (기본 계산 법칙)**  
임의의 $a\in K$, $\mathbf{v}\in V$에 대해 다음이 성립한다.
1. $0\mathbf{v}=\mathbf{0}$
2. $a\mathbf{0}=\mathbf{0}$
3. $(-1)\mathbf{v}=-\mathbf{v}$
4. $(-a)\mathbf{v}=-(a\mathbf{v})$

**증명.**  
1. $(0+0)\mathbf{v}=0\mathbf{v}+0\mathbf{v}$이므로 $0\mathbf{v}$를 양변에서 더해 없애면 $0\mathbf{v}=\mathbf{0}$.
2. $a(\mathbf{0}+\mathbf{0})=a\mathbf{0}+a\mathbf{0}$에서 같은 방식으로 $a\mathbf{0}=\mathbf{0}$.
3. $\mathbf{v}+(-1)\mathbf{v}=(1+(-1))\mathbf{v}=0\mathbf{v}=\mathbf{0}$이므로 $(-1)\mathbf{v}$는 $\mathbf{v}$의 역벡터, 즉 $-\mathbf{v}$.
4. $(-a)\mathbf{v}+a\mathbf{v}=((-a)+a)\mathbf{v}=0\mathbf{v}=\mathbf{0}$이므로 $(-a)\mathbf{v}$는 $a\mathbf{v}$의 역벡터, 즉 $-(a\mathbf{v})$. $\square$

## 4. 예제
### 예제 1.1 [기초] $\mathbb{R}^n$은 $\mathbb{R}$ 위의 벡터공간
벡터를
$$
\mathbf{x}=(x_1,\dots,x_n),\quad \mathbf{y}=(y_1,\dots,y_n)
$$
로 두고,
$$
\mathbf{x}+\mathbf{y}=(x_1+y_1,\dots,x_n+y_n),\quad
a\mathbf{x}=(ax_1,\dots,ax_n)
$$
로 정의하면 공리 8개가 모두 성립합니다.  
따라서 $\mathbb{R}^n$은 가장 기본적인 벡터공간입니다.

### 예제 1.2 [연결] 다항식 공간 $P_n(\mathbb{R})$
차수가 $n$ 이하인 실계수 다항식 전체를
$$
P_n(\mathbb{R})=\{a_0+a_1x+\cdots+a_nx^n\mid a_i\in\mathbb{R}\}
$$
라고 하자. 다항식의 덧셈과 실수배는 여전히 차수 $n$ 이하 다항식이므로 공리가 성립합니다.  
즉 $P_n(\mathbb{R})$도 $\mathbb{R}$ 위의 벡터공간입니다.

> ⚠️ **자주 나오는 실수**  
> $\mathbb{R}^2$는 표준 연산으로는 $\mathbb{R}$ 위의 벡터공간입니다.  
> 이때 스칼라곱이 실수배로만 정의되어 있으므로, 같은 연산을 그대로 두고 $\mathbb{C}$를 스칼라 체로 바꿀 수는 없습니다.
{: .prompt-warning }

## 5. 연습문제 (4단계 + 힌트)
### Level 1. 기초 확인
1. $\mathbb{Q}, \mathbb{Z}, \mathbb{R}, \mathbb{C}$ 중 체인 것을 모두 고르시오.  
힌트: "0이 아닌 원소의 곱셈 역원" 존재 여부를 확인하라.

2. 벡터공간 공리 중 분배법칙에 해당하는 두 식을 정확히 써 보시오.  
힌트: 스칼라가 벡터합에 분배되는 식, 스칼라합이 벡터에 분배되는 식을 구분하라.

### Level 2. 표준 응용
3. $W=\{(x,y,z)\in\mathbb{R}^3\mid x+y+z=0\}$가 $\mathbb{R}^3$의 부분공간인지 판정하시오.  
힌트: 영벡터 포함, 덧셈 닫힘, 스칼라곱 닫힘의 3가지를 순서대로 확인하라.

4. 정리 1.1.4의 (2) $a\mathbf{0}=\mathbf{0}$을 공리만으로 다시 증명하시오.  
힌트: $\mathbf{0}+\mathbf{0}=\mathbf{0}$에서 시작하라.

### Level 3. 연결 추론
5. 벡터공간 $V$에서 식
$$
a(\mathbf{u}-\mathbf{v})=a\mathbf{u}-a\mathbf{v}
$$
을 증명하시오.  
힌트: $\mathbf{u}-\mathbf{v}=\mathbf{u}+(-\mathbf{v})$로 바꾼 뒤 정리 1.1.4의 (4)를 사용하라.

6. 역벡터 유일성을 이용해 다음을 보이시오:  
$\mathbf{u}+\mathbf{w}=\mathbf{v}+\mathbf{w}$이면 $\mathbf{u}=\mathbf{v}$.  
힌트: 양변에 $-\mathbf{w}$를 더하라.

### Level 4. 도전 확장
7. 집합 $\mathbb{R}^2$에서 덧셈은 표준 덧셈으로 두고, 스칼라곱을
$$
a\odot(x,y)=(ax,y)
$$
로 정의하자. 이 구조가 $\mathbb{R}$ 위의 벡터공간인지 판단하시오.  
힌트: 공리 중 $(a+b)\mathbf{v}=a\mathbf{v}+b\mathbf{v}$ 또는 $1\mathbf{v}=\mathbf{v}$를 대입해 보라.

8. 체 공리에서 곱셈 교환법칙을 제거하면 어떤 대수 구조가 되는지 조사하고, 선형대수에서 어떤 주제로 확장되는지 짧게 정리하시오.  
힌트: division ring(또는 skew field) 키워드를 찾아보라.

## 6. 절 요약
1. 벡터공간의 스칼라는 체 $K$에서 온다.
2. 벡터공간 공리는 "덧셈 구조 + 스칼라곱 호환성"으로 구성된다.
3. 공리만으로도 $0\mathbf{v}=\mathbf{0}$, $(-1)\mathbf{v}=-\mathbf{v}$ 같은 기본 법칙을 증명할 수 있다.
4. $\mathbb{R}^n$, $P_n(\mathbb{R})$는 대표적인 벡터공간이다.
5. 이후 장의 기저, 차원, 선형사상은 모두 이 공리 위에서 전개된다.
