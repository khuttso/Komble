# ADR 003: k=5 and a conservative threshold

Date: 20 October 2026. Status: implemented, agent-verified; teammate review pending.

Baseline: [k=3, threshold=0.55](../../evals/results/20261020T193019665098Z.json)
passed **2/5**. Three generated replies did not finish within the bounded output.
Optional reasoning was consuming the output budget. Disable it only when the
selected model advertises the parameter; preserve every failure. A subsequent
[k=3 run](../../evals/results/20261020T193214021939Z.json) remained **2/5**: two
answers were refused by citation checks and the reasoning case lacked its required
second source. Local retrieval ranked `behavioral-structure.md` fourth (0.7119)
for that question.

Decision: increase k from 3 to **5**, retain threshold **0.55**, and accept either
standard citation punctuation (`Claim [1].` or `Claim. [1]`) while still rejecting
unknown markers and uncited sentences. The [k=5 run](../../evals/results/20261020T193257001485Z.json)
passed **4/5 (80%)**. The truthful-achievements case still refused due to invalid
citations or grounded=false; preserve it as FAIL and inspect next.

Request settings and citation punctuation also changed between runs, so this is
not a controlled causal experiment attributing all improvement to k. Keep both
settings/results for review. The unrelated-question top score was 0.500, below
0.55; it refused without generation. Do not lower the threshold merely to pass.

Consequences: more context tokens; better coverage for the two-source case. The
threshold is supported by this small set only, not a general safety guarantee.
