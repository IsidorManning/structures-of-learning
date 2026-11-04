# Priors in Deep Learning: Empirical Forms, Realizations, and Their Relation to Generalization

**A literature survey and research-program memo for _Structures of Learning_**  
**Date:** 4 September 2026

## Executive conclusion

The empirical literature does not support a single established meaning of **prior**. At least three traditions use the word differently:

1. **Bayesian prior:** a probability measure on parameters, functions, latent variables, structures, or hyperparameters.
2. **Inductive bias:** any property of the complete learning procedure that makes some predictors more accessible or likely than others.
3. **Prior knowledge / structural prior:** task-relevant information supplied independently of the target training sample and integrated into data, architecture, objective, optimization, or inference.

There is nevertheless a common empirical core:

> A prior is an ex ante asymmetry among hypotheses that the observed target-training data alone do not determine.

That asymmetry may remove hypotheses, rank them, assign them probability, make some easier to reach, change what observations are shown, or reject outputs. Consequently, **parameter tying is a special case, not the essence**. It is one mechanism for making a parameterization land inside a function class satisfying an equality such as equivariance.

The most important distinction for the proposed research program is:

> **Prior specification ≠ realization mechanism ≠ induced learning bias ≠ prior satisfaction ≠ generalization.**

The literature repeatedly shows that the same semantic prior can be realized through different mechanisms with different optimization and generalization behavior. Conversely, one architecture normally bundles many priors. There is no task-independent theorem of the form “respecting a prior implies generalization”: even a constant function can satisfy many invariances. Generalization depends on the prior's alignment with the target rule, the realization, the learning dynamics, the data regime, the evaluation shift, and the resource budget.

This leads to a categorical recommendation. Lawvere theories and finitary monads form a good **local doctrine for exact finitary equational priors**. They do not cover the empirical field of priors: inequalities, approximate laws, probability measures, conditional independence, causal interventions, topology, differential constraints, global properties, implicit optimizer preferences, learned priors, and post-hoc certification all fall outside or require substantial additional structure. Moreover, a Lawvere theory is a specification and an Eilenberg–Moore algebra is a model; identifying the “category of priors” with a category of algebras conflates these levels.

A better first abstraction is an indexed **specification–realization–learning** framework:

- a heterogeneous category or doctrine of prior specifications;
- a satisfaction/violation semantics for predictors, distributions, or trajectories;
- a fiber of realizations over each specification;
- translations of specifications inducing contravariant reduct functors between realization fibers;
- a separate category of complete learning systems—data, parameterization, objective, update rule, and inference—where lenses/optics can express learning dynamics;
- a graded notion of respect and an empirical generalization functional, rather than treating respect and generalization as identical.

The repository's proposed presheaf

\[
\mathrm{Real}:\mathrm{Prior}^{op}\to \mathbf{Cat}
\]

is therefore directionally right for exact constraints. The main revision is to make `Prior` a category of **specifications/theories**, not their algebras, and to treat this construction as one doctrine inside a broader indexed family rather than the category of all priors.

---

## 1. Scope and method

This survey is organized around the questions in the `structures-of-learning` repository, especially the notes on empirical forms of priors, categories and morphisms of priors, prior–architecture relations, mixed priors, presheaves of realizations, and the prior–generalization relation.

The emphasis is empirical and operational:

- What semantic content is called a prior?
- What object is constrained or preferred?
- Where is the prior integrated into a learning system?
- How strongly is it imposed?
- What would count as “respecting” it?
- What evidence connects it to generalization?
- Which cases do finitary algebraic theories capture or miss?

The literature is too large for an exhaustive paper-by-paper bibliography. The goal here is comprehensive coverage of **forms and mechanisms**, with representative primary papers, major surveys, constructive results, and important negative results.

Two broad surveys are especially useful points of orientation. Von Rueden et al. classify prior knowledge by **source**, **representation**, and **integration point**, with representations including algebraic and differential equations, simulations, spatial invariances, logic, knowledge graphs, probabilistic relations, and human feedback; integration occurs in data, hypothesis sets, learning algorithms, or final hypotheses ([von Rueden et al., 2021](https://arxiv.org/abs/1903.12394)). Fortuin surveys the much narrower but mathematically precise Bayesian meaning of prior, including weight-space, function-space, hierarchical, and learned priors ([Fortuin, 2022](https://arxiv.org/abs/2105.06868)). Their nonmatching taxonomies are themselves evidence that there is no consensus object called “the prior.”

---

## 2. Terminology: what should and should not be identified

### 2.1 Bayesian prior

In Bayesian learning, a prior is a measure such as \(p(\theta)\), \(p(f)\), or \(p(z)\), combined with a likelihood. It assigns relative mass, not merely admissibility. A full-support Gaussian prior does not remove hypotheses at all; it ranks regions of parameter space. In neural networks, apparently weak parameter priors may induce highly structured function-space priors, and different parameterizations produce different function priors. This is why “prior = subset of architectures” cannot cover even the canonical probabilistic usage.

### 2.2 Inductive bias

Inductive bias is broader: it is the bias of the complete learning rule toward some generalizations over others. It can arise from architecture, parameterization, initialization, loss, optimizer, batching, stopping time, augmentation, or pretraining. Gradient descent on separable logistic regression, for example, converges in direction to a max-margin solution without an explicit regularizer ([Soudry et al., 2018](https://arxiv.org/abs/1710.10345)). ReLU networks also exhibit a frequency preference toward lower-frequency functions ([Rahaman et al., 2019](https://arxiv.org/abs/1806.08734)). These are priors in the loose empirical sense, but they are not explicit specifications that the model must satisfy.

### 2.3 Prior knowledge / structural prior

In informed or physics-informed learning, “prior” often means task-relevant knowledge that exists independently of the target sample and is explicitly integrated. It can be a PDE, a symmetry group, a causal assumption, a monotonicity requirement, a graph, a simulator, or a logical sentence. The knowledge may be correct, approximate, local, conditional, or normative.

### 2.4 Constraint

A constraint is one way to express or realize a prior. Constraints can be:

- equalities, inequalities, or logical formulas;
- local or global;
- hard or soft;
- constraints on weights, functions, distributions, outputs, or trajectories;
- enforced by construction, optimization, projection, or certification.

A probability measure, a data-augmentation distribution, or an implicit optimizer preference need not be naturally described as a constraint. Therefore **prior** should not be defined as **restriction** if the intended object is empirically broad.

### 2.5 Architecture

An architecture is a parameterized computational family, not normally a single prior. A CNN simultaneously introduces locality, translation-related weight sharing, hierarchical composition, receptive-field growth, and a particular parameterization and optimization geometry. A transformer introduces content-dependent aggregation, shared tokenwise maps, permutation equivariance in the absence of positional information, and—depending on masks and positions—temporal or spatial assumptions. Architecture is best treated as a **realization site** where multiple priors may be compiled.

### 2.6 Generalization

Generalization is performance on a specified distribution or family of environments not used to fit the model. It is not satisfaction. A predictor may respect a symmetry and be useless; a predictor may violate an approximate symmetry yet perform better because the task is only partially symmetric. “Does a prior improve generalization?” is incomplete without specifying:

- the target distribution or OOD family;
- data size and sampling;
- model and compute budget;
- prior strength and misspecification;
- the realization mechanism;
- optimization and stopping;
- the relevant metric: error, calibration, robustness, sample efficiency, compute efficiency, or extrapolation.

---

## 3. An operational decomposition

Represent a learning system schematically as

$$\mathcal S=(\mathcal D,\;\Phi:\Theta\to\mathcal F,\;\mu_0,\;J,\;U,\;Q),$$

where:

- \(\mathcal D\) is the data pipeline or experiment design;
- \(\Phi\) is the architecture/parameterization into a predictor space \(\mathcal F\);
- \(\mu_0\) is an initialization or parameter prior;
- \(J\) is the training objective;
- \(U\) is the optimizer/update dynamics;
- \(Q\) is inference, decoding, projection, or post-processing.

Training on a sample induces a distribution—or, in a deterministic idealization, a point—in predictor space. That induced distribution is the empirical **bias of the entire system**.

Define a prior specification minimally by

\[
P=(\text{scope},\;V_P,\;\varepsilon,\;\text{provenance}),
\]

where \(V_P\) is a violation functional or, in the exact case, a satisfaction relation. Its scope may be predictors, representations, distributions, parameters, outputs, or state trajectories. A realization \(\rho\) maps this specification into interventions on one or more components of \(\mathcal S\).

This yields five objects that should not be collapsed:

| Level | Question | Example |
|---|---|---|
| Semantic prior \(P\) | What is believed or desired? | Rotation equivariance |
| Realization \(\rho\) | How is it integrated? | Group convolution, augmentation, feature averaging, canonicalization, or penalty |
| Induced bias \(B_{\mathcal S}\) | Which solutions become likely/easy? | Greater mass on approximately equivariant, low-norm functions |
| Respect criterion | Did the model/process satisfy the prior? | Worst-case equivariance defect below \(\varepsilon\) |
| Generalization effect | Did this help on a specified target? | Lower test risk at fixed data and compute |

This decomposition is the main empirical abstraction recommended by the survey.

---

## 4. The empirical forms of priors

The following table classifies **semantic content**, separately from enforcement mechanisms.

| Family                                 | Typical semantic statement                                                        | Object scoped by the prior                                    | Representative realizations                                                                                | Empirical lesson                                                                                                                | Fit to finitary equational theories                                                                                             |
| -------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Symmetry and equivariance              | \(f(gx)=g'f(x)\); permutation invariance                                          | Functions/representations                                     | Weight sharing, group convolution, averaging, augmentation, canonicalization                               | Strong sample/compute gains when correct; full symmetry can be too rigid                                                        | Good for exact action/homomorphism structure, but approximate/partial/input-dependent symmetry needs enrichment                 |
| Algebraic and compositional laws       | Associativity, distributivity, conservation under composition                     | Operations/circuits                                           | Shared modules, typed composition, constrained parameters, symbolic modules                                | Useful for systematic/combinatorial generalization when computation aligns with task                                            | Core territory for Lawvere theories, PROPs, operads, monads                                                                     |
| Logical and rule priors                | \(A\land B\Rightarrow C\); output satisfies formula                               | Outputs, latent assignments, proof traces                     | Semantic loss, posterior constraints, differentiable logic, neuro-symbolic programs, verified architecture | Often improves weak/semi-supervised structured prediction; exactness and trainability trade off                                 | Equational fragments fit; implication, quantification, proof theory, approximate truth, and probability need richer doctrines   |
| Relational, graph, locality, hierarchy | Objects interact through relations/local neighborhoods                            | Computation graph/representations                             | GNN message passing, convolutions, sparse attention, modular networks                                      | Alignment with dynamic programming and relational structure can improve sample complexity and combinatorial transfer            | Often multi-sorted/multi-output; PROPs, operads, sketches, or presheaf models may be more natural                               |
| Shape, order, and inequality           | Monotone, convex, Lipschitz, positive, bounded                                    | Functions/parameters/Jacobians                                | Sign constraints, lattice layers, spectral normalization, penalties, certification                         | Guarantees can improve trust and extrapolation; hard constraints can reduce approximation quality                               | Not ordinary equational algebra; needs ordered/enriched logic, cones, or inequality doctrines                                   |
| Physical/differential/dynamical        | PDE residual zero; Hamiltonian flow; conserved energy                             | Functions and trajectories                                    | PINN loss, Hamiltonian/Lagrangian parameterization, symplectic layers, differentiable solvers              | Correct structure can improve data efficiency and long-horizon behavior; soft residuals can create severe optimization problems | Differential/global/trajectory structure exceeds finitary Set-based theories                                                    |
| Probabilistic and independence         | Factorization, exchangeability, \(X\perp Y\mid Z\), calibrated uncertainty        | Measures, kernels, posteriors                                 | Bayesian priors, graphical models, posterior regularization, stochastic programs                           | Prior and likelihood choices materially affect accuracy/calibration; “vague” weight priors are not neutral                      | Probability monads alone do not express all conditional-independence semantics; Markov categories/statistical models are closer |
| Causal/environmental                   | Same mechanism/classifier across interventions or environments                    | Representations/predictors across environments                | IRM objectives, invariant prediction, causal graph restrictions                                            | Can target OOD generalization, but practical surrogates may fail to capture intended invariance                                 | Requires environment/intervention indexing and asymmetry of causal structure, not only equations on one carrier                 |
| Topological/global                     | Fixed Betti numbers, connectivity, no holes                                       | Whole outputs/data manifolds                                  | Persistent-homology losses/layers, projection                                                              | Especially useful in label-scarce difficult segmentation                                                                        | Global and often non-finitary; not naturally a finitary term equation                                                           |
| Simplicity/compression                 | Sparse, low-rank, low norm, short description, smooth/low frequency               | Parameters/functions/circuits                                 | Weight decay, \(\ell_1\), nuclear norm, pruning, architectural bottlenecks, optimizer bias                 | Central in interpolation and grokking; the relevant simplicity measure depends on parameterization and dynamics                 | Usually a preorder/energy, not satisfaction of algebraic equations                                                              |
| Algorithmic, temporal, and resource    | Recurrent state, causality, bounded memory, iterative algorithm, locality in time | Programs/state machines/traces                                | RNNs, causal masks, recurrence, neural executors, halting/iteration mechanisms                             | Computation structure can align with algorithms and extrapolate in size or steps, but learned execution is brittle              | Monads/automata can model syntax; performance depends on dynamics, resources, and training distribution                         |
| Learned/meta/pretraining priors        | Tasks share representations, initialization, or latent structure                  | Initialization, features, hyperparameters, task distributions | Pretraining, MAML, hierarchical Bayes, empirical Bayes                                                     | Prior is learned from previous tasks and can yield few-shot gains; transfer can also be negative                                | Naturally higher-level/indexed: a learner maps task distributions to learning systems                                           |
| Normative/safety/fairness priors       | Outputs must satisfy policy, fairness, or safety rules                            | Outputs or decisions                                          | Constrained optimization, shields, rejection, certification, human feedback                                | Conformity may be the target even when predictive accuracy falls                                                                | A specification doctrine can include these, but they should not be confused with descriptive laws of the data                   |

### 4.1 Symmetry, invariance, equivariance, and exchangeability

This is the cleanest success case for “prior → architecture.” Group-equivariant CNNs use structured weight sharing so that layers commute with group actions; the original G-CNN paper reported improved results on rotated MNIST and CIFAR-10 ([Cohen & Welling, 2016](https://arxiv.org/abs/1602.07576)). Deep Sets characterizes a broad class of permutation-invariant set functions and derives a corresponding architecture ([Zaheer et al., 2017](https://arxiv.org/abs/1703.06114)). Geometric Deep Learning unifies many such constructions around symmetry, locality, and scale separation ([Bronstein et al., 2021](https://arxiv.org/abs/2104.13478)).

However, symmetry also provides the clearest evidence that **the semantic prior does not determine a unique architecture**:

- Lyle et al. compare data augmentation and feature averaging for the same invariance, prove different risk/variance properties, and show that augmentation can fail to learn invariance outside the training distribution ([Lyle et al., 2020](https://arxiv.org/abs/2005.00178)).
- Learned canonicalization can attach an equivariance-inducing front end to an ordinary backbone and be competitive while faster ([Kaba et al., 2023](https://proceedings.mlr.press/v202/kaba23a.html)).
- At scale, equivariant models remain more data- and compute-efficient at tested budgets, while non-equivariant models with augmentation can close the data-efficiency gap given enough epochs ([Brehmer et al., 2025](https://arxiv.org/abs/2410.23179)).
- Full group equivariance can be misspecified for data with only partial or input-dependent symmetry; variational partial G-CNNs explicitly learn how much symmetry applies per instance ([Kim et al., 2024](https://proceedings.mlr.press/v235/kim24q.html)).
- Theory makes the approximation–generalization tradeoff explicit when either data or model is only approximately equivariant ([Petrache & Trivedi, 2023](https://arxiv.org/abs/2305.17592)).

Empirical conclusion: exact equivariance is a hard support restriction when built into every layer, but augmentation changes the empirical risk, averaging changes inference, and canonicalization changes representation. They may share a semantic specification while inducing different hypothesis accessibility and training dynamics.

### 4.2 Algebraic, logical, and compositional priors

Logical priors appear empirically in several non-equivalent forms:

- **Loss compilation:** Semantic Loss translates a propositional formula over outputs into a differentiable penalty and improves semi-supervised classification and structured prediction of rankings and paths ([Xu et al., 2018](https://proceedings.mlr.press/v80/xu18h.html)).
- **General logical penalties and queries:** DL2 compiles declarative constraints into losses and applies them in supervised, semi-supervised, and unsupervised settings ([Fischer et al., 2019](https://proceedings.mlr.press/v97/fischer19a.html)).
- **Distributional constraints:** Posterior regularization constrains posterior moments in expectation and covers bijectivity, symmetry, and group sparsity while separating model complexity from constraint complexity ([Ganchev et al., 2010](https://jmlr.org/papers/v11/ganchev10a.html)).
- **Probabilistic programs:** DeepProbLog combines neural predicates with probabilistic logic programs and trains the composite end to end ([Manhaeve et al., 2018](https://arxiv.org/abs/1805.10872)).
- **Many-valued first-order semantics:** Logic Tensor Networks use differentiable fuzzy semantics for relational and semi-supervised tasks ([Badreddine et al., 2022](https://arxiv.org/abs/2012.13635)).
- **Architectural construction:** Nye proposes compiling finitary logical theories, represented as Lawvere theories, into parametric architectures ([Nye, 2025](https://arxiv.org/abs/2508.11647)).

These approaches disagree on what “respect” means: zero loss, high expected satisfaction, valid symbolic execution, asymptotic Boolean correctness, or exact architectural closure. Treating them all as algebras for a finitary monad erases distinctions that matter empirically.

Compositional and algorithmic alignment is a related but distinct family. Graph Networks impose entity–relation structure and are motivated by combinatorial generalization ([Battaglia et al., 2018](https://arxiv.org/abs/1806.01261)). Xu et al. formalize alignment between a network's computation graph and an algorithmic solution and derive sample-complexity improvements with stronger alignment, supported on reasoning tasks connected to dynamic programming ([Xu et al., 2020](https://arxiv.org/abs/1905.13211)). Here the prior is not simply an equation that every forward map satisfies; it is a factorization of computation into reusable steps.

### 4.3 Shape constraints: monotonicity, convexity, positivity, and Lipschitzness

Shape priors are decisive counterexamples to the claim that the empirical prior space is exhausted by finitary equational theories.

- Input Convex Neural Networks constrain parameters so that the output is convex in selected inputs and enable optimization-based inference; the paper reports improvements in structured prediction, image completion, and reinforcement learning ([Amos et al., 2017](https://proceedings.mlr.press/v70/amos17b.html)).
- Deep Lattice Networks enforce partial monotonicity by constrained calibrators, lattices, and linear embeddings and obtain competitive classification and regression performance with guarantees ([You et al., 2017](https://arxiv.org/abs/1709.06680)).
- Certified Monotonic Neural Networks instead train relatively general piecewise-linear networks with heuristic regularization and then use mixed-integer verification, reporting more accurate approximation than deep lattices ([Liu et al., 2020](https://arxiv.org/abs/2011.10219)).

The same monotonicity prior can therefore be respected by construction, encouraged during training, or certified at the end. The set of monotone functions is closed under some operations, but the defining condition is order-theoretic and infinitary over the input domain. Its most natural empirical measure is a worst-case derivative/order violation, not an equation of finitary operations.

### 4.4 Physical, differential, and conservation priors

Physics-informed neural networks add differential-equation residuals and boundary/initial conditions to the loss; the original work frames this as data-efficient approximation with physical laws as prior information ([Raissi et al., 2017](https://arxiv.org/abs/1711.10561)). In contrast, Hamiltonian Neural Networks parameterize a Hamiltonian and derive dynamics from it, obtaining conservation, reversibility, faster training, and better generalization than a generic baseline on selected systems ([Greydanus et al., 2019](https://arxiv.org/abs/1906.01563)). Lagrangian Neural Networks similarly build a Lagrangian form into the learned dynamics ([Cranmer et al., 2020](https://arxiv.org/abs/2003.04630)).

The negative evidence is crucial. Krishnapriyan et al. show that the standard soft PINN residual can make the loss ill-conditioned and fail even when the network is expressive; curriculum regularization and sequence-to-sequence reformulation reduce error by one to two orders of magnitude ([Krishnapriyan et al., 2021](https://arxiv.org/abs/2109.01050)).

This is almost a direct empirical validation of the proposed hierarchy:

\[
\text{same physical prior} \;\longrightarrow\; \text{different embedding in the learning structure} \;\longrightarrow\; \text{different optimization geometry} \;\longrightarrow\; \text{different generalization}.
\]

The prior cannot be studied only as a set of valid functions. The way it enters backpropagation matters.

### 4.5 Probabilistic, independence, and Bayesian priors

Probabilistic priors range from simple parameter distributions to function-space processes, hierarchical models, stochastic-process priors, learned priors, and priors over predictive complexity ([Fortuin, 2022](https://arxiv.org/abs/2105.06868); [Nalisnick et al., 2021](https://proceedings.mlr.press/v130/nalisnick21a.html)). A vague parameter prior is not neutral because architecture and parameterization push it forward to a structured measure on functions. Wilson and Izmailov emphasize function-space effects and marginalization in understanding generalization and double descent ([Wilson & Izmailov, 2020](https://arxiv.org/abs/2002.08791)).

The empirical picture is not that orthodox Bayes automatically gives the best generalization. The “cold posterior” literature finds settings where tempering the posterior improves predictive performance, exposing mismatch among prior, likelihood, data augmentation, and model ([Wenzel et al., 2020](https://proceedings.mlr.press/v119/wenzel20a.html)). Detailed posterior studies likewise show strong interactions among the prior, multimodal posterior geometry, and inference approximation ([Izmailov et al., 2021](https://proceedings.mlr.press/v139/izmailov21a.html)).

Conditional independence is a relation among probability kernels/distributions, not ordinary algebraic equality on deterministic operations. Markov categories were developed precisely to express conditioning, disintegration, conditional independence, sufficiency, and related probabilistic structure abstractly ([Fritz, 2020](https://arxiv.org/abs/1908.07021)). They are a more plausible local categorical home for Nye's informal “probability independence” example than finitary monad algebras alone.

### 4.6 Causal and environmental priors

Invariant Risk Minimization encodes the claim that a representation should admit the same optimal classifier across environments, motivated by causal invariance and OOD generalization ([Arjovsky et al., 2019](https://arxiv.org/abs/1907.02893)). But the practical IRMv1 surrogate can fail to capture even natural invariances and can generalize worse than empirical risk minimization ([Kamath et al., 2021](https://proceedings.mlr.press/v130/kamath21a.html)).

This separates at least four levels:

1. a causal semantic claim about mechanisms or interventions;
2. an environment-indexed invariance criterion;
3. a differentiable surrogate objective;
4. the behavior reached by optimization.

The failure of level 3 to realize level 1 is exactly the kind of “ill-posed prior morphism” problem the categorical program should make visible rather than abstract away.

### 4.7 Topological and global priors

Persistent homology permits losses on global output topology. Clough et al. specify desired Betti numbers and report improvements in difficult 2D and 3D segmentation, including semi-supervised and post-processing settings ([Clough et al., 2020](https://arxiv.org/abs/1910.01877)). A general differentiable topology layer has been used to regularize reconstructions, weights, and generative outputs ([Brüel-Gabrielsson et al., 2020](https://proceedings.mlr.press/v108/gabrielsson20a.html)).

These priors are global, may be discontinuous before relaxation, and can be integrated at the loss, representation, or output stage. They do not resemble a finite family of operations and equations.

### 4.8 Simplicity, sparsity, norms, smoothness, and implicit bias

Modern overparameterized networks can fit random labels and even unstructured inputs, so raw hypothesis-class size does not explain their ordinary generalization ([Zhang et al., 2017](https://arxiv.org/abs/1611.03530)). Generalization changes with model size, data, and even training duration in double-descent regimes ([Nakkiran et al., 2019](https://arxiv.org/abs/1912.02292)). These findings force attention from mere representability to the **ordering and accessibility of interpolating solutions**.

Important examples include:

- explicit \(\ell_2\), \(\ell_1\), group, path, nuclear, or spectral penalties;
- low-rank factorization and bottlenecks;
- architectural locality and sparsity;
- early stopping;
- max-margin bias of gradient descent;
- frequency/spectral bias;
- flatness or robustness to perturbation;
- compression and minimum-description preferences.

Such priors are usually **energies or preorders** on predictors/parameterizations. A hard zero set loses much of their content. Two parameterizations of the same function class can induce different norms and therefore different learned functions.

### 4.9 Data, simulation, augmentation, and self-supervised task design

Data transformations are often implementation mechanisms for semantic priors. Mixup favors approximately linear behavior between samples and empirically improves generalization, robustness, and resistance to corrupt-label memorization ([Zhang et al., 2018](https://arxiv.org/abs/1710.09412)). Data augmentation can be modeled as a Markov process and approximated in kernel settings by feature averaging plus variance regularization ([Dao et al., 2019](https://proceedings.mlr.press/v97/dao19b.html)). In SimCLR, the composition of augmentations is critical because it defines which information the self-supervised task treats as invariant ([Chen et al., 2020](https://arxiv.org/abs/2002.05709)).

This suggests a precise rule: augmentation is not itself the prior. The prior is the semantic assertion that selected transformations preserve task-relevant content; augmentation is a stochastic realization that changes the training distribution and objective.

### 4.10 Learned and transferred priors

Inductive bias can itself be learned from a distribution of tasks. Baxter's inductive-bias-learning framework formalizes learning a hypothesis-space family across tasks ([Baxter, 2000](https://arxiv.org/abs/1106.0245)). MAML learns an initialization from which a few gradient steps generalize on new tasks ([Finn et al., 2017](https://proceedings.mlr.press/v70/finn17a.html)). Pretraining similarly changes the initial function, features, parameter scale, and local geometry available to downstream learning.

This is not a prior independent of all data; it is prior relative to the **current target task**. Any formal definition should therefore index provenance: prior relative to which sample, task, or environment?

---

## 5. How priors are imposed: a mechanism taxonomy

Empirically, “imposition” varies along two independent axes: **where** the learning system is altered and **with what force**.

### 5.1 Integration locus

| Locus | Intervention | Typical examples | What changes mathematically |
|---|---|---|---|
| Data / experiment | Augment, simulate, resample, curate, choose environments, curriculum | Rotations, mixup, PDE collocation, counterfactual environments | Empirical distribution and information available to the learner |
| Representation / preprocessing | Canonicalize, engineer features, quotient inputs | Learned pose canonicalization, invariant descriptors | Map from observations to the model's carrier space |
| Architecture / parameterization | Tie weights, delete edges, restrict signs, use equivariant layers, recurrence, graph message passing | CNN, G-CNN, Deep Sets, ICNN, HNN | Image of \(\Phi:\Theta\to\mathcal F\) and geometry/multiplicity of parameterization |
| Initialization / probabilistic prior | Set \(\mu_0\), pretrained weights, function prior, hyperprior | Gaussian weight prior, pretrained model, MAML initialization | Initial measure and reachable basin structure |
| Objective | Add penalty, semantic loss, PDE residual, contrastive task, robust risk | PINN, DL2, IRM, topology loss | Energy landscape and gradients |
| Update rule | Projection, natural/Riemannian gradient, mirror descent, constrained optimizer, optimizer choice | Projected monotone weights, manifold optimization | Trajectory kernel and invariant sets |
| Inference / output | Average, decode, project, reject, shield, certify | Group averaging, structured decoder, monotonicity certificate | Final map from learned state to prediction and acceptance |

Von Rueden et al.'s four integration stages—data, hypothesis set, learning algorithm, and final hypothesis—are the closest broad empirical consensus ([von Rueden et al., 2021](https://arxiv.org/abs/1903.12394)). Splitting representation, initialization, objective, and update gives the resolution needed for this research program.

### 5.2 Force of imposition

| Force | Operational meaning | Example |
|---|---|---|
| Exact/hard | Every representable predictor satisfies the property | Group-equivariant layer; sign-constrained monotone lattice |
| Feasible-set/constrained | Training is restricted to a valid subset | Projected or manifold optimization |
| Soft/graded | Violations add finite cost | PDE residual; semantic loss; approximate equivariance penalty |
| Probabilistic | Solutions receive different prior mass | Bayesian function prior |
| Stochastic/data-mediated | Training sees samples transformed according to a prior-dependent kernel | Augmentation |
| Implicit | Preference emerges from parameterization and update dynamics | Max-margin or spectral bias |
| Learned/adaptive | Strength/content is estimated from data or per input | Learned canonicalization; partial equivariance; meta-learned initialization |
| Post-hoc/certified | The trained predictor is checked or projected after learning | MILP monotonicity certification; output shield |

These mechanisms are not ordered from “weak” to “strong” in a single way. A soft penalty may induce stronger practical conformity than a nominal hard architecture with discretization error; a certificate may give the strongest terminal guarantee while saying nothing about the training path.

---

## 6. What should “respecting a prior” mean?

There is no single respect relation because priors have different scopes. A useful framework should require authors to state both **scope** and **quantifier**.

### 6.1 Architectural respect

Let \(\mathrm{Sat}(P)\hookrightarrow\mathcal F\) be the predictors satisfying an exact property. The architecture respects \(P\) if its evaluation map factors through the satisfying subspace:

\[
\require{AMScd}
\Phi:\Theta\longrightarrow \mathrm{Sat}(P)\hookrightarrow\mathcal F.
\]

Equivalently, every parameter value is valid. Parameter tying is one way to construct such a factorization; it is not the definition.

### 6.2 Trajectory respect

Let \(M_P\hookrightarrow\Theta\) be a valid parameter subset and let \(U\) be an update. Training respects \(P\) throughout if the update preserves \(M_P\): there exists \(U_P\) such that

\[
i\circ U_P = U\circ(i\times \mathrm{id}).
\]

This is the clean categorical expression of “the prior is respected throughout training.” It says that the update on ambient parameters factors through the constrained state space. Initialization must also land in \(M_P\). In lens language, the learner's backward/update component restricts to a sub-lens or invariant subobject.

### 6.3 Terminal respect

Only the trained predictor must satisfy \(V_P(f_{\theta_T})\le \varepsilon\). Soft penalties, projection, and post-hoc certification often target this weaker notion.

### 6.4 Distributional respect

For Bayesian or stochastic systems, respect may mean

\[
\mathbb E_{f\sim K_{\mathcal S}}[V_P(f)]\le\varepsilon
\quad\text{or}\quad
\Pr[V_P(f)\le\varepsilon]\ge 1-\delta.
\]

Posterior regularization is of this form; it constrains expectations rather than every realization.

### 6.5 Environment-indexed respect

For causal or OOD priors, respect is a relation over a family of environments or interventions, not one function in isolation. For example, a predictor head may be required to remain optimal across all environments after a shared representation.

### 6.6 Approximate respect

Approximate equivariance, PDE residuals, monotonicity defects, and topological losses require a graded violation. The metric itself is part of the prior specification. Average-case defect, worst-case defect, and defect on observed transformations are not equivalent.

### 6.7 Certification versus construction

“Guaranteed by architecture,” “preserved by the optimizer,” and “certified after training” are distinct proof obligations. A satisfactory formal vocabulary should make all three expressible.

---

## 7. Does respecting a prior improve generalization?

### 7.1 The strongest defensible answer

Empirically, aligned priors often improve:

- sample efficiency;
- compute efficiency;
- robustness to transformations encoded by the prior;
- OOD behavior under shifts covered by the prior;
- physical/logical/topological conformity;
- interpretability or certifiability.

But the effect is conditional, not universal. Exact priors introduce an approximation-bias risk under misspecification. Soft priors introduce optimization and tuning problems. Learned priors can overfit the meta-distribution. Implicit priors are difficult to control and may favor the wrong simplicity notion.

### 7.2 Why respect is not sufficient

Let a classification problem be rotation invariant. Every constant classifier is rotation invariant. Hence exact respect alone does not distinguish useful from useless functions. The prior must be:

- **aligned:** the target belongs to or is close to the preferred family;
- **discriminating:** it meaningfully reduces/ranks hypotheses relevant to the data regime;
- **non-degenerate:** it does not make trivial solutions disproportionately easy;
- **compatible with learning:** the realization must not make optimization pathological;
- **matched to evaluation:** the held-out shift must exercise the structure the prior addresses.

### 7.3 Why respect is not necessary

If the true task only approximately respects a symmetry, a slightly non-equivariant model may generalize better. Partial-equivariance results and relaxed spatial sharing are direct examples. A model can also violate a structural prior outside the data support while attaining low target risk.

### 7.4 A comparative generalization functional

For a semantic prior \(P\), realization \(\rho\), base system \(\mathcal S\), sample size \(n\), compute budget \(c\), and evaluation environment family \(\mathcal E\), define

\[
\Delta_G(P,\rho;\mathcal S,n,c,\mathcal E)
=
\mathbb E\left[
R_{\mathcal E}(\widehat f_{\mathcal S})-
R_{\mathcal E}(\widehat f_{\rho(P,\mathcal S)})
\right].
\]

This makes explicit that a generalization benefit is not a property of \(P\) alone. A useful theory should predict the sign and scaling of \(\Delta_G\), together with prior violation and optimization cost.

### 7.5 What the evidence says by mechanism

- **Hard correct symmetry:** usually strong sample-efficiency gains; may remain compute-efficient at scale, but gains can narrow with augmentation and training.
- **Hard misspecified symmetry:** increased approximation error; partial or relaxed symmetry may win.
- **Soft logical/physical priors:** often useful in low-data regimes, but benefits depend heavily on loss scaling and conditioning.
- **Probabilistic priors:** affect calibration and marginalization as well as accuracy; convenient weight priors can be poorly matched.
- **Causal invariance surrogates:** promising target, fragile realization.
- **Global/topological priors:** most useful when ordinary labels underspecify the desired output and the prior is reliable.
- **Implicit simplicity priors:** central in interpolation, but the selected simplicity measure is parameterization- and optimizer-dependent.

---

## 8. Grokking as a prior–learning-structure phenomenon

Grokking is unusually relevant because the architecture already represents both memorizing and generalizing solutions. The transition is therefore not primarily a hard hypothesis-class restriction.

Power et al. observe delayed generalization long after training interpolation and find that smaller datasets require more optimization before generalization ([Power et al., 2022](https://arxiv.org/abs/2201.02177)). Nanda et al. identify a Fourier-based modular-addition circuit and decompose learning into memorization, circuit formation, and cleanup: structured mechanisms grow before memorizing components are removed ([Nanda et al., 2023](https://arxiv.org/abs/2301.05217)). Varma et al. explain grokking through competition between a slowly learned but more norm-efficient generalizing circuit and a memorizing circuit and derive successful predictions including ungrokking and semi-grokking ([Varma et al., 2023](https://arxiv.org/abs/2309.02390)). Later work shows that \(\ell_1\), nuclear-norm, explicit and implicit regularization can induce grokking toward sparse or low-rank properties, and that data selection alone can amplify it ([Junior et al., 2025](https://proceedings.mlr.press/v267/junior25a.html)).

The appropriate concept of prior here is a time-dependent **preference over competing circuits**, induced jointly by parameterization, regularizer, optimizer, dataset, and training duration. A zero-set notion misses the phenomenon. The falsifiable object is closer to an energy/order on mechanisms plus transition dynamics.

A categorical program that includes learning lenses could contribute by distinguishing:

1. the algebraic task structure (e.g. a finite group operation);
2. architectures capable of realizing structured and memorizing circuits;
3. the optimizer/regularizer lens that changes their relative accessibility;
4. the trajectory of a structure-violation or circuit-efficiency observable;
5. the eventual generalization transition.

---

## 9. Assessment of Lawvere theories, monads, PROPs, and Nye

### 9.1 What Lawvere theories capture well

A single-sorted finitary Lawvere theory presents operations of finite arity and equations among terms. Its models are product-preserving functors into a semantic category. Finitary monads on `Set` provide an equivalent style of presentation under standard hypotheses. This is well suited to:

- Boolean, monoid, group, ring, semilattice, and related algebraic laws;
- reuse of operations and equations under composition;
- exact homomorphisms between algebras;
- translations of theories and induced reduct functors;
- free constructions and syntax/semantics separation.

PROPs or colored PROPs improve the fit for typed, multiple-input/multiple-output circuits, tensorial wiring, and conservation/flow structures. Operads fit hierarchical many-to-one composition. These are meaningful extensions, not mere notational alternatives.

### 9.2 What they do not capture without substantial enrichment

Ordinary finitary equational theories do not directly capture:

- inequalities and order constraints;
- approximate equations with a meaningful defect metric;
- probability measures and posterior mass;
- conditional independence and almost-sure equality;
- interventions and environment-indexed causal invariance;
- differential equations over function spaces and whole trajectories;
- global topological properties;
- non-finitary constraints quantified over continuous domains;
- norm, compression, sparsity, and low-rank preferences;
- optimizer-induced accessibility and time-dependent selection;
- certification or output rejection as a realization mode;
- learned/data-dependent prior strength.

Some of these can be handled by enriched, ordered, metric, probabilistic, differential, or higher categorical structures. But “can be encoded after enough enrichment” is not evidence that one base category is the correct empirical abstraction.

### 9.3 The theory/model distinction

If \(T\) is a finitary monad, an Eilenberg–Moore algebra \((A,a:TA\to A)\) is a **model/realization of the algebraic theory**, not the prior specification itself. Thus:

- category of theories/specifications: finitary monads with suitable monad morphisms, or Lawvere theories with interpretations;
- fiber of models for a theory: \(\mathrm{Alg}(T)\) or product-preserving models;
- architecture realization: selected parametric models in an appropriate target;
- learned parameter: a point/distribution/trajectory inside a realization.

This separation aligns closely with the repository's emerging presheaf idea and resolves a central type confusion.

### 9.4 A careful reading of Nye

Nye's paper has the right motivating separation—logical specification should compile to architectural structure—but should presently be read as a research sketch, not an established construction. Several claims are materially stronger than what is shown:

1. A Lawvere theory does not determine a canonical embedding into `Para` without choosing carrier objects and interpretations of operations. Syntax does not by itself select differentiable connectives or parameter spaces.
2. The sigmoid Boolean operations in the paper converge to Boolean truth tables as temperature tends to infinity; at finite temperature they do not exactly satisfy Boolean equations. This conflicts with the simultaneous claim that violations are mathematically impossible during differentiable training.
3. The paper later requires parameter constraints and constrained/Riemannian optimization. Therefore correctness is not obtained from architecture/weight sharing alone.
4. A zero set of algebraic constraints need not be a smooth manifold. The displayed projection formula is not generally the orthogonal projection when constraint gradients are non-orthogonal or dependent; regularity and a Jacobian-based construction are needed.
5. “Every logically constrained network” is narrowed by defining a structurally logical network to be a DAG whose layers already implement the signature and satisfy the axioms. The resulting universality/uniqueness is correspondingly restricted and partly built into the definition.
6. Uniqueness up to reparameterization is too strong without a carefully specified category of implementations; many computational graphs can implement the same algebraic model without being related by an invertible parameter reparameterization.

None of this invalidates the core research direction. It identifies the exact interfaces that need to be made well typed: specification → model → parametric implementation → constraint-preserving learner.

### 9.5 Relation to Categorical Deep Learning

Gavranović et al. propose monads valued in a 2-category of parametric maps as a bridge between architectural constraints and implementations ([Gavranović et al., 2024](https://arxiv.org/abs/2402.15332)). Gavranović's thesis separately develops parametric maps, weighted optics/lenses, differentiation, optimizers, and supervised learning as an end-to-end categorical account ([Gavranović, 2024](https://arxiv.org/abs/2403.13001)).

This offers the ingredients for the user's hierarchy, but not yet the empirical theorem connecting them. The survey suggests using:

- algebraic doctrines for a subset of semantic priors;
- `Para`-like structures for parameterized implementations;
- lenses/optics for update rules and training composition;
- invariant subobjects/factorization to define preservation through training;
- an external statistical risk functional to state generalization predictions.

---

## 10. A broader categorical architecture for the program

### 10.1 Replace one universal category with indexed doctrines

Let \(\mathbf{Doc}\) index prior doctrines:

- equational/algebraic;
- ordered/inequational;
- metric/approximate;
- probabilistic/Markov;
- causal/environmental;
- differential/dynamical;
- topological/global;
- complexity/preference.

Each doctrine \(d\) supplies a category of specifications \(\mathbf{Spec}_d\), a category of semantic models, and a satisfaction or violation relation. Translations between doctrines are allowed when justified, but need not force all priors into the same syntax.

### 10.2 Use an institution-like core

Institution theory abstracts a logical system into signatures, sentences, models, and a satisfaction relation invariant under change of notation ([Goguen & Burstall, 1992](https://dl.acm.org/doi/10.1145/147508.147524)). Its crucial lesson for this program is not that every prior is logic, but that **syntax, models, and satisfaction should be separate objects connected by a satisfaction condition**.

For a specification \(P\), define a category \(\mathrm{Mod}(P)\) or \(\mathrm{Real}(P)\). A specification translation \(\alpha:P\to Q\) induces a contravariant reduct functor

\[
\alpha^*:\mathrm{Mod}(Q)\to\mathrm{Mod}(P),
\]

when the satisfaction condition holds. This is the principled version of

\[
\mathrm{Real}:\mathbf{Spec}^{op}\to\mathbf{Cat}.
\]

For a strength order, if \(Q\) entails \(P\), then every exact \(Q\)-model is a \(P\)-model. This gives the expected contravariance without pretending that every morphism of priors is merely inclusion.

### 10.3 Add graded satisfaction

For approximate priors, replace a Boolean relation \(M\models P\) with a value \(V(P,M)\) in an ordered commutative monoid, quantale, or other enrichment. This supports:

- tolerance;
- composition bounds;
- tradeoffs among mixed priors;
- empirical measurement of violation;
- approximate preservation under training.

Hard satisfaction is the zero sublevel set as a special case.

### 10.4 Separate realizations from full learners

An architecture category is insufficient. Let \(\mathbf{LearnSys}\) contain objects such as

\[
(\mathcal D,\Phi,\mu_0,J,U,Q)
\]

and morphisms that preserve the relevant interfaces. A realization is a compilation or interpretation

\[
\rho:P\rightsquigarrow \mathcal S_P
\]

that may alter any learning-system component. It should carry proof obligations:

- semantic adequacy: what specification is actually implemented?
- preservation: at which times and scopes is it respected?
- optimization compatibility: does learning remain defined/stable?
- resource semantics: what compute or parameter overhead is introduced?

Lenses are most compelling at this level: they express how forward computation and backward update compose. They should not be required to serve as the semantic category of priors.

### 10.5 Mixed priors

A distributive law is appropriate when two monadic effects/theories genuinely compose. Empirically, mixed priors can instead be:

- intersected hard constraints;
- weighted sums of violations;
- products/mixtures of probability measures;
- lexicographic priorities;
- constrained objectives;
- environment-conditional rules;
- mutually inconsistent specifications.

Therefore “combination” should be doctrine-specific. The general object may be a structured specification with explicit compatibility/witness data. A distributive law is one important special case, not the universal operation.

---

## 11. Falsifiable predictions suggested by the survey

The program becomes empirically testable once semantic prior and realization mechanism are crossed factorially.

### 11.1 Core experimental design

For each prior \(P\):

1. Define an architecture-independent violation metric \(V_P\).
2. Construct at least three realizations: hard architectural, soft objective, and data/inference-based where possible.
3. Match or systematically sweep sample size, parameters, wall-clock compute, and optimizer budget.
4. Evaluate both aligned and deliberately misspecified target families.
5. Track \(V_P\), training loss, representation/circuit measures, and test risk through time.
6. Distinguish interpolation time, prior-satisfaction time, and generalization time.
7. Test both IID and prior-targeted OOD shifts.

### 11.2 Concrete hypotheses

**H1: realization non-equivalence.** Two learners with equal terminal prior violation will exhibit different generalization when their training paths differ. PINN failure modes and invariance mechanisms already suggest this.

**H2: hard-prior sample-efficiency / approximation tradeoff.** When the target exactly satisfies \(P\), hard realization reduces the sample/compute required to reach a risk threshold. Under controlled misspecification, an intermediate graded strength minimizes risk.

**H3: trajectory preservation matters beyond terminal projection.** A constraint-preserving optimizer and an unconstrained optimizer followed by terminal projection reach predictors with measurably different risk even when both end in the same satisfying set.

**H4: generalization is mediated by effective-volume reduction, not raw parameter count.** Gains correlate with the prior-induced concentration of the training kernel over task-aligned functions, orbit representatives, or circuits—not simply with fewer parameters.

**H5: prior alignment has an environment signature.** A prior helps most on test shifts generated by the same transformations/interventions encoded by the prior; gains may disappear or reverse on orthogonal shifts.

**H6: grokking is a change in relative circuit accessibility.** The onset time is predicted by the efficiency gap between memorizing and prior-aligned circuits and by the rate at which the optimizer/regularizer changes their relative energy. Altering realization while holding the semantic task law fixed shifts onset predictably.

**H7: stronger exact prior produces contravariant realization inclusion only locally.** For hard algebraic priors, entailment predicts inclusions/reducts of realization categories. For soft/probabilistic priors, the analogous map fails unless extra graded or measure-preserving structure is supplied. This is a mathematical prediction about where the presheaf formalism applies.

### 11.3 Best first benchmark

A strong initial benchmark would use one finite algebraic task such as modular addition or finite-group composition and compare:

- a generic transformer/MLP;
- an exact equivariant/algebraic architecture;
- a soft law-violation penalty;
- augmentation over algebraic identities;
- a constrained optimizer preserving a law manifold;
- a post-hoc projection/certificate.

Measure:

- exact law violation on the whole finite domain;
- IID and held-out-combination accuracy;
- sample and compute efficiency;
- memorizing versus structured circuit strength;
- grokking onset;
- behavior after controlled corruption of the law.

This directly tests the proposed chain:

\[
P \to \rho(P) \to \text{learning dynamics} \to \text{selected mechanism} \to \text{generalization}.
\]

---

## 12. Direct recommendations for `structures-of-learning`

1. **Keep the hierarchy.** `prior → architecture → learning structure → generalization` is a good causal decomposition, provided “architecture” is widened to “realization in a learning system.” Some priors enter data, objective, optimizer, or inference without a distinctive architecture.

2. **Rename the core objects.** Use `Specification` or `PriorSpec` for laws/requirements; reserve `Realization` or `Model` for algebras/architectures; reserve `Learner` for the dynamical system.

3. **Do not define priors as finitary monad algebras.** If working algebraically, let finitary monads/Lawvere theories be specifications and their algebra categories be fibers of models.

4. **Retain the contravariant presheaf.** `Real : Spec^op → Cat` is a valuable local construction. Interpret morphisms as theory translations or entailments with a satisfaction condition.

5. **Make respect indexed.** Use labels such as architectural, trajectory, terminal, distributional, environment-indexed, and certified respect.

6. **Use graded violation as the empirical bridge.** Every prior should come with one or more measurable defect functionals. Exact satisfaction is defect zero.

7. **Move lenses one level down.** Lenses/optics should model the embedding of a prior in the learning/update structure and its preservation, not be the universal semantics of the prior.

8. **Treat parameter tying as compilation.** It is a map from a semantic equality/equivariance requirement into a reduced/reused parameterization. Ask what proof obligation shows that the compiled architecture factors through the satisfying function class.

9. **Use multiple doctrines.** Start with algebraic, ordered/metric, probabilistic, and dynamical doctrines. Demonstrate translations where they genuinely exist.

10. **Make generalization comparative and resource-indexed.** A prior's value is a curve over data, compute, strength, and misspecification, not a Boolean property.

---

## 13. Prioritized reading map

### Empirical taxonomies and broad framing

- [von Rueden et al., _Informed Machine Learning_](https://arxiv.org/abs/1903.12394)
- [Fortuin, _Priors in Bayesian Deep Learning_](https://arxiv.org/abs/2105.06868)
- [Battaglia et al., _Relational Inductive Biases_](https://arxiv.org/abs/1806.01261)
- [Xu et al., _What Can Neural Networks Reason About?_](https://arxiv.org/abs/1905.13211)

### Same prior, different realizations

- [Lyle et al., _On the Benefits of Invariance_](https://arxiv.org/abs/2005.00178)
- [Kaba et al., _Equivariance with Learned Canonicalization_](https://proceedings.mlr.press/v202/kaba23a.html)
- [Brehmer et al., _Does Equivariance Matter at Scale?_](https://arxiv.org/abs/2410.23179)
- [Krishnapriyan et al., _Failure Modes in PINNs_](https://arxiv.org/abs/2109.01050)
- [Liu et al., _Certified Monotonic Neural Networks_](https://arxiv.org/abs/2011.10219)

### Logical and constraint integration

- [Xu et al., _Semantic Loss_](https://proceedings.mlr.press/v80/xu18h.html)
- [Fischer et al., _DL2_](https://proceedings.mlr.press/v97/fischer19a.html)
- [Ganchev et al., _Posterior Regularization_](https://jmlr.org/papers/v11/ganchev10a.html)
- [Manhaeve et al., _DeepProbLog_](https://arxiv.org/abs/1805.10872)
- [Nye, _Categorical Construction of Logically Verifiable Neural Architectures_](https://arxiv.org/abs/2508.11647)

### Generalization, implicit bias, and grokking

- [Zhang et al., _Rethinking Generalization_](https://arxiv.org/abs/1611.03530)
- [Soudry et al., _Implicit Bias of Gradient Descent_](https://arxiv.org/abs/1710.10345)
- [Rahaman et al., _Spectral Bias_](https://arxiv.org/abs/1806.08734)
- [Power et al., _Grokking_](https://arxiv.org/abs/2201.02177)
- [Nanda et al., _Progress Measures for Grokking_](https://arxiv.org/abs/2301.05217)
- [Varma et al., _Grokking through Circuit Efficiency_](https://arxiv.org/abs/2309.02390)
- [Junior et al., _Grokking Beyond the Euclidean Norm_](https://proceedings.mlr.press/v267/junior25a.html)

### Categorical foundations to combine carefully

- [Gavranović et al., _Categorical Deep Learning Is an Algebraic Theory of All Architectures_](https://arxiv.org/abs/2402.15332)
- [Gavranović, _Fundamental Components of Deep Learning_](https://arxiv.org/abs/2403.13001)
- [Goguen & Burstall, _Institutions_](https://dl.acm.org/doi/10.1145/147508.147524)
- [Fritz, _A Synthetic Approach to Markov Kernels, Conditional Independence and Sufficient Statistics_](https://arxiv.org/abs/1908.07021)

---

## 14. Final synthesis

The literature validates the object of study, but not under one standardized name. Researchers call it prior knowledge, inductive bias, structural bias, domain knowledge, constraint, invariance, regularization, implicit bias, physics, causal structure, or learned initialization. What unifies these empirically is not “being a monad algebra” and not even “being a restriction.” It is the introduction of task-external asymmetry into an underdetermined learning problem.

The strongest research question is therefore not initially:

> What is the category of all priors?

It is:

> What data must a prior specification expose so that realizations, preservation through learning, and generalization effects can be compared compositionally and experimentally?

The evidence suggests that the minimal exposed data are:

1. provenance and task scope;
2. semantic object and satisfaction/violation;
3. strength or tolerance;
4. realization locus and mechanism;
5. preservation quantifier over architectures, trajectories, distributions, or environments;
6. induced preference over learned solutions;
7. target environment and resource-indexed generalization effect.

That interface is broad enough to include parameter tying as a special case, exact Lawvere-theoretic models as a particularly elegant special case, and the empirical cases that presently escape them. It also gives category theory a focused role: not declaring disparate priors identical, but organizing translations, realizations, preservation proofs, and compositional learning structures while leaving statistical generalization as a separately measured consequence.
