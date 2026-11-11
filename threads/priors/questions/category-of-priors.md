---
id: Q-20260827183501
type: question
status: finished
created: 2026-08-27
---

# Category of Priors
## Relations
- **Depends on:**
	- [empirical-forms-of-priors](empirical-forms-of-priors.md)
	- [structure-of-priors](structure-of-priors.md)
	- [morphism-of-priors](morphism-of-priors.md)
- **Related to:**
	- [generalizing-priors](generalizing-priors.md)

## Question
Does there exist a category of priors? What would morphisms between priors mean theoretically and empirically? Are there examples of a prior being changed and an observation in how that changes the underlying architecture?

If there is a useful relation between priors, could one model the category of priors as perhaps $\mathbf{Prior}\to{}\mathbf{Cat}$, where perhaps $\mathbf{Prior}=\mathbf{Law}$ or $\mathbf{Prior}=\mathbf{Mnd}_{f,\mathbf{Set}}$, sending $\mathbb{L}\mapsto \mathbf{Para}(\mathcal{C})$ in some sense, and some morphism of algebraic theories gets sent to a morphism between parametric categories? If this would be a useful abstraction, in line with nature, we could explore this mathematics purely mathematically.

## Answers log

- **2026-10-16:** There does indeed exist such category, but it would of course depend on the chosen abstraction for priors. The candidate outlined in [priors-as-triples-of-specification-representations](../constructions/priors-as-triples-of-specification-representations.md) forms a category under a specifically defined [morphism-of-priors](morphism-of-priors.md). I believe a useful prior morphism should induce some sort of contravariance, in the sense that a prior morphism from $P_{1}\to{}P_{2}$ should, broadly speaking, correspond to saying that "models that respect $P_{2}$ can be transformed into models that respect $P_{1}$". I think my initial question of asking whether "the category of priors is $\mathbf{Law}$ or $\mathbf{Mnd}_{f,\mathbf{Set}}$" misses the point, because we might model a prior using both a Lawvere theory, or another category. The category of priors is not a specific category put rather a *type of category* where you can choose, say, to represent the structure of the prior as a Lawvere theory, *or* a a one-object category, *or* a terminal category, all giving different forms of priors. Moreover, simply asking whether "there exists a category of priors" is rather meaningless to me at this point. The more interesting question is whether a defined category of priors actually yields some form of structure that allows us to see new perspectives and ask new questions that we couldn't do without it, perhaps via functoriality, and "higher relational structures" that you cannot simply define on objects/priors alone.

## Research log

*created: 2026-08-27.*
