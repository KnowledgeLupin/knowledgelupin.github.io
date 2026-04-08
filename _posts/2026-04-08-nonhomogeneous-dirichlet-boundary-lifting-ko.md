---
title: "비동차 Dirichlet 경계조건의 약형과 Boundary Lifting"
date: 2026-04-08 06:24:46 +0900
categories: [Mathematics, PDE]
tags: [weak-formulation, dirichlet-boundary, sobolev-spaces, pde, poisson-equation]
toc: true
math: true
author: KnowledgeLupin
---

다음 Poisson 경계값 문제를 생각하자.
$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=g \quad \text{on } \partial\Omega.
$$

표준 Sobolev 약형에서 Dirichlet 경계자료는 보통 경계적분의 형태로 식 안에 나타나지 않는다. Dirichlet 조건은 trace를 통해 admissible class에 부과되며, 비동차 경계자료는 boundary lifting을 이용하여 동차 경계문제로 환원한다.

아래에서는 $\Omega$를 bounded Lipschitz domain으로 가정하며, 간단히
$$
f\in L^2(\Omega)
$$
로 두고, 비동차 Dirichlet 자료와 Neumann 자료는 각각
$$
g\in H^{1/2}(\partial\Omega), \qquad h\in H^{-1/2}(\partial\Omega)
$$
로 하여 이 절차를 Poisson 방정식의 경우에 정리한다.

## 동차 Dirichlet 문제의 약형

먼저 동차 Dirichlet 문제
$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=0 \quad \text{on } \partial\Omega
$$
를 생각하자.

적절한 함수공간은 $H_0^1(\Omega)$이며, weak formulation은 다음과 같다. 주어진 $f$에 대하여 $u \in H_0^1(\Omega)$를 찾아
$$
\int_\Omega \nabla u \cdot \nabla v\,dx
=
\int_\Omega fv\,dx
\qquad \forall v\in H_0^1(\Omega)
$$
를 만족시키게 한다.

이 식은 smooth한 경우의 적분 by parts로부터 얻어진다. 실제로
$$
\int_\Omega (-\Delta u)v\,dx
=
\int_\Omega \nabla u\cdot \nabla v\,dx
- \int_{\partial\Omega}\partial_\nu u\,v\,dS
$$
인데, 시험함수 $v\in H_0^1(\Omega)$는 trace가 0이므로 경계항이 사라진다. 따라서 Dirichlet 조건 $u=0$ on $\partial\Omega$는 적분식의 우변에 나타나는 것이 아니라, 함수공간 $H_0^1(\Omega)$의 선택 속에 반영된다.

## 비동차 Dirichlet 경계자료

이제 비동차 문제
$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=g \quad \text{on } \partial\Omega
$$
를 생각하자.

이 경우 해는 $u\in H^1(\Omega)$, $\operatorname{Tr}(u)=g$를 만족해야 한다. 여기서 경계조건은 pointwise 의미가 아니라 trace sense에서 부과된다.

보다 정확히 말하면, bounded linear operator
$$
\operatorname{Tr}:H^1(\Omega)\to H^{1/2}(\partial\Omega)
$$
가 존재하며, smooth한 함수에 대해서는 usual restriction $\operatorname{Tr}(u)=u|_{\partial\Omega}$와 일치한다. 또한 이 operator는 $H^{1/2}(\partial\Omega)$ 위로 surjective이며, 그 kernel은 $H_0^1(\Omega)$이다.

비동차 Dirichlet 문제의 표준 약형은
$$
\int_\Omega \nabla u\cdot \nabla v\,dx
=
\int_\Omega fv\,dx
\qquad \forall v\in H_0^1(\Omega)
$$
와 함께 $u\in H^1(\Omega)$, $\operatorname{Tr}(u)=g$를 요구하는 것이다. 즉 경계자료 $g$는 경계적분으로 약하게 부과되는 것이 아니라, admissible class의 조건으로 강하게 부과된다. 시험함수는 여전히 $H_0^1(\Omega)$에서 택한다.

## Boundary Lifting

$g$를 경계 trace로 갖는 함수
$$
w\in H^1(\Omega), \qquad \operatorname{Tr}(w)=g
$$
를 하나 택하자. 이 $w$를 boundary lifting이라 부르며, 그 존재는 trace operator의 surjectivity로 보장된다.

$z:=u-w$로 두면 $\operatorname{Tr}(z)=0$이므로 $z\in H_0^1(\Omega)$가 된다. 원래 약형에 $u=z+w$를 대입하면
$$
\int_\Omega \nabla z\cdot \nabla v\,dx
=
\int_\Omega fv\,dx
- \int_\Omega \nabla w\cdot \nabla v\,dx
\qquad \forall v\in H_0^1(\Omega)
$$
를 얻는다.

즉 비동차 Dirichlet 문제는 다음의 동차 경계문제로 환원된다. $z\in H_0^1(\Omega)$를 찾아
$$
\int_\Omega \nabla z\cdot \nabla v\,dx
=
\int_\Omega fv\,dx
- \int_\Omega \nabla w\cdot \nabla v\,dx
\qquad \forall v\in H_0^1(\Omega)
$$
를 만족시키게 한 뒤, $u=z+w$로 원래 해를 복원하면 된다.

보다 일반적인 divergence form elliptic operator $L$에 대해서도 동일한 구조가 유지된다. 계수가 충분히 bounded하여 $Lw\in H^{-1}(\Omega)$가 잘 정의된다고 하면, 경계 lifting $w$를 정한 뒤
$$
\tilde f := f-Lw
$$
를 $H^{-1}(\Omega)$의 원소로 정의할 수 있고, 문제는 $z\in H_0^1(\Omega)$에 대한 동차 Dirichlet 약형으로 바뀐다.

## Neumann 문제와의 비교

같은 Poisson 방정식이라도 Neumann 경계조건에서는 함수공간의 선택이 달라진다. 먼저 homogeneous Neumann 문제
$$
-\Delta u=f \quad \text{in } \Omega, \qquad \partial_\nu u=0 \quad \text{on } \partial\Omega
$$
를 생각하자. smooth한 해에 대해 적분 by parts를 하면
$$
\int_\Omega \nabla u\cdot \nabla v\,dx
=
\int_\Omega fv\,dx
\qquad \forall v\in H^1(\Omega)
$$
를 얻는다. Dirichlet 문제와 달리 시험함수의 trace를 0으로 둘 필요가 없으므로, 자연스러운 시험함수 공간은 $H^1(\Omega)$이다. 이 문제에서는 상수함수가 kernel에 속하므로 해의 존재를 위해 $\int_\Omega f\,dx=0$이 필요하며, 해는 상수 차이까지만 결정된다.

더 일반적으로 비동차 Neumann 문제
$$
-\Delta u=f \quad \text{in } \Omega, \qquad \partial_\nu u=h \quad \text{on } \partial\Omega
$$
를 생각하자. smooth한 경우에는 적분 by parts에 의해
$$
\int_\Omega \nabla u\cdot \nabla v\,dx
=
\int_\Omega fv\,dx+\int_{\partial\Omega}hv\,dS
\qquad \forall v\in H^1(\Omega)
$$
를 얻는다. trace operator $\operatorname{Tr}:H^1(\Omega)\to H^{1/2}(\partial\Omega)$의 boundedness를 이용하면, 경계항은
$$
\langle h,\operatorname{Tr}(v)\rangle_{H^{-1/2}(\partial\Omega),\,H^{1/2}(\partial\Omega)}
$$
로 해석할 수 있다.

따라서 비동차 Neumann 문제의 weak formulation은 $u\in H^1(\Omega)$를 찾아
$$
\int_\Omega \nabla u\cdot \nabla v\,dx
=
\int_\Omega fv\,dx
+\langle h,\operatorname{Tr}(v)\rangle
\qquad \forall v\in H^1(\Omega)
$$
를 만족시키는 것이다. 마찬가지로 상수함수가 kernel에 속하므로 해의 존재를 위해 compatibility condition
$$
\int_\Omega f\,dx+\langle h,1\rangle =0
$$
이 필요하며, 해는 상수 차이까지만 유일하다. 예를 들어 $\int_\Omega u\,dx=0$을 추가하면 유일성이 회복된다.

이 차이는 본질적인 것이다. Dirichlet 조건은 essential boundary condition으로서 함수공간에 반영되고, Neumann 조건은 natural boundary condition으로서 적분식의 경계항에 나타난다.

## 참고문헌

- Lawrence C. Evans, *Partial Differential Equations*, 2nd ed., American Mathematical Society, 2010.
- Haim Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*, Springer, 2011.
