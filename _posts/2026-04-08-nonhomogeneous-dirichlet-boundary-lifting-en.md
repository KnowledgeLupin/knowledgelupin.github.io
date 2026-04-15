---
title: "Weak Formulation and Boundary Lifting for Nonhomogeneous Dirichlet Boundary Conditions"
date: 2026-04-08 06:24:46 +0900
lang: en
translation_key: nonhomogeneous-dirichlet-boundary-lifting
categories: [Mathematics, PDE]
tags: [weak-formulation, dirichlet-boundary, sobolev-spaces, pde, poisson-equation]
toc: true
math: true
author: KnowledgeLupin
---

Consider the following Poisson boundary value problem:

$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=g \quad \text{on } \partial\Omega.
$$

In the standard Sobolev weak formulation, Dirichlet boundary data usually do not appear inside the equation as a boundary integral. The Dirichlet condition is imposed on the admissible class through the trace, and nonhomogeneous boundary data are reduced to a homogeneous boundary problem by means of boundary lifting.

Below, we assume that $\Omega$ is a bounded Lipschitz domain and that the data satisfy

$$
f\in L^2(\Omega), \qquad
g\in H^{1/2}(\partial\Omega), \qquad
h\in H^{-1/2}(\partial\Omega).
$$

We summarize this procedure for the Poisson equation.

## Weak Formulation of the Homogeneous Dirichlet Problem

First, consider the homogeneous Dirichlet problem

$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=0 \quad \text{on } \partial\Omega.
$$

The appropriate function space is $H_0^1(\Omega)$, and the weak formulation is as follows.

Given $f$, find $u$ such that

$$
\begin{aligned}
u &\in H_0^1(\Omega), \\
\int_\Omega \nabla u \cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
\qquad \forall v\in H_0^1(\Omega).
\end{aligned}
$$

This identity comes from integration by parts in the smooth setting. Indeed,

$$
\begin{aligned}
\int_\Omega (-\Delta u)v\,dx
&=
\int_\Omega \nabla u\cdot \nabla v\,dx \\
&\quad - \int_{\partial\Omega}\partial_\nu u\,v\,dS.
\end{aligned}
$$

Since a test function $v\in H_0^1(\Omega)$ has zero trace, the boundary term vanishes. Thus the Dirichlet condition $u=0$ on $\partial\Omega$ does not appear on the right-hand side of the integral identity; instead, it is encoded in the choice of the function space $H_0^1(\Omega)$.

## Nonhomogeneous Dirichlet Boundary Data

Now consider the nonhomogeneous problem

$$
-\Delta u=f \quad \text{in } \Omega, \qquad u=g \quad \text{on } \partial\Omega.
$$

In this case, the solution must satisfy $u\in H^1(\Omega)$ and $\operatorname{Tr}(u)=g$. Here the boundary condition is imposed not pointwise, but in the trace sense.

More precisely, there exists a bounded linear operator

$$
\operatorname{Tr}:H^1(\Omega)\to H^{1/2}(\partial\Omega).
$$

For smooth functions, this agrees with the usual restriction $\operatorname{Tr}(u)=u\vert_{\partial\Omega}$. Moreover, this operator is surjective onto $H^{1/2}(\partial\Omega)$, and its kernel is $H_0^1(\Omega)$.

The standard weak formulation of the nonhomogeneous Dirichlet problem is

$$
\begin{aligned}
u &\in H^1(\Omega), \\
\operatorname{Tr}(u) &= g, \\
\int_\Omega \nabla u\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
\qquad \forall v\in H_0^1(\Omega).
\end{aligned}
$$

That is, the boundary data $g$ are not imposed weakly through a boundary integral; rather, they are imposed strongly as a condition on the admissible class. The test functions are still taken from $H_0^1(\Omega)$.

## Boundary Lifting

Choose a function

$$
w\in H^1(\Omega), \qquad \operatorname{Tr}(w)=g,
$$

that has $g$ as its boundary trace. This $w$ is called a boundary lifting, and its existence is guaranteed by the surjectivity of the trace operator.

If we set $z:=u-w$, then

$$
\operatorname{Tr}(z)=0, \qquad z\in H_0^1(\Omega),
$$

so substituting $u=z+w$ into the original weak formulation gives

$$
\begin{aligned}
\int_\Omega \nabla z\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
- \int_\Omega \nabla w\cdot \nabla v\,dx \\
&\qquad \forall v\in H_0^1(\Omega).
\end{aligned}
$$

Hence the nonhomogeneous Dirichlet problem is reduced to the following homogeneous boundary problem:

$$
\begin{aligned}
z &\in H_0^1(\Omega), \\
\int_\Omega \nabla z\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
- \int_\Omega \nabla w\cdot \nabla v\,dx \\
&\qquad \forall v\in H_0^1(\Omega).
\end{aligned}
$$

After solving for $z$, the original solution is recovered by setting $u=z+w$.

The same structure remains valid for a more general elliptic operator $L$ in divergence form. If the coefficients are sufficiently bounded so that $Lw\in H^{-1}(\Omega)$ is well defined, then after choosing a boundary lifting $w$ one may define

$$
\tilde f := f-Lw
$$

as an element of $H^{-1}(\Omega)$. The problem is then transformed into a homogeneous Dirichlet weak formulation for $z\in H_0^1(\Omega)$.

## Comparison with the Neumann Problem

Even for the same Poisson equation, the choice of function space changes when the boundary condition is of Neumann type. First consider the homogeneous Neumann problem

$$
-\Delta u=f \quad \text{in } \Omega, \qquad \partial_\nu u=0 \quad \text{on } \partial\Omega.
$$

Its weak formulation is

$$
\begin{aligned}
u &\in H^1(\Omega), \\
\int_\Omega \nabla u\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
\qquad \forall v\in H^1(\Omega).
\end{aligned}
$$

Unlike the Dirichlet problem, there is no need to require the test functions to have zero trace, so the natural test space is $H^1(\Omega)$.

Since constant functions lie in the kernel of this problem, the existence of a solution requires

$$
\int_\Omega f\,dx=0,
$$

and the solution is determined only up to an additive constant.

More generally, consider the nonhomogeneous Neumann problem

$$
-\Delta u=f \quad \text{in } \Omega, \qquad \partial_\nu u=h \quad \text{on } \partial\Omega.
$$

In the smooth setting, integration by parts yields

$$
\begin{aligned}
\int_\Omega \nabla u\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx+\int_{\partial\Omega}hv\,dS \\
&\qquad \forall v\in H^1(\Omega).
\end{aligned}
$$

Using the boundedness of the trace operator $\operatorname{Tr}:H^1(\Omega)\to H^{1/2}(\partial\Omega)$, the boundary term can be interpreted as

$$
\langle h,\operatorname{Tr}(v)\rangle_{H^{-1/2}(\partial\Omega),\,H^{1/2}(\partial\Omega)}.
$$

Therefore, the weak formulation of the nonhomogeneous Neumann problem is

$$
\begin{aligned}
u &\in H^1(\Omega), \\
\int_\Omega \nabla u\cdot \nabla v\,dx
&=
\int_\Omega fv\,dx
+\langle h,\operatorname{Tr}(v)\rangle \\
&\qquad \forall v\in H^1(\Omega).
\end{aligned}
$$

Again, since constants belong to the kernel, the existence of a solution requires the compatibility condition

$$
\int_\Omega f\,dx+\langle h,1\rangle =0,
$$

and the solution is unique only up to an additive constant. For example, uniqueness is restored by imposing

$$
\int_\Omega u\,dx=0.
$$

This difference is essential. Dirichlet conditions are essential boundary conditions and are reflected in the function space, whereas Neumann conditions are natural boundary conditions and appear as boundary terms in the weak formulation.

## References

- Lawrence C. Evans, *Partial Differential Equations*, 2nd ed., American Mathematical Society, 2010.
- Haim Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*, Springer, 2011.
