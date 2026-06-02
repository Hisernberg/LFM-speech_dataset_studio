# Dataset and Bundles

## Dataset

Default dataset:

```text
SUST-CSE-Speech/banspeech
```

The latest run found:

| Field | Value |
|---|---:|
| Total rows | 8,085 |
| Train rows | 6,468 |
| Validation rows | 808 |
| Test rows | 809 |
| Domains | 13 |
| Cached sample rows | 165 |

## Domains

```text
audio_books
biography
celebrity_interview
class_lecture
documentary
drama_series
kid_cartoon
kid_voice
medicine
parliament_speech
political_talkshow
sports
television_news
```

## Generated subsets

| Subset | Rows |
|---|---:|
| random_audit | 80 |
| clean_demo | 45 |
| stress | 40 |

## Heavy assets

The repository should not commit:
- WAV files,
- GGUF models,
- HF cache files,
- raw datasets,
- large model checkpoints.

Instead, store:
- manifests,
- summaries,
- figures,
- small JSONL examples,
- result tables.
