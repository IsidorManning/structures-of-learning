---
id: N-202610170004
type: construction
status: active
created: 2026-10-17
---

Building on the work in \citet[Corollary 2]{maruyama2025categoricalequivariantdeeplearning}, we ask whether there exists a useful prior morphism between $\Pi_{BG}$ and a certain \textit{groupoid prior} $\Pi_{\mathcal{G}}$. Let $\mathcal{G}$ be a groupoid. Then the groupoid prior studied is $\Pi_\mathcal{G}=(\mathcal{G}^{op},X,Y)$ over $\mathbf{Top}$. To construct the prior morphism we are interested in, choose an object $s\in \mathcal{G}$, and let $H=\mathrm{Hom}_{\mathcal{G}}(s)$ be its isotropy group. Then, there is an inclusion functor $i:BH\hookrightarrow \mathcal{G}$ with $*\mapsto s$ and each group element to its corresponding loop. Define $\Pi_{BH}=(BH,Xi,Yi)$, then we immediately obtain a prior morphism $(i,\id,\id):\Pi_{BH}\to \Pi_{\mathcal{G}}$. The action on admissible models maps $h\mapsto h_s$. For a connected groupoid, we get an equivalence of priors. There would exist arrows
$$t_a:s\to a,\quad t_s=\id _s.$$
Now, we can define a prior morphism in the other direction:
$$r:\mathcal{G}\to BH,\quad r(u)=t_a^{-1}ut_b,\quad u:b\to a.$$
Then,
$$n=(r,\alpha,\beta):\Pi_{\mathcal{G}}\to \Pi_{BH}$$
exists with
$$\alpha_a=Xi(t_a^{-1}),\quad \beta_a=Yi(t_a).$$
Then, its induced map on admissible models is
$$h_a=Y(t_a)\circ f \circ X(t_a)^{-1}.$$
Thus we have prior morphisms in both directions whose induced maps on admissible models are inverse, so
$$\Pi_\mathcal{G}=\Pi_{BH}.$$
Here we see that models respecting the groupoid prior gives an ordinary $H$-equivariant model by evaluation at $s$. 

\begin{comment}
    \begin{example}
    Let $\mathcal{G}_{\mathrm{graph}}$ be a groupoid of finite typed graphs and type-preserving graph isomorphisms. Use a collection of labels of graphs with vertices drawn from $\N$. Define $\Pi_{\mathrm{graph}}=(\mathcal{G}_{\mathrm{graph}},X,Y)$ with $X(G)=(\R^d)^{V(G)}$, $Y(G)=\R$, where the input contains code features. For an isomorphism $\phi:G\to H$, $(X(\phi)x)_{\phi(v)}=h_G(x)$. For a scalar quantity attatched to each node, take $Y(G)=\R^{V(G)}$, with $Y(\phi)$ reindexing the outputs. 
    \end{example}
\end{comment}
