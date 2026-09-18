# Introduction: Temporal Credit Assignment in *Aplysia*

## The question in everyday terms

Learning is straightforward when an action and its outcome happen together. It is much harder when an outcome arrives later: which earlier action, event, or neural pattern should be credited? This is the **temporal credit-assignment problem**. It appears in reinforcement-learning theory and in neuroscience because a nervous system must connect later consequences to earlier activity without treating every preceding event as equally important.[1] One formal family of approaches, temporal-difference learning, assigns credit using differences between successive predictions rather than only a final observed outcome.[8]

*Aplysia* is useful for studying this problem because its feeding behavior and learning-related neural activity can be measured in a comparatively tractable system. Operant-learning experiments can compare outcomes delivered contingently on behavior with outcomes delivered on a matched schedule that is not contingent on the animal’s own behavior. That comparison asks whether the timing and structure of neural activity differ when an outcome is linked to behavior rather than merely delivered.[2] In isolated feeding-network preparations, contingent and noncontingent reinforcement have also been used to study activity in identified neurons.[9] Later work examined the temporal organization of activity within a feeding-network subcircuit after operant training.[10] Population-recording work has also shown that low-dimensional activity patterns can provide a useful description of learning-related dynamics in this setting.[3]

## From many neural traces to descriptive patterns

Neural recordings contain many signals that change at once. **Dimensionality reduction** summarizes those signals using a smaller number of recurring patterns. This can make a complex recording easier to inspect, but the patterns are statistical descriptions. A component is not automatically a neuron type, circuit, or causal mechanism.[4]

This repository uses **non-negative matrix factorization** (NMF), which approximates a non-negative activity matrix with additive components and time-varying weights. The non-negativity constraint can make the resulting patterns easier to describe as additive contributions.[5] When recordings are organized as repeated trials, related tensor factorization methods can represent neuron, within-trial-time, and trial axes with separate factors.[11] Related factorization approaches can help identify temporal structure in large neural datasets, but factorization settings, preprocessing, and component-selection rules are analytical choices rather than biological facts.[6]

## What this project did

The completed deterministic Python re-analysis examined a contingent-minus-yoked timing contrast using a fixed NMF route. It found a directionally negative pattern in most matched pairs, including leave-one-pair-out summaries. That is **directional support**, not confirmation.

The planned component-count and smoothing checks did not produce a precise, stable contrast. The descriptive comparison with an archived reference also showed incomplete pair-level directional correspondence, and the reference MATLAB/seqNMF workflow was not executed here. The appropriate conclusion is therefore **directionally suggestive but inconclusive**. The project does not claim an exact rerun, numerical replication, causal explanation, or biological mechanism.

## Why the limitations matter

Reproducibility and independent replication are related but distinct: a transparent computational workflow can make the original analysis inspectable and repeatable, yet it does not substitute for a new empirical test.[13] For computational work, preserving code, data where sharing is permitted, and an explicit protocol can support that level of audit; version control, recorded dependencies, and organized project materials are practical safeguards.[14][15]

A reproducible analysis is more useful when its reasonable choices are visible. Sensitivity checks show whether a conclusion depends strongly on choices such as smoothing or model complexity. A multi-team neuroimaging study documented variability among analyses of a shared dataset; that result does not predict the behavior of this pipeline, but it illustrates why analytical choices should be exposed rather than treated as invisible defaults.[12] Reporting those checks prevents a favorable setting from being selected after outcomes are known.[7] Synthetic tests in this repository verify specified code behavior; they do not establish the empirical hypothesis.

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
[8]: https://doi.org/10.1007/BF00115009 "Sutton (1988), Learning to predict by the methods of temporal differences"
[9]: https://doi.org/10.1523/JNEUROSCI.19-06-02247.1999 "Nargeot, Baxter, and Byrne (1999), In vitro analog of operant conditioning in Aplysia. I. Contingent reinforcement modifies the functional dynamics of an identified neuron"
[10]: https://doi.org/10.1016/j.cub.2009.05.030 "Nargeot, Le Bon-Jego, and Simmers (2009), Cellular and network mechanisms of operant learning-induced compulsive behavior in Aplysia"
[11]: https://pubmed.ncbi.nlm.nih.gov/29887338/ "Williams et al. (2018), Unsupervised discovery of demixed, low-dimensional neural dynamics across multiple timescales through tensor component analysis"
[12]: https://doi.org/10.1038/s41586-020-2314-9 "Botvinik-Nezer et al. (2020), Variability in the analysis of a single neuroimaging dataset by many teams"
[13]: https://doi.org/10.1126/science.1213847 "Peng (2011), Reproducible research in computational science"
[14]: https://doi.org/10.1371/journal.pcbi.1003285 "Sandve et al. (2013), Ten simple rules for reproducible computational research"
[15]: https://doi.org/10.1371/journal.pcbi.1005510 "Wilson et al. (2017), Good enough practices in scientific computing"
