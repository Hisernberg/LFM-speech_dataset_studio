# Mathematics

This file defines the metrics and decision rules used in the project.

## Character Error Rate

For reference transcript \(r\) and hypothesis \(h\), let \(d_{\text{edit}}(r,h)\) be the Levenshtein edit distance over characters.

\[
\mathrm{CER}(r,h) = \frac{d_{\text{edit}}(r,h)}{\max(1, |r|)}
\]

A clipped version is used for dashboard readability:

\[
\mathrm{CER}_{\mathrm{clip}}(r,h) = \min(1, \mathrm{CER}(r,h))
\]

Raw CER is still reported because it exposes catastrophic runaway predictions.

## Word Error Rate

Let \(r_w\) and \(h_w\) be word-tokenized reference and hypothesis sequences.

\[
\mathrm{WER}(r,h) = \frac{d_{\text{edit}}(r_w,h_w)}{\max(1, |r_w|)}
\]

\[
\mathrm{WER}_{\mathrm{clip}}(r,h) = \min(1, \mathrm{WER}(r,h))
\]

## Character accuracy

\[
\mathrm{CharAcc}(r,h) = \max(0, 1 - \mathrm{CER}_{\mathrm{clip}}(r,h))
\]

## Repair deltas

Let:
- \(h_{\text{raw}}\): raw ASR transcript,
- \(h_{\text{cand}}\): Liquid candidate correction,
- \(h_{\text{safe}}\): deploy-safe transcript,
- \(h_{\text{oracle}}\): evaluation-oracle best transcript.

Candidate repair delta:

\[
\Delta_{\text{cand}} =
\mathrm{CER}(r,h_{\text{raw}}) -
\mathrm{CER}(r,h_{\text{cand}})
\]

Deploy-safe delta:

\[
\Delta_{\text{safe}} =
\mathrm{CER}(r,h_{\text{raw}}) -
\mathrm{CER}(r,h_{\text{safe}})
\]

Evaluation-oracle best:

\[
h_{\text{oracle}} =
\begin{cases}
h_{\text{cand}}, & \mathrm{CER}(r,h_{\text{cand}}) < \mathrm{CER}(r,h_{\text{raw}}) \\
h_{\text{raw}}, & \text{otherwise}
\end{cases}
\]

\[
\Delta_{\text{oracle}} =
\mathrm{CER}(r,h_{\text{raw}}) -
\mathrm{CER}(r,h_{\text{oracle}})
\]

The evaluation oracle is **not** a deployable metric. It measures possible future improvement if candidate selection improves.

## Deploy-safe gate

A Liquid candidate correction is accepted only if it passes conservative gates:

\[
0.8 \le \frac{|h_{\text{cand}}|}{\max(1, |h_{\text{raw}}|)} \le 1.2
\]

\[
\mathrm{CER}(h_{\text{raw}}, h_{\text{cand}}) \le 0.12
\]

The full run also disables deploy-safe replacement if mean deploy-safe delta is negative.

## Router confidence

The router returns class probabilities:

\[
p(y \mid x) = \mathrm{softmax}(f_\theta(x))
\]

The forced route is:

\[
\hat{y} = \arg\max_y p(y \mid x)
\]

Confidence:

\[
c = \max_y p(y \mid x)
\]

## Abstention

The route is accepted only if:

\[
c \ge \tau_c
\]

\[
|x| \ge L_{\min}
\]

\[
\mathrm{CER}_{\text{ASR}} \le \tau_{\text{CER}}
\]

Otherwise:

\[
\hat{y}_{\text{final}} = \texttt{unknown\_review}
\]

## Coverage

Let \(A_i = 1\) if sample \(i\) is routed without abstention.

\[
\mathrm{Coverage} = \frac{1}{N} \sum_{i=1}^{N} A_i
\]

## Accuracy on covered examples

\[
\mathrm{Acc}_{\text{covered}} =
\frac{\sum_i A_i \cdot \mathbf{1}[\hat{y}_i = y_i]}
{\max(1, \sum_i A_i)}
\]

## JSON validity

Let \(V_i = 1\) if action card \(i\) satisfies the required schema.

\[
\mathrm{JSONValidRate} = \frac{1}{N} \sum_i V_i
\]
