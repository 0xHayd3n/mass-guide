# Paper map and reading paths

[Back to README](../README.md) · [Method](02-method-and-notation.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

All references below are to **arXiv:2610.12176v1**. PDF page numbers are 1-based and coincide with the printed labels. The paper is a 39-page preprint. The notes explain and qualify the authors' work; they do not replace reading the source.

## Section map

| Paper location | PDF pages | What to read for |
| --- | --- | --- |
| Abstract and Figure 1 | [1](https://arxiv.org/pdf/2610.12176v1#page=1) | Author credit, headline claim, nested loops |
| §1 Introduction and Figure 2 | [2–3](https://arxiv.org/pdf/2610.12176v1#page=2) | Supervision bottleneck; quality and learning-efficiency hypotheses; benchmark overview |
| §2 Notations and problem statement | [3–4](https://arxiv.org/pdf/2610.12176v1#page=3) | Task, trajectory, workspace, role equality, external preference |
| §3 Method and Algorithm 1 | [4–5](https://arxiv.org/pdf/2610.12176v1#page=4) | Search, self-ranking, prompt removal, masked SFT |
| §4.1 Experimental setup | [5–6](https://arxiv.org/pdf/2610.12176v1#page=5) | Base model, fixed scaffold, private-task split, external panel |
| §4.2 Main results | [6–7](https://arxiv.org/pdf/2610.12176v1#page=6) | Two cycles; task solving, optimizer transfer, evaluator agreement |
| §4.3 Information flow | [7–8](https://arxiv.org/pdf/2610.12176v1#page=7) | Task-information proxies, contract/hop changes, redundancy |
| §4.4 Training efficiency | [7–9](https://arxiv.org/pdf/2610.12176v1#page=8) | Teacher controls; processed-token comparison; confounds |
| §§5.1–5.2 Ablations | [9–10](https://arxiv.org/pdf/2610.12176v1#page=9) | Optimizer bottleneck, instability, behavioral internalization |
| §§6–7 Related works and conclusion | [10](https://arxiv.org/pdf/2610.12176v1#page=10) | Empirical scope and relationship to prior methods |
| References; appendix contents | [10–14](https://arxiv.org/pdf/2610.12176v1#page=10) | Literature cited by the authors and appendix navigation |
| Appendix A Algorithms | [15](https://arxiv.org/pdf/2610.12176v1#page=15) | Complete search and internalization procedures |
| Appendix B Training data and optimization | [16–18](https://arxiv.org/pdf/2610.12176v1#page=16) | Exact split, teacher selection, window sampling, checkpoint and compute |
| Appendix C Evaluation and additional results | [18–22](https://arxiv.org/pdf/2610.12176v1#page=18) | Reporting unit, reference selection, public metrics and caveats |
| Appendix D Teacher composition and token accounting | [22–24](https://arxiv.org/pdf/2610.12176v1#page=22) | S/M/X controls, stored/processed/generated token distinction |
| Appendix E Search ablations and execution variability | [24–25](https://arxiv.org/pdf/2610.12176v1#page=24) | Coverage versus current performance, identical-workflow reversal |
| Appendix F Workflow-information estimates | [25–27](https://arxiv.org/pdf/2610.12176v1#page=25) | Embedding representations, estimators, non-causal interpretation |
| Appendix G Behavioral audit | [26–29](https://arxiv.org/pdf/2610.12176v1#page=26) | Event definitions, training exposure, useful and invalid revisions |
| Appendix H Representative task specifications | [29–32](https://arxiv.org/pdf/2610.12176v1#page=29) | Original computational-study requirements in three domains |
| Appendix I Complete workflow examples | [32–38](https://arxiv.org/pdf/2610.12176v1#page=32) | Concrete finance and pharmacy contracts and recall routes |
| Appendix J Related methods | [38–39](https://arxiv.org/pdf/2610.12176v1#page=38) | Mechanism comparison; absence of progress guarantees |

## Questions to carry through the paper

1. **What changes in each loop?** Search changes textual workflows with fixed weights; SFT changes shared weights. The scaffold stays fixed.
2. **Who supplies each signal?** Current-model workspace comparisons drive search and teacher ranking. Validation loss selects the main checkpoint. External judges report outcomes.
3. **What is a unit of evidence?** A task execution produces one workspace. Repeated judge seeds produce multiple assessments of that workspace pair.
4. **What does efficiency count?** Figure 2 uses output tokens; Figure 6 uses processed assistant training targets. Neither measures complete pipeline compute.
5. **What changed besides teacher structure?** Training-task coverage, selection, directives, and sampling vary in the controls.
6. **Does coordination preserve the task?** Appendix G includes a preferred robotics output whose revision changes the physical meaning of success.

## Reading routes

For a conceptual first pass, read §§1–3, Figure 3, then Appendices C.1 and J. For an evidence audit, start at C.5/Table 7, D/Tables 8–9, and G, then return to the headline figures. For training details, read A.2 and B before §4.4. For concrete orchestration, compare H's original task requirements with I's optimizer-added workflow instructions.

Related-work claims in this companion summarize how MASS's authors characterize prior methods in §6 and Appendix J. They are not independent reviews or matched performance comparisons of those papers.
