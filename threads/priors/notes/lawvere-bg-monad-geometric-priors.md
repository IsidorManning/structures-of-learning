---
id: N-202610162357
type: note
status: active
created: 2026-10-16
---

In [[../../../literature/nye-2025-categorical-construction|nye-2025-categorical-construction]], group equivariance is studied logically using first-order logic 

Fix a group $G$ and take our base category to be $\mathcal{C}=\mathbf{Set}$. Consider the prior
$$\Pi_{\mathbb{L}G}:=(\mathbb{L}^\mathrm{act}_G,X_{1},Y_{1}),$$
with the prior specification consisting of the Lawvere theory of actions of $G$, denoted $\mathbb{L}^\mathrm{act}_G$. This is the algebraic theory generated freely by the following operations and axioms:
$$    \Sigma = \{s_g : 1 \to 1 \quad \forall g \in G\}, \quad 
    E = \left\{ 
        \begin{aligned}
            s_g \circ s_h &= s_{gh} & \forall g,h \in G \\
            s_e &= \text{id}_1 & e\in G
        \end{aligned} 
    \right\}.$$
Then,
$$\mathbb{L}_{G}^{\mathrm{act}}=\mathrm{Free}_\times (\Sigma) / \sim_{E}$$
The input and output adapters $X_1,Y_1:\mathbb{L}_G^\mathrm{act}\to\mathbf{Set}$ are then technically algebras of $\mathbb{L}_{G}^\mathrm{act}$, defined as:
$$\begin{aligned}
    X_1(1)&:=\mathbb{R}^m,&Y_1(1)&:=\mathbb{R}^n,\\
    X_1(s_g)&:= \rho _\mathbb{R}^n(g),& Y_2(s_g)&:= \rho _\mathbb{R}^m(g).
\end{aligned}$$
We can prove functoriality of $X$ by using the axioms of the algebraic theory and the axioms of a group action $\rho:\mathbb{R^n}\to \mathbb{R}^n$:
$$\begin{aligned}
    X(s_g\circ s_h)&=X(s_{gh})=\rho_{\mathbb{R}^n}(gh)=\rho_{\mathbb{R}^n}(g)\circ \rho_{\mathbb{R}^n}(h)=X(s_g)\circ X(s_h),\\
    X(\mathrm{id}_1)&=X(s_e)=\rho_{\mathbb{R}^n}(e)=\mathrm{id} _\mathbb{R}.
\end{aligned}$$
The prior $\Pi_{\mathbb{L}G}$ is not very interesting to consider in isolation, but we note that $\mathcal{H}_{\Pi_{\mathbb{L}G}}$ describes the set of equivariant models. In this case, since Lawvere theories have finite products, $n\cong 1^n$, and since algebras $X$ and $Y$ are product-preserving, $X(n)\cong X(1^n)=X(1)^n$. Likewise for $Y$. Thus, $\mathcal{H}_{\Pi_{\mathbb{L}G}}$ is the set of predictors $\set{h_1:X(1)\to Y(1)}$ such that:
% https://q.uiver.app/#q=WzAsOSxbNCwwLCJcXG1hdGhiYntSfV5tIl0sWzYsMCwiXFxtYXRoYmJ7Un1ebSJdLFswLDAsIlgoMSkiXSxbMiwwLCJYKDEpIl0sWzIsMiwiWSgxKSJdLFswLDIsIlkoMSkiXSxbMywxLCI9Il0sWzQsMiwiXFxtYXRoYmJ7Un1ebiJdLFs2LDIsIlxcbWF0aGJie1J9Xm4iXSxbMCwxLCJcXHJob197XFxtYXRoYmJ7Un1ebX0oZykiXSxbMiwzLCJYKHNfZykiXSxbMiw1LCJoXzEiLDJdLFszLDQsImhfMSJdLFs1LDQsIlkoc19nKSIsMl0sWzcsOCwiXFxyaG9fe1xcbWF0aGJie1J9Xm19KGcpIl0sWzAsNywiaF8xIiwyXSxbMSw4LCJoXzEiXV0=
\[\begin{tikzcd}
	{X(1)} && {X(1)} && {\mathbb{R}^m} && {\mathbb{R}^m} \\
	&&& {=} \\
	{Y(1)} && {Y(1)} && {\mathbb{R}^n} && {\mathbb{R}^n}
	\arrow["{X(s_g)}", from=1-1, to=1-3]
	\arrow["{h_1}"', from=1-1, to=3-1]
	\arrow["{h_1}", from=1-3, to=3-3]
	\arrow["{\rho_{\mathbb{R}^m}(g)}", from=1-5, to=1-7]
	\arrow["{h_1}"', from=1-5, to=3-5]
	\arrow["{h_1}", from=1-7, to=3-7]
	\arrow["{Y(s_g)}"', from=3-1, to=3-3]
	\arrow["{\rho_{\mathbb{R}^m}(g)}", from=3-5, to=3-7]
\end{tikzcd}\]
Unpacking this element-wise yields group equivariance:
$$h_1(g\cdot x)=g\cdot h_1(x).$$
So $\mathcal{H}_{\Pi_{\mathbb{L}G}}$ really describes the set of models that respect the prior.

Using Lawvere theories is certainly not the only way to mathematically represent groups. In [[../../../literature/maruyama-2025-categorical-equivariant|maruyama-2025-categorical-equivariant]], the same notion of geometric priors is expressed using the one-object category $BG$. Fix a group $G$, then $BG$ consists of one object $G$ with morphisms $s_g:G\to G$ for each $g\in G$, with the axioms of a group quotiented out. A functor $X:BG\to{}\mathcal{C}$ then specifies an object $X\in{}\mathcal{C}$ together with an endomorphism $g_{*}:X\to{}X$ for all $g\in{}G$. Functoriality of $X$ gives the same two conditions we've seen: $h_{*}g_{*}=(hg)_{*}$ for all $g,h\in{}\mathcal{C}$ and $e_{*}=\text{id}_{X}$ where $e\in{}G$ is the identity element. The functor $X$ defines an action of $G$ on $X$. Fix a group $G$ and let $BG$ be its one-object category representation. Then, we can describe a geometric prior; consider two spaces $A,B\in \mathcal{C}$ and let $\rho_A:G\to \mathrm{Aut}(A)$ and $\rho_B:G\to \mathrm{Aut}(B)$ describe group actions of $G$ on $A$ and $B$, respectively. These actions induce two functors
$$\begin{aligned}
    A_G:BG\to \mathcal{C},&\quad A_G(G)=A,&\quad A_G(s_g)=\rho_A(g),\\
    B_G:BG\to \mathcal{C},&\quad B_G(G)=B,&\quad B_G(s_g)=\rho_B(g), 
\end{aligned}$$
Thus, we get a prior $\Pi_{BG}=(BG, A_G,B_G)$. Then, an element of $\mathcal{H}_{\Pi_{BG}}$ has one component $h:A\to B$, whose naturality equations are precisely equivariance. There exists a functor $J:BG\to \mathbb{L}_G^{\mathrm{act}}$ defined by $*\mapsto1$ and $g\mapsto s_g$. Because $Xj=A_G$ and $Bj=B_G$, we get a prior morphism:
$$m_j=(j,\mathrm{id},\mathrm{id} ):\Pi_{BG} \to \Pi_{\mathbb{L}_G^{\mathrm{act}}}.$$
Its induced map on admissible models is the restriction:
$$T_{m_j} : \mathrm{Nat}(X,Y)\longrightarrow \mathrm{Nat}(A_G,B_G),\quad h \mapsto h_1.$$
However, this restriction is bijective. Therefore, $\mathrm{Nat}(X,Y)\cong \mathrm{Nat}(A_G,B_G)$, yet the specification categories themselves are not isomorphic! A category isomorphic to a one-object category has only one isomorphism class of objects. But a Lawvere theory has objects $0$ and $1$ that are not isomorphic. But the priors $\Pi_{BG}$ and $\Pi_{\mathbb{L}_G^{\mathrm{act}}}$ are equivalent by presentation.