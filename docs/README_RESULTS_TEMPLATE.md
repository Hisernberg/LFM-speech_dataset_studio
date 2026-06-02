# README Results Template

Paste this block into the README after every new run.

```markdown
## Latest run: YYYY-MM-DD

| Component | Subset | n | Metric | Value | Claim |
|---|---:|---:|---|---:|---|
| LFM-Audio audit | clean demo sample | ... | ok rate | ... | ... |
| BanglaASR | clean demo | ... | clipped CER | ... | baseline |
| BanglaASR | random audit | ... | clipped CER | ... | baseline |
| Liquid repair | all | ... | eval-oracle delta | ... | repair potential |
| Router | reference test | ... | accuracy / macro-F1 | ... | deterministic |
| Action cards | clean demo first | ... | JSON valid rate | ... | reviewable |
```
