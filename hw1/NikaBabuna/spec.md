# Spec v1 · InterviewCoach Pack Hub

## Problem

Students preparing for interviews may not know which question set matches the role they want to practise for. They need a simple place to browse available interview packs and add their own question packs without setting up an account or database.

## Users

Students and recent graduates preparing for entry-level interviews. A user may want to practise a prepared pack or assemble questions they found elsewhere.

## Success criteria

A user can find a relevant locally available interview pack, inspect its questions, and add a personal pack that remains available after a browser refresh.

## Core feature

A Node.js web application provides an Interview Pack Hub.

The hub starts with at least three locally defined packs. Each pack has a title, target role, optional tags, and a short list of interview questions. A user can search the packs by title, role, or tag.

A user can add a personal pack through a form by entering a pack title, target role, optional comma-separated tags, and one or more questions entered one per line. Added packs are stored in browser `localStorage`.

Clicking a pack opens a preview with its metadata and questions. The pack can later be used by the separate interview-practice feature, but starting a practice session is outside this slice.

## Context list

- **Initial packs:** locally defined in the application; no external API or database.
- **Personal packs:** stored only in the browser through `localStorage`.
- **Search:** case-insensitive matching against title, target role, and tags.
- **Pack preview:** displays the selected pack's title, role, tags, question count, and questions.
- **Question format:** plain text; one question per line in the add-pack form.

## Acceptance criteria

1. The initial hub displays at least three locally defined interview packs with title, target role, tags, and question count.
2. A search term filters the visible packs by matching title, role, or tag without changing the stored data.
3. A user can add a pack only when its title, target role, and at least one non-empty question are present.
4. An added pack appears in the hub and is still available after a browser refresh.
5. Clicking a pack opens a preview showing its metadata and full question list.
6. The feature makes no external database, AI, or API request.

## Napkin math

A realistic homework mock might hold 20 packs with 10 questions each. At roughly 200 characters per question, that is:

20 packs × 10 questions × 200 characters = 40,000 characters

This is a small amount of local browser data, so `localStorage` is sufficient for the mock.

## Out of scope

- User accounts, sharing, or collaboration
- Cloud storage and databases
- File import/export
- AI-generated interview questions
- Starting or scoring an interview-practice session
- Answer feedback and OpenRouter integration
- Public deployment
