---
id: Q-20260827191130
type: question
status: active
created: 2026-08-27
---

<!-- Generated from the Obsidian source on main. Do not edit this branch directly. -->

# Learning rates
## Relations
- **Motivated by:**
	- [gavranovic-2024-fundamental-components](../../../literature/gavranovic-2024-fundamental-components.md)

## Question
The functors used to backpropagate, like $\mathbf{R}_{\mathcal{C}}:\mathcal{C}\to \mathbf{Lens}(\mathcal{C})$, must be additive in the backward pass. While we express learning rates in the codomain category of this functor, it isn't generally contained in the image of the functor. If the learning rate lens were additive, it would continually output a gradient of exactly zero, regardless of the loss $L$. The network would never update. A functional learning rate must break additivity. This means that a full network in supervised learning does not come from merely implementing some morphisms in $\mathbf{Para}(\mathcal{C})$ via $\mathbf{Para}(\mathbf{R}_{\mathcal{C}})$. So what are learning rates really in this level of abstraction? Maybe they come from another functor, useful extension, or some other construction? 

## Answers log

- **2026-08-27:** 
## Next steps

- 

## Exploration



## Research log

*created: 2026-08-27.*
