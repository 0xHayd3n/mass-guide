# Results and evidence

[Back to README](../README.md) · [Paper map](01-paper-map.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

These are original reading notes on the authors' reported experiments in *Recursive Self-Improvement through Multi-Agent Self-Supervision*, arXiv 2610.12176v1. They do not report a reproduction. Page references refer to the 39-page v1 PDF; the printed and PDF page numbers agree.

## Read the evaluation units first

MASS improves a shared model through two reported cycles, L(0) -> L(1) -> L(2). In each homogeneous cycle, the current model executes the task, compares workspaces, and proposes workflows. The external GPT-5.5/Claude Opus 4.8 panel is used for reporting after execution; its judgments and rationales are withheld from the agents and workflow optimizer. Validation loss selects the main MASS checkpoint. A separate control study uses external judgments for checkpoint selection, so it should not be conflated with the homogeneous training loop. [Section 4.1, PDF pp.5-6; Appendix C.1, p.18](https://arxiv.org/pdf/2610.12176v1#page=18)

For private-task comparisons, win share means W/(W+L), excluding ties. Each workspace pair normally receives six judgments: two reporting models, each with three seeds. These are six assessments of the same two outputs, not six separate agent executions. The paper reports descriptive shares and expressly avoids treating the number of judgments as evidence of statistical significance. Public-benchmark scores use their own task metrics; they are not these pairwise win shares. [Appendix C.1, PDF p.18](https://arxiv.org/pdf/2610.12176v1#page=18)

## Private research tasks: separate three scopes

The private suite has twelve synthetic research-programming tasks, four each in finance, pharmacy, and robotics. Nine are designated for training, but task 221 is excluded because workflow search does not beat its reference. Eight tasks contribute SFT episodes. The three post-training test tasks are excluded from SFT, validation, and checkpoint selection; search itself is also evaluated on them. [Section 4.1, PDF p.5; Appendix B.1/Table 3, p.16](https://arxiv.org/pdf/2610.12176v1#page=16)

| Scope | L(1) vs L(0) | L(2) vs L(0) | L(2) vs L(1) |
|---|---:|---:|---:|
| Eight private training tasks | 65.6% | 82.5% | 68.1% |
| Three private test tasks | 53.9% | 69.9% | 60.8% |

Source: [Section 4.2/Figure 3b, PDF p.6](https://arxiv.org/pdf/2610.12176v1#page=6). The three-task held-out aggregate is the source of the 53.9% -> 69.9% result. It is not the 68.3% value used in the training-efficiency comparison below.

Appendix C gives more detail for the first cycle. Ten bare-prompt student rollouts are paired by index with ten fixed bare-base references per task; index matching does not mean equal generation seeds. For six tasks outside the common control set, eligible references are selected for completion and at least 0.6 coverage of expected output filenames. Loop halts remain outcomes; API-error interruptions are retried. The results therefore describe performance against this fixed reference set. [Appendix C.2, PDF p.18](https://arxiv.org/pdf/2610.12176v1#page=18)

| First-cycle task | Split | Wins-losses-ties | Win share |
|---|---|---:|---:|
| 51: macro signals/trading | Train | 53-7-0 | 88.3% |
| 53: monetary-policy trading | Train | 52-8-0 | 86.7% |
| 56: yield-curve strategies | Train | 38-22-0 | 63.3% |
| 202: protein interfaces | Train | 44-16-0 | 73.3% |
| 205: force-field validation | Train | 12-48-0 | 20.0% |
| 302: learned planning heuristics | Train | 45-15-0 | 75.0% |
| 307: manipulation datasets | Train | 33-27-0 | 55.0% |
| 324: navigation subgoals | Train | 38-22-0 | 63.3% |
| 60: trading costs/capacity | Test | 29-31-0 | 48.3% |
| 207: inverse folding | Test | 27-33-0 | 45.0% |
| 305: manipulation tool use | Test | 41-19-0 | 68.3% |
| Eight training tasks pooled | Train | 315-165-0 | 65.6% |
| Three test tasks pooled | Test | 97-83-0 | 53.9% |
| All eleven included tasks | Both | 412-248-0 | 62.4% |

Source: [Appendix C.2/Table 5, PDF p.19](https://arxiv.org/pdf/2610.12176v1#page=19). Each task has ten execution pairs and sixty judgments. The pooled improvement is uneven: two of the three test tasks remain below 50% in the first cycle, as does training task 205.

The first-cycle student also has a 17.3% share against selected ranked team teachers (112 wins, 536 losses, 108 pairs). This comparison uses workflow-prompted teachers, including selected test workflows generated only for evaluation. Two halted task-207 references reduce the total from 110 to 108. This measures a remaining gap to selected teacher outputs, rather than a comparison between bare-prompt model generations. [Appendix C.2/Table 6, PDF pp.18-19](https://arxiv.org/pdf/2610.12176v1#page=19)

## Public transfer: metric values and evaluated scope

All three generations use qwen-code 0.20.0, the same tools including delegation, and benchmark instructions without an optimized MASS workflow. Sampling is temperature 0.6, top-p 0.95, top-k 20, reasoning enabled, a 262,144-token context limit, and up to 32,768 output tokens per request. Generation seeds are matched within each task/trial; timeouts remain final outcomes. [Appendix C.5, PDF p.20](https://arxiv.org/pdf/2610.12176v1#page=20)

| Benchmark and aggregate metric | Evaluated scope | L(0) | L(1) | L(2) |
|---|---|---:|---:|---:|
| ScienceAgentBench success (%) | 102 tasks x 3 trials | 28.8 +/- 1.5 | 30.4 +/- 2.0 | 31.7 +/- 2.0 |
| MLR-Bench overall (0-10 aggregate) | 12-task subset x 5 trials | 1.58 +/- 0.38 | 1.80 +/- 0.30 | 2.40 +/- 0.28 |
| AstaBench E2E-Bench-Hard rubric | 40 tasks x 3 trials | 0.053 +/- 0.002 | 0.055 +/- 0.004 | 0.067 +/- 0.017 |
| DSBench normalized score | 74 data-modeling tasks x 3 trials | 0.473 +/- 0.029 | 0.465 +/- 0.011 | 0.482 +/- 0.025 |
| Terminal-Bench 2.0 pass (%) | 89 scheduled tasks x 3 trials | 37.5 +/- 2.2 | 35.3 +/- 2.1 | 35.2 +/- 1.7 |
| SWE-bench Verified pass (%) | 500 scheduled tasks x 3 trials | 62.6 +/- 1.4 | 61.8 +/- 1.9 | 61.1 +/- 0.6 |

Source: [Appendix C.5/Table 7, PDF pp.20-22](https://arxiv.org/pdf/2610.12176v1#page=20). Uncertainty is sample standard deviation over trial means, not a standard error or confidence interval. Terminal-Bench scores only jointly recorded verifier outcomes: 86, 88, and 87 tasks across trials. SWE uses 499, 499, and 496. The table's 89/500 counts describe scheduled tasks.

The benchmark metrics answer different questions:

- **ScienceAgentBench:** the official dockerized evaluator executes the submitted program and checks task outputs. Runs have a thirty-minute agent limit. The authors' reference-program environment check succeeds on 80.4%, with failures attributed to package differences or the 900-second evaluator limit; scores are descriptive and environment dependent.
- **MLR-Bench:** the agent proposes, implements, and writes up research within two hours, three CPU cores, 16 GB RAM, and no GPU. GPT-5.5 and Claude Opus 4.8 use the official MLR-Judge overall-review rubric; delivered work is judged on 1-10, while missing or sub-200-byte papers receive zero. This makes the aggregate scale 0-10.
- **AstaBench:** a two-hour CPU-only experiment/report task, scored by the official Claude Sonnet 4.6 rubric judge as the fraction of checklist items satisfied. Missing reports receive zero. The scaffold omits the benchmark's literature-search tool.
- **DSBench:** one-hour CPU-only modeling tasks; the official competition metric is normalized so baseline=0 and best-human reference=1. Negative normalized values are clipped to zero; missing/invalid predictions are zero. This score is not an accuracy percentage.
- **Terminal/SWE:** official hidden tests or issue-repair tests determine binary outcomes, with benchmark-specific container/time limits and joint-result exclusions.

Definitions and limits: [Appendix C.5, PDF pp.20-22](https://arxiv.org/pdf/2610.12176v1#page=21).

### Completion explains part of the research-score pattern

MLR paper delivery increases from 31/60 to 36/60 to 50/60. Among delivered papers, mean score is 3.07, 3.00, and 2.88. Asta report delivery rises from 60/120 to 69/120 to 91/120; delivered-report means are 0.105, 0.095, and 0.088. Because these conditional means concern different sets of completed tasks, neither sequence establishes a quality decline on a common completed set. They do show that improved aggregate scores accompany more completed outputs. None of the 180 MLR executions calls the delegation tool, so delegation is not established as the mechanism of that public transfer. [Appendix C.5, PDF p.21](https://arxiv.org/pdf/2610.12176v1#page=21)

For MLR, the authors report exploratory tests. L(2) versus L(0)/L(1) has Welch p=0.0053/0.0109 on trial means and Fisher p=0.0004/0.0079 on pooled delivery counts. Yet paired task-mean sign tests give p=0.2266 for both comparisons; the L(1)-L(0) values are 0.3430, 0.4623, and 0.5488 respectively. Repeated tasks in pooled counts and unused seed matching in Welch tests limit interpretation. The source explicitly says evidence depends on the aggregation unit and does not establish consistent gains across tasks. [Appendix C.5, PDF p.21](https://arxiv.org/pdf/2610.12176v1#page=21)

### What the 1.2-1.6x headline measures

Figure 2 compares score divided by generated output tokens per task, for L(2) versus L(0). Its reported ratios are MLR 1.60x, DSBench 1.35x, ScienceAgentBench 1.20x, and AstaBench 1.28x. Terminal-Bench and SWE ratios are 0.96x and 0.94x. These are token-normalized inference scores, not uniform accuracy improvements or end-to-end compute savings. DSBench illustrates the distinction: raw mean score changes only 0.473 -> 0.482 while its reported score/token ratio is 1.35x. [Figure 2, PDF p.3](https://arxiv.org/pdf/2610.12176v1#page=3)

Source discrepancies: Section 4.2 prose gives ScienceAgentBench 28.7 -> 31.8%, whereas Figure 3/Table 7 and the supplied trial counts support 28.8 -> 31.7%; the table values are used here. Figure 2's caption says three trials universally, while Appendix C.5 specifies five for MLR. Figure 3's caption says two research benchmarks despite displaying six public benchmark rows. Appendix C.5 mentions Asta infrastructure interruptions but does not supply their promised details in this version. [PDF pp.3,6,20-21](https://arxiv.org/pdf/2610.12176v1#page=20)

## Training efficiency: targets processed, not total compute

The first-cycle main student M+=L(1) comes from 119 selected trajectories on eight tasks. These contain 2,435 stored windows (282 orchestrator, 2,054 worker, 99 auxiliary) and 17,221,055 supervised assistant tokens. Task/role sampling with replacement uses an orchestrator probability of 1/3 and worker/auxiliary probability of 2/3. A nominal epoch is a draw budget, rather than a guaranteed visit to each stored window. [Appendix B.2, PDF p.16](https://arxiv.org/pdf/2610.12176v1#page=16)

| Independent first-generation student | Episodes | Stored supervised tokens (M) | Processed targets at selected checkpoint (M) | Win share on five common tasks |
|---|---:|---:|---:|---:|
| S: single-agent | 17 | 0.90 | 1.82 | 44.0% |
| M: multi-agent | 17 | 2.27 | 3.64 | 56.0% |
| X: S union M | 34 | 3.17 | 8.85 | 58.8% |
| S+: larger single-agent | 78 | 4.43 | 9.11 | 59.0% |
| S++: largest single-agent | 290 | Unreported | 42.00 | 64.0% |
| M+: main MASS first cycle | 119 | 17.22 | 28.82 | 68.3% |

Source: [Appendix D.1/Table 8, PDF p.22](https://arxiv.org/pdf/2610.12176v1#page=22). The evaluation pools tasks 51, 53, 56, and 307 (training) plus task 60 (test). It is not test-only performance. M+ scores 73.3% on those four training tasks and 48.3% on task 60 alone. X has 49 evaluated pairs; other reported arms have 50 where specified.

M+ exceeds S++ by 4.3 percentage points in these scores against the base, with 31.4% fewer processed targets (28,818,370 versus 42,000,000; the larger budget is about 1.46x). Figure 6 also reports gaps of 8.3 points for M and 6.3 for M+ against a linearly interpolated reference joining S, S+, and S++. No single-agent student was measured at those exact budgets, and M+ versus S++ is not direct head-to-head. Processed tokens omit masked inputs, validation, teacher collection, workflow search, evaluation, and updates after the selected checkpoint. The full M+ run processes 39,465,522 targets. [Section 4.4, PDF p.8; Appendix D.2, pp.22-23](https://arxiv.org/pdf/2610.12176v1#page=23)

The arms share a parent/adapter architecture/core recipe but differ in task coverage, sampling, windows per step, and checkpoint selection. M+ is explicitly not a matched-data control. The reported six-H100, roughly nineteen-hour first-cycle time refers to SFT including validation, not the entire MASS pipeline. [Appendices B.2/D.1, PDF pp.17,22](https://arxiv.org/pdf/2610.12176v1#page=22)

## Workflow, evaluator, and behavioral evidence

Post-training is on task-solving trajectories, yet Figure 3 reports faster discovery of workflows attaining unanimous external wins and evaluator agreement rising 0.73 -> 0.91 -> 0.93. This agreement is against the external panel, not an independently verified scientific truth criterion. [Section 4.2/Figure 3, PDF pp.6-7](https://arxiv.org/pdf/2610.12176v1#page=6)

Holding execution weights at L(0), student-discovered workflows have mean win share 0.64 against base-discovered workflows. Table 1 averages per-iteration shares across eleven iterations, each covering twelve tasks with one execution per task. Discovery itself still used each generation's executor and evaluator, so this isolates execution weights during transfer, rather than all search causes. [Table 1/Appendix C.3, PDF pp.7,18-19](https://arxiv.org/pdf/2610.12176v1#page=19)

The stronger optimizer/evaluator ablation reaches successful workflows earlier than evaluator replacement alone. All-L(0) nevertheless eventually reaches an ever-observed 6/6 win on eleven of twelve tasks. Cumulative coverage measures reachability; it does not guarantee that the current iterate remains good. Table 10 finds weak Spearman edit-size association (absolute correlations <=0.12). Two identical task-53 workflows and rendered prompts with the same recorded seed produce a complete 6-0 win and a loop-halt 0-6 loss, illustrating execution variability rather than a repeated reliability estimate. [Section 5.1/Figure 7, PDF p.9; Appendix E, pp.24-25](https://arxiv.org/pdf/2610.12176v1#page=24)

Information analysis of retained workflows uses embedding-based Gaussian proxies, not runtime messages. Across iterations 3 to 11, role/instruction task specificity falls and contract/hop specificity rises. Unconditional total correlation falls in all four encoder/adjustment variants; task-centered correlation falls in three, with permutation-adjusted MPNet rising 2.39 -> 2.57 nats. Samples contain only 43-51 agents from 8-9 tasks, with repeated descriptions/hops. The result is descriptive support for the information-flow hypothesis. [Section 4.3/Figures 4-5, PDF pp.7-8; Appendix F/Tables 12-13, pp.25-27](https://arxiv.org/pdf/2610.12176v1#page=27)

| Bare-prompt behavior | L(0) | L(1) | L(2) |
|---|---:|---:|---:|
| Returned delegation | 1/110 | 48/110 | 87/110 |
| Recorded cross-worker Python handoff | 1/110 | 42/110 | 83/110 |
| Worker revision of earlier worker code | 0/110 | 10/110 | 39/110 |
| Orchestrator edit of worker code | 1/110 | 14/110 | 12/110 |

Source: [Section 5.2/Table 2, PDF pp.9-10](https://arxiv.org/pdf/2610.12176v1#page=10). These are explicit trace events, not correctness scores. With an explicit generic team directive, the base already delegates 110/110 times and handoffs 103/110, so training increases spontaneous use of available coordination patterns. The first-cycle teacher audit covers 114/119 teachers and finds 98 handoff episodes and 57 revision episodes, of which 79 and 37 have the requisite targets sampled. It does not attribute a student action to a particular teacher example. [Appendix G, PDF pp.26-28](https://arxiv.org/pdf/2610.12176v1#page=28)

Finally, the retrospective teacher-output analysis reports 85.1% multi-agent preference over 206 pairs, and 80.0% over ten comparable-length pairs. Multi-agent eligible-pool mean generated length is 141,844 versus 59,355 (2.39x). Workflow mixes, directive differences, reused opponents, and successful-completion filtering remain confounds; matching realized length is not an equal imposed generation budget. [Appendix D.3/Table 9, PDF pp.23-24](https://arxiv.org/pdf/2610.12176v1#page=23)
