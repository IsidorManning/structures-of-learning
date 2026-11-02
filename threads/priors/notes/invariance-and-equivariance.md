---
id: N-202610170003
type: construction
status: active
created: 2026-10-17
---

A core part of the definition of the prior is that the input and output representation of the prior is part of the prior itself. This means morphisms of priors are not just morphisms between prior specifications, but between prior representations as well. Let $\Pi_{\mathbb{L}G}:=(\mathbb{L}^\mathrm{act}_G,X,Y)$ be as in \Cref{eg:lawvere-bg-equivalence}. Next, consider a second prior $\Pi_{\mathbb{L}G}'=(\mathbb{L}^\mathrm{act}_G,X,T)$ where $T:\mathcal{\mathbb{L}}_G^\mathrm{act}\to \mathbf{Set}$ is a \enquote{trivial} output functor defined as:
$$\begin{aligned}
    T(1)&:=\R^n,\\
    T(s_g)&:=\id _{\mathbb{R}^n}.
\end{aligned}$$
Functoriality of $T$ holds since:
$$\begin{aligned}
    T(s_g\circ s_h)&=X(s_{gh})=\id _{\mathbb{R}^n}=\id _{\mathbb{R}^n}\circ \id_{\mathbb{R}^n}=T(s_g)\circ T(s_h),\\
    T(\id_1)&=T(s_e)=\id_{\mathbb{R}^n}.
\end{aligned}$$
$\mathcal{H}_{\Pi_{\mathbb{L}G}'}$ consists of predictors that satisfy invariance, which, element-wise, after unpacking the naturality square becomes:
$$h_1(g\cdot x)=\id _{\R^n}\circ h(x)=h(x).$$
Now, there exists a morphism from the invariance prior to the equivariance prior, namely
$$\phi:=(\id _\mathcal{S},\id _X,q):\Pi'_{\mathbb{L}G}\to \Pi_{\mathbb{L}G},$$
where $q:T\Rrightarrow Y$ is determined by $q_1:\R^n \to \R^n$, which we define as:
$$q_1(\rho(g)x)=q_1(x).$$
This satisfies naturality:
$$(q_1 \circ \rho_{\R^n}(g))(x)=q_1(\rho_{\R^n}(g)(x))=q_1(x)=\id_{\R^n}\circ q_1(x). $$
By \Cref{thm:contravariance}, $\phi$ induces a contravariant function
$$T_\phi :\mathrm{Nat}(X,T)\longrightarrow \mathrm{Nat}(X,Y),\quad T_\phi(h)=q \circ (h\id _{\mathcal{S}})\circ \id _X=q\circ h.$$
This means prior morphisms can express output postprocessing, and here an equivariant predictor is turned into an invariant one by an invariant readout $q$. To take it down one more level of abstraction, let $G=\{e,\sigma\}$ act on $\R^2$ by swapping coordinates. That is, $\sigma(x_1,x_2):=(x_2,x_1)$ and $\rho(g)=\sigma$. We can for example choose $q(y_1,y_2)=y_1+y_2$, which is invariant because
$$q(\sigma(y_1,y_2))=q(y_2,y_1)=y_2+y_1=q(y_1,y_2).$$
Now, consider a neural network $h:\R^2 \to \R$ that respects this specific instance of $\Pi_{\mathbb{L}G}$. Then, for $f:=q\circ h : \R^2 \to \R$,
$$\begin{aligned}
    f(\sigma x)&=q(h(\sigma x))\\
    &= q(\sigma h (x))\\
    &= q(h(x))\\
    &= f(x).
\end{aligned}$$
So $f$ is invariant.

This highlights the semantic content of the prior morphism; a morphism from the equivariance prior $\Pi_{\mathbb{L}G}$ to the invariance prior $\Pi'_{\mathbb{L}G}$ induces a contravariant function which maps any equivariant model to its invariant model. The distinction between prior morphism and the induced admissible model morphism is important to note here.

The prior morphism $\phi$ in \Cref{eg:group-invariance-lawvere} should not be misinterpreted as saying that \enquote{all equivariant models are invariant}, which isn't true. Instead, it should be interpreted as saying that every equivariant predictor $h$ can be transformed into an invariant predictor $f$, provided we have chosen an invariant output map $q$, by precomposing with $q$.