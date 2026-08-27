---
id: Q-20260827183639
type: question
status: active
created: 2026-08-27
---

# Generalizing Priors

## Question
Does there exist a useful mathematical formalism that packages and unifies both logical and geometric separate manner? A prior may be represented by an algebraic theory, while a network respecting that prior is an algebra of that theory in an appropriate category of parametric maps.

In my line of reasoning it is important to separate the prior from the neural network restricted by the prior. Nye builds a one-way construction from selected logical theories.

## Answers log

- **2026-08-27:**

## Next steps

-

## Exploration
There are various notions of "priors" and a great number of motivations for their necessity as a fundamental component of deep learning itself. But what are they mathematically?

In [[../../../literature/nye-2025-categorical-construction|Categorical Construction of Logically Verifiable Neural Architectures]], Logan describes what I call a certain "logical prior", where universal algebra is used to instantiate models, with the para construction, based of a logical (Lawvere) theory. It formalizes mixed priors via distributive laws for monads.

In [[../../../literature/bronstein-2021-geometric-deep|Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges]], "geometric priors" are introduced, which are symmetry group action constraints on the neural networks themselves. [[../../../literature/gavranovic-2024-position-categorical|Categorical Deep Learning is an Algebraic Theory of All Architectures]] showed that "geometric priors" arise as group action monad homomorphisms, and can be generalized using other types of monads like the binary tree or list monad, which give rise to other forms of architectures. These monads are generated freely by an endofunctor in $\mathbf{Para}(\mathbf{Set})$.

## Research log

*created: 2026-08-27.*
