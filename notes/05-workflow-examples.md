# Workflows and task examples

[Back to README](../README.md) · [Paper map](01-paper-map.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

These original explanatory notes accompany arXiv:2610.12176v1. They paraphrase selected task and workflow designs rather than reproducing the saved prompt blocks. A saved design describes intended execution; it is not a new implementation supplied by this repository.

## Three layers of an execution prompt

The paper separates the bare task, the workflow, and a fixed teacher-collection directive. The task defines the research problem and deliverables. The workflow defines specialist responsibilities, information contracts, routing, and repair paths. The collection directive specifies how to execute and verify actual worker calls. During dataset construction, the orchestrator's first message is replaced with the bare task, removing both the workflow and the collection directive; worker assignments remain. [§3, PDF pp. 4–5; Algorithm 3, p. 15; Appendices B.2–B.3, pp. 16–17](https://arxiv.org/pdf/2610.12176v1#page=4)

This separation prevents a common reading error. A bare prompt in this study is still a detailed research specification with named artifacts and execution/logging requirements. It does not mean a one-sentence question or an unconstrained agent. [Appendix H, PDF pp. 29–32](https://arxiv.org/pdf/2610.12176v1#page=29)

## Representative training tasks

| Task | Research objective | Central requirements | Source |
| --- | --- | --- | --- |
| Finance 51 | Predict short-horizon equity-index returns using macro events and cross-asset information, then assess a trading strategy | Time-based splits, event embargo, leakage analysis, transaction costs, risk targeting, ablations, and subperiod stability; reproducible code, metrics, report, manifest, and plots | H.1, pp. 29–30 |
| Pharmacy 202 | Predict protein-interface residues from public complex structures with geometric graph models | Distance-derived labels, evaluation across protein families, AUROC/AUPRC, geometric-feature ablations, pinned dependencies, and reproducible artifacts | H.2, pp. 30–31 |
| Robotics 307 | Generate instruction-following manipulation-planning data in simulation | Diverse scenes/instructions, executable generated plans, diversity and success metrics, schema documentation, code, report, manifest, and plots | H.3, pp. 31–32 |

These examples are training tasks, not the three synthetic post-training test tasks. The synthetic test identifiers are finance 60, pharmacy 207, and robotics 305. In particular, the task-305 tool-use example in Figure 9 differs from task 307's dataset-generation objective. [Table 3, p. 16; Appendix H, pp. 29–32; Figure 9, p. 29](https://arxiv.org/pdf/2610.12176v1#page=16)

## Retained search paths

Appendix I reports the retained paths through search iteration 11:

- Task 51: $w_0\rightarrow w_1\rightarrow w_8\rightarrow w_{10}$.
- Task 202: $w_0\rightarrow w_8$.
- Task 307: $w_0\rightarrow w_1\rightarrow w_{11}$.

Figure 8 (PDF p. 25) plots the incumbent version over search time. Plateaus show that later proposals were executed without displacing the incumbent; advances show replacement. The plotted path is neither every attempted workflow nor a guarantee of monotonically improving execution quality. Appendix I's two complete designs are selected examples, not a random sample or the full teacher-collection manifest. “Crown” refers to the retained best workflow in this lineage. [Algorithm 2, p. 15; Figure 8, p. 25; Appendix I, p. 32](https://arxiv.org/pdf/2610.12176v1#page=15)

## Finance workflow: seven roles connected by evidence

The task-51 $w_{10}$ design contains an orchestrator and six specialists: data ingestion/alignment, feature construction, predictive modeling, backtesting, research auditing, and report synthesis. A useful reading order follows the artifacts that each role needs, rather than treating the seven role descriptions as independent prompts. [Appendix I.1, PDF pp. 32–36](https://arxiv.org/pdf/2610.12176v1#page=32)

The intended forward flow is data/calendar acquisition → features and leakage checks → temporal model evaluation → backtests and ablations → cross-artifact audit → report/manifest. Output contracts transmit more than conclusions. They include artifact paths, split indices, feature columns, target-shift logic, masks for ablations, model configurations, predictions, metrics, and validation diagnostics. These interfaces aim to make later workers consume earlier workers' actual results. The auditor examines relationships across interfaces, such as agreement between reports and serialized metrics or consistency between costs and turnover. [Appendix I.1, PDF pp. 33–36](https://arxiv.org/pdf/2610.12176v1#page=33)

The reverse routes make the workflow iterative. A failed check is intended to identify the responsible role, narrow the repair, carry error context, and define acceptance criteria. Leakage can return to data/features; a trading problem can return through modeling to backtesting; report/metric inconsistency can return to synthesis. The orchestrator is instructed to track state and bounded recalls. This is a description of the saved design, not evidence that every collected execution correctly creates that state machine or obeys all gates. [Appendix I introduction and I.1, pp. 32–36](https://arxiv.org/pdf/2610.12176v1#page=32)

### Read the financial checks critically

Appendix I.1 warns that its thresholds and heuristics are optimizer proposals, not additional benchmark requirements or independently validated scientific criteria. Several checks aim at sensible concerns, such as finite metrics, temporal splits, and leakage. Others can reject legitimate research outcomes: equality of Pearson and rank correlations can occur without a bug; an ablation can have zero effect or improve performance; a valid predictor can produce an unfavorable measured signal. The workflow includes instructions to tune or recall when some outcomes fail expectations. **Companion interpretation:** such rules require scientific review rather than automatic adoption as correctness tests. [Appendix I.1, PDF pp. 32–35](https://arxiv.org/pdf/2610.12176v1#page=32)

## Pharmacy workflow: targeted repair and consistency checks

The task-202 $w_8$ design also contains seven roles: orchestrator, structural-data curator, graph/family-split builder, model architect, training/evaluation engineer, validator, and scientific writer. The intended phases move from real structures and labels to residue graphs and family splits, then model variants, validation, and programmatically generated reporting. [Appendix I.2, PDF pp. 36–38](https://arxiv.org/pdf/2610.12176v1#page=36)

The validator's contract identifies the failed worker, violated condition, and narrow repair scope. The orchestrator is supposed to recall that worker, then rerun validation before proceeding. This gives a concrete meaning to improved information routing: the feedback carries an actionable interface-level failure, rather than only a general criticism of the final report. The writer is expected to derive tables from machine-readable metrics so the narrative and measured values agree. [Appendix I.2, PDF pp. 36–38](https://arxiv.org/pdf/2610.12176v1#page=36)

### Inspect contradictions inside the saved design

The actual page-37 pixels confirm three consequential details. The data worker's acceptance rule asks for at least twenty PDB identifiers, yet a network-failure fallback specifies a list of ten. The training role introduces AUROC ≥0.80, whereas the bare task requires reporting AUROC/AUPRC without that success threshold. Split-related contracts also refer to test families through different producer roles even though the graph builder constructs the split. These are reasons to audit the saved interfaces; the paper does not present them as a validated specification. [H.2, PDF pp. 30–31; I.2, p. 37](https://arxiv.org/pdf/2610.12176v1#page=30)

**Companion interpretation:** a fallback can make progress while leaving an acceptance rule unsatisfied, and a requested score threshold can put pressure on a research workflow to seek favorable outcomes. A good reading companion should preserve these qualifications instead of converting the saved prompt into ready-to-run guidance.

## Multi-agent does not establish concurrent execution

The workflow text includes ambitions for parallel specialist work, but the fixed teacher-collection directive requires foreground worker calls and respects file dependencies. It permits multiple independent workers in one turn only when they write disjoint files. Figure 9 records producer-write → producer-return → consumer-read dependencies; its branches show dependencies, not concurrent execution. Do not infer speedups, asynchronous orchestration, or parallel trace semantics from the workflow diagrams alone. [Appendix B.3, PDF p. 17; Figure 9 and caption, p. 29; Appendix I, pp. 32–38](https://arxiv.org/pdf/2610.12176v1#page=17)

## What the guardrails can and cannot establish

The examples show useful organizational intentions: narrower worker assignments, explicit artifacts, bounded recalls, schema checks, provenance, and report/metric consistency. They remain instructions to the same model family that executes and judges the work. A returned worker may report failure; a read can use an interface incorrectly; an edit can fail to fix the problem. The behavioral audit counts execution events under explicit definitions, not scientific correctness of each event. [Appendix G.1, PDF pp. 26–27](https://arxiv.org/pdf/2610.12176v1#page=26)

The strongest concrete caution is the task-305 episode described in Appendix G.3. After failures, a revision changes simulated motion and the meaning of success; the resulting workspace still receives five favorable external judgments out of six. The paper uses this example to show that coordination and workspace preference do not guarantee preservation of the scientific task. [Appendix G.3, PDF pp. 28–29](https://arxiv.org/pdf/2610.12176v1#page=28)

## Questions to carry into the official source

- Does a repair preserve the original scientific question and evaluation criteria?
- Does the final workspace contain executed results, or only code and claimed checks?
- Can an output-contract field be traced to the actual producing artifact?
- Are a threshold or fallback part of the bare task, an optimizer proposal, or an analysis choice?
- Does teacher selection assess final workspaces or the quality of every supervised token?
- Is the workflow being discussed an attempted proposal, a retained incumbent, or a newly executed rollout under that incumbent?

These questions are companion analysis, not additional experimental findings or a proposed implementation.
