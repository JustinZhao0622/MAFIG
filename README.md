<div align="center">
  <a href="./pipeline.pdf"><strong>Open the MAFIG pipeline diagram (PDF)</strong></a>
</div>

<embed src="./pipeline.pdf" type="application/pdf" width="100%" height="720px" />

# MAFIG: Multi-agent Driven Formal Instruction Generation Framework

This repository contains the implementation and experimental materials for **MAFIG**, a framework for handling emergency situations in scheduling systems through multi-agent formal instruction generation.

Paper: [MAFIG: Multi-agent Driven Formal Instruction Generation Framework](https://arxiv.org/abs/2604.10989)

## Overview

Emergency events in real-world scheduling systems often cause local functional failures. Traditional robust scheduling and reactive scheduling methods usually depend on predefined rules or rescheduling strategies, which makes them difficult to apply when emergencies are diverse, unexpected, or highly context-dependent.

MAFIG addresses this problem by using large language models to generate **formal instructions** that repair the affected scheduling logic. Instead of asking an LLM to reason over the entire scheduling system, MAFIG narrows the decision scope to the local functional modules that are directly affected by the emergency. This design reduces context length, improves decision focus, and enables fast emergency handling.

## Method

MAFIG is built around a two-agent pipeline:

1. **Perception Agent**

   The Perception Agent analyzes the emergency description and the current scheduling context. It identifies which local functions or modules are affected by the event, then extracts the relevant state information needed for repair.

2. **Emergency Decision Agent**

   The Emergency Decision Agent receives the focused context from the Perception Agent and generates formal instructions for modifying the affected scheduling logic. These instructions are designed to be executable or directly convertible into updates over the local function library.

This decomposition prevents the model from processing unnecessary global system context and makes emergency decision-making more targeted.

## Key Components

- **Local function scope control**: MAFIG restricts reasoning to the local functional modules influenced by an emergency, reducing irrelevant context.
- **Formal instruction generation**: The framework converts emergency-handling decisions into structured instructions that can repair scheduling behavior.
- **Multi-agent collaboration**: Perception and decision-making are separated into different agents, improving clarity and robustness.
- **Span-focused loss-driven local distillation (SFL)**: MAFIG transfers decision-making capability from powerful cloud LLMs to lightweight local models, reducing inference latency while preserving effectiveness.

## Experimental Scenarios

The paper evaluates MAFIG on three scheduling scenarios:

- **Port scheduling**
- **Warehousing scheduling**
- **Deck scheduling**

Across these settings, MAFIG achieves high emergency-handling success rates while keeping average processing time low. Reported results include success rates of **98.49%** on Port, **94.97%** on Warehousing, and **97.50%** on Deck, with average processing times of **0.33 s**, **0.23 s**, and **0.19 s**, respectively.

## Repository Structure

```text
MAFIG/
  pipeline.pdf          # Pipeline diagram for the proposed method
  ours/                 # MAFIG implementations and datasets for each scenario
    port/
    warehousing/
    deck/
  agent-planning/       # ReAct-based planning baseline
  program-repair/       # Code-editing / mini-SWE-agent comparison experiments
```

## Citation

```bibtex
@article{zhao2026mafig,
  title={MAFIG: Multi-agent Driven Formal Instruction Generation Framework},
  author={Zhao, Shixing and Si, Zheng and Ouyang, Pengpeng and Hu, Zhengqing and Zhu, Wanqi and Chen, Dong and Guo, Yibo and Xu, Mingliang},
  journal={arXiv preprint arXiv:2604.10989},
  year={2026}
}
```
