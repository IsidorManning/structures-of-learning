---
id: Q-20260827183603
type: question
status: active
created: 2026-08-27
---

# Empirical forms of priors
## Relations
- **Related to:**
	- [prior-architecture-relations](prior-architecture-relations.md)

## Question
Are there other forms of priors other than geometric and logical? Perhaps locality, sparsity, causality, probabilistic independence, or even regularization? Is there a notion of a "prior" such that regularization becomes a prior? What actual forms of priors exist in empiricism and what is it that characterizes them all? What other forms of priors genuinely exist? There might exist crucial priors like probabilistic or temporal constraints that this framework can't express. If so, we should rethink our abstraction.

## Answers log

- **2026-11-02:** There are other forms of priors and it isn't clear what so far what [[../../../field-notes/structural_priors_v0.pdf|my candidate abstraction]] captures. For instance, the scale separation prior in GDL is indeed a prior about hierarchical composition and coarsening/locality approximation, but is this a prior? Well, that depends how we define "prior". But there certainly are more *flavors* of priors other than geometric and logical.   
## Next steps

- **2026-11-02:** Perhaps a tinier survey of the empirical forms of priors. The empirical literature does not support a single established meaning of prior. Perhaps that is a problem worth keeping in the back of my head as I move on?

## Exploration
There are many notions of "priors" and part of this exploration is determining a better definition and characterization of what such object is. In general, I would refer to it as something which restricts the space of possible neural network models. Intuitively, some architectures might not be able to satisfy a certain mathematical property (the prior) and are then excluded from a space of "prior-satisfying models". 



#### Bayesian priors
In Bayesian learning, a prior is a measure combined with a likelihood, assigning relative mass. A full-support Gaussian prior does not remove hypotheses at all; it ranks regions of parameter space. In neural networks, apparently weak parameter priors may induce highly structured function-space priors, and different parameterizations produce different function priors. This is why “prior = subset of architectures” cannot cover even the canonical probabilistic usage.

#### Geometric priors

#### Logical priors

#### Probabilistic priors


## Research log

*created: 2026-08-27.*
