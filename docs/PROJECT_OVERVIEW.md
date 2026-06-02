# Project Overview

## Problem

Low-resource speech workflows often fail at the point where a demo becomes a deployable local assistant. A local audio model may not run in a specific environment, ASR outputs may contain severe outliers, and downstream classification/routing can become unsafe when transcripts are short or noisy.

## Solution

**LFM Speech Dataset Studio** turns this into a structured pipeline:

1. Audit the local LFM-Audio runner.
2. Evaluate a baseline Bangla ASR model.
3. Measure Liquid text-model transcript repair potential.
4. Route evidence only when confidence is adequate.
5. Generate deterministic, schema-valid, reviewable action cards.

## Project stance

This is a dataset-studio and capability-audit project, not an inflated audio-model benchmark.

## Target users

- Liquid cookbook maintainers reviewing community projects.
- Researchers testing local speech workflows.
- Low-resource-language AI developers.
- Builders of review-gated local assistants.

## Final deliverable

A GitHub repository and artifact zip containing:
- code,
- notebook,
- result tables,
- failure casebook,
- documentation,
- model card,
- action-card JSONL,
- figures.
