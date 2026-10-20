# ADR 001: shared app boundary, stack and initial storage

Date: 20 October 2026. Status: accepted direction from the user's roadmap approval.

## Context

Individual homework contains React pack browsing and a C# feedback prototype. The
shared product must connect practice, multimodal extraction and grounded guidance.
Course requirements explicitly use Pydantic validation and pytest.

## Decision

Build a new shared app in `project/`: React/Vite plus Python/FastAPI/Pydantic. Keep
course evidence at root paths. Reuse homework ideas and reviewed content without
modifying individual submissions. Starter content is versioned; personal packs
will use browser localStorage. Answers/images are temporary. No database initially.

## Consequences

One backend language for all lab paths and offline tests, with a small Python
rewrite of feedback logic. Browser-only packs are device/origin-specific; clearing
browser storage loses them. Cross-device sync and persistent history are deferred.
Python dependency/runtime availability must be verified. The app remains local.
