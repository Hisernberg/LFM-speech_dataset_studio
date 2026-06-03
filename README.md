# LFM Speech Dataset Studio  link : [https://www.kaggle.com/code/nabidnur/banlfm-wavjepa-nat] code

**LFM Speech Dataset Studio** is a local-first Bangla speech-dataset workflow for Liquid-model ecosystem experiments.  
It audits the local **LFM-Audio GGUF** runner, evaluates a baseline Bangla ASR front-end, measures Liquid text-model transcript-repair potential, applies abstaining evidence routing, and produces schema-valid reviewable assistant action cards.

> This repository is intentionally claim-safe. It does **not** report LFM-Audio Bangla ASR quality unless the local LFM-Audio runner produces valid transcripts.

---

## Latest demo run

The latest Kaggle v5.1 run completed successfully and produced the final PR artifacts.

| Component | Model / Method | Subset | n | Main metric | Value | Claim status |
|---|---|---:|---:|---|---:|---|
| LFM-Audio capability audit | `LiquidAI/LFM2.5-Audio-1.5B-GGUF` | clean demo sample | 5 | ok rate | 0.0000 | blocked ASR claim |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | clean demo | 45 | clipped CER | 0.2290 | baseline ASR |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | random audit | 80 | clipped CER | 0.2393 | baseline ASR |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | stress | 40 | clipped CER | 0.2842 | baseline ASR |
| Liquid repair potential | `LiquidAI/LFM2.5-1.2B-Instruct` | all | 125 | eval-oracle CER delta | 0.2157 | repair-potential only |
| Evidence router | char-wb + word TF-IDF | reference test | 809 | accuracy / macro-F1 | 0.6613 / 0.6558 | deterministic router |
| Safe action cards | deterministic schema + optional Liquid proposal | clean demo first | 60 | JSON valid rate | 1.0000 | reviewable artifacts |
| Safe action cards | deterministic schema + optional Liquid proposal | accepted routes only | 20 | accuracy on covered | 0.9500 | abstaining route |

Raw CER is also reported for transparency. Clipped CER is used only for dashboard-level comparison because a few runaway ASR predictions can dominate the mean.

---

## Repository purpose

This repo is meant to support a **Liquid cookbook/community-project PR**:

> *Bangla Speech Dataset Studio: local LFM-Audio capability auditing, Liquid text repair-potential analysis, abstaining route selection, and reviewable JSONL action cards.*

The project is not positioned as a leaderboard ASR benchmark. It is a practical, reproducible, local-first speech workflow for low-resource language datasets.

---

## Main features

- Three evaluation subsets:
  - `random_audit`: honest stratified audit subset.
  - `clean_demo`: stable subset for README screenshots and examples.
  - `stress`: short/noisy/outlier subset for failure analysis.
- LFM-Audio GGUF download and local runner audit.
- Baseline Bangla ASR inference with CER/WER summaries.
- Liquid text-model repair-potential measurement:
  - raw ASR output,
  - Liquid candidate correction,
  - deploy-safe transcript,
  - evaluation-oracle best transcript.
- Abstaining evidence router:
  - routes only when confidence and ASR quality are sufficient,
  - otherwise sends examples to `unknown_review`.
- Deterministic-first action cards:
  - schema-valid JSONL,
  - explicit review reasons,
  - no autonomous medical/political/child-safety decisions.
- Full PR artifact bundle:
  - README,
  - model card,
  - contribution summary,
  - failure casebook,
  - examples,
  - figures,
  - tests.

---

## Quick start

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-core.txt
```

For full Liquid/HF experiments:

```bash
pip install -r requirements-extension.txt
```

### 2. Run the full pipeline

```bash
python scripts/run_all.py --run-fast
```

### 3. Build final artifacts

```bash
python scripts/07_make_artifacts.py
```

### 4. Run tests

```bash
pytest -q
```

---

## Kaggle one-cell version

A Kaggle-ready notebook template is in:

```text
notebooks/LFM_Speech_Dataset_Studio_v5_1_demo.ipynb
```

The notebook calls the modular code under `src/lfm_speech_dataset_studio/`.  
For a strict one-cell Kaggle submission, paste the final v5.1 one-cell script into a new notebook and export it into `notebooks/`.

Recommended Kaggle settings:

```text
Internet: ON
Accelerator: T4 GPU
RUN_FAST=1
```

For a larger run:

```bash
RUN_FAST=0
RANDOM_AUDIT_N=220
CLEAN_DEMO_N=80
STRESS_N=80
LFM_AUDIO_N=10
LFM_REPAIR_N=260
ACTION_CARD_N=120
```

---

## Claim discipline

This repo follows strict claim discipline:

1. **LFM-Audio ASR is claimed only if `ok_rate > 0`.**
2. Failed LFM-Audio runs are kept as capability-audit evidence.
3. BanglaASR is reported as a baseline, not as a Liquid model.
4. Liquid text repair is reported as repair potential, not automatic ASR improvement.
5. Deploy-safe repair must not worsen mean CER.
6. The router abstains when transcript evidence is weak.
7. Action cards are reviewable artifacts, not autonomous decisions.

---

## Important limitation

In the latest v5.1 Kaggle run, the LFM-Audio GGUF files downloaded and `llama-liquid-audio-cli` built successfully, but the runner returned nonzero exits and produced no valid transcripts. Therefore, this repo blocks LFM-Audio ASR claims and reports that component only as a capability audit.

---

## Suggested cookbook PR title

**LFM Speech Dataset Studio: Bangla Speech Audit, Repair Potential, and Reviewable Action Cards**

Recommended first PR type: **Community Project entry** linking to this full repository and generated artifacts.
