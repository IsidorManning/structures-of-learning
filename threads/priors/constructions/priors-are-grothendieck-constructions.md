---
id: 202610282309
type: construction
status: active
created: 2026-10-28
---

This is directly related to [[priors-as-triples-of-specification-representations|priors-as-triples-of-specification-representations]]. It seems what I've described in [[../../../field-notes/structural_priors_v0.pdf|structural_priors_v0]] is captured by the theory fibered and indexed categories, and Grothendieck constructions. 

# A breakdown of the abstraction
## Structural priors
Let $\mathcal{C}$ be a locally small category, called our *base category*. We define a prior as a triple $\Pi=(\mathcal{S},X,Y)$ where $X,Y:\mathcal{S}\rightarrow{}\mathcal{C}$ are functors and $\mathcal{S}$ is a small category.

A morphism $(F,a,b):\Pi_{1}\rightarrow{}\Pi_{2}$ consists of a functor $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$ and natural transformations $a:X_{1}\Rightarrow{}X_{2}F$ and $b:Y_{2}F\Rightarrow{}Y_{1}$.

We get a canonical category of priors whose objects are priors $\Pi$ over a fixed base $\mathcal{C}$, and whose morphisms are these prior morphisms. Composition $\Pi_{1}\xrightarrow{(F,a,b)}\Pi_{2}\xrightarrow{(G,c,d)}\Pi_{3}$ is given by:
$$(G,c,d)\circ{}(F,a,b)=(GF,(cF)\circ{}a,b\circ{}(dF)).$$
Identity is given by $(\text{id}_{\mathcal{S}},\text{id}_{X},\text{id}_{Y})$.
## Admissible models
We can consider the set of *admissible models* $\mathcal{H}_{\Pi}=\text{Nat}(X,Y)$. Thus, an admissible model $h$ consists of components $h_{s}:X(s)\rightarrow{}Y(s)$ satisfying, for every $u:s\rightarrow{}t$, the naturality square
$$Y(u)\circ{}h_{s}=h_{t}\circ{}X(u).$$
The prior gives the representations and therefore the compatibility equations. An admissible model is one particular family of maps satisfying those equations. There exists a functor
$$\mathcal{H}:\mathbf{Prior}(\mathcal{C})^{\text{op}}\longrightarrow{}\mathbf{Set}.$$
## Realizations
Let now $\mathcal{C}$ have finite products. Fixing a parameter space $P\in{}\mathcal{C}$, a *realization* of a prior $\Pi$ is a pair $(P,\Phi)$, where $P\in{}\mathcal{C}$, and
$$\Phi:\Delta P\times X\Rightarrow{}Y.$$
A morphism of realizations $r:(Q,\Psi)\rightarrow(P,\Phi)$ is a parameter map $r:Q\to P$ satisfying
$$\Psi=\Phi\circ(\Delta r\times\mathrm{id}_X).$$
It says that the source family is obtained by substituting $r(q)$ into the target family’s parameters. The map $r$ need not be invertible; it may restrict parameters, tie parameters together, or introduce redundant coordinates. There exists a functor
$$\mathcal{R}_{\Pi}:\mathcal{C}^{\text{op}}\longrightarrow{}\mathbf{Set}.$$
This is the analogue of the admissible-model presheaf $\mathcal{H}$, but with the parameter object varying while holding the prior fixed. $\mathcal{H}$ lets the prior itself vary.
# Priors as Grothendieck Constructions
Fix a specification $\mathcal{S}$, and consider the functor category $[\mathcal{S},\mathcal{C}]\times[\mathcal{S},\mathcal{C}]^{\text{op}}$. We will equivalently see that there is a category of priors given by the (contravariant) Grothendieck construction of the the functor $K:\mathbf{Cat}_{\text{sm}}^{\text{op}}\rightarrow{}\mathbf{CAT}$ given by:
$$K(\mathcal{S})=[\mathcal{S},\mathcal{C}]\times[\mathcal{S},\mathcal{C}]^{\text{op}},\quad K(F)=(-\circ{}F,-\circ{}F).$$

To see this. Let's investigate both what the objects and morphisms of $\int K$ are.  

Let $\Pi_{1}=(\mathcal{S}_{1},X_{1},Y_{1})$, $\Pi_{2}=(\mathcal{S}_{2},X_{2},Y_{2})$, and $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$. The objects in $\int K$ are pairs $\binom{\mathcal{S}}{z}$, where $z\in{}K(\mathcal{S})$, which is (by the universal property of the categorical product) equivalent to specifying a pairing $(X,Y)$, where $X\in{}[\mathcal{S},\mathcal{C}]$ and $Y\in{}[\mathcal{S},\mathcal{C}]$, and so we clearly see that an object in $\int K$ is isomorphic to a triple $(\mathcal{S},X,Y)$. 

Next, we consider a morphism in $\int K$, which is again a pair $\binom{F}{F'}$, where $F:\mathcal{S}_{1}\rightarrow{}\mathcal{S}_{2}$ and $F':z_{1}\rightarrow{}K(F)(z_{2})$, for $z_{1}\in{}K(\mathcal{S}_{1})$, $z_{2}\in{}K(\mathcal{S}_{2})$. Using the universal property once again, this is equivalent to a mapping $F':(X_{1},Y_{1})\rightarrow{}K(F)((X_{2},Y_{2}))$. Unpacking this using the definition of $K$, we get that a morphism in $\int K$ consists of $F$ and a single morphism $F':(X_{1},Y_{1})\rightarrow{}(X_{2}F,Y_{2}F)$ in $K(\mathcal{S}_{1})$. To recover the adapters, compute the hom-set in which $F'$ lives:
$$\begin{align}
K(\mathcal{S}_{1})((X_{1},Y_{1}),(X_{2}F,Y_{2}F))&= [\mathcal{S}_{1},\mathcal{C}](X_{1},X_{2}F)\times[\mathcal{S}_{1},\mathcal{C}]^{\text{op}}(Y_{1},Y_{2}F) \\
&=\text{Nat}(X_{1},X_{2}F)\times\text{Nat}(Y_{2}F,Y_{1}).
\end{align}$$
Hence, $F'$ encodes both an input adapter $a:X_{1}\Rightarrow{}X_{2}F$ and an output adapter $b:Y_{2}F\Rightarrow{}Y_{1}$, precisely the prior morphism we described.

Technically, the isomorphism $J:\int K\cong{}\mathbf{Prior}(\mathcal{C})$ that we are using is explicitly described by:
$$J(\mathcal{S},(X,Y))=(\mathcal{S},X,Y),\quad J(F,(a,b^{\text{op}}))=(F,a,b),$$
where $b^{\text{op}}:Y_{1}\rightarrow{}Y_{2}F$ denotes the morphism in the opposite category corresponding to $b:Y_{2}F\rightarrow{}Y_{1}$. The inverse $J^{-1}$ would put the parentheses back and instead interpret $b$ as a morphism in the opposite category. 

Furthermore, $J$ is an isomorphism of categories, rather than merely bijections on objects and morphisms. We can verify this by showing that $J$ satisfies functoriality, and so we will retrieve the identity and composition of prior morphisms we defined. Take a second prior morphism $(G,c,d):\Pi_{2}\rightarrow{}\Pi_{3}$. The assignments defining $J$ can be verified to preserve identities and composition by the definitions of composition in the Grothendieck construction and in $\mathbf{Prior}(\mathcal C)$. Thus, $J$ is a functor:
$$J\big((G,(c,d^{\mathrm{op}}))\circ (F,(a,b^{\mathrm{op}}))\big) = J(G,(c,d^{\mathrm{op}})) \circ J(F,(a,b^{\mathrm{op}})).$$
We've found that they are bijective on objects and morphisms, with inverse obtained by restoring the product-category pairing. Hence  $J$ is an isomorphism of categories.

We technically only need $K$ to be oplax. 

The reason we spend time connecting the seemingly simple (but perhaps initially arbitrary-looking) definition of priors to the theory of both fibered categories and Grothendieck constructions, is because we believe it offers useful perspective. It connects the abstraction to established mathematical literature, while offering two equivalent ways of viewing priors. Moreover, we will see this pattern continue through our abstractions of admissible models and parametric realizations of models.

# Admissible models in the category of elements
A prior specifies which models are admissible. An object of $\mathbf{El}(\mathcal{H})$ specifies a prior together with one particular model admissible for it. This category of elements keeps both pieces of information (both the prior and the set of admissible models) and organizes the comparisons that respect them.

The category $\mathbf{El}(\mathcal{H})$ consists of:
- **Objects:** Pairs $\binom{\Pi}{h}$, where $\Pi$ is a prior and $h\in{}\mathcal{H}_{\Pi}$.
- **Morphisms:** An arrow $m:\binom{\Pi_{1}}{h_{1}}\rightarrow{}\binom{\Pi_{2}}{h_{2}}$ is a prior morphism $m:\Pi_{1}\rightarrow{}\Pi_{2}$ satisfying$$h_{1}=\mathcal{H}(m)(h_{2}).$$Unpacking this in a bit more detail,$$\mathbf{El}(\mathcal{H})((\Pi_{1},h_{1}),(\Pi_{2},h_{2}))=\{(F,a,b):\Pi_{1}\rightarrow{}\Pi_{2}\mid{}h_{1}=b\circ{}(h_{2}F)\circ{}a\}.$$
- **Identity and composition:** Those of the underlying prior morphisms, i.e., the ones in $\mathbf{Prior}(\mathcal{C})$.

The category axioms follow directly from the contravariance theorem I included in the draft's version 0.

The existence of $\mathbf{El}(\mathcal{H})$ does not mean that the construction picks one preferred model for every prior. It contains *all* such choices.

Lastly, there is a projection
$$p:\mathbf{El}(\mathcal{H})\rightarrow{}\mathbf{Prior}(\mathcal{C}),\quad p(\Pi,h)=\Pi,\quad p(m)=m,$$
which forgets which model was specified.

Already here, we get a useful interpretation of a prior morphism: A prior morphism does not automatically give an arrow between every pair of chosen models. It gives an arrow between these particular objects precisely when transporting the chosen target model produces the chosen source model. $\mathcal{H}$ describes how sets of admissible models vary with the prior; $\mathbf{El}(H)$ describes individual admissible models together with the prior under which they are being considered. Its arrows record exact transport between those specified models.

# Realizations
Realizations also form a category of elements. $\mathbf{El}(\mathcal{R}_{\Pi})$ has as objects pairs $\binom{P}{\Phi}$, $\Phi\in{}\mathcal{R}_{\Pi}(P)$, where $P\in{}\mathcal{C}$ is some parameter object. A morphism in $\mathbf{El}(\mathcal{R}_{\Pi})$ aligns exactly with the morphism defined above for realizations. So we actually have
$$\mathbf{El}(\mathcal{R}_{\Pi})\cong{}\mathbf{Real}_{\mathcal{C}}(\Pi).$$
A perhaps useful thing to notice here is that once the target family and the parameter substitution are specified, the resulting source family is determined exactly. It does not say that there is at most one morphism between two realizations.

The category of realizations is supposed to record exact factorization of one family through another, restrictions, parameter tying, and redundant parameterizations, and parameter symmetries preserving the realized behavior.

There is a connection to individual models here. Since $\Delta1\times X\cong{}X$, there is a canonical bijection
$$\mathcal{R}_{\Pi}(1)\cong{}\mathcal{H}_{\Pi}.$$
For a parameter value $p:1\rightarrow{}P$, reindexing gives
$$p^{*}\Phi\in{}\mathcal{R}_{\Pi}(1),$$
hence an "individual admissible model". In the category of realizations, this gives $(1,p^{*}\Phi)\xrightarrow{p}(P,\Phi)$. Are there examples of different parameter values that yield the same model while defining different arrows into this family?

# Changing priors and parameters simultaneously
We can let the prior and the parameter object vary together. For a prior morphism $m=(F,a,b):\Pi_1\to\Pi_2$ the family transport is
$$T_m^P(\Phi) = b\circ(\Phi F)\circ(\mathrm{id}_{\Delta P}\times a).$$
It commutes with parameter substitution $r:Q\to P$:
$$r^*(T_m^P\Phi)=T_m^Q(r^*\Phi).$$
Hence the assignment
$$(\Pi,P)\longmapsto\mathcal R_\Pi(P)$$
defines a presheaf
$$\mathfrak{R}: (\operatorname{Prior}(\mathcal C)\times\mathcal C)^{\text{op}} \longrightarrow\mathbf{Set}$$
Its category of elements has objects \((\Pi,P,\Phi)\), and arrows
$$(\Pi_1,Q,\Psi)\longrightarrow(\Pi_2,P,\Phi)$$
given by pairs $(m,r)$ satisfying
$$\Psi=r^*(T_m^P\Phi).$$
