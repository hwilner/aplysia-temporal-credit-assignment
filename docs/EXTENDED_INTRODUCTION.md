# Extended Introduction: Temporal Credit Assignment in *Aplysia*

This document is a from-scratch introduction for readers with **no neuroscience background and no mathematical background**. Every quantitative idea is first carried out as an explicit, finite procedure on a few numbers you could check by hand, and only then named. For the shorter, technical introduction with the full literature list, see [docs/INTRODUCTION.md](INTRODUCTION.md).

Because no single mental model suits everyone, each core concept below ends with a **"many roads"** subsection: several independent mathematical lenses on the same idea, each with one tiny fully-worked example. Take whichever road matches your intuition and skip the rest. All of them use nothing beyond counting, sets, and tables — no calculus, no differential equations.

**Concept figure.** The experiment and the analysis — contingent versus yoked reward, additive decomposition of the recording, and the peak-timing question — are drawn in [concept_figure.md](concept_figure.md) as an embedded Mermaid diagram. (The release boundary does not allow image files in the tracked tree, so the figure lives as text.)

## 1. The sea slug that taught us about learning

*Aplysia californica* is a large sea slug. It is famous in biology for a simple reason: its nervous system is small and its neurons are enormous. Where a human brain has on the order of 86 billion neurons, *Aplysia* has on the order of 20,000, and some of them are so large (up to a millimeter across) that you can see them with the naked eye and record from the same identified cell, in the same location, in animal after animal. That tractability made *Aplysia* a workhorse of learning research — work recognized with a share of a Nobel Prize in the year 2000.

Think of it this way. If you wanted to understand how a factory works, you would rather start with a workshop of twenty machines you can each name and watch than with a city of a billion machines you cannot distinguish. *Aplysia* is that workshop. In particular, its **feeding network** — the small set of neurons that drives the animal's biting and swallowing — can be recorded while the animal learns, and the same experiment can be repeated on an isolated preparation of that network [9].

## 2. Operant learning: "do something, get a reward"

**Operant learning** (also called instrumental conditioning) is the kind of learning where an animal discovers that its own action produces a consequence. A rat presses a lever and gets food; it presses more. A sea slug performs a biting movement and receives a reinforcing nerve stimulation; the pattern of its feeding movements changes [2].

The key experimental trick is the **yoked control**. Two animals receive the *same* rewards on the *same* schedule. For the **contingent** animal, the reward is caused by its own behavior. For the **yoked** animal, rewards arrive on a recording of the first animal's schedule, regardless of what the yoked animal does. Both animals experience identical reward timing; only the *relationship between action and reward* differs. If the two animals end up behaving or firing differently, the difference must come from contingency — from the animal's own action being the cause — rather than from reward exposure alone.

```mermaid
flowchart LR
    subgraph Contingent animal
        A1[Animal bites] --> C1[Reward delivered
because of the bite]
        C1 --> A1
    end
    subgraph Yoked animal
        A2[Animal behaves] -.->|no causal link| C2[Reward delivered
on the other animal's schedule]
    end
```

### The many roads to a yoked control

**Road 1: set theory.** The design holds one set identical across animals — the set of reward times {t1, t2, t3, …} — and varies exactly one membership fact: in the contingent animal, each reward time is a member of the set "moments caused by this animal's own bites"; in the yoked animal it is not. Every difference in outcome must be blamed on that single changed membership, because every other set was copied. *What this buys you:* the logic of the control as one symmetric-difference computation — what differs between the two conditions is a set you can name. *What it costs you:* sets assume the copying was perfect; if the yoked schedule drifts, the "identical" claim fails silently.

**Road 2: game theory.** Contingency is a payoff table with your action as a row. The contingent animal faces: (bite, reward) = +1, (bite, no reward) = 0, (rest, reward) = 0, (rest, no reward) = 0 — rewards live only in the "bite" row, so the best strategy is to bite. The yoked animal faces a table where both rows average the same reward rate, so no strategy changes its payoff. Learning "bite more" is rational only in the first table. *What this buys you:* contingency as *action-dependent payoffs* — the difference between the two animals is whether actions move you between rows that matter. *What it costs you:* real animals do not read payoff tables; the lens describes what would be learned, not how.

**Road 3: automata.** Each animal is a state machine, and the experiment copies every transition rule except one edge. Contingent machine: state "just bit" + input "reward" → strengthen biting. Yoked machine: that edge is deleted; reward inputs loop back without changing anything. Comparing the two machines' long-run behavior isolates the effect of the single deleted transition. *What this buys you:* the experiment as a diff between two machines — one edge. *What it costs you:* a machine has sharp states; a real animal's "just bit" is fuzzy and graded.

## 3. Temporal credit assignment: which earlier signal caused the later outcome?

Here is a puzzle you already know from daily life. You eat a meal with ten ingredients; two hours later you feel sick. Which ingredient was responsible? The outcome is delayed, and everything that happened beforehand is a suspect. Assigning credit to the right earlier cause is the **temporal credit-assignment problem** [1].

A nervous system faces this constantly. Neural activity unfolds continuously, and a reward arrives at one moment. The brain must decide which earlier patterns of activity deserve to be strengthened. One formal family of solutions, temporal-difference learning, assigns credit by comparing each moment's prediction with the next moment's — propagating credit backward step by step rather than waiting for the final outcome [8]. The step-by-step logic is the same as the fading-sticky-note arithmetic worked out in the sibling synthesis project's documentation: each past event keeps a number that decays every step, and a late outcome updates events in proportion to what is left.

This repository studies a concrete version of the question: after operant training in *Aplysia*, does the *timing* of a neural activity pattern shift in the contingent animals relative to the yoked controls — for example, does a component of population activity peak *earlier* within each behavior cycle?

### The many roads to temporal credit assignment

**Road 1: discrete iterated maps.** Give each past event a mark that evolves by one rule: mark_next = 0.5 × mark_now + (1 if the event happens now, else 0). A bite at time 0 leaves marks 1, 0.5, 0.25, 0.125 at times 0–3. If a reward worth 8 arrives at time 3, the update credited to that bite is 8 × 0.125 = 1, while an event one step old gets 8 × 0.25 = 2. The whole "send credit back in time" idea is this single iterated multiplication — no differential equation anywhere. *What this buys you:* the complete credit mechanism as a table you can extend by hand, with "how far back does credit reach" answered by counting rows until the mark is negligible. *What it costs you:* a fixed decay per step is an assumption; real traces may decay differently at different delays.

**Road 2: graph theory.** Lay the episode out as a directed path graph: event 1 → event 2 → … → reward. Credit assignment is walking backwards along the edges, discounting at each hop. Count a 4-node path by hand: events A, B, C then reward R; with one hop costing a factor of 0.5, C gets 0.5, B gets 0.5 × 0.5 = 0.25, A gets 0.125. The graph makes visible that credit decays with *path length*, not with clock time — two events equally old in seconds can sit at different path lengths if the circuit routed them differently. *What this buys you:* credit as a structural property of a graph, computable by counting hops. *What it costs you:* you must know the graph; in a real brain the path itself is uncertain.

**Road 3: probability as frequencies.** Credit is what repeated tallies assign. Over 100 episodes, count a 2×2 table: rows = "pattern X fired in the last cycle?", columns = "reward followed?" If the counts are 45 / 5 / 20 / 30, then reward follows X in 45 of 50 episodes but follows not-X in only 20 of 50. The gap between 0.9 and 0.4 is the credit X earns — later outcomes vote for the earlier events that predicted them. Delay simply thins the table: the longer the gap, the more irrelevant events sneak into the "yes" row and wash the gap toward zero. *What this buys you:* credit as an auditable recount; delay-as-confusion falls out naturally. *What it costs you:* tallies need many episodes, and rare-but-decisive events may never fill a cell.

**Road 4: game theory as shared blame.** Treat the episode's events as players sharing the reward as a prize. If events A and B each alone would earn 0 but together earn 6, a fair split gives each 3; if A alone earns 4, the fair split tilts toward A. Temporal distance enters as a cost of joining the coalition late. Worked example: prize 6 for the coalition {early event, late event}; if the late event alone also earns 4, the early event's unique contribution is 6 − 4 = 2 — most of the credit belongs to the late event. *What this buys you:* a principled split when events overlap and interact, not just when they are cleanly separated in time. *What it costs you:* enumerating coalitions grows explosively (10 events have 1024 subsets), so practice uses approximations.

## 4. Non-negative matrix factorization: splitting a smoothie into ingredients, by hand

A recording of many neurons over time is a big table of numbers: one row per time point, one column per neuron. It is hard to look at directly. **Non-negative matrix factorization (NMF)** is a way to summarize it [5].

The recipe analogy: imagine you taste a smoothie and want to recover the recipe. NMF assumes the smoothie (the full recording) is a blend of a small number of *pure ingredients* (recurring spatial patterns across neurons), each added in a *time-varying amount* (how strongly that pattern is active at each moment). The non-negativity rule says you can only *add* ingredients, never subtract them — which matches neural firing, since a neuron cannot fire a negative number of spikes.

Here is the whole mechanism on four numbers. Suppose two neurons are recorded for two time points, giving the table: neuron 1 reads (4, 0) and neuron 2 reads (0, 6) at times (1, 2). That table can be written exactly as a sum of two ingredients:

- ingredient A: pattern "neuron 1 only," switched on with strength 4 at time 1 and 0 at time 2;
- ingredient B: pattern "neuron 2 only," switched on with strength 6 at time 2 and 0 at time 1.

The recording equals (strength × pattern) added over ingredients — four multiplications and two additions, nothing else. Real NMF is this same bookkeeping for the case where no exact split exists: the computer proposes strengths and patterns, measures the squared mismatch in every table cell, adds those squares up, and adjusts the proposal until that total mismatch stops shrinking. "Fit" means "we ran that adjustment loop and kept the best attempt," not "we found the true ingredients." A component is a *statistical description*, not a discovered neuron or mechanism [4]; it is a useful compression whose timing can be measured objectively, but calling it biology requires more than a good fit [6].

### The many roads to matrix factorization

**Road 1: linear algebra as weight tables (the native road).** The recording table equals (strength table) × (pattern table): each cell is a weighted sum over ingredients. Trace one cell of the example: recording(neuron 1, time 1) = 4 × (A has neuron 1) + 6 × 0? No — with strengths 4-at-time-1 for A and 0-at-time-1 for B, the cell is 4×1 + 0×1 = 4. Every cell of the big table is one such two-term sum; checking a whole fit is checking a grid of tiny sums. *What this buys you:* the decomposition as two small tables whose product you can verify cell by cell. *What it costs you:* the tables are underdetermined — many different ingredient pairs multiply to the same recording, which is the algebraic root of "a component is not a neuron."

**Road 2: geometry.** Each ingredient is a direction; the recording at each time point is a point reached by walking non-negative distances along the ingredient directions. Non-negativity confines you to a *cone*: with ingredients "neuron 1 only" (the x-axis) and "neuron 2 only" (the y-axis), the point (4, 0) at time 1 is 4 steps along x, 0 along y — inside the cone, exactly representable. A point like (−2, 3) is outside the cone and no non-negative recipe reaches it. *What this buys you:* a picture of why non-negativity is restrictive and why some recordings fit better than others. *What it costs you:* cones beyond three dimensions cannot be visualized; the picture is a faithful metaphor, not a tool.

**Road 3: discrete iterated maps.** The fitting procedure is itself an iterated map: proposal_next = adjust(proposal_now, measured mismatch). Start with a guess of strengths (3, 5); the mismatch at the four cells is (1, 0, 0, 1), total squared mismatch 2; nudge the strengths to (3.5, 5.5), mismatch drops to (0.5²+ 0.5²) = 0.5; nudge again to (4, 6), mismatch 0 — a fixed point of the adjustment rule, found by iteration exactly like a settling control loop. "Converged" means the map stopped moving. *What this buys you:* fitting demystified into "iterate an adjustment rule until it stalls." *What it costs you:* the stall point can depend on where you started — a local fixed point, not necessarily the best one; that is why the pipeline uses a fixed, deterministic initialization.

**Road 4: information theory by counting.** Factorization is compression: a 1000-time-point, 20-neuron recording is 20,000 numbers; two ingredients cost 2 patterns of 20 numbers (40) plus 2 strength traces of 1000 (2000) — about 2040 numbers instead of 20,000, roughly a tenfold saving. If each number costs the same number of yes/no questions, the compressed description needs about a tenth of the questions. *What this buys you:* "summary" made quantitative — the components are worth exactly the questions they save. *What it costs you:* question-counting ignores *which* information was discarded; a tenfold compression that throws away the one informative cell is a bad trade the count cannot see.

## 5. The timing score, computed once explicitly

The repository's contrast uses two tiny recipes, both of which fit in a margin.

**Retraction-association score.** For each component, subtract its average activity *outside* the behavior intervals from its average *inside* them. Example: a component's activity during three biting intervals is 5, 7, 6 (inside mean = 18/3 = 6) and at three moments outside them is 2, 3, 1 (outside mean = 6/3 = 2). The score is 6 − 2 = 4: positive, so the component is enriched during biting. `fit_primary_factorization` selects the component with the largest score — literally the argmax of a short list of such differences.

**Median peak phase.** Within each behavior interval, find where the selected component reaches its maximum, expressed as a fraction of the interval (0 = start, 1 = end, ties broken toward the earliest maximum), then take the median across intervals so one odd interval cannot dominate. Example: peaks at fractions 0.6, 0.5, 0.7 before training ("pre") sort to 0.5, 0.6, 0.7 with median 0.6; after training ("post") peaks at 0.3, 0.4, 0.5 give median 0.4. The scientific contrast is then one subtraction per matched pair: post-minus-pre peak phase for the contingent animal minus the same difference for its yoked partner. Negative means the contingent animal's component shifted earlier relative to its partner's.

That is the entire quantitative core of the project: means, differences, a middle value, and subtractions.

### The many roads to a timing score

**Road 1: geometry.** Each behavior cycle is a line segment from 0 to 1; a peak phase is a point on that segment, and "did timing shift?" asks whether the point moved along the segment. Pre peaks at {0.6, 0.5, 0.7} cluster around the middle-right; post peaks at {0.3, 0.4, 0.5} cluster left of them; the shift of the middle point from 0.6 to 0.4 is a leftward walk of 0.2 segment-units. *What this buys you:* "earlier" as a direction on a picture. *What it costs you:* the segment view flattens the cycle's circularity — a peak at 0.95 is one small step from 0.05, but the segment shows them at opposite ends.

**Road 2: probability as frequencies.** The median is a counting object: sort the peak fractions, take the middle tally. With pre values {0.6, 0.5, 0.7}, exactly one value lies above 0.6 and one below — that balance is what "median" means, and it is why one wild interval (say a peak at 0.05) cannot drag the summary the way a mean would (the mean of {0.6, 0.5, 0.05} is 0.38; the median is still 0.5). *What this buys you:* robustness explained as tallying, not as a theorem. *What it costs you:* the median throws away magnitude information — a shift from 0.59 to 0.61 and one from 0.1 to 0.9 can produce identical medians.

**Road 3: set theory.** The retraction-association score is a comparison of two subsets: the set of moments inside behavior intervals and its complement. The score is the difference of the two subsets' average activity — a set-difference statement (inside versus outside) before it is a number. Worked example: moments {1..6}, inside set {2, 4, 5} with activities 5, 7, 6, outside set {1, 3, 6} with 2, 3, 1; moving moment 6 (activity 1) from outside to inside changes the inside mean to 24/4 = 6 and the outside mean to 5/2 = 2.5 — the score moves 4 → 3.5 purely because one moment changed membership. *What this buys you:* the score's sensitivity to interval boundaries made visible — the definition of "inside" is part of the measurement. *What it costs you:* set membership is binary; a moment just at an interval's edge must be forced in or out.

## 6. Why synthetic time series with known ground truth?

Here is the deepest problem in testing an analysis method: with real data, you never know the right answer. If your method says "component 2 peaks early," is that true of the neurons, or an artifact of your smoothing?

The escape is **synthetic data**. An Aplysia-inspired time series is generated in code — spike times, smoothing, intervals — so the ground truth is known by construction, and the tests check whether the code recovers what was planted. Every test in `tests/` builds a tiny in-memory array with a known answer (for example, `test_retraction_association_scores_favors_interval_enrichment` plants a component enriched in a known interval and checks that the scoring rule finds it). These tests verify **code behavior**; they do not, by themselves, prove anything about real animals. The repo says this explicitly in its [methods scope](METHODS_SCOPE.md), and its open issues (#9–#14) ask for more synthetic tests of exactly this kind.

## 7. How the pieces fit together

```mermaid
flowchart TD
    S[Spike times
padded 1-based sample indices] --> L[spike_times_to_logical
boolean time x feature matrix]
    L --> G[gaussian_smooth
finite normalized Gaussian kernel]
    G --> D[downsample_mean
exact non-overlapping windows]
    D --> N[NMF fit
nndsvda init, cd solver,
Frobenius loss, fixed settings]
    N --> R[retraction_association_scores
inside-minus-outside interval means]
    R --> SEL[select component
argmax of scores]
    SEL --> P[median_peak_phase
when does the component peak
inside each interval?]
    P --> O[FactorizationOutcome
pre/post peak phases,
score, reconstruction error]
```

The pipeline above is literally `fit_primary_factorization` in `src/factorization.py`. It is run separately on a "pre" (before-training) and "post" (after-training) activity segment, and the scientific contrast compares the selected component's peak phase between them, for a contingent animal versus its yoked partner — the subtraction recipe of section 5.

```mermaid
flowchart LR
    subgraph Repository layout
        SRC[src/
preprocessing.py
factorization.py]
        TST[tests/
synthetic behavior tests]
        DOC[docs/
status, scope, this file]
        TLS[tools/
check_release_boundary.py]
    end
    TST -->|verifies| SRC
    TLS -->|keeps the public tree free of
data and result claims| DOC
```

## 8. The math that is actually used — one sentence each

Each named resource below is free; search for it by title.

- **NMF objective (Frobenius loss).** Find non-negative strength and pattern tables whose product reproduces the recording, where "reproduces" is measured by summing the squared mismatch of every cell — the adjustment loop of section 4, run by a library instead of by hand. *(Learn: the StatQuest videos on matrix factorization; the 3Blue1Brown series Essence of Linear Algebra for the multiplication intuition.)*
- **Retraction-association score.** Inside-interval mean minus outside-interval mean, one subtraction per component — worked out in section 5. *(Learn: the Khan Academy unit on measures of central tendency.)*
- **Median peak phase.** The peak position within each interval as a fraction, then the middle value across intervals — worked out in section 5. *(Learn: the Khan Academy unit on the median; the Seeing Theory interactive statistics chapters.)*
- **Gaussian smoothing.** Replace each spike moment with a small bell-shaped bump of fixed width (standard deviation 1000 samples, finite half-window 2500 samples, renormalized so the bumps' weights sum to one) and add the bumps up, turning sharp events into a smooth activity level — like replacing camera flashes with a gentle brightness curve.

## 9. What this project concluded — and did not

The completed re-analysis produced a **directionally negative** contingent-minus-yoked timing pattern in most matched pairs, and the direction survived leaving any single pair out. But the contrast was not stable under the planned component-count and smoothing sensitivity checks, and a comparison with an archived reference workflow agreed only partially. The honest bottom line, stated in the README and [status document](STATUS_AND_PLAN.md), is: **directionally suggestive but inconclusive**. No causal, mechanistic, or exact-replication claim is made, and the archived reference workflow was not rerun.

## References

All literature pointers above refer to the numbered, verified reference list in [docs/INTRODUCTION.md](INTRODUCTION.md), which is the repository's single citable source list. The entries used here are: [1] (eligibility and credit assignment on behavioral time scales), [2] (operant conditioning of the sea-slug feeding network), [3] (population recording during operant learning), [4] (dimensionality reduction for large neural recordings), [5] (the founding non-negative matrix factorization paper), [6] (factorization of neural time series into components), [8] (temporal-difference learning), and [9] (the identified-neuron studies of operant reward in this system). Per the release boundary, this document contains no external addresses or identifier links. No citations beyond that list are made in this document.

## Choosing your road

If you think in step-by-step tables, take **discrete iterated maps** — a fading memory trace and a fitting loop are both one rule applied row after row. If you think in arrows and hops, take **graph theory** — credit flows backward along edges, discounted per hop. If you think in tallies, take **probability as frequencies** — credit is a gap in a 2×2 table and a median is a balanced count. If you think in tables of mixing proportions, take **linear algebra as weight tables** — factorization is two tables whose product you can check cell by cell. If you think in pictures, take **geometry** — non-negativity is a cone, and a timing shift is a walk along a segment. If you think in membership, take **set theory** — a yoked control is one changed membership, and a timing score is an inside/outside partition. If you think in incentives, take **game theory** — contingency is an action-dependent payoff table, and credit is a fair split of a shared prize. If you think in questions, take **information theory** — a summary is worth the questions it saves.
