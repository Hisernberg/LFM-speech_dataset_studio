# Liquid AI Usage

## Liquid components used

The workflow is designed around:

```text
LiquidAI/LFM2.5-Audio-1.5B-GGUF
LiquidAI/LFM2.5-1.2B-Instruct
LiquidAI/LFM2.5-350M
```

## Audio component

The LFM-Audio component is used as a **capability audit**:

1. Download required GGUF files.
2. Build or detect `llama-liquid-audio-cli`.
3. Attempt transcription commands.
4. Store stdout/stderr/output files.
5. Block ASR claims when no valid transcript is produced.

## Text component

The Liquid text model is used for:
- transcript repair-potential analysis,
- optional action-card metadata proposals.

The final card does not depend on hallucination-prone model output. The final card is deterministic-first.

## Correct PR claim

Use:

> This project audits LFM-Audio local runner behavior and uses Liquid text models for repair-potential analysis and optional metadata proposal.

Do not use:

> This project benchmarks LFM-Audio Bangla ASR.

## Why this is useful

For maintainers, this produces:
- reproducible runtime audit evidence,
- failure logs,
- command-line traces,
- claim-safe examples,
- local-first speech workflow design.
