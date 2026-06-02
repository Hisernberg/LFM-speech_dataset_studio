# Limitations

## LFM-Audio transcripts were not produced

In the latest run, LFM-Audio GGUF files downloaded and the local runner built successfully, but the runner returned nonzero exits. No valid transcripts were produced.

Therefore, LFM-Audio ASR quality is not claimed.

## BanglaASR is a baseline, not Liquid

The ASR front-end is used only to provide a practical transcript source for the rest of the pipeline.

## Raw CER can exceed 1

A runaway ASR generation can be much longer than the reference. The project reports both raw CER and clipped CER.

## Eval-oracle repair is not deployable

Evaluation-oracle repair uses references to choose the better transcript. It is a diagnostic upper bound, not a deployable method.

## Action cards require review

Action cards are not autonomous decisions. High-risk domains, low confidence routes, and weak ASR cases are review-gated.
