# Pattern Journal

Write one short personal entry for each week. These entries are yours; prompts are provided only as a starting point.

## Week 1

Week 1 was about getting the working environment ready before attempting project work. I completed the course setup checklist: a working runtime, GitHub access, one free OpenRouter call, and an agentic coding tool. The useful lesson was that setup should be verified early: a small check now is better than discovering a missing account, runtime, or tool during a timed lab.

## Week 2

Draft for my review: The pattern was Spec Before Code. For the Pack Hub, I agreed on a small scope and approved the specification before delegating the React implementation. Making search, required fields, and persistence explicit gave us concrete behavior to check. I would include the course's exact test command in the initial acceptance checklist next time; we had to add the `pytest` entry point after the first build.

## Week 3

Draft for my review: I reviewed the Uncertainty-Aware UX lab and its rule that missing evidence must not become a confident guess. Our Pack Hub work showed a related need for honest failure states: unreadable saved packs produce an explanation, while the original browser data is preserved. My individual feature does not extract images, and I have not completed the team's multimodal lab through this HW1 feature. Next time I would specify the storage-failure behavior alongside the successful flow before implementation.

## Week 4

Draft for my review: I reviewed Grounded Generation: answers must cite retrieved sources or refuse when support is missing. The Pack Hub has no generated answers, so this was a pattern I studied rather than a RAG feature I implemented. In our verification work, I saw why evidence matters: a passing build did not prove browser persistence, and an empty error console did not prove that no external request occurred. I would define how to collect each golden result earlier and keep incomplete checks visible instead of treating plausible behavior as a pass.
