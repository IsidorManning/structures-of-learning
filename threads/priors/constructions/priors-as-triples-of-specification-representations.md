---
id: Q-20260912231152
type: construction
status: active
created: 2026-09-12
---

<!-- Generated from the Obsidian source on main. Do not edit this branch directly. -->

Let $\mathcal{C}$ be a base category. I propose that a *prior* is a triple
$$\Pi=(\mathcal{S},X,Y)$$
with the following data:
1. $\mathcal{S}$ is a small symmetric monoidal category enriched in $\mathcal{B}$, typically taken to be $\mathbf{Set}$.
2. $X,Y:\mathcal{S}\to{}\mathcal{C}$ are enriched strong symmetric monoidal functors.

Now, the question is what an admissible model is? It could be a monoidal natural transformation $h:X\Rightarrow{}Y$ itself or a single component of it? The space of admissible models, or the hypothesis space, would be:
$$\mathcal{H}_{\Pi}=\text{Nat}(X,Y).$$

The reason we package a prior as a triple of both its specification and its "input and output representations" in the base category, is because the same prior specifications can have drastically different ways to respect it. The representation is part of the prior. A simple example is to take $S=BG$ and define two priors
$$\Pi_{1}=(\mathcal{S},X_{1},Y_{1}),\quad \Pi_{2}=(\mathcal{S},X_{2},Y_{2})$$
with:
$$X_{1}(1)=X_{2}(1)=a,\quad Y_{1}(1)=Y_{2}(1)=b,$$
and
$$X_{1}(s_{g})=X_{2}(s_{g})=\cdot_{a},\quad Y_{1}(s_{g})=\cdot_{b},\quad Y_{2}(s_{g})=\text{id}_{b}.$$
Here, if one check the naturality squares, $\Pi_{1}$ describes equivariance, while $\Pi_{2}$ describes invariance. All invariant models are equivariant but the converse is not true, hence:
$$\mathcal{H}_{\Pi_{2}}\subset{}\mathcal{H}_{\Pi_{1}}.$$
It wouldn't make sense to restrict ourselves to define priors as simply their specification (in this case, a group specification). Instead, we might define two priors to be equivalent in the following way:
$$\Pi_{1}\sim \Pi_{2}\iff \mathcal{H}_{\Pi_{1}}=\mathcal{H}_{\Pi_{2}}.$$
An important question which seems a bit stupid mathematically but empirically important. Does:
$$\mathcal{S}_{1}=S_{2}\land X_{1}=X_{2}\land Y_{1}=Y_{2}\iff(\mathcal{S}_{1},X_{1},Y_{1})\sim (\mathcal{S}_{2},X_{2},Y_{2})?$$

This framework allows us to capture various types of priors by changing the underlying $\mathcal{S}$. For logical priors, one might choose a Lawvere theory. For geometric priors, one might choose $BG$ or a group Lawvere theory. The framework is deliberately general to allow the study of priors themselves and their connections to other components of learning.

I could also propose a morphism of priors: A morphism $(\mathcal{S},X,Y)\xrightarrow{f}(\mathcal{S}',X',Y')$ is an enriched strong symmetric monoidal functor $f:S'\to{}S$ with:
$$X'=X\circ{}f,\quad Y'=Y\circ{}f.$$
I have a conjecture: A morphism of priors induces a contravariant embedding map between hypothesis spaces:
$$\leadsto{} f^{*}:\mathcal{H}_{(\mathcal{S}',X',Y')}\to{}\mathcal{H}_{(\mathcal{S},X,Y)}.$$
This means equivalent prior specifications combined with a morphism between them results in equivalent hypothesis spaces? 

# Theory
Consider the space of all possible components maps:
$$Q=\prod_{a\in{}\text{Ob}(\mathcal{S})}[X(a),Y(a)].$$
Assuming the base category is Cartesian closed, an element of $Q$ is a family of continuous maps $\{ h_{a}:X(a)\to{}Y(a) \}_{a\in{}\text{Ob}(\mathcal{S})}$ without any enforced naturality requirements. Can we define a trivial prior $\Pi_{1}$ such that $\mathcal{H}_{\Pi_{1}}=Q$? Just guessing, we might have something trivial like $(\mathcal{C},\text{id}_{\mathcal{C}},\text{id}_{\mathcal{C}})$ but I am unsure if this works.

In deep learning, $\mathbf{Para}_{\times}(\mathcal{C})$ consists of:
1. **Objects:** Those of $\mathcal{C}$.
2. **1-Morphisms:** Parameterized morphisms $(P,f)\in{}\mathbf{Para}_{\times}(\mathcal{C})(a,b)$, where $P\in{}\mathcal{C}$ and $f:P\times a\to{}b$.
3. **2-Morphisms:** Reparameterizations.

I am unsure how this picture connects to the general presheaf idea in [presheaf-of-prior-realizations](presheaf-of-prior-realizations.md) of some:
$$F:\mathbf{Prior}^{\text{op}}\to{}\mathbf{Cat}$$

# Examples
One useful thing that I believe this framework could offer is that we can construct equivalent priors based on $\mathcal{S}=BG$ and $S=\mathbb{L}_{G}$ for groups, and perhaps even "$S=M_{G}$" where $G$ is a monad, although the monad example doesn't quite form a category and satisfy the definition.