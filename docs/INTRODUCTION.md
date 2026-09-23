# Introduction: Temporal Credit Assignment in *Aplysia*

> **Start here — scope.** This page first teaches a general question about learning: when a consequence arrives after an action, how might a nervous system connect that consequence with earlier activity? It then explains this repository’s much narrower record: a completed, data-free, deterministic Python re-analysis of a contingent-minus-yoked timing contrast. It is **not** a new experiment, a research-data release, or an exact execution of the reference MATLAB/seqNMF workflow. Its current result is **directionally suggestive but inconclusive**.
>
> Read the background sections before the project-status section. Every educational and scholarly source cited here is **general external background**, not evidence for this repository’s own result.

## A concept ladder: from an everyday event to the project question

### 1. Begin with behavior and its consequence

An animal can do something that can be observed, such as making a feeding-related movement. That action is called **behavior**. Something may happen afterward, such as the delivery of an outcome. In the kind of learning discussed here, an outcome can change how likely the behavior is to happen again. This is called **operant conditioning**: learning about the consequences of one’s own actions. **Reinforcement** has a specific meaning in this setting. It is a consequence that increases the future likelihood of a behavior; it does not simply mean something pleasant in ordinary conversation.[1]

Here is a deliberately hypothetical example. Imagine that an animal makes several movements while searching for food. A beneficial outcome arrives a few seconds later. If the animal learns from that event, it should not treat every event from the preceding day as equally responsible. But it also cannot safely assume that only the final movement mattered. The central question is how much importance, or **credit**, should be assigned to earlier actions and activity after a later outcome occurs.

### 2. Add the timing problem

That question is the **temporal credit-assignment problem**. “Temporal” means related to time. “Credit assignment” means deciding which earlier events should be adjusted in light of a later consequence. It is a general problem in the study of learning and in the study of nervous systems.[11] Formal learning models, including temporal-difference learning, describe particular mathematical ways to update expectations over time.[14] They are useful background ideas, but they do **not** show that a particular animal uses a particular algorithm. This repository does not claim that *Aplysia* uses temporal-difference learning, eligibility traces, or any other named learning rule.

### 3. Place the question in a biological setting

*Aplysia* is a marine sea slug used as a **model organism** in learning research. A model organism lets researchers investigate a broad question under a defined set of conditions. It is not a miniature human brain, and a finding in this setting does not automatically apply to people, to other animals, or to every kind of learning. Background work on *Aplysia* feeding has made it a useful setting for relating behavior to measurements from parts of a nervous system.[3] [4]

A **neuron** is a cell that receives and sends signals in a nervous system. A **neural recording** is a measurement related to activity from one or more neurons over time.[2] A recording is not a direct view of a thought or a complete explanation of behavior. It is a set of measurements that must be interpreted cautiously. Some background studies have used intact animals, while others have used isolated parts of a feeding network. An isolated preparation is a specific experimental setup, not automatically the same as an intact, freely behaving animal.[15] [16]

### 4. Picture the comparison before naming it

The project’s central design term is easier to understand as two hypothetical timelines. The comparison asks what changes when the timing of an outcome is tied to a subject’s own behavior, rather than simply experienced on a similar schedule.

| Condition | Simple hypothetical timeline | What the comparison is designed to examine |
|---|---|---|
| **Contingent** | A specified behavior occurs → an outcome is delivered because that behavior occurred. | Measurements when outcome timing is linked to the subject’s own behavior. |
| **Yoked (noncontingent)** | An outcome is delivered on a schedule matched to a partner’s outcomes → this subject’s own behavior did not trigger it. | Measurements when outcome timing is similar but is not controlled by the subject’s own behavior. |

**Contingent** means delivered because a specified event happened. **Noncontingent** means delivered without being triggered by the subject’s own specified behavior. A **yoked control** receives an outcome schedule matched to another subject, while lacking control over when its own outcome is delivered. This design helps separate the action–outcome relationship from exposure to the outcome alone. It does not, by itself, eliminate every other possible difference between conditions or establish a biological mechanism.[4]

### 5. Move from many measurements to a compact description

A recording can contain many values at many moments. For analysis, those values can be arranged in a grid: one direction might represent recorded signals and the other time. A **trial** is one repeat of an experimental episode. Related information may also be arranged across signals, time within each trial, and repeated trials. This organization does not require a reader to program; it is simply a way to keep track of what was measured and when.

When many signals change together, a researcher may use **dimensionality reduction**. This is a statistical way to describe a complicated collection of measurements with fewer recurring patterns. The goal is a more manageable description, not a claim that the smaller set is the full biological reality. Reviews of large neural recordings emphasize both the usefulness of these summaries and the need to interpret them with care.[6]

This repository’s fixed route used **non-negative matrix factorization** (NMF). NMF starts with a table of values that are not below zero. It asks whether that table can be approximated by adding together a small number of non-negative patterns. The output includes **components**, which are patterns supplied by the mathematical model, and values showing how strongly those patterns contribute at different times. Because the contributions are additive, the result can be easier to describe than the original large table.[7] [8]

The key limit is simple: a component is a descriptive model output. It is not automatically a neuron type, a biological circuit, a cause, or a mechanism. Related methods can summarize time structure across large datasets or across trials, but their settings and selection rules remain analytical choices rather than biological facts.[12] [17]

### 6. Learn how to read the reported contrast

The project compares a timing summary for contingent and yoked conditions in **matched pairs**. A matched pair is two observations deliberately linked under a stated matching rule so that a comparison can be made. “Contingent-minus-yoked” names the subtraction used for the summary. A **negative** contrast describes the direction of that number under the stated convention. It does not mean bad, biologically harmful, inhibitory, or confirmed.

A **leave-one-pair-out** summary repeats a calculation while omitting one matched pair at a time. Its purpose is to ask whether one pair alone may be driving an observed direction. This is a check on a descriptive pattern, not proof of causation. The analysis also considered choices such as the number of NMF components and **smoothing**, a step that reduces rapid variation in a signal so broader time trends are easier to see. A **sensitivity check** asks whether an interpretation remains similar when reasonable choices such as these are changed. Such checks matter because analytical choices can affect the conclusions drawn from the same underlying measurements.[13] [18]

## Project status: the completed result remains limited

This repository records a **completed deterministic Python re-analysis**. It examined the planned contingent-minus-yoked timing contrast using one fixed NMF route. In most matched pairs, that contrast was directionally negative. The direction also remained negative in leave-one-pair-out summaries. This is the limited supportive part of the result: under that fixed route, the summary pointed in one direction.

That directional pattern is **not confirmation**. The planned checks that changed component count and smoothing did not produce a timing contrast that was precise and stable enough to support a robust conclusion. The repository therefore does not choose a favorable setting after looking at the outcome. It reports the non-supportive checks alongside the directional pattern.

There are further limits. Within each model fit, the selected component had the intended positive association with retraction under the stated selection rule. That supports use of the selection rule **within that fit**. It does not show that components fitted separately are the same biological pattern. A descriptive comparison with an archived reference found broad directional correspondence at one level but incomplete agreement for individual matched pairs, and the methods were not identical. The reference MATLAB/seqNMF workflow was not run here.

The appropriate project conclusion is therefore **directionally suggestive but inconclusive**. The analysis does not establish a robust or precise effect, a causal explanation, a biological mechanism, a mapping from a component to a named cell type or circuit process, an exact rerun, a numerical replication, or equivalence with the reference workflow. It supplies a bounded description of what happened under one completed computational route.

## What the public code and tests can, and cannot, show

The public repository contains data-free computational utilities and synthetic tests. The retained utilities accept caller-provided arrays; they do not include a bundled dataset, a data loader, a repository-local execution route, a result writer, or a figure generator. The synthetic tests check specified program behavior, such as shape handling, indexing conventions, and deterministic tie handling. They do **not** test a biological hypothesis, validate an experimental protocol, or establish an empirical conclusion.

This distinction is part of why reproducibility language needs care. **Computational reproducibility** means obtaining consistent results with the same input data, computational steps, methods, code, and conditions of analysis. **Replicability** means obtaining consistent results across studies that address the same question with their own data.[9] A transparent computational record can make an analysis inspectable and repeatable, but it cannot substitute for an independent empirical study.[19] Practical safeguards such as documented code, dependencies, and procedures support inspection; they do not turn a bounded re-analysis into a new experiment.[20] [21]

The public release also does not distribute research data, numerical outputs, pair-level results, figures, or external research material. This boundary is deliberate. It allows readers to inspect the data-free methods and stated limitations without mistaking synthetic code checks or external background literature for new empirical evidence.

## Plain-language glossary

| Term | Plain-language meaning |
|---|---|
| **Action / behavior** | Something an animal does that can be observed or measured, such as a feeding-related movement. |
| **Outcome / consequence** | An event that follows behavior and may change how likely that behavior is to happen again. |
| **Operant conditioning** | Learning in which the consequences of behavior affect future behavior. |
| **Reinforcement** | A consequence that increases the future likelihood of a behavior. |
| **Contingent** | Delivered because a specified behavior or event occurred. |
| **Noncontingent** | Delivered without being triggered by the subject’s own specified behavior. |
| **Yoked control** | A comparison condition given an outcome schedule matched to another subject rather than controlled by its own behavior. |
| **Temporal credit assignment** | Deciding how a later consequence should affect the importance given to earlier events or activity. |
| **Neuron** | A cell that receives and sends signals in a nervous system. |
| **Neural recording** | A measurement related to activity from one or more neurons over time. |
| **Trial** | One repeat of an experimental episode or observation period. |
| **Matched pair** | Two observations deliberately linked for a comparison under a stated matching rule. |
| **Dimensionality reduction** | A statistical approach that describes many measurements with fewer summary patterns. |
| **Component** | A pattern returned by a statistical method; it is not automatically a cell type, circuit, or cause. |
| **NMF** | Non-negative matrix factorization: a method that approximates non-negative data with additive non-negative patterns and their time-varying contributions. |
| **Smoothing** | An analysis step that reduces rapid variation to emphasize broader time trends. |
| **Sensitivity check** | A planned check of whether an interpretation changes when reasonable analysis choices are varied. |
| **Reproducibility and replicability** | Reproducibility concerns the same computational inputs and conditions; replicability concerns separate studies with their own data. |

## Learn the basics in this order

These nine durable public resources are **general background only**. They are ordered to build vocabulary before introducing specialist methods or papers. They are not evidence for this repository’s completed re-analysis or its result.

1. **OpenStax, “6.3 Operant Conditioning.”** Start here for the difference between behavior, consequence, reinforcement, and punishment. It supplies the everyday vocabulary needed before reading about contingent and yoked conditions.[1]
2. **National Institute of Neurological Disorders and Stroke, “Brain Basics: Know Your Brain.”** Read the short sections on neurons and synapses to understand what a neuron is before encountering neural recordings. The page is a public educational primer, not a source about this repository.[2]
3. **Brembs, “Aplysia operant conditioning,” Scholarpedia.** Read this after the first two items to connect the learning vocabulary with *Aplysia* feeding behavior and the contingent-versus-yoked design. It is more detailed than a basic primer, so it works best as a bridge rather than a first reading.[3]
4. **Brembs and colleagues, “Operant reward learning in *Aplysia*: neuronal correlates and mechanisms.”** This stable record for a historical primary paper is optional context once the design vocabulary is familiar. Read the abstract to see the earlier experimental setting; do not treat it as evidence that this repository repeated its workflow or result.[4]
5. **Sutton and Barto, *Reinforcement Learning: An Introduction*, second edition.** Use the official free textbook only after the hypothetical timing example makes sense. Begin with the introduction; leave temporal-difference learning for later because it is a formal framework, not a prerequisite for reading the project status.[5]
6. **Cunningham and Yu, “Dimensionality reduction for large-scale neural recordings.”** This review is the first advanced bridge from recordings to compact statistical summaries. Its abstract and figures help explain why many signals may be summarized and why the output still needs careful interpretation.[6]
7. **scikit-learn User Guide, “Non-negative matrix factorization (NMF or NNMF).”** Use this official documentation for the method’s input–output idea: a non-negative data table is approximated by two non-negative tables whose product reconstructs it. Read it after the conceptual explanation here, not before.[7]
8. **National Academies, *Reproducibility and Replicability in Science*, “Summary.”** Read the definitions before interpreting words such as re-analysis, reproducibility, and replication. The distinction guards against treating repeatable code as a new independent experiment.[9]
9. **Costa, Baxter, and Byrne, “Neuronal population activity dynamics reveal a low-dimensional signature of operant learning in *Aplysia*.”** This is advanced contextual reading after the earlier resources. It describes an external population-analysis setting that motivates the topic; it is not proof that this repository achieved the same analysis, result, or mechanism.[10]

## Editorial note on citations

No valid prior GenSpark citation was recoverable from this repository’s reachable history. The references below were verified for this introduction. They provide general educational or scholarly background and do not supply evidence for the repository-specific status statements above.

## References

[1]: https://openstax.org/books/psychology-2e/pages/6-3-operant-conditioning "OpenStax Psychology 2e, 6.3 Operant Conditioning"
[2]: https://www.ninds.nih.gov/health-information/public-education/brain-basics/brain-basics-know-your-brain "National Institute of Neurological Disorders and Stroke, Brain Basics: Know Your Brain"
[3]: http://www.scholarpedia.org/article/Aplysia_operant_conditioning "Brembs, Aplysia operant conditioning"
[4]: https://doi.org/10.1126/science.1069434 "Brembs et al. (2002), Operant reward learning in Aplysia: neuronal correlates and mechanisms"
[5]: http://incompleteideas.net/book/the-book-2nd.html "Sutton and Barto, Reinforcement Learning: An Introduction, Second Edition"
[6]: https://doi.org/10.1038/nn.3776 "Cunningham and Yu (2014), Dimensionality reduction for large-scale neural recordings"
[7]: https://scikit-learn.org/stable/modules/decomposition.html#nmf "scikit-learn User Guide, Non-negative matrix factorization (NMF or NNMF)"
[8]: https://doi.org/10.1038/44565 "Lee and Seung (1999), Learning the parts of objects by non-negative matrix factorization"
[9]: https://www.nationalacademies.org/read/25303/chapter/3 "National Academies, Reproducibility and Replicability in Science, Summary"
[10]: https://doi.org/10.1038/s42003-022-03044-1 "Costa, Baxter, and Byrne (2022), Neuronal population activity dynamics reveal a low-dimensional signature of operant learning in Aplysia"
[11]: https://doi.org/10.1371/journal.pcbi.1002092 "Friedrich, Urbanczik, and Senn (2011), Spatio-temporal credit assignment in neuronal population learning"
[12]: https://doi.org/10.7554/eLife.38471 "Mackevicius et al. (2019), Unsupervised discovery of temporal sequences in high-dimensional datasets"
[13]: https://doi.org/10.1177/1745691616658637 "Steegen et al. (2016), Increasing transparency through a multiverse analysis"
[14]: https://doi.org/10.1007/BF00115009 "Sutton (1988), Learning to predict by the methods of temporal differences"
[15]: https://doi.org/10.1523/JNEUROSCI.19-06-02247.1999 "Nargeot, Baxter, and Byrne (1999), In vitro analog of operant conditioning in Aplysia. I. Contingent reinforcement modifies the functional dynamics of an identified neuron"
[16]: https://doi.org/10.1016/j.cub.2009.05.030 "Nargeot, Le Bon-Jego, and Simmers (2009), Cellular and network mechanisms of operant learning-induced compulsive behavior in Aplysia"
[17]: https://pubmed.ncbi.nlm.nih.gov/29887338/ "Williams et al. (2018), Unsupervised discovery of demixed, low-dimensional neural dynamics across multiple timescales through tensor component analysis"
[18]: https://doi.org/10.1038/s41586-020-2314-9 "Botvinik-Nezer et al. (2020), Variability in the analysis of a single neuroimaging dataset by many teams"
[19]: https://doi.org/10.1126/science.1213847 "Peng (2011), Reproducible research in computational science"
[20]: https://doi.org/10.1371/journal.pcbi.1003285 "Sandve et al. (2013), Ten simple rules for reproducible computational research"
[21]: https://doi.org/10.1371/journal.pcbi.1005510 "Wilson et al. (2017), Good enough practices in scientific computing"
