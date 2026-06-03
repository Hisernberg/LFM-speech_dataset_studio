## LFM Speech Dataset Studio

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Project type](https://img.shields.io/badge/project-claim--safe%20speech%20dataset%20studio-purple.svg)](#claim-discipline)
[![Kaggle](https://img.shields.io/badge/Kaggle-demo%20notebook-20BEFF.svg)](https://www.kaggle.com/code/nabidnur/banlfm-wavjepa-nat)

**LFM Speech Dataset Studio** is a local-first Bangla speech-dataset workflow for Liquid-model ecosystem experiments. It audits the local **LFM-Audio GGUF** runner, evaluates a baseline Bangla ASR front-end, measures Liquid text-model transcript-repair potential, applies abstaining evidence routing, and produces schema-valid reviewable assistant action cards.

> **Claim-safe design:** this repository does **not** report LFM-Audio Bangla ASR quality unless the local LFM-Audio runner produces valid transcripts.

---

## Contents

- [Why this project exists](#why-this-project-exists)
- [What this project does](#what-this-project-does)
- [Latest v5.1 run](#latest-v51-run)
- [Result interpretation](#result-interpretation)
- [Pipeline overview](#pipeline-overview)
- [Repository structure](#repository-structure)
- [Quick start](#quick-start)
- [Kaggle one-cell workflow](#kaggle-one-cell-workflow)
- [Generated artifacts](#generated-artifacts)
- [Metrics](#metrics)
- [Claim discipline](#claim-discipline)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Suggested Liquid cookbook PR](#suggested-liquid-cookbook-pr)
- [Citation](#citation)

---

## Why this project exists

Low-resource speech workflows often fail at the point where a demo becomes a reproducible local system. A local audio model may not run in a given environment, ASR outputs may contain severe outliers, and downstream routing can become unsafe when transcripts are short, noisy, or domain-ambiguous.

This project turns that problem into a structured, auditable workflow:

1. Check whether the local LFM-Audio runtime can actually produce transcripts.
2. Use a functioning Bangla ASR baseline when audio runtime support is unavailable.
3. Measure whether Liquid text models can help repair transcripts.
4. Route evidence only when confidence is high enough.
5. Generate reviewable, schema-valid action cards instead of autonomous decisions.

The intended contribution is not a leaderboard ASR result. It is a **claim-safe local speech dataset studio** for Liquid-model workflows.

---

## What this project does

The project:

- Loads `SUST-CSE-Speech/banspeech`.
- Builds three evaluation subsets:
  - `random_audit`: honest stratified audit subset.
  - `clean_demo`: stable examples for README, screenshots, and PR review.
  - `stress`: short/noisy/outlier subset for failure analysis.
- Downloads and audits `LiquidAI/LFM2.5-Audio-1.5B-GGUF`.
- Builds or detects `llama-liquid-audio-cli`.
- Blocks LFM-Audio ASR claims unless valid transcripts are produced.
- Runs `bangla-speech-processing/BanglaASR` as a baseline speech front-end.
- Uses `LiquidAI/LFM2.5-1.2B-Instruct` for transcript repair-potential analysis.
- Adds `unknown_review` abstention for weak routing evidence.
- Generates deterministic-first, schema-valid, reviewable JSONL action cards.
- Saves metrics, figures, failure logs, README/model-card files, and PR-ready artifacts.

---

## Latest v5.1 run

The latest Kaggle v5.1 run completed end-to-end and generated the final PR artifact bundle.

| Component | Model / Method | Subset | n | Primary metric | Value | Secondary metric | Value | Claim status |
|---|---|---:|---:|---|---:|---|---:|---|
| LFM-Audio capability audit | `LiquidAI/LFM2.5-Audio-1.5B-GGUF` | clean demo sample | 5 | ok rate | 0.0000 | failure type | nonzero returncode | blocked ASR claim |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | clean demo | 45 | clipped CER | 0.2290 | raw CER | 0.3684 | baseline ASR |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | random audit | 80 | clipped CER | 0.2393 | raw CER | 0.5180 | baseline ASR |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | stress | 40 | clipped CER | 0.2842 | raw CER | 3.8959 | baseline ASR |
| BanglaASR front-end | `bangla-speech-processing/BanglaASR` | all | 165 | clipped CER | 0.2474 | raw CER | 1.2961 | baseline ASR |
| Liquid repair potential | `LiquidAI/LFM2.5-1.2B-Instruct` | clean demo | 45 | eval-oracle CER delta | 0.1462 | deploy-safe delta | 0.0000 | repair-potential only |
| Liquid repair potential | `LiquidAI/LFM2.5-1.2B-Instruct` | random audit | 80 | eval-oracle CER delta | 0.2548 | deploy-safe delta | 0.0000 | repair-potential only |
| Liquid repair potential | `LiquidAI/LFM2.5-1.2B-Instruct` | all | 125 | eval-oracle CER delta | 0.2157 | deploy-safe delta | 0.0000 | repair-potential only |
| Evidence router | char-wb + word TF-IDF | reference test | 809 | accuracy | 0.6613 | macro-F1 | 0.6558 | deterministic router |
| Safe action cards | deterministic schema + optional Liquid proposal | clean demo first | 60 | JSON valid rate | 1.0000 | needs-review rate | 0.8667 | reviewable artifacts |
| Safe action cards | deterministic schema + optional Liquid proposal | accepted routes only | 20 | accuracy on covered | 0.9500 | macro-F1 on covered | 0.9510 | abstaining route |

### Runtime summary

| Item | Value |
|---|---|
| Dataset | `SUST-CSE-Speech/banspeech` |
| Total dataset rows | 8,085 |
| Train / validation / test rows | 6,468 / 808 / 809 |
| Domains | 13 |
| Cached evaluation rows | 165 |
| Random audit rows | 80 |
| Clean demo rows | 45 |
| Stress rows | 40 |
| GPU | Tesla T4 |
| LFM-Audio claim status | `blocked_no_lfm_audio_asr_claim` |
| Action-card JSON validity | 1.0000 |
| Router abstention rate | 0.6667 |
| PR artifact zip | `lfm_speech_dataset_studio_v5_1_pr_artifacts.zip` |

---

## Result interpretation

### LFM-Audio

The LFM-Audio GGUF files downloaded and the local `llama-liquid-audio-cli` runner built successfully. However, the runner returned nonzero exits and produced no valid transcripts in the Kaggle runtime. Therefore, the repository reports this component only as a **capability audit** and blocks all LFM-Audio ASR claims.

Correct wording:

> LFM-Audio GGUF download and local runner build were successful, but no valid transcripts were produced in this run; LFM-Audio ASR quality is not claimed.

Incorrect wording:

> LFM-Audio performs Bangla ASR.

### BanglaASR baseline

BanglaASR provides the practical speech front-end for the rest of the pipeline. The project reports both raw CER and clipped CER:

- **Raw CER** exposes catastrophic decoding failures.
- **Clipped CER** is used for dashboard-level comparison so a few runaway outputs do not dominate the mean.

The clean-demo and random-audit clipped CER values are usable for demonstration and analysis.

### Liquid repair potential

Liquid text repair is reported in three forms:

| Output | Meaning | Deployable? |
|---|---|---|
| `lfm_candidate` | Direct Liquid candidate correction | No |
| `deploy_safe_transcript` | Candidate accepted only if conservative gates pass | Yes |
| `eval_oracle_best_transcript` | Reference-based upper-bound analysis | No |

The eval-oracle delta is positive, which means Liquid text repair has measurable potential. The deploy-safe delta is zero because the gate did not safely overwrite ASR outputs in this run.

### Abstaining router

The router accepts only confident examples and sends weak evidence to `unknown_review`.

- Forced route accuracy before abstention: **0.5667**
- Coverage after abstention: **0.3333**
- Accuracy on covered examples: **0.9500**

This is the intended behavior: the system prefers abstention over wrong automatic routing.

---

## Pipeline overview

```text
BanSpeech dataset
      |
      v
Dataset Studio
(random_audit / clean_demo / stress)
      |
      +----------------------+
      |                      |
      v                      v
LFM-Audio GGUF audit     BanglaASR baseline
      |                      |
      |                      v
      |              Liquid text repair-potential analysis
      |                      |
      |                      v
      |              Abstaining evidence router
      |                      |
      |                      v
      +------------> Reviewable action-card JSONL
```

Recommended architecture diagram path:

```text
figures/pipeline_overview.png
```

---

## Repository structure

```text
lfm-speech-dataset-studio/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── requirements-core.txt
├── requirements-extension.txt
├── .gitignore
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── TECHNICAL_DESIGN.md
│   ├── MATHEMATICS.md
│   ├── EXPERIMENTS.md
│   ├── DATASET_AND_BUNDLES.md
│   ├── LIQUID_AI_USAGE.md
│   ├── LIMITATIONS.md
│   ├── COOKBOOK_PR.md
│   ├── FAQ.md
│   └── TECHNIQUES_USED.md
│
├── src/lfm_speech_dataset_studio/
│   ├── config.py
│   ├── text_bn.py
│   ├── metrics.py
│   ├── audio_io.py
│   ├── lfm_audio_audit.py
│   ├── asr_baseline.py
│   ├── repair.py
│   ├── router.py
│   ├── cards.py
│   ├── schemas.py
│   └── artifacts.py
│
├── scripts/
│   ├── run_all.py
│   ├── 01_prepare_banspeech.py
│   ├── 02_audit_lfm_audio_runner.py
│   ├── 03_run_bangla_asr.py
│   ├── 04_liquid_repair_potential.py
│   ├── 05_route_and_abstain.py
│   ├── 06_make_action_cards.py
│   └── 07_make_artifacts.py
│
├── notebooks/
│   ├── LFM_Speech_Dataset_Studio_v5_1_demo.ipynb
│   └── LFM_Speech_Dataset_Studio_v5_1_full.ipynb
│
├── examples/
│   ├── final_pr_comparison_table.csv
│   ├── demo_action_cards_safe.jsonl
│   └── README_RESULTS_TEMPLATE.md
│
├── figures/
│   ├── dataset_domain_distribution.png
│   ├── banglaasr_clipped_cer_by_subset.png
│   ├── repair_potential_bar.png
│   ├── router_abstention_counts.png
│   ├── card_risk_distribution.png
│   ├── lfm_audio_failure_types.png
│   └── sample_spectrogram.png
│
└── tests/
    ├── test_metrics.py
    ├── test_text_bn.py
    ├── test_card_schema.py
    ├── test_router_abstention.py
    └── test_lfm_audio_error_parser.py
```

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/lfm-speech-dataset-studio.git
cd lfm-speech-dataset-studio
```

### 2. Create environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 3. Install dependencies

For lightweight tests and utility modules:

```bash
pip install -r requirements-core.txt
```

For full HF/Liquid experiments:

```bash
pip install -r requirements-extension.txt
```

### 4. Run tests

```bash
pytest -q
```

### 5. Run the modular pipeline

```bash
python scripts/run_all.py --run-fast
```

---

## Kaggle one-cell workflow

A Kaggle-ready notebook is available at:

```text
notebooks/LFM_Speech_Dataset_Studio_v5_1_full.ipynb
```

Kaggle settings:

```text
Internet: ON
Accelerator: T4 GPU
```

Fast run:

```bash
RUN_FAST=1
```

Larger run:

```bash
RUN_FAST=0
RANDOM_AUDIT_N=220
CLEAN_DEMO_N=80
STRESS_N=80
LFM_AUDIO_N=10
LFM_REPAIR_N=260
ACTION_CARD_N=120
```

Kaggle demo link:

```text
https://www.kaggle.com/code/nabidnur/banlfm-wavjepa-nat
```

---

## Generated artifacts

The v5.1 pipeline writes:

```text
pr_artifacts/
├── README.md
├── MODEL_CARD.md
├── CONTRIBUTION_SUMMARY.md
├── failure_casebook.md
├── final_audit.json
├── final_pr_comparison_table.csv
├── demo_action_cards_safe.jsonl
├── lfm_audio_capability_audit.csv
├── lfm_audio_summary.csv
├── banglaasr_predictions_all.csv
├── banglaasr_summary_by_subset.csv
├── lfm_repair_potential_predictions.csv
├── lfm_repair_summary_by_subset.csv
├── lfm_action_cards_safe.csv
├── lfm_action_cards_summary.csv
├── router_summary.csv
├── router_reference_eval.csv
├── error_analysis.csv
└── figures/
```

Recommended files to attach to a release:

```text
lfm_speech_dataset_studio_v5_1_pr_artifacts.zip
final_pr_comparison_table.csv
demo_action_cards_safe.jsonl
failure_casebook.md
```

---

## Metrics

### Character Error Rate

For reference transcript \(r\) and hypothesis \(h\):

\[
\mathrm{CER}(r,h) = \frac{d_{\text{edit}}(r,h)}{\max(1, |r|)}
\]

The clipped version is used for dashboard readability:

\[
\mathrm{CER}_{clip}(r,h) = \min(1, \mathrm{CER}(r,h))
\]

### Word Error Rate

\[
\mathrm{WER}(r,h) = \frac{d_{\text{edit}}(r_w,h_w)}{\max(1, |r_w|)}
\]

### Repair delta

\[
\Delta_{\text{candidate}} =
\mathrm{CER}(r,h_{\text{raw}}) -
\mathrm{CER}(r,h_{\text{candidate}})
\]

\[
\Delta_{\text{safe}} =
\mathrm{CER}(r,h_{\text{raw}}) -
\mathrm{CER}(r,h_{\text{safe}})
\]

A positive delta indicates improvement.

### Router coverage

\[
\mathrm{Coverage} = \frac{\#\text{accepted routes}}{\#\text{all routes}}
\]

### Accuracy on covered routes

\[
\mathrm{Acc}_{covered} =
\frac{\#\text{correct accepted routes}}{\#\text{accepted routes}}
\]

---

## Claim discipline

This repo follows strict claim discipline:

1. **LFM-Audio ASR is claimed only if `ok_rate > 0`.**
2. Failed LFM-Audio runs are retained as capability-audit evidence.
3. BanglaASR is reported as a baseline, not as a Liquid model.
4. Liquid text repair is reported as repair potential, not automatic ASR improvement.
5. Deploy-safe repair must not worsen mean CER.
6. The router abstains when transcript evidence is weak.
7. Action cards are reviewable artifacts, not autonomous decisions.
8. Medical, child, civic, news, and political items are review-gated.

---

## Limitations

- LFM-Audio did not produce valid transcripts in the latest Kaggle runtime.
- LFM-Audio quality is therefore not measured or claimed.
- BanglaASR is a baseline front-end, not a Liquid model.
- Raw CER can be high because runaway predictions are intentionally preserved in failure analysis.
- Eval-oracle repair is not deployable because it uses references to choose the better transcript.
- Action cards are not autonomous decisions and require human review when marked.

---

## Roadmap

- [ ] Add official LFM-Audio runtime guidance if maintainers provide a stable command path.
- [ ] Add a non-Kaggle local CPU/GPU runtime audit.
- [ ] Add more Bangla ASR baselines.
- [ ] Tune deploy-safe repair gates with validation-only criteria.
- [ ] Add more robust uncertainty calibration for the router.
- [ ] Add a small Streamlit UI for reviewing action cards.
- [ ] Add release assets with figures and example JSONL cards.
- [ ] Convert the one-cell notebook into fully executable modular scripts.

---

## Suggested Liquid cookbook PR

Recommended PR type:

```text
Community Project
```

Recommended title:

```text
LFM Speech Dataset Studio: Bangla Speech Audit, Repair Potential, and Reviewable Action Cards
```

Recommended PR description:

> This project provides a local-first, claim-safe speech dataset workflow around Liquid models. It audits LFM-Audio GGUF runner behavior, evaluates a Bangla ASR baseline, measures Liquid text-model transcript repair potential, applies abstaining evidence routing, and generates schema-valid reviewable JSONL action cards. The workflow blocks LFM-Audio ASR claims unless valid transcripts are produced.

---

## Citation

```bibtex
@software{lfm_speech_dataset_studio_2026,
  title        = {LFM Speech Dataset Studio},
  author       = {Nabidnur Abrar},
  year         = {2026},
  url          = {https://github.com/YOUR_USERNAME/lfm-speech-dataset-studio},
  note         = {Local-first Bangla speech dataset workflow for Liquid-model capability auditing, repair-potential analysis, and reviewable action-card generation}
}
```

---

## Author

**Nabidnur Abrar**  
AI research engineer focused on low-resource NLP, speech, multimodal systems, and local-first model workflows.

---

## License

This repository is released under the MIT License. External datasets, Hugging Face models, Liquid AI models, and GGUF assets are governed by their respective licenses
)
