# codex-loop-lab Design

## Goal

Create a deliberately small command-line Todo project for testing the workflow “ChatGPT Sol supervision → GitHub PR → Codex implementation → Sol review”. The first feature branch implements only `add` and `list`, leaving the PR open for a later review cycle.

## Constraints

- Python 3.11+
- No database and no web framework
- No third-party runtime dependencies
- Tests use pytest
- User-facing CLI output is Chinese
- Task IDs start at 1 and are never reused
- Existing CLI behavior must not change silently

## Design

`src/tasklist.py` is the only production module. It uses the Python standard library to load and save a JSON array of task objects. The default data file is `tasks.json` in the current working directory; tests override the path with `TASKLIST_DATA_FILE` so they never touch a user's real file.

The CLI accepts `add TITLE` and `list`. `add` appends a task with the next ID, `done: false`, and a Chinese confirmation. `list` prints each task with a Chinese status marker and prints a Chinese empty-state message when no tasks exist. No later Todo commands or architectural abstractions are included.

## Verification

Tests cover adding a task and persisting it, listing persisted tasks, and test data isolation through a temporary path. The full pytest suite must pass before the feature branch is pushed or a PR is created.
