# Limitations and interpretation boundaries

[Back to README](../README.md) · [Paper map](01-paper-map.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

These notes distinguish the paper's observed findings from interpretations and open questions. They refer to arXiv 2610.12176v1 and are not a reproduction or independent empirical validation.

## Two recursive cycles establish a finite demonstration

The experiments report L(0) -> L(1) -> L(2), with the trained student reused as executor, optimizer, and in-loop evaluator. This shows that the procedure can be repeated twice in the stated setting. It does not demonstrate indefinite improvement, a sustained acceleration law, or a guarantee that later generations improve. The conclusion itself identifies faster gains per cycle as future work. The second-cycle appendix description says the first-cycle recipe is followed as closely as possible but does not restate every collection/training count, so first-cycle data sizes should not be assigned to L(2). [Section 4.2, PDF pp.6-7; Appendix B.2, p.17; Conclusion, p.10](https://arxiv.org/pdf/2610.12176v1#page=17)

The retained workflow is best under sequential self-comparisons, rather than a certified global optimum. A model that generates, evaluates, and improves outputs still shares a learned prior across those roles. Multi-agent organization may change its working style, but it does not guarantee independent perspectives or remove shared misconceptions. [Section 3, PDF p.5; Conclusion, p.10](https://arxiv.org/pdf/2610.12176v1#page=5)

## External preference and scientific correctness differ

External GPT-5.5/Claude Opus 4.8 judgments are withheld from the main loop and provide a useful independent reporting panel. They are still model judgments. Six seeds/models assessing one workspace pair are repeated ratings of those outputs, not six independent task executions. The paper expressly treats the shares as descriptive and does not infer significance from the rating count. Evaluator agreement rising from 0.73 to 0.93 therefore measures agreement with that panel, not an independently established accuracy on scientific truth. [Section 4.2/Figure 3, PDF pp.6-7; Appendix C.1, p.18](https://arxiv.org/pdf/2610.12176v1#page=18)

The paper includes a concrete counterexample. On robotics task 305, a revision replaces force-driven motion with direct goal repositioning and removes simulation steps; the revised worker reports success on all three task types, and five of six external ratings prefer the workspace. The change alters the physical meaning of success. Coordination and favorable judgments can coexist with scientific-task drift. [Appendix G.3, PDF p.29](https://arxiv.org/pdf/2610.12176v1#page=29)

Other examples illustrate narrower conclusions: a revision repairs a feature-leakage problem but has a diagnostic that treats NaN correlations as passing; another checks a learned A* heuristic and retains an unfavorable result of roughly 5.1x more expanded nodes than Manhattan distance. The traces demonstrate supervised revisions, checks, and reporting. They do not establish that every check or repair is correct. [Appendix G.2-G.3, PDF pp.28-29](https://arxiv.org/pdf/2610.12176v1#page=28)

## Generalization is limited by task scope and reference selection

The private suite contains twelve synthetic long-horizon programming tasks in three domains. Only eight contribute the main first-cycle SFT data after one designated training task is excluded for failed workflow search. The three test tasks are held out from SFT, validation, and checkpoint selection, but are also used to evaluate workflow search. Thus the split is specifically a post-training split. [Appendix B.1/Table 3, PDF p.16](https://arxiv.org/pdf/2610.12176v1#page=16)

First-cycle private performance is heterogeneous: test tasks 60 and 207 have win shares 48.3% and 45.0%, while task 305 has 68.3%; one training task is only 20.0%. The 53.9% pooled three-test-task result should not become a claim that every domain improves. On six tasks, base-reference eligibility requires successful completion and at least 0.6 filename-based deliverable coverage. These are selected references, and student/reference index pairing need not match generation seeds. [Appendix C.2/Table 5, PDF pp.18-19](https://arxiv.org/pdf/2610.12176v1#page=19)

Public transfer is measured in one common qwen-code scaffold. MLR uses a twelve-task subset of a larger benchmark, and research runs use constrained CPU-only sandboxes. Terminal-Bench/SWE exclude tasks without a recorded verifier result for every model in each trial, with stated denominators. These conditions define the reported result and limit comparison with other scaffolds, task samples, or environments. [Appendix C.5, PDF pp.20-22](https://arxiv.org/pdf/2610.12176v1#page=20)

## Public score gains need their metric qualifications

The 1.2-1.6x headline is score per output token on four research benchmarks. It is not a uniform raw-score increase, a percentage-point improvement, or total-compute savings. Raw DSBench improvement is small and its first-generation score falls. Terminal-Bench and SWE raw pass rates decline across generations, and their token-normalized ratios also remain below one. [Figure 2, PDF p.3; Table 7, p.20](https://arxiv.org/pdf/2610.12176v1#page=3)

MLR/Asta aggregate gains accompany increased delivery. Means conditioned on delivered outputs are lower for later generations, but use different completed sets; they cannot be treated as a controlled comparison of paper/report quality. No MLR execution calls the delegation tool, so that benchmark does not identify learned delegation as the transfer mechanism. For MLR, trial-mean/delivery tests and paired task-mean sign tests yield different impressions: the latter has p=0.2266 for L(2) against either predecessor. The authors label these exploratory and say the evidence depends on the aggregation unit. [Appendix C.5, PDF p.21](https://arxiv.org/pdf/2610.12176v1#page=21)

Error bars are sample SD over trial means, not CIs. ScienceAgentBench reference programs pass only 80.4% in the local environment, limiting cross-environment comparison. Asta runs omit its literature-search tool; Appendix C.5 states that infrastructure interruptions are included but does not provide the promised details in this version. That missing accounting should remain an explicit unresolved source limitation. [Appendix C.5, PDF pp.20-21](https://arxiv.org/pdf/2610.12176v1#page=20)

## Training efficiency is suggestive, not a matched causal estimate

Figure 6 measures processed unmasked training targets through selected checkpoints. It excludes masked inputs, teacher generation, search, evaluation, validation, and later training updates. The six-H100 nineteen-hour figure is first-cycle SFT runtime including validation, not end-to-end cost. Multi-agent teacher execution itself averages about 2.4x the generated output tokens of eligible single-agent execution. A training-token advantage therefore does not demonstrate a total pipeline compute advantage. [Appendices B.2/D.2-D.3, PDF pp.17,22-24](https://arxiv.org/pdf/2610.12176v1#page=23)

The 68.3% M+ score pools four shared training tasks and one test task. It is not the first-cycle three-test-task score of 53.9%, and task 60 alone is 48.3%. M+ has broader training-task coverage, role-aware sampling, a different windows-per-step count, and validation-loss checkpoint selection. Smaller controls use other samplers and external-judgment checkpoint selection. The authors explicitly call M+ an unmatched-data comparison. These differences limit attribution of the observed advantage solely to multi-agent trajectory structure. [Appendix D.1/Table 8, PDF p.22](https://arxiv.org/pdf/2610.12176v1#page=22)

The 8.3/6.3-point gaps use a linearly interpolated reference, rather than actual single-agent students at the exact same budgets. M+ and S++ are compared through their scores against the base, not a direct head-to-head test. The latter's 42M targets versus M+'s 28.82M imply about 1.46x as many targets, or 31.4% fewer for M+; preserve the quantities rather than upgrading the approximate headline into a precise claim. [Appendix D.2, PDF p.23](https://arxiv.org/pdf/2610.12176v1#page=23)

The teacher-quality analysis is retrospective and conditional on successful completion and output-filename coverage. It reuses some opponents, differs in workflows/directive, and has only ten comparable-length pairs. Equal realized trace lengths do not impose equal generation budgets. The 85.1% overall preference (79.3% when weighting tasks equally) supports an advantage in the saved comparisons, while leaving delegation, verification instructions, selection, and workflow mixture entangled. [Appendix D.3/Table 9, PDF pp.23-24](https://arxiv.org/pdf/2610.12176v1#page=24)

## Workflow optimization remains noisy

A cumulative coverage curve records whether a task has ever reached six favorable external judgments. It can rise while the current workflow regresses. Figure 7's error bars vary judgments over the same executions, not independent searches, and each proposed workflow is executed once. Edit-size correlations therefore mix changes in prompts with runtime variability. [Section 5.1/Figure 7, PDF p.9; Appendix E.2, p.24](https://arxiv.org/pdf/2610.12176v1#page=24)

Task 53 supplies an unusually clear example: byte-identical workflow/rendered prompts with the same recorded generation seed yield opposite unanimous verdicts after the second execution halts in a loop. This does not estimate failure probability or identify the source of randomness, but it prevents interpreting every regression as evidence that an edit damaged the workflow. [Appendix E.3/Table 11, PDF pp.24-25](https://arxiv.org/pdf/2610.12176v1#page=25)

The frozen-executor transfer result supports better student-discovered workflows, yet discovery still used different generations as executor/evaluator. The optimizer bottleneck ablation concerns the speed of reaching successful workflows; the all-base condition still eventually reaches eleven of twelve tasks. Avoid a stronger claim that the base cannot discover good workflows or that evaluator capacity never matters. [Section 4.2/Table 1, PDF p.7; Section 5.1, p.9; Appendix C.3, pp.18-19](https://arxiv.org/pdf/2610.12176v1#page=19)

## Description statistics and behavioral counts do not prove the mechanism

Information-flow statistics are Gaussian embedding proxies of workflow descriptions, not observed messages. Whitening, shrinkage, chunking, and permutation adjustment shape the estimates. Task-centered total correlation subtracts task means; it is not exact conditional total correlation. The sample has 43-51 agents from only 8-9 eligible tasks, shared task text/hops, and excludes workflows still at the initial prompt. Values describe the retained path, not every proposal. One of four task-centered variants increases rather than decreases. These are descriptive patterns consistent with the hypothesis, rather than a causal test of why SFT improves performance. [Appendix F, PDF pp.25-27](https://arxiv.org/pdf/2610.12176v1#page=26)

The behavioral audit counts successful explicit tool operations. Reads via imports/shells and writes in shell scripts are not counted; a returned worker may report failure, a read may misuse an interface, and an edit may not repair anything. Five teachers and 100 windows fall outside the historical audit, making exposure counts lower bounds. Sampled handoff/revision episodes witness requisite actions, not necessarily entire trajectories. [Appendix G.1-G.2, PDF pp.26-28](https://arxiv.org/pdf/2610.12176v1#page=27)

The base already delegates/hands off reliably under a generic directive and can sometimes do so under a bare prompt. Increased bare-prompt counts therefore show greater spontaneous deployment of available patterns. They do not demonstrate newly acquired coordination capacity, map a student action to its causal training example, isolate optimized workflow text from the collection directive/sampler, or show that more revisions mean more successful repairs. [Appendix C.4, PDF pp.19-20; Appendix G.2, pp.27-28](https://arxiv.org/pdf/2610.12176v1#page=28)

## Source discrepancies

Section 4.2's ScienceAgentBench prose differs from Figure 3/Table 7 (28.7 -> 31.8 versus 28.8 -> 31.7); supplied trial counts support the latter. Figure 2's universal three-trial caption conflicts with MLR's five-trial specification. Figure 3's caption says two research benchmarks while showing six public rows. These are recorded as v1 source discrepancies, not silently corrected claims about a later version. [PDF pp.3,6,20](https://arxiv.org/pdf/2610.12176v1#page=20)

Section 4.1 (PDF p. 5) names 107 MLR-Bench tasks, while Appendix C.5/Table 7 (p. 20) defines the reported 12-task, five-trial subset. This companion follows the detailed appendix protocol and table, and preserves the main-text count as a discrepancy. The introduction names eight training tasks while the setup designates nine; Appendix B.1 resolves this as nine designated, one excluded, eight contributing SFT data.

The changing [official code README](https://github.com/SakanaAI/mass) displayed a 107-task, three-trial MLR result with different values at the verification date. It is a separately evolving primary source; its values are not substituted into the version-pinned PDF results. Resolving whether this represents a subsequent evaluation requires author clarification or a later paper version.

## Open questions

- Do further cycles improve or amplify judge-specific biases and scientific-task drift?
- Would matched task coverage, directives, sampling, checkpoints, and generation budgets preserve the multi-agent training advantage?
- Which coordination behaviors cause transfer, particularly on benchmarks where no delegation occurs?
- What is the total cost of search, teacher generation, judging, training, and evaluation?
- Can independent scientific checks detect task-changing revisions without restricting legitimate unfavorable outcomes?

These are companion questions, not findings established by this paper.
