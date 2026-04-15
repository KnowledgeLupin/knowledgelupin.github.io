---
title: "A Beginner's Introduction to CFD with SU2: Airfoils, Angle of Attack, Aerodynamic Coefficients, and Unsteady Flow"
date: 2026-03-08 22:45:00 +0900
lang: en
translation_key: su2-cfd-beginner-project
categories: [Mathematics, CFD]
tags: [CFD, SU2, NACA0012, Aerodynamics, Simulation]
toc: true
math: true
author: KnowledgeLupin
---

Today I built a very small beginner `CFD` project with `SU2` and practiced interpreting the results. I started with an `AOA sweep` for the `NACA0012` airfoil, and then, because static plots alone did not feel intuitive enough, I continued with an `unsteady` cylinder-wake problem.

This post is a record of what I learned today, written so that I can understand it again later. The three main points are:

1. understanding what an `airfoil`, `angle of attack`, and `aerodynamic coefficients` are,
2. learning how to read the results of a static `AOA sweep`,
3. developing some intuition for time-dependent flow through a `wake` and a `probe`.

# 1. What kind of tool is SU2?

`SU2` is an open-source `CFD` solver. The user prepares a mesh file and a configuration file, then runs `SU2_CFD` to compute the flow field.

What confused me at first was the question, "Is this Python?" The precise answer is no. The actual computation is carried out by a separate solver, while Python is used more as a supporting tool for case generation, result collection, animation, and post-processing.

Very roughly speaking,

$$
\text{SU2} = \text{flow solver engine}, \qquad
\text{Python} = \text{automation and post-processing tool}
$$

# 2. What is an airfoil?

An airfoil is the `2D` cross-sectional shape you see when a wing is cut from the side. A full wing is a three-dimensional structure, but many introductory ideas in aerodynamics are first learned from this single cross section.

So a good way to think about it is

$$
\text{airfoil} = \text{basic cross-sectional shape that determines wing performance}
$$

The airfoil used here was `NACA0012`. Its name already tells us some of its geometric features.

- `00`: a symmetric airfoil with no maximum camber
- `12`: maximum thickness equal to $$12\%$$ of the chord length

So `NACA0012` is a classic introductory airfoil: symmetric, moderately thick, and very commonly used.

# 3. What is the angle of attack (AOA)?

`AOA` stands for `Angle of Attack`. It is the angle between the reference line of the airfoil and the direction of the relative flow.

![AOA diagram](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/angle_of_attack.jpg)

The key lines in the diagram are:

- `chord line`: the reference line connecting the leading and trailing edges of the airfoil
- `relative wind`: the direction of the oncoming flow seen by the airfoil

So the definition is

$$
AOA = \text{angle between the chord line of the airfoil and the relative flow direction}
$$

Intuitively, it measures how much the wing is tilted relative to the airflow.

# 4. What are aerodynamic coefficients?

The three main quantities that appeared throughout this project were

$$
C_L = \text{lift coefficient}
$$

$$
C_D = \text{drag coefficient}
$$

$$
C_M = \text{moment coefficient}
$$

In very intuitive terms,

- $$C_L$$: how well the wing generates lift
- $$C_D$$: how much resistance the wing experiences
- $$C_M$$: how strongly the wing tends to rotate

And when we want a simple measure of efficiency, we usually look at

$$
\frac{C_L}{C_D}
$$

because, for the same amount of lift, a smaller drag means better efficiency.

# 5. First project: an AOA sweep for NACA0012

The first project was very simple. For the `NACA0012` airfoil, I prescribed several values of `AOA` and compared the resulting $$C_L$$, $$C_D$$, and $$C_M$$.

The angles used in this computation were

$$
AOA = [-2, 0, 2, 4, 6, 8]^\circ
$$

## 5.1 How does the lift coefficient change?

![CL vs AOA](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/cl_vs_aoa.svg)

In this plot, the horizontal axis is `AOA`, and the vertical axis is the lift coefficient $$C_L$$.

The main observations are immediate:

- at $$AOA = 0^\circ$$, we have $$C_L \approx 0$$;
- as $$AOA$$ increases, $$C_L$$ also increases.

Since `NACA0012` is a symmetric airfoil, it is natural that the lift is close to zero at $$AOA = 0^\circ$$. Once the wing is tilted, the flow above and below the airfoil becomes asymmetric, and lift is generated.

## 5.2 How does the drag coefficient change?

![CD vs AOA](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/cd_vs_aoa.svg)

In this figure, the horizontal axis is `AOA`, and the vertical axis is the drag coefficient $$C_D$$.

The message of this graph is simple but very important: as lift increases, drag also increases. In other words, producing more lift comes with the cost of greater aerodynamic resistance.

In summary,

$$
AOA \uparrow \Rightarrow C_L \uparrow,\quad C_D \uparrow
$$

## 5.3 Why is the drag polar important?

![Drag polar](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/drag_polar.svg)

In this plot, the horizontal axis is $$C_D$$ and the vertical axis is $$C_L$$. So it shows, all at once, how much lift we gain for a given amount of drag.

In this computation, the best value of $$\frac{C_L}{C_D}$$ appeared around $$AOA = 2^\circ$$. By contrast, at $$AOA = 8^\circ$$, the lift $$C_L$$ is the largest, but the drag $$C_D$$ has also increased substantially, so the efficiency is actually worse.

This interpretation is very intuitive:

- `small AOA`: little lift, but also little drag
- `moderate AOA`: a good balance between lift and drag
- `large AOA`: strong lift, but at the price of a much larger drag

# 6. But static graphs had a limitation

Up to this point the results were interesting, but something still felt missing. The graphs told me the numbers, but they did not show me clearly how the flow was actually moving and changing.

This is exactly where the distinction between `steady-state` and `unsteady` becomes important.

- `steady-state`: compare the final converged state for each condition
- `unsteady`: compute how the flow field itself evolves in time

So I moved on to the second project.

# 7. Second project: an unsteady wake behind a cylinder

The second project was an `unsteady` cylinder-wake problem designed to visualize `von Karman vortex shedding`. In some sense, this problem is even more intuitive for a beginner than an airplane wing, because the flow behind the cylinder oscillates from side to side and sheds vortices alternately.

## 7.1 What is a wake?

`wake` refers to the disturbed flow region behind an object.

$$
\text{wake} = \text{disturbed flow region behind an object}
$$

In front of the cylinder, the flow splits; behind it, the flow merges again. But that process is not perfectly smooth, so a fluctuating and distorted region forms downstream. That trailing disturbed region is the `wake`.

## 7.2 What is a probe?

A `probe` is a virtual sensor that measures the value of a quantity at one point in the flow field.

$$
\text{probe} = \text{measurement point at a specific location in the flow field}
$$

In this problem, I continuously recorded the velocity magnitude at one point near the centerline behind the cylinder. If the wake oscillates from side to side, then the measured velocity at that point should also rise and fall over time.

# 8. This is what unsteady flow looks like

This time, instead of looking only at static coefficient plots, I created time snapshots and a `GIF` so that I could see the flow field itself.

## 8.1 Snapshots at several times

![Velocity snapshots](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/velocity_snapshots.png)

This figure shows the velocity magnitude at several different times.

- the black circle is the cylinder,
- the colormap represents the velocity magnitude,
- each panel displays the time, drag coefficient, lift coefficient, and probe value.

You can see that the wake behind the cylinder keeps changing its shape over time. This is the crucial difference from the `AOA sweep`. Now the object of interest is no longer a comparison of outcomes across parameter values, but the flow field itself as it evolves in time.

## 8.2 Animation

![Velocity wake gif](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/velocity_wake.gif)

This `GIF` is made by stitching those time snapshots together. If the earlier `AOA sweep` animation was essentially just stepping through several steady states in sequence, this animation really shows

$$
\text{flow field}(t)
$$

directly.

That is, it lets us see how the `wake` develops over time.

## 8.3 Probe and drag time series

![Probe and drag](/assets/img/posts/2026/2026-03-08-su2-cfd-intro/probe_and_drag.png)

This figure plots the `probe` value measured at one point in the flow field together with the drag coefficient $$C_D(t)$$ on the same time axis.

This time series matters for the following reason:

- the flow-field images provide spatial intuition;
- the time series shows how that change is actually recorded numerically.

In other words, it connects "flow seen as a picture" with "flow seen as data."

# 9. Main lessons from today

What I learned most clearly today is that reading graphs and looking at flow fields are different skills, but they complement one another.

In the first project, I:

- learned what an `airfoil` is,
- understood what `AOA` means,
- developed some intuition for interpreting $$C_L$$, $$C_D$$, and $$C_M$$,
- used the `drag polar` to think about efficiency.

In the second project, I:

- learned that a `wake` is the disturbed flow behind an object,
- understood that a `probe` is a sensor for observing the flow at a single point,
- felt the difference between `steady-state` and `unsteady`,
- confirmed that `GIF`s and time series can be much more intuitive than static coefficient plots.

# 10. Things I want to try next

Today I focused on short demonstrations for a quick introduction, but the next steps could be much more interesting.

1. Run a viscous `RANS` analysis for the `NACA0012` airfoil
2. Run the `unsteady` cylinder case longer to see a more clearly periodic wake
3. Perform an `FFT` on the `probe` signal to extract the dominant frequency
4. Add post-processing for an animation of the `pressure coefficient` distribution around the airfoil

The conclusion from today is simple.

When first learning `CFD`, there is no need to begin with complicated turbulence models or a full three-dimensional aircraft. Even small, clear examples like an `AOA sweep` for a single airfoil and the `wake` behind a cylinder are enough to develop a surprisingly deep intuition for the core ideas of aerodynamics.
