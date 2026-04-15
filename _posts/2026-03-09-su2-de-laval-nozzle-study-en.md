---
title: "Understanding the de Laval Nozzle with SU2: Mach Number, Back Pressure, Nozzle Shape, and Performance Analysis"
date: 2026-03-09 16:48:23 +0900
lang: en
translation_key: su2-de-laval-nozzle-study
categories: [Mathematics, CFD]
tags: [CFD, SU2, Nozzle, DeLavalNozzle, MachNumber, RocketPropulsion]
toc: true
math: true
author: KnowledgeLupin
---

This post is a study note that systematically organizes the basic concepts of the de Laval nozzle and the interpretation of its results, based on axisymmetric nozzle simulations performed with `SU2`. The goal is not merely to list separate terms, but to explain clearly how `Mach number`, `nozzle shape`, `back pressure`, `exit state`, and `thrust` are connected as one physical flow process.

The central question is the following:

$$
\text{How does a rocket nozzle convert pressure energy into kinetic energy, and how does that process change with geometry and back pressure?}
$$

To answer this question, I proceed in the following order:

1. what `Mach number` is
2. what a nozzle and a de Laval nozzle are
3. where the nozzle sits inside a rocket
4. why performance changes with nozzle shape
5. what my `SU2` simulation actually modeled
6. how each figure should be read in a textbook-style way

# 1. Definition of Mach Number

The `Mach number` is a dimensionless quantity that measures how fast a flow is relative to the speed of sound in that medium.

$$
M = \frac{V}{a}
$$

Here,

$$
V
$$

is the flow speed, and

$$
a
$$

is the local speed of sound.

This quantity is not just a velocity ratio. It is a criterion that distinguishes the very nature of the flow itself.

$$
M < 1 \Rightarrow \text{subsonic}
$$

$$
M = 1 \Rightarrow \text{sonic}
$$

$$
M > 1 \Rightarrow \text{supersonic}
$$

In the supersonic regime, the way pressure information propagates differs from the subsonic case, and compressible phenomena such as `shock` waves appear. A rocket nozzle is a device that relies precisely on this supersonic acceleration, so nozzle analysis always tracks the progression

$$
M < 1 \rightarrow M \approx 1 \rightarrow M > 1
$$

# 2. Role of a Nozzle

A nozzle is a passage that accelerates or decelerates a fluid in a prescribed direction. In rocketry, it specifically refers to the component that produces thrust by ejecting high-temperature, high-pressure gas rapidly backward.

Physically, the essential conversion is

$$
\text{pressure energy} \rightarrow \text{kinetic energy}
$$

The gas in the combustion chamber has high pressure and temperature, and the nozzle converts that energy into a fast jet. Accordingly, rocket thrust can be understood conceptually as

$$
F = \dot{m}V_e + (p_e - p_b)A_e
$$

Here,

- $$\dot{m}V_e$$ is the momentum thrust
- $$(p_e - p_b)A_e$$ is the pressure thrust

# 3. Basic Geometry of the de Laval Nozzle

The most basic rocket nozzle geometry is the **de Laval nozzle**. A de Laval nozzle consists of a converging section, a throat, and a diverging section.

![Basic geometry of a de Laval nozzle](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/de_laval_nozzle.svg)

The three regions to focus on in the figure are the following:

- `converging section`: the region that guides the flow toward the throat
- `throat`: the narrowest cross-section
- `diverging section`: the region that further accelerates the supersonic flow

The basic flow path is

$$
\text{converging section} \rightarrow \text{throat} \rightarrow \text{diverging section}
$$

The de Laval nozzle matters because, as the flow passes through the throat, it reaches

$$
M \approx 1
$$

and then, in the diverging section,

$$
M > 1
$$

so that supersonic exhaust becomes possible.

# 4. Where the Nozzle Sits Inside a Rocket

The nozzle is located at the lower center of the rocket, namely in the exhaust part below the engine. In the figure below, the tanks and structural elements are placed above, while the engine and nozzle are placed below.

![Cross-section of a V-2 rocket](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/v2_rocket_diagram.png)

Rather than memorizing every component name in detail, it is more useful to read this figure in terms of the overall sequence

$$
\text{combustion chamber} \rightarrow \text{throat} \rightarrow \text{nozzle exit}
$$

The nozzle can be understood as the `bell-shaped` passage at the bottom of the rocket through which the exhaust is finally discharged to the outside.

# 5. Why Performance Changes with Shape

A nozzle is not just a hole. If the wall geometry changes, then the internal pressure distribution, the acceleration process, and the exit state all change together. This is why practical design compares shapes such as `conical nozzle`, `bell nozzle`, and `aerospike`.

![Performance comparison for different nozzle geometries](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/nozzle_performance_comparison.svg)

When the shape changes, the following quantities typically change as well:

- exit velocity
- exit pressure
- internal shock structure
- pressure recovery location
- final thrust

In other words, even when starting from the same total pressure and total temperature, one obtains the chain

$$
\text{nozzle shape} \Rightarrow \text{internal flow structure} \Rightarrow \text{exit state} \Rightarrow \text{thrust}
$$

# 6. Modeling Scope of This Simulation

This computation did not attempt to copy the CAD of a real launch vehicle engine directly. Instead, it compares a **simplified 2D axisymmetric de Laval nozzle model for introductory study**.

The two geometries considered were

- `conical15`
- `bell80`

The common geometric parameters were chosen as follows:

$$
r_{\mathrm{inlet}} = 0.06\ \mathrm{m}, \quad
r_{\mathrm{throat}} = 0.02\ \mathrm{m}, \quad
r_{\mathrm{exit}} = 0.04\ \mathrm{m}
$$

$$
L_{\mathrm{conv}} = 0.06\ \mathrm{m}, \quad
L_{\mathrm{div,conical}} = 0.12\ \mathrm{m}, \quad
L_{\mathrm{div,bell}} = 0.096\ \mathrm{m}
$$

The analysis conditions were:

- `2D axisymmetric Euler`
- total pressure $$p_0 = 500000\ \mathrm{Pa}$$
- total temperature $$T_0 = 300\ \mathrm{K}$$
- back pressure $$p_b = 40000,\ 15000,\ 5000\ \mathrm{Pa}$$

So this model should be understood as

$$
\text{full real engine} \neq \text{idealized de Laval nozzle for geometry comparison}
$$

The reason for this simplification is threefold:

1. to see the essential nozzle physics first
2. to read the relationship among `Mach`, `pressure`, and `thrust` directly
3. to begin geometry comparison without requiring complex 3D CAD, combustion, cooling, or turbulence modeling

# 7. Basic Principles for Interpreting the Results

For the present results, it is more appropriate to focus on trend interpretation than on absolute performance values themselves. Not all cases converged to sufficiently low residuals. Therefore, the safest interpretation principle is

$$
\text{absolute numerical values} < \text{shape-dependent trends and flow structure}
$$

Even so, the results are still very useful for educational purposes, because the four figures illuminate the key questions of nozzle analysis from different angles.

- internal flow structure: `Mach panel`
- pressure variation: `wall pressure`
- final performance: `thrust`
- exit state: `exit Mach`

I now interpret each figure in a textbook-style manner.

# 8. Figure 1: Mach Panel

![Mach panel](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/mach_panel.png)

This figure shows the distribution of `Mach number` throughout the inside of the nozzle. It is the first figure to inspect in nozzle analysis, because the purpose of the nozzle is ultimately the conversion

$$
\text{pressure energy} \rightarrow \text{velocity energy}
$$

This figure should be read according to the following criteria:

1. Does the flow reach

$$
M \approx 1
$$

near the throat?

2. In the diverging section, does it increase smoothly to

$$
M > 1
$$

?

3. As the back pressure increases, do shocks or compression structures appear?

In the present results, both geometries form a strongly supersonic flow all the way to the exit at `15000 Pa`. At `40000 Pa`, the higher back pressure suppresses the expansion in the diverging section more strongly. By contrast, at `5000 Pa`, the exit pressure remains relatively high, so the flow can be read as `underexpanded`, with

$$
p_e > p_b
$$

Thus, this figure shows **how the flow is accelerated inside the nozzle**.

# 9. Figure 2: Wall Pressure Comparison

![Wall pressure comparison](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/wall_pressure_comparison.svg)

The wall-pressure distribution $$p_w(x)$$ is one of the most classical diagnostic plots in nozzle analysis. If the flow expands properly, the pressure decreases.

$$
\frac{dp_w}{dx} < 0
$$

If a strong internal shock or pressure recovery occurs, then the pressure rises again or bends upward over some interval.

$$
\frac{dp_w}{dx} > 0
$$

From this figure, one can read the following trends:

- At `15000 Pa`, both geometries expand reasonably well overall.
- At `40000 Pa`, the wall pressure remains higher because of the higher back pressure.
- At `5000 Pa`, the pressure does not drop sufficiently by the exit, so pressure energy is still left over.

Thus, the wall-pressure plot is a pressure-side diagnostic tool that shows **where and how much pressure has been converted into velocity**.

# 10. Figure 3: Thrust vs Back Pressure

![Thrust comparison against back pressure](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/thrust_vs_back_pressure.svg)

This figure shows how the estimated thrust changes as the back pressure $$p_b$$ varies. From a practical perspective, this is the most direct performance-comparison plot.

From the textbook point of view, thrust is written as

$$
F = \dot{m}V_e + (p_e - p_b)A_e
$$

so this plot shows how the final outcome of the internal flow structure appears as force.

The numerical results are summarized as follows.

| Shape | $$p_b$$ (Pa) | $$M_e$$ | Estimated thrust (N) |
| --- | ---: | ---: | ---: |
| bell80 | 40000 | 2.962 | 778.51 |
| bell80 | 15000 | 3.166 | 1002.42 |
| bell80 | 5000 | 1.336 | 2598.68 |
| conical15 | 40000 | 2.940 | 787.53 |
| conical15 | 15000 | 3.131 | 1002.40 |
| conical15 | 5000 | 1.471 | 2973.39 |

Reading the table together with the graph, one can summarize the results as follows:

- At `15000 Pa`, the two geometries are almost equivalent.
- At `40000 Pa`, `conical15` is slightly higher.
- At `5000 Pa`, `conical15` comes out noticeably higher.

However, there is an important caveat. Since the residuals in this computation were not sufficiently low, these numbers should not be read as if they were design-approval values. A safer interpretation is to read the trend

$$
\text{when the back pressure changes, the relative advantage of each geometry can change as well}
$$

# 11. Figure 4: Exit Mach vs Back Pressure

![Exit Mach comparison against back pressure](/assets/img/posts/2026/2026-03-09-su2-de-laval-nozzle-study/exit_mach_vs_back_pressure.svg)

This figure shows how the mean exit `Mach number` changes with back pressure. This quantity indicates how strongly the nozzle has accelerated the flow by the time it reaches the exit.

In general, a larger exit Mach suggests a larger velocity term, but thrust is not determined by $$M_e$$ alone. In reality,

$$
\dot{m},\quad p_e,\quad p_b
$$

all act together.

In the present results:

- At `15000 Pa`, both geometries accelerate well to about

$$
M_e \approx 3
$$

- At `40000 Pa`, the flow is still supersonic, but constrained by the higher back pressure.
- At `5000 Pa`, the exit pressure remains very high, and the flow simultaneously shows `underexpanded` behavior.

Thus, this figure shows the **exit velocity state**, whereas the thrust plot above shows **how that result appears as actual force**.

# 12. Summary of the Results

The clearest conclusion from this simulation is the following:

$$
\text{Back pressure changes the internal expansion structure of the nozzle, and that change carries over to the exit state and thrust difference.}
$$

Nozzle analysis cannot be understood from a single figure alone. At minimum, the following four perspectives must be viewed together:

$$
\text{Mach field} \rightarrow \text{wall pressure} \rightarrow \text{exit state} \rightarrow \text{thrust}
$$

Only then can one explain in a structural way why a particular geometry appears more favorable.

# 13. Limitations of the Analysis

These results are certainly meaningful for educational purposes, but they also have clear limitations if one tries to read them as practical quantitative results.

1. Not all cases converged to sufficiently low residuals.
2. The analysis is based on `Euler`, so viscosity, turbulence, heat transfer, and separation effects are not represented directly.
3. The actual 3D engine geometry, cooling channels, combustion chemistry, and multicomponent gas effects are not included.

Therefore, the appropriate interpretation standard for this post is

$$
\text{accuracy of absolute performance values} \;<\; \text{understanding of shape-dependent trends and physical structure}
$$

# 14. Next Steps

As follow-up study tasks, the following three directions are natural:

1. upgrade the same pipeline to `RANS` to include viscous effects
2. improve convergence quality through more stable continuation and mesh adjustment
3. go beyond `bell` and `conical` toward geometry-parameter optimization

In one sentence:

$$
\text{Nozzle shape is not merely an external geometric difference, but a key design variable that changes the internal flow structure and performance.}
$$

`SU2` is a useful tool for making those differences visible even at the introductory stage.
