---
title: "Saint Venant Equations and the Physics of Shallow Water"
date: 2026-04-18 07:15:00 +0900
slug: "saint-venant-shallow-water-en"
categories: ["Mathematics", "PDE"]
tags: ["saint-venant", "shallow-water-equations", "balance-law", "hyperbolic-pde", "depth-average"]
description: "An introduction to the Saint Venant equations from the geometry of shallow water, depth averaged velocity, and the conservation of mass and horizontal momentum."
excerpt: "The Saint Venant equations become much easier to read once one starts from the geometry of a shallow water layer. This post explains the variables, the conservative form, and the meaning of each term in the momentum balance."
image: "/assets/img/posts/2026/2026-04-18-saint-venant-shallow-water/bottom-elevation-visualization.png"
author: "KnowledgeLupin"
math: true
toc: true
---

# Saint Venant Equations and the Physics of Shallow Water

When one first meets the Saint Venant equations, the formulas often look familiar and yet slightly mysterious. The terms $$hu$$, $$hu^2$$, $$\frac{g}{2}h^2$$, and the topography term on the right all resemble standard pieces of fluid equations, but their meaning becomes much clearer once we start from the geometry of a shallow water layer.

This post follows that route. I will first describe the physical variables, then explain the depth averaged velocity, and finally show how conservation of mass and horizontal momentum lead to the Saint Venant system

$$
\partial_t h+\partial_x(hu)=0,
$$

$$
\partial_t(hu)+\partial_x\left(hu^2+\frac{g}{2}h^2\right)=-gh\,\partial_x z_b.
$$

## The geometry of the water layer

Consider a long channel. The horizontal coordinate is $$x$$ and the vertical coordinate is $$z$$. The bottom of the channel is not necessarily flat, so we write its elevation as $$z_b(x)$$.

The upper boundary of the water is the free surface, denoted by $$\eta(x,t)$$. The actual water depth is therefore

$$
h(x,t)=\eta(x,t)-z_b(x).
$$

The quantity $$h$$ is the first state variable of the model. It measures how much water is stored above the bottom at each horizontal location.

![Bottom elevation and free surface](/assets/img/posts/2026/2026-04-18-saint-venant-shallow-water/bottom-elevation-visualization.png)

*Figure 1. The bottom elevation $$z_b$$ and the free surface $$\eta$$ determine the water depth $$h=\eta-z_b$$.*

This picture already explains why the bottom elevation matters. Even if the free surface stays the same, changing the bottom changes the depth, and changing the depth changes the local flow.

## What depth averaged velocity means

In the full fluid description, the horizontal velocity may vary with height. Near the bottom the fluid may move more slowly, while near the free surface it may move faster. The Saint Venant model does not keep that full vertical profile. Instead, it replaces it by a single representative horizontal velocity.

If $$v(x,z,t)$$ denotes the true horizontal velocity, then the depth averaged velocity is defined by

$$
u(x,t)=\frac{1}{h(x,t)}\int_{z_b(x)}^{\eta(x,t)} v(x,z,t)\,dz.
$$

So $$u$$ is not the velocity at one specific height. It is the average horizontal velocity of the entire water column. This is why the Saint Venant equations are a reduced one dimensional model obtained from a vertically averaged flow.

![Depth averaged horizontal velocity](/assets/img/posts/2026/2026-04-18-saint-venant-shallow-water/depth-averaged-velocity.png)

*Figure 2. The true horizontal velocity may vary across the depth, but the model replaces that profile by one depth averaged velocity $$u$$.*

## Why $$hu$$ appears naturally

Mass conservation is the simplest part of the system. The amount of water stored in an interval $$[x_1,x_2]$$ is

$$
\int_{x_1}^{x_2} h(x,t)\,dx.
$$

This amount changes only because water enters or leaves through the endpoints. The discharge per unit width is the product of depth and depth averaged velocity, namely $$hu$$. Therefore mass conservation gives

$$
\partial_t h+\partial_x(hu)=0.
$$

So $$hu$$ is not an arbitrary product. It is the discharge carried by the water column.

## Reading the momentum equation term by term

The second equation expresses horizontal momentum balance. Since $$hu$$ can be viewed as horizontal momentum per unit width,

$$
\partial_t(hu)
$$

represents the time variation of momentum.

The term

$$
\partial_x(hu^2)
$$

describes transport of momentum by the flow itself. Faster flow and deeper water carry more momentum across the channel.

The term

$$
\partial_x\left(\frac{g}{2}h^2\right)
$$

comes from hydrostatic pressure. Deeper water produces a larger pressure load, and after integrating that pressure over depth one obtains the familiar quadratic contribution $$\frac{g}{2}h^2$$.

This is why the momentum flux takes the form

$$
hu^2+\frac{g}{2}h^2.
$$

One part comes from transport, and the other comes from pressure.

## Why the bottom term is on the right

The source term

$$
-gh\,\partial_x z_b
$$

accounts for the slope of the bottom. If the bottom rises, the geometry pushes the water against that change. If the bottom falls, the effect is reversed.

Without this term, the model would only describe a flat bottom. More importantly, it would fail to preserve a stationary water surface over uneven topography.

A particularly important equilibrium is

$$
u=0,\qquad h+z_b=\text{constant}.
$$

This is the lake at rest state. The water is motionless, but the free surface is flat. In this regime the pressure contribution and the bottom source term must cancel each other exactly.

## A conservation law and a balance law

The first equation is a pure conservation law for mass. The second equation includes both a flux and a source term, so it is a balance law rather than a pure conservation law.

This distinction matters in numerical approximation as well. If the source term is discretized poorly, even the lake at rest state may begin to move numerically. That is why well balanced discretizations are central for the Saint Venant system.

## Closing remarks

The Saint Venant equations are not just a shallow version of the Euler equations. They combine the geometry of a thin water layer, the depth averaged horizontal velocity, conservation of mass, and the balance between transport, hydrostatic pressure, and bottom topography.

Once that structure is visible, each term becomes easier to read. The variable $$h$$ is the water depth. The variable $$u$$ is the depth averaged horizontal velocity. The quantity $$hu$$ is both discharge and the natural momentum variable. The flux $$hu^2+\frac{g}{2}h^2$$ combines transport and pressure. The source term $$-gh\,\partial_x z_b$$ records the effect of the bottom geometry.

At that point the system stops looking like a formula to memorize and starts looking like a compact expression of the physics of shallow water.
