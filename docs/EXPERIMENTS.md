# Experiments

## Latest v5.1 result summary

| Component | Subset | n | Primary metric | Value |
|---|---:|---:|---|---:|
| LFM-Audio audit | clean demo sample | 5 | ok rate | 0.0000 |
| BanglaASR | clean demo | 45 | clipped CER | 0.2290 |
| BanglaASR | random audit | 80 | clipped CER | 0.2393 |
| BanglaASR | stress | 40 | clipped CER | 0.2842 |
| Liquid repair potential | all | 125 | eval-oracle delta | 0.2157 |
| Evidence router | reference test | 809 | accuracy | 0.6613 |
| Safe action cards | clean demo first | 60 | JSON-valid rate | 1.0000 |
| Safe action cards | covered only | 20 | covered accuracy | 0.9500 |

## Interpretation

The strongest result is not LFM-Audio transcription. The strongest result is a reproducible local-first workflow with:
- reliable artifact generation,
- explicit claim blocking,
- useful ASR analysis,
- Liquid repair-potential reporting,
- abstaining routing,
- schema-valid reviewable JSONL.

## Run modes

### Fast demo mode

```bash
python scripts/run_all.py --run-fast
```

### Larger audit mode

```bash
RUN_FAST=0 python scripts/run_all.py
```

## Result files

Expected files:

```text
results/final_pr_comparison_table.csv
results/lfm_audio_capability_audit.csv
results/banglaasr_summary_by_subset.csv
results/lfm_repair_summary_by_subset.csv
results/lfm_action_cards_summary.csv
results/failure_casebook.md
```
