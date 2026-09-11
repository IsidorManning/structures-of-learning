---
id: Q-20260827183603
type: question
status: active
created: 2026-08-27
---

# Empirical forms of priors
## Relations
- **Related to:**
	- [[prior-architecture-relations]]

## Question
Are there other forms of priors other than geometric and logical? Perhaps locality, sparsity, causality, probabilistic independence, or even regularization? Is there a notion of a "prior" such that regularization becomes a prior? What actual forms of priors exist in empiricism and what is it that characterizes them all? What other forms of priors genuinely exist? There might exist crucial priors like probabilistic or temporal constraints that this framework can't express. If so, we should rethink our abstraction.

## Answers log

- **2026-08-27:** 
## Next steps

- 

## Exploration
There are many notions of "priors" and part of this exploration is determining a better definition and characterization of what such object is. In general, I would refer to it as something which restricts the space of possible neural network models. Intuitively, some architectures might not be able to satisfy a certain mathematical property---the prior---and are then excluded from a space of "prior-satisfying models". 

The empirical literature does not support a single established meaning of prior.

#### Bayesian priors
In Bayesian learning, a prior is a measure combined with a likelihood, assigning relative mass. A full-support Gaussian prior does not remove hypotheses at all; it ranks regions of parameter space. In neural networks, apparently weak parameter priors may induce highly structured function-space priors, and different parameterizations produce different function priors. This is why “prior = subset of architectures” cannot cover even the canonical probabilistic usage.

#### Geometric priors

#### Logical priors

#### Probabilistic priors


## Research log

*created: 2026-08-27.*
