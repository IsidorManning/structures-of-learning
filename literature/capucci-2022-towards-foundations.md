---
id: L-Capucci2022TowardsFoundations
type: literature
citekey: Capucci2022TowardsFoundations
created: 2026-11-03
year: 2022
authors:
  - Capucci, Matteo
  - Gavranović, Bruno
  - Hedges, Jules
  - Rischel, Eigil Fjeldgren
doi: 10.4204/eptcs.372.17
venue: Electronic Proceedings in Theoretical Computer Science
url: http://dx.doi.org/10.4204/EPTCS.372.17
---

# Towards Foundations of Categorical Cybernetics

[Source](http://dx.doi.org/10.4204/EPTCS.372.17) · [DOI](https://doi.org/10.4204/eptcs.372.17)

## General summary
Proposes a general framework to study the central pattern observed across "systems that learn":
- A system acts on an environment.
- Information comes back from the environment.
- An internal state changes in response to that information.
For a neural network, this might be a forward pass, a gradient flowing backward, and an optimizer updating the parameters. 

The paper talks about applications to other fields outside of machine learning, like game theory, but those applications are not relevant here.

The motivation the authors have is to answer whether there is a single mathematical theory of interacting, adaptive systems in which apparently distinct mechanisms (neural networks, open learners, etc.) arise as particular cases?

The abstraction they use is parameterized optics, which describe bidirectional computations that themselves possess parameters and can be composed.

## Relevancy to the research
The part about deep learning is relevant. The compositional derivation of backpropagation is useful, where the backward pass composes in precisely the way optics are designed to compose. This allows reverse differentiation to be expressed functorially:
$$R:\mathcal{C}\rightarrow{}\mathbf{Lens}_{A}(\mathcal{C}).$$
Applying the para construction then gives a compositional account of gradient-based learning. This shift from gradient descent as a numerical algorithm to gradient descent as one instance of a broader family of compositional feedback mechanisms produces some new questions:
- Which properties remain true when the underlying category changes?
- Can two different learning implementations be shown to preserve the same abstract behavior.
