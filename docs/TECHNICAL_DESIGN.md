# Technical Design

## Pipeline

```text
BanSpeech dataset
      |
      v
Subset builder
(random_audit / clean_demo / stress)
      |
      +--> LFM-Audio GGUF runner audit
      |
      +--> BanglaASR baseline transcription
                |
                v
        Liquid text repair-potential analysis
                |
                v
        Abstaining evidence router
                |
                v
        Deterministic schema-valid action cards
```

## Subsets

| Subset | Purpose |
|---|---|
| `random_audit` | honest stratified evaluation |
| `clean_demo` | stable examples for screenshots and README |
| `stress` | short/noisy/outlier examples for failure analysis |

## LFM-Audio audit

The audit checks:
- GGUF files downloaded,
- local CLI builds,
- CLI help is available,
- command attempts complete,
- transcripts are produced or claims are blocked.

When no transcript is produced, the repo reports only capability-audit evidence.

## ASR baseline

The baseline is not a Liquid model. It is used to produce transcripts for the rest of the workflow.

## Liquid text repair

The repair section separates:
- `raw_asr`,
- `lfm_candidate`,
- `deploy_safe_transcript`,
- `eval_oracle_best_transcript`.

Only deploy-safe output is suitable for automatic use. Eval-oracle output is an upper-bound analysis.

## Router

The router uses character-boundary and word-level TF-IDF features with logistic regression. It abstains to `unknown_review` when evidence is weak.

## Action cards

Action cards are deterministic-first and include:
- route,
- risk,
- review reasons,
- keywords,
- summary,
- transcript,
- JSON-valid schema.

Optional Liquid metadata proposals can be stored separately but are not required for final cards.
