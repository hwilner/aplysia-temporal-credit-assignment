# Introduction: Temporal Credit Assignment in *Aplysia*

## The question in everyday terms

Learning is straightforward when an action and its outcome happen together. It is much harder when an outcome arrives later: which earlier action, event, or neural pattern should be credited? This is the **temporal credit-assignment problem**. It appears in reinforcement-learning theory and in neuroscience because a nervous system must connect later consequences to earlier activity without treating every preceding event as equally important.[1]

*Aplysia* is useful for studying this problem because its feeding behavior and learning-related neural activity can be measured in a comparatively tractable system. Operant-learning experiments can compare outcomes delivered contingently on behavior with outcomes delivered on a matched schedule that is not contingent on the animal’s own behavior. That comparison asks whether the timing and structure of neural activity differ when an outcome is linked to behavior rather than merely delivered.[2] Population-recording work has also shown that low-dimensional activity patterns can provide a useful description of learning-related dynamics in this setting.[3]

## From many neural traces to descriptive patterns

Neural recordings contain many signals that change at once. **Dimensionality reduction** summarizes those signals using a smaller number of recurring patterns. This can make a complex recording easier to inspect, but the patterns are statistical descriptions. A component is not automatically a neuron type, circuit, or causal mechanism.[4]

This repository uses **non-negative matrix factorization** (NMF), which approximates a non-negative activity matrix with additive components and time-varying weights. The non-negativity constraint can make the resulting patterns easier to describe as additive contributions.[5] Related factorization approaches can help identify temporal structure in large neural datasets, but factorization settings, preprocessing, and component-selection rules are analytical choices rather than biological facts.[6]

## What this project did

The completed deterministic Python re-analysis examined a contingent-minus-yoked timing contrast using a fixed NMF route. It found a directionally negative pattern in most matched pairs, including leave-one-pair-out summaries. That is **directional support**, not confirmation.

The planned component-count and smoothing checks did not produce a precise, stable contrast. The descriptive comparison with an archived reference also showed incomplete pair-level directional correspondence, and the reference MATLAB/seqNMF workflow was not executed here. The appropriate conclusion is therefore **directionally suggestive but inconclusive**. The project does not claim an exact rerun, numerical replication, causal explanation, or biological mechanism.

## Why the limitations matter

A reproducible analysis is more useful when its reasonable choices are visible. Sensitivity checks show whether a conclusion depends strongly on choices such as smoothing or model complexity. Reporting those checks prevents a favorable setting from being selected after outcomes are known.[7] Synthetic tests in this repository verify specified code behavior; they do not establish the empirical hypothesis.

## Citation provenance

No valid prior GenSpark citation was recoverable from this repository’s reachable history. The references below were newly verified for this introduction and provide background, not evidence for the repository’s own result.

## References

[1]: https://doi.org/10.1371/journal.pcbi.1002092 "Friedrich, Urbanczik, and Senn (2011), Spatio-temporal credit assignment in neuronal population learning"
[2]: https://doi.org/10.1126/science.1069434 "Brembs et al. (2002), Operant reward learning in Aplysia: neuronal correlates and mechanisms"
[3]: https://doi.org/10.1038/s42003-022-03044-1 "Costa, Baxter, and Byrne (2022), Neuronal population activity dynamics reveal a low-dimensional signature of operant learning in Aplysia"
[4]: https://doi.org/10.1038/nn.3776 "Cunningham and Yu (2014), Dimensionality reduction for large-scale neural recordings"
[5]: https://doi.org/10.1038/44565 "Lee and Seung (1999), Learning the parts of objects by non-negative matrix factorization"
[6]: https://doi.org/10.7554/eLife.38471 "Mackevicius et al. (2019), Unsupervised discovery of temporal sequences in high-dimensional datasets"
[7]: https://doi.org/10.1177/1745691616658637 "Steegen et al. (2016), Increasing transparency through a multiverse analysis"
