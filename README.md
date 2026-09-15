# Detecting and Adapting to Context Drift in Long-Running Generative AI Systems Using Multi-Agent Frameworks

## Overview

This repository contains the implementation and experimental materials for the master's thesis:

"Detecting and Adapting to Context Drift in Long-Running Generative AI Systems Using Multi-Agent Frameworks."

The study investigates whether a specialised multi-agent framework can detect controlled changes in conversational context and adapt its internal context representation to improve contextual recovery.

## Research Framework

The proposed framework consists of specialised agents for:

- Context Monitoring
- Context Drift Detection
- Belief Validation
- Reflective Memory
- Response Adaptation

The framework also includes an experimental Equilibrium-Based Drift Control mechanism that considers both drift magnitude and drift trajectory when selecting adaptation intensity.

## Context Drift Types

Six controlled drift categories are evaluated:

1. Slot Update
2. Slot Insertion
3. Slot Deletion
4. Contradiction
5. Goal Drift
6. Multi-Slot Drift

## Experimental Design

The final quantitative evaluation uses structured MultiWOZ dialogue data.

- 8 selected dialogues
- 6 controlled drift types
- 48 paired baseline/proposed cases
- 96 total evaluation records

## Evaluation Metrics

The experiments evaluate:

- Context Retention Score (CRS)
- Belief Revision Accuracy (BRA)
- Hallucination Rate (HR)
- Agent Stability Index (ASI)
- Contradiction Resolution Rate (CRR)
- Adaptation Success Rate (ASR)
- Equilibrium Deviation Score (EDS)
- Equilibrium Recovery Rate (ERR)

## Repository Structure

```text
agents/              Multi-agent components and adaptation policies
core/                Core data structures and cognitive state
data/                Dataset loading and adapters
drift_injection/     Controlled context-drift injection
evaluation/          Evaluation runner and metrics
experiments/         Experiment and ablation runners
pipeline/            Cognitive processing pipeline
notebooks/           Research notebooks
results/             Experimental results
tests/               Tests and validation
requirements.txt     Python dependencies
