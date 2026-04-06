---
title: "왜 평균을 빼야 Poincare 부등식이 성립할까?"
date: 2026-04-06 09:00:00 +0900
categories: [Mathematics, Functional Analysis]
tags: [poincare-inequality, poincare-wirtinger, sobolev-spaces, pde]
toc: true
math: true
author: KnowledgeLupin
---

다음 문제를 생각해 보자. 왜 어떤 곳에서는 Poincaré 부등식을
$$
\|u\|_{L^p(\Omega)} \le C \|\nabla u\|_{L^p(\Omega)}
$$
처럼 쓰고, 어떤 곳에서는 반드시 평균
$$
\bar u = \frac{1}{|\Omega|}\int_\Omega u \, dx
$$
를 빼서
$$
\|u-\bar u\|_{L^p(\Omega)} \le C \|\nabla u\|_{L^p(\Omega)}
$$
로 써야 할까?

결론부터 말하면, gradient는 함수의 절대 높이를 보지 못하고 오직 진동만 본다. 따라서 상수항을 어떻게 제거할지 정해 주어야만 함수 전체의 크기를 제어할 수 있다.

## 왜 평균을 빼야 하는가

이 결론이 왜 불가피한지는 간단한 반례 하나로 확인된다. 아무 조건 없는 공간에서
$$
\|u\|_{L^p(\Omega)} \le C \|\nabla u\|_{L^p(\Omega)}
$$
를 기대하면, 상수함수
$$
u(x) \equiv 1
$$
을 넣는 순간 등식이 깨진다.
$$
\nabla u = 0
$$
이지만
$$
\|u\|_{L^p(\Omega)} > 0
$$
이기 때문이다.

즉 gradient는 상수함수를 전혀 구별하지 못한다. 더 정확히 말하면,
$$
\nabla(u+c) = \nabla u
$$
이므로 gradient의 입장에서는 함수와 그 함수에 상수를 더한 것이 같은 대상이다. Poincaré 부등식이 성립하려면 먼저 이 상수 자유도를 제거해야 한다.

## 상수함수는 gradient로 보이지 않는다

이처럼 gradient가 상수를 무시한다는 사실은, 다음 세 가지로 정리된다.

- gradient가 보는 것은 함수의 절대 위치가 아니라 변화량이다.
- 따라서 gradient의 kernel은 상수함수들이다.
- 함수의 크기를 gradient로 제어하려면 이 kernel을 먼저 없애야 한다.

이 kernel을 없애는 방식은 대표적으로 두 가지다.

첫째, 경계값을 0으로 고정한다. 그러면 상수함수 가운데 살아남는 것은 0뿐이다. 이때 얻는 것이
$$
\|u\|_{L^p(\Omega)} \le C \|\nabla u\|_{L^p(\Omega)}
\qquad
\text{for } u \in W_0^{1,p}(\Omega)
$$
형태의 Poincaré 부등식이다.

둘째, 경계값을 고정하지 않는 대신 평균을 뺀다. 그러면 함수에서 상수 성분을 제거한
$$
u-\bar u
$$
만 남고, 여기에 대해
$$
\|u-\bar u\|_{L^p(\Omega)} \le C \|\nabla u\|_{L^p(\Omega)}
$$
가 성립한다. 이것이 보통 Poincaré–Wirtinger 부등식이라고 부르는 형태다.

## 경계값을 0으로 두면 무엇이 달라지는가

첫 번째 방법, 즉 경계값을 0으로 고정하는 경우를 1차원에서 먼저 살펴보자. Bounded interval
$$
I=(a,b)
$$
위의 함수
$$
u \in W_0^{1,p}(I)
$$
를 잡으면, 한 점에서 값이 0이라는 사실로부터
$$
u(x)=u(x)-u(a)=\int_a^x u'(t)\,dt
$$
를 쓸 수 있다. 따라서
$$
|u(x)| \le \int_a^x |u'(t)|\,dt \le \int_I |u'(t)|\,dt
$$
이고, 여기서 Hölder 부등식을 적용하면 원하는 Poincaré 부등식이 나온다.

이 증명은 1차원 미적분학의 기본정리만으로 직관이 거의 다 드러난다. 경계값이 고정되면 함수의 높이 자체가 derivative의 적분으로 복원된다는 뜻이다.

## 평균을 빼면 무엇이 달라지는가

그렇다면 경계값을 고정하지 않는 두 번째 경우는 어떻게 될까. 이제는
$$
u(a)=0
$$
같은 기준점이 없다. 대신 평균
$$
\bar u
$$
를 기준점으로 삼는다.

구간에서는 연속성 때문에 어떤 점
$$
x_0 \in [a,b]
$$
에서
$$
u(x_0)=\bar u
$$
가 된다고 생각할 수 있다. 그러면
$$
u(x)-\bar u = u(x)-u(x_0)=\int_{x_0}^x u'(t)\,dt
$$
이므로
$$
|u(x)-\bar u| \le \int_I |u'(t)|\,dt
$$
가 된다.

두 경우를 나란히 놓으면 구조가 선명해진다. 경계값을 0으로 고정할 수 없으면, 평균을 0으로 맞춰서 상수항을 제거하면 된다. 기준점만 달라질 뿐, 논리의 뼈대는 동일하다.

## 연결된 영역이라는 가정은 왜 필요한가

이상의 논의를 고차원으로 옮기면, 조건이 조금 더 구조적으로 정리된다.

- bounded open set에서는 $W_0^{1,p}(\Omega)$ 버전 Poincaré 부등식을 쓴다.
- connected regular domain에서는 Poincaré–Wirtinger 부등식을 쓴다.

이 배치는 우연이 아니다. 핵심은 `경계조건으로 상수를 죽이는 경우`와 `평균을 빼서 상수를 죽이는 경우`를 분명히 구분하는 데 있다.

특히 connectedness가 들어가는 이유도 이 틀 안에서 자연스럽게 이해된다. Domain이 여러 connected component로 나뉘면, 각 성분마다 다른 상수를 붙여도 gradient는 여전히 0이기 때문이다. 전체 평균 하나만 빼는 것으로는 그 자유도를 모두 제거할 수 없다.

## Dirichlet 문제와 Neumann 문제를 비교해 보면

같은 구분이 PDE를 볼 때도 그대로 나타난다.

Dirichlet 문제에서는 해를
$$
H_0^1(\Omega)
$$
에서 찾는다. 경계에서 값이 0이므로 상수 자유도가 이미 제거되어 있고, 에너지
$$
\int_\Omega |\nabla u|^2\,dx
$$
가 함수의 크기를 실제로 제어한다. 그래서 coercivity가 성립하고 Lax–Milgram 정리를 적용하기 좋아진다.

반대로 Neumann 문제에서는 상수함수를 더해도 미분방정식이 바뀌지 않는다. 그래서 해는 원래부터 상수만큼의 불확정성을 가진다. 이 경우 자연스럽게 쓰는 정규화가
$$
\int_\Omega u\,dx = 0
$$
이며, 바로 이 mean-zero 조건 위에서 Poincaré–Wirtinger 부등식이 작동한다. Dirichlet과 Neumann, 두 문제가 각각 다른 방법으로 같은 상수 자유도 문제를 해결하고 있는 셈이다.

## 1차원에서는 그림이 더 선명하다

이 현상을 다시 1차원으로 내려오면, 핵심이 더욱 투명하게 보인다.

함수의 derivative만 알면 함수 전체를 복원할 수 있을 것처럼 느껴지지만, 실제로는 상수 하나만큼 정보가 빠져 있다. 즉
$$
u'
$$
만 알아서는
$$
u,\quad u+3,\quad u-10
$$
를 서로 구별할 수 없다.

그래서 복원을 하려면 기준점이 하나 필요하다.

- 경계값 $u(a)=0$을 주거나,
- 평균 $\bar u = 0$을 주거나,
- 혹은 한 점에서의 함수값을 지정해야 한다.

Poincaré 부등식은 바로 이 `기준점을 준 뒤에는 derivative가 함수 전체를 제어한다`는 사실의 정량적 버전이라고 볼 수 있다.

## 정리

Poincaré 부등식이 그대로 성립하지 않는 이유는 gradient가 상수항을 보지 못하기 때문이다. 따라서 함수의 크기를 gradient로 제어하려면 먼저 상수 자유도를 제거해야 한다.

경계값을 0으로 고정하면 $W_0^{1,p}(\Omega)$ 위에서 표준적인 Poincaré 부등식이 성립한다. 경계값을 고정하지 않는다면 평균을 빼서 상수 성분을 제거해야 하고, 이때 Poincaré–Wirtinger 부등식이 자연스럽게 등장한다.

이 차이는 PDE에서도 그대로 나타난다. Dirichlet 문제에서는 경계조건이 상수 자유도를 제거하고, Neumann 문제에서는 mean-zero 조건이 그 역할을 맡는다. 형태는 달라도, 두 경우 모두 gradient가 보지 못하는 상수 모드를 제거함으로써 에너지가 실제 노름처럼 행동하도록 만든다는 점은 같다.

## 참고문헌

- Haim Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*, Springer, 2011.