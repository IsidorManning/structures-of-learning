---
id: N-202610170005
type: construction
status: active
created: 2026-10-17
---

Imagine a streaming speech recognizer. Its output at time $t$ must be determined by the audio received up to $t$. Let $A$ be the space of input samples and $B$ the space of outputs emitted at each step. Define a prior $\Pi_{\mathrm{stream}}=(\mathcal{T},X,Y)$, where $\mathcal{T}$ is the poset category on $(\mathbb{N},\leq)$, $X(n)=A^n$ with arrows $n\to m$ interpreted as prefix truncations, meaning that we map it to some truncation $A^n \to A^m$ by truncating $(a_1,a_2,\dots,a_m,\dots,a_n)$ to $(a_1,a_2,\dots,a_m)$. An admissible model is a family of component $h_n:A^n \to B^n$ satisfying
$$h_n(x_1,\dots,x_n)\mid _{1:m}=h_m(x_1,\dots,x_m).$$
Intuitively, extending the input cannot revise an already emitted output. This is a non-anticipation constraint for the resulting stream map.

This sort of prior modeled using poset specifications is common across non-anticipation tasks, such as in attention mechanisms, and WaveNets. 

Let $A$ be the input-token or input-feature space, and $B$ the per-position output space. For language modeling, $B$ could be the space of next-token probability distributions. Define a category $\mathcal{S}_{\mathrm{prefix}}$ with objects corresponding to sequences of lengths $n\in \mathbb{N}$, and with a morphism $n\to m$ existing whenever $m\leq n$, representing truncation to the first $m$ positions. Define $X$ and $Y$ as in \Cref{eg:non-anticipation}. Then, let $\Pi_{\mathrm{causal}}=(\mathcal{S}_{\mathrm{prefix}},X,Y)$. An admissible model consists of functions $f_n:A^n \to B^n$ satisfying
$$\pi_{n,m}^B\circ f_n = f_m \circ \pi^A_{n,m}.$$
Intuitively, processing the whole sequence and keeping its first $m$ outputs, or first truncating the input and then processing it should yield the same result. This is one prior that the attention mechanism in the original transformer respects, where future text cannot change earlier predictions. Indeed, taking $m=i$ gives
$$[f_n(x_1,\dots,x_n]_i=[f_i(x_1,\dots,x_i)]_i.$$
The right-hand side has no access to $x_{i+1},\dots,x_n$\footnote{Note that this prior expresses both non-anticipation and consistency across sequence lengths. Separate functions $f_n$ could each avoid future tokens while still change their behavior depending on the total length $n$. Naturality rules that out too.}. Consider an attention layer with the same parameters at every supported sequence length. At position $i$,
$$\begin{aligned}
    f(\sigma x)&=q(h(\sigma x))\\
    &= q(\sigma h (x))\\
    &= q(h(x))\\
    &= f(x).
\end{aligned}$$
Appending tokens after $i$ changes neither the terms nor the denominator. Therefore the output at $i$ stays unchanged. Shared positionwise feed-forward layers, ordinary per-token normalization, and residual connections preserve this property. Consequently, their composition does too. This gives a proof for the whole transformer by checking its components.
