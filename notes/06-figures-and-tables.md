# Figure and table reading guide

[Back to README](../README.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

These are original descriptions of source visuals inspected as rendered PDF pixels. No original figure image is redistributed. Open the linked exact-version PDF page to see the source.

## Figures

| Figure | Page | Reading guidance |
| --- | --- | --- |
| 1 | [1](https://arxiv.org/pdf/2610.12176v1#page=1) | Distinguishes the workflow feedback loop from the weight-update loop. All in-loop roles share the model. The stylized performance progression illustrates the intended loop; it is not a proof of future improvement. |
| 2 | [3](https://arxiv.org/pdf/2610.12176v1#page=3) | Six separate score-versus-output-token panels, with different scales. Dashed lines indicate L0 score per token; arrows label L0→L2 ratios. Research-panel ratios exceed one, software-panel ratios do not. Read Table 7 for exact units/trial counts; MLR has five trials despite the figure caption's general three-trial wording. |
| 3 | [6](https://arxiv.org/pdf/2610.12176v1#page=6) | Coverage counts tasks that have ever reached a unanimous external win, alongside model comparisons and evaluator agreement. Cumulative coverage cannot show whether the current iterate is stable. The table displays six public benchmarks despite the caption mentioning two. |
| 4 | [8](https://arxiv.org/pdf/2610.12176v1#page=8) | Changes in embedding-based task information relative to iteration 3. Role/instruction and contract/hop panels use different vertical scales. Four encoder/estimator configurations share the endpoint pattern; intermediate trajectories need not be monotonic. |
| 5 | [8](https://arxiv.org/pdf/2610.12176v1#page=8) | Redundancy changes relative to iteration 3. Unconditional estimates fall in all four configurations; task-centered permutation-adjusted MPNet rises. Do not erase this exception. |
| 6 | [8](https://arxiv.org/pdf/2610.12176v1#page=8) | Each point is a separately trained first-generation student. Horizontal position is processed supervised tokens through the selected checkpoint. The gray single-agent line is interpolation, not actual matched-budget training runs. |
| 7 | [9](https://arxiv.org/pdf/2610.12176v1#page=9) | The left panel's cumulative coverage rises while the right panel's current-iterate win shares can reverse. Its error bars describe judging variation over the same executions, not independent repetitions of search. |
| 8 | [25](https://arxiv.org/pdf/2610.12176v1#page=25) | Tracks retained workflow indices separately for finance, pharmacy, and robotics. Plateaus keep the incumbent while new proposals continue. The information analysis samples this retained path. |
| 9 | [29](https://arxiv.org/pdf/2610.12176v1#page=29) | Selected producer-write → producer-return → consumer-read dependencies on a robotics test task. Branches show dependencies and do not establish parallel execution. |

## Tables

| Table | Page | What it establishes and what to retain |
| --- | --- | --- |
| 1 | [7](https://arxiv.org/pdf/2610.12176v1#page=7) | Transfer of discovered workflows across execution weights; the 0.64 mean is across 11 iterations and 12 tasks. |
| 2 | [10](https://arxiv.org/pdf/2610.12176v1#page=10) | Bare-prompt structural events and audited teacher exposure. Event counts do not certify successful research or repairs. |
| 3 | [16](https://arxiv.org/pdf/2610.12176v1#page=16) | Nine designated training tasks, task 221 excluded, eight contributors, 119 training episodes, three held-out tasks. |
| 4 | [18](https://arxiv.org/pdf/2610.12176v1#page=18) | Separates search feedback, teacher ranking, checkpoint selection, and external reporting. |
| 5 | [19](https://arxiv.org/pdf/2610.12176v1#page=19) | Per-task first-cycle wins/losses. Test 53.9% = 97/(97+83); all-task 62.4% = 412/(412+248). |
| 6 | [19](https://arxiv.org/pdf/2610.12176v1#page=19) | Comparisons have different evaluation scopes; the 17.3% teacher comparison uses selected workflow-prompted teachers. |
| 7 | [20](https://arxiv.org/pdf/2610.12176v1#page=20) | Public results, units, scheduled counts, trial counts, and delivery counts. Read the adjacent metric definitions and exclusions. |
| 8 | [22](https://arxiv.org/pdf/2610.12176v1#page=22) | Teacher arms, stored/processed tokens, pooled five-task versus test-task-only scores. M+ differs in coverage and sampler. |
| 9 | [23](https://arxiv.org/pdf/2610.12176v1#page=23) | Teacher-output preference, reused episodes, and small retrospective length-matched subsets. Rows overlap. |
| 10–11 | [25](https://arxiv.org/pdf/2610.12176v1#page=25) | Weak edit-size association and an identical-workflow/seed reversal. One execution per proposed workflow does not isolate textual-edit effects. |
| 12–13 | [27](https://arxiv.org/pdf/2610.12176v1#page=27) | Absolute embedding-information and redundancy values behind Figures 4–5, including the MPNet exception. |
| 14 | [28](https://arxiv.org/pdf/2610.12176v1#page=28) | Base model already coordinates under a generic team directive; SFT increases bare-prompt deployment of that capability. |
| 15 | [39](https://arxiv.org/pdf/2610.12176v1#page=39) | Related-method mechanisms and feedback sources. Rows are not matched benchmark comparisons. |
