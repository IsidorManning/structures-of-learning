---
id: Q-20260827191150
type: construction
status: active
created: 2026-08-27
---
# Presheaf of Prior Realizations
We might specify $\mathbf{Prior}$ to be the category of Lawvere theories or some other form of algebraic theory:
$$\mathbf{Prior}=\mathbf{Law}\cong{}\mathbf{Mnd}_{f}(\mathbf{Set})$$
If $\mathbb{L},\mathbb{T}\in{}\text{Ob}(\mathbf{Prior})$, then, functorially, is there a construction where we send $\mathbb{L}\mapsto \mathbf{Alg}(\mathbb{L},\mathbf{Para}(\mathcal{C}))$ and a morphism $\mathbb{L}\to{}\mathbb{T}$ to a restriction $\mathbf{Alg}(\mathbb{T},\mathbf{Para}(\mathcal{C}))\to{}\mathbf{Alg}(\mathbb{L},\mathbf{Para}(\mathcal{C}))$? This means that the fundamental relation relating priors and architectures might be some 2-categorical presheaf $$F:\mathbf{Prior}^{\text{op}}\to{}\mathbf{Cat}$$
Another possible constructing is:
$$\text{Impl}_{\mathcal{C}}:\mathbf{Prior}^{\text{op}}\times \mathbf{Arch}_{\mathcal{C}}\to{}\mathbf{Cat}$$
where $\mathbf{Arch}_{\mathcal{C}}$ is a category of architecture presentations, for instance, $\mathbf{Set}$, or $\mathbf{Para}_{}(\mathbf{Set})$. Then, we might construct a functor which yields a category of ways in which an architecture presentation $A$ realizes a prior $P$. But this seems to depends on whether architectural syntax (or "wiring topology") determines whether an implemented model respects a prior. This might not be the case generally. 

This directly recognizes the problem in [[../../../literature/nye-2025-categorical-construction|nye-2025-categorical-construction]] which is elaborated on in [[../questions/prior-architecture-relations|prior-architecture-relations]]: a Lawvere theory does not canonically select real carrier spaces, differentiable realizations, parameter spaces, or neural implementations.

