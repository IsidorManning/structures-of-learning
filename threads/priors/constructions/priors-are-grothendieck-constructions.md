---
id: 202610282309
type: construction
status: active
created: 2026-10-28
---

This is directly related to [[../questions/priors-as-triples-of-specification-representations|priors-as-triples-of-specification-representations]]. It seems what I've described in [[../../../field-notes/structural_priors_v0.pdf|structural_priors_v0]] is captured by the theory fibered and indexed categories, and Grothendieck constructions. 

# A breakdown of the abstraction
### Structural priors
Let $\mathcal{C}$ be a locally small category, called our *base category*. We define a prior as a triple $\Pi=(\mathcal{S},X,Y)$ where $X,Y:\mathcal{S}\rightarrow{}\mathcal{C}$ are functors and $\mathcal{S}$ is a small category.

We can consider the set of *admissible models* $\mathcal{H}_{\Pi}=\text{Nat}(X,Y)$.

A morphism $(F,a,b):\Pi_{1}\rightarrow{}\Pi_{2}$ consists of a functor $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$ and natural transformations $a:X_{1}\Rightarrow{}X_{2}F$ and $b:Y_{2}F\Rightarrow{}Y_{1}$.

We get a canonical category of priors whose objects are priors $\Pi$ over a fixed base $\mathcal{C}$, and whose morphisms are these prior morphisms. Composition $\Pi_{1}\xrightarrow{(F,a,b)}\Pi_{2}\xrightarrow{(G,c,d)}\Pi_{3}$ is given by:
$$(G,c,d)\circ{}(F,a,b)=(GF,(cF)\circ{}a,b\circ{}(dF)).$$
Identity is given by $(\text{id}_{\mathcal{S}},\text{id}_{X},\text{id}_{Y})$.
# Realizations
Fixing a parameter space $P\in{}\mathcal{C}$, a *realization* of a prior $\Pi$ is given by:
$$\Phi:\Delta P\times X\Rightarrow{}Y.$$
# As Grothendieck Constructions
Fix a specification $\mathcal{S}$, and consider the functor category $[\mathcal{S},\mathcal{C}]\times[\mathcal{S},\mathcal{C}]^{\text{op}}$. To allow the specification to vary via $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$, define a functor $K:\mathbf{Cat}_{\text{sm}}^{\text{op}}\rightarrow{}\mathbf{CAT}$ given by:
$$K(\mathcal{S})=[\mathcal{S},\mathcal{C}]\times[\mathcal{S},\mathcal{C}]^{\text{op}},\quad K(F)=(-\circ{}F,-\circ{}F).$$
So for $\Pi_{1}=(\mathcal{S}_{1},X_{1},Y_{1})$ and $\Pi_{2}=(\mathcal{S}_{2},X_{2},Y_{2})$, the mapping works as follows: 
$$(X_{2},Y_{2})\xrightarrow{K(F)}(X_{2}F,Y_{2}F),$$
where $(X_{2},Y_{2})\in{}\text{Ob}(K(\mathcal{S}_{2}))$ and $(X_{2}F,Y_{2}F)\in{}\text{Ob}(K(\mathcal{S}_{1}))$. 

For a contravariant category-valued functor $K$, the Grothendieck construction has objects corresponding to pairs $\binom{\mathcal{S}}{z}$ where $z\in{}K(\mathcal{S})$, where $z\cong{}(X,Y)$, and morphisms consist of pairs $\binom{F}{F'}$ where $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$ (the specification functor!) and where $F':K(\mathcal{S}_{1})\rightarrow{}K(F)(K(\mathcal{S}_{2}))$. But $K(F)(K(\mathcal{S}_{2}))$ is ?isomorphic? to applying $(-\circ{}F,-\circ{}F)$ to a choice of $(X_{2},Y_{2})$. So, under $F'$, $(X_{2},Y_{2})\mapsto(X_{2}F,Y_{2}F)$.

# Connections to Fibered Categories

$$$$
