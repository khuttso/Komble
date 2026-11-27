# Pattern Journal · aniararis · Weeks 5–7

These reflections connect the three course patterns to the HW2 implementation
and verification performed on 27 November 2026. They do not claim that this work
was performed during the original teaching weeks. Review the reflections against
the code and test output before submitting them as a personal learning record.

## Week 5 · Tool Contract

**Reflection date: 27 November 2026.** The question lookup has a small capability:
read a named public starter pack and return at most four questions. Its fixed pack
names, bounded integer and forbidden extra fields make the allowed request clear.
The revealing experiment was changing `extra="forbid"` to `extra="ignore"`:
ordinary requests still worked, but the forged-identity golden case failed because
the unwanted field was silently accepted. A useful contract test must cover what
the tool refuses, not only what it returns. Next time, define the adversarial case
before implementing the wrapper, and verify it through every exposed interface.

## Week 6 · Session State

**Reflection date: 27 November 2026.** InterviewCoach separates public starter
content, personal packs in browser localStorage, and answer drafts in page memory.
The MCP tool deliberately reads only the public catalogue. Adding a `user_id`
argument would not create a trustworthy session or give the server legitimate
access to browser-only data. The same public lookup can therefore serve a visitor
without inventing authentication. A future personal-pack tool would need a real
server-side session and ownership check, plus tests that one session cannot read
another's data. The next design step would be to define that boundary before
adding storage or accepting identity information.

## Week 7 · Supervised Autonomy Loop

**Reflection date: 27 November 2026.** Delegating the tool implementation does not
remove the need to inspect its effects and evidence. Here the tool performs one
bounded read, makes no model call and has no automatic retry loop. The local red
experiment demonstrates a useful supervision checkpoint: a weakened rule must
stop the test suite before release. But a local failure does not prove GitHub
blocks a merge; the required check and branch protection must also be observed.
The next improvement is to complete the remote red/green experiment and inspect
the actual merge gate, keeping review and merge decisions separate from an
agent's report that the code works.
