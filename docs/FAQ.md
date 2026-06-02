# FAQ

## Is this an LFM-Audio ASR benchmark?

No. It is a capability audit unless LFM-Audio produces valid transcripts.

## Why use BanglaASR?

The project needs a functioning speech front-end so that the rest of the local assistant workflow can be demonstrated.

## Why report clipped CER?

Raw CER reveals catastrophic outliers. Clipped CER is used for dashboard-level readability.

## Why is deploy-safe repair delta zero?

The deploy gate is conservative. It prevents unsafe overwriting of ASR transcripts. Repair potential is measured separately.

## Why does the router abstain so often?

Because wrong automatic routing is worse than manual review for noisy/short transcripts.

## Can this become a stronger Liquid cookbook example?

Yes. The next improvement is to get LFM-Audio producing valid transcripts in a stable runtime.
