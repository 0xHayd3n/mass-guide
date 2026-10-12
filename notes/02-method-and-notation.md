# Method and notation

[Back to README](../README.md) · [Paper map](01-paper-map.md) · [Results](03-results.md) · [Limitations](04-limitations.md)

These notes explain the method reported in *Recursive Self-Improvement through Multi-Agent Self-Supervision*, arXiv:2610.12176v1. They are an unofficial reading companion, not an implementation or reproduction. Page references count PDF pages and match the printed page numbers in this version.

## What changes in a MASS cycle?

MASS alternates two kinds of change. First, a fixed model searches for task-specific prompts that organize several copies of itself. Second, selected executions under those prompts supply supervised training data, changing the shared model's weights. The resulting model fills the executor, evaluator, and optimizer roles in the following cycle. The coding-agent harness, tools, and memory setup stay fixed in the paper's formal setting. This distinction matters: a better workflow prompt and a better trained model are separate outcomes. [§2, PDF pp. 3–4; §3, pp. 4–5; Appendix A, p. 15](https://arxiv.org/pdf/2610.12176v1#page=3)

Figure 1 (PDF p. 1) depicts the inner feedback loop as workspace execution → self-evaluation → workflow revision. Its outer transition represents training on the resulting executions. The increasing model-performance sketch is a conceptual overview, not a proof that further cycles must keep improving. Appendix J explicitly characterizes the recursive loop as empirical. [Figure 1, p. 1; Appendix J, pp. 38–39](https://arxiv.org/pdf/2610.12176v1#page=1)

## Notation lookup

| Symbol | Meaning | Why the distinction matters |
| --- | --- | --- |
| $\mathcal T$, $\mathcal T_{\mathrm{train}}$, $\mathcal T_{\mathrm{test}}$ | Task collection, training subset, and disjoint test subset | The synthetic test tasks are excluded from SFT, validation, and checkpoint selection; workflow search is also evaluated on them. |
| $t$, $x_t$ | A task and its textual specification | A bare task can already contain extensive deliverable and execution requirements. |
| $\mathcal L_\theta$ | Language model with parameters $\theta$ | Its distribution is $p_\theta(z_\ell\mid z_{<\ell})$. |
| $\mathcal A(\cdot;\mathcal L)$ | Coding agent using model $\mathcal L$ | The agent includes the fixed harness, rather than only a text-completion model. |
| $(\tau_t,y_t)$ | Execution trajectory and resulting deliverable workspace | A judge ranks workspaces; the associated conversations become training data. |
| $\oplus$ | Prompt concatenation | $\mathcal A(x_t\oplus w_t;\mathcal L)$ runs the task with an added workflow. |
| $\mathcal L_{\mathrm{agent}}$, $\mathcal L_{\mathrm{eval}}$, $\mathcal L_{\mathrm{opt}}$ | Executor, in-loop evaluator, and workflow optimizer | These share current weights in the homogeneous condition. |
| $\mathcal L_{\mathrm{ext}}$ | External strong-model evaluator | It reports final quality; its judgments do not train the main MASS loop or select its checkpoint. |
| $y_1\succ y_2$ | The specified judge prefers workspace $y_1$ | Preference is an evaluation outcome, not a mathematical proof of correctness. |
| $d_{t,i}$, $D_t$ | Feedback at search iteration $i$, and its task-specific history | Feedback from losing proposals can still influence later proposals. |
| $g$, $R$ | Model generation and total MASS cycles | The reported experiment runs two cycles. |
| $i$, $I$ | Workflow-search iteration and its budget | These are distinct from weight-training steps and generations. |
| $w_t^*$, $y_t^*$ | Retained workflow and the workspace that earned its incumbent status | The star denotes the best retained result under sequential self-comparisons. |
| $M$, $K$ | Candidate runs per training task and number selected including validation | Ranks 1 through $K-1$ enter training; rank $K$ enters validation. |
| $z$, $L_{\max}$ | A training window and maximum window length | Long conversations are split; preceding context can remain available without carrying loss. |
| $\mu_\ell$, $q$ | Assistant-target loss mask and window sampling distribution | Which tokens receive loss and how windows are drawn both affect the effective training signal. |

Sources: [§2, pp. 3–4; §3, pp. 4–5; Algorithms 2–3, p. 15; Appendices B.1–B.2, pp. 16–17](https://arxiv.org/pdf/2610.12176v1#page=3).

## Workflow representation

The paper writes a workflow as

$$w_t=\{\mathbf h_t,(\mathbf r_{t,j},\mathbf u_{t,j},\mathbf c_{t,j})_{j=1}^{m_t}\}.$$

Here $m_t$ is the number of workers, $\mathbf r$ specifies roles, $\mathbf u$ gives local instructions, $\mathbf c$ describes what a worker returns, and $\mathbf h$ specifies call order. The search prompt prioritizes call order and output contracts over rewriting role names or instructions. The proposal is a textual specification consumed by the orchestrator; this notation should not be read as a separately implemented, formally verified computation graph. [§3, PDF pp. 4–5](https://arxiv.org/pdf/2610.12176v1#page=4)

## Stage 1: fixed-weight workflow search

1. For each task, execute an initial workflow and retain its workspace as the first incumbent.
2. Give the optimizer the previous workflow, retained workflow, task-specific feedback history, and optimization instructions.
3. Execute the new proposal using the current model.
4. Compare its deliverable workspace with the retained workspace using the same model as evaluator.
5. Add the verdict and rationale to history. Replace the incumbent only when the new workspace is preferred.
6. Continue to the search budget and return the retained workflow for each task.

This is an evolutionary analogy with one elite incumbent. Every proposal is executed, including proposals that do not replace it. The next execution can be worse than the previous one. The paper explicitly qualifies the word “optimal”: $w_t^*$ is retained through sequential self-evaluation, not certified as a global optimum. [§3, p. 5; Algorithm 2 and surrounding text, p. 15](https://arxiv.org/pdf/2610.12176v1#page=5)

A judge compares outputs, not workflow text alone. Stochastic execution and runtime behavior therefore affect the search signal. Appendix E.3 records two executions of byte-identical workflow and rendered-prompt text that receive opposite external verdicts; a later run halts after repeated identical shell calls. This example is evidence of execution variability, not an estimate of a workflow's reliability across repeated trials. [Appendices E.1–E.3 and Table 11, PDF pp. 24–25](https://arxiv.org/pdf/2610.12176v1#page=24)

## Stage 2: collect, rank, and train

For each retained training workflow, execute $M$ independent candidate runs. The self-evaluator compares their deliverable workspaces within the task, and Bradley–Terry scores turn pairwise preferences into a ranking. Select the top $K-1$ associated trajectories for training and the next for validation. The paper describes a pairwise tournament; these notes do not assume an undocumented all-pairs schedule or implementation of the ranking model. [§3, p. 5; Algorithm 3, p. 15; Appendix B.1, p. 16](https://arxiv.org/pdf/2610.12176v1#page=5)

For the reported first-cycle dataset, $M=18$ and $K=16$: fifteen ranks per task are assigned to training and rank sixteen to validation. Nine tasks were designated for training, but task 221 did not obtain a workflow that beat its reference and supplied no teacher data. Across the remaining eight tasks, one prematurely terminated run on task 56 was removed, leaving 119 training trajectories. Validation uses different trajectories from those same training tasks; it is not a held-out-task evaluation. [§4.1, pp. 5–6; Appendix B.1 and Table 3, p. 16](https://arxiv.org/pdf/2610.12176v1#page=5)

Before rendering training conversations, replace the orchestrator's initial task-plus-workflow-plus-collection-directive prompt with the bare task. Keep worker assignments. The data consequently demonstrate delegation and execution without requiring the orchestrator's initial input to restate the optimized team. This is the setup for testing internalization; it does not remove all workflow-related information from the recorded worker conversations. [Algorithm 3, p. 15; Appendices B.2–B.3, pp. 16–17](https://arxiv.org/pdf/2610.12176v1#page=15)

## The loss mask and sampling distribution

The objective is masked, per-window average negative log-likelihood:

$$\ell_{\mathrm{SFT}}(\theta)=-\mathbb E_{z\sim q}\left[\frac{\sum_{\ell=1}^{|z|}\mu_\ell\log p_\theta(z_\ell\mid z_{<\ell})}{\sum_{\ell=1}^{|z|}\mu_\ell}\right].$$

Assistant reasoning, text, and tool calls carry loss. System/user messages, tool outputs, and overlapping preceding context are masked. Masking excludes a token from the training target; it does not necessarily remove that token from the model's conditioning context. Windows have at most 49,152 total tokens, including up to 8,192 preceding-context tokens. [§3, p. 5; Appendix B.2, p. 16](https://arxiv.org/pdf/2610.12176v1#page=5)

The stored first-cycle data contain 2,435 windows: 282 orchestrator, 2,054 worker, and 99 auxiliary windows, with 17,221,055 supervised tokens. On each draw, select a task uniformly, select an orchestrator group with probability 1/3 or a worker/auxiliary group with probability 2/3, then sample a window within that group uniformly with replacement. The advertised two nominal epochs set a draw budget; they do not guarantee two visits to every stored window. The expectation over $q$ is therefore not simple uniform coverage of all tokens. [Appendix B.2, PDF p. 16](https://arxiv.org/pdf/2610.12176v1#page=16)

The first cycle trains a BF16 parent with a fresh LoRA adapter (rank 64, scaling factor 128, dropout 0.05) for 1,624 optimizer steps, three windows per step. The checkpoint selected by the lowest masked validation loss is step 1200; its adapter is merged and the model quantized to block-FP8 for inference. External workspace judgments do not select this checkpoint. The second cycle starts a fresh adapter on the merged first-cycle model and follows the same recipe as closely as possible. These are reported settings, not experiments performed in this companion. [Appendix B.2, pp. 16–17](https://arxiv.org/pdf/2610.12176v1#page=16)

## Method qualifications

- The in-loop evaluator judges final workspaces. Selecting a good-looking workspace does not establish that every assistant target in its trajectory is correct or beneficial to imitate.
- The optimizer, executor, and self-evaluator share learned priors. Multi-agent organization changes their interaction, but does not supply an independent truth oracle.
- Validation loss selects an imitation checkpoint on other runs of the same training tasks. A decrease in that loss is distinct from better external workspace preference or scientific validity.
- “Structural guardrails” describe a search emphasis and task-specific workflow instructions in this paper. Neither the algorithms nor the reproduced workflows establish a formal correctness guarantee.
- Only two recursive cycles are evaluated. Appendix J explicitly disclaims a guarantee that future generations improve.

The first three points explain the reported procedure's practical implications; the lack of formal guarantees is also explicit in [§6, p. 10; Appendices D.3, p. 24, and J, pp. 38–39](https://arxiv.org/pdf/2610.12176v1#page=10).

## Relationship to related methods

Appendix J organizes prior work by the mechanism that changes: prompt/program/harness search, weight updates, and the source of feedback. MASS combines workflow search with supervised updates of weights shared by orchestrator and workers. Its comparisons with RHI, TTHE, SIA, HASE, HELIX, and other methods identify reported mechanisms; they are not matched performance experiments. A shared model across several roles does not by itself imply weight learning, and exporting data for future training does not demonstrate a trained successor. [Appendix J and Table 15, PDF pp. 38–39](https://arxiv.org/pdf/2610.12176v1#page=38)
