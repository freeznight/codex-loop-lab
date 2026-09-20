# codex-loop-lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the minimal Chinese CLI Todo project and implement only the first-round `add` and `list` commands.

**Architecture:** Keep one production module, `src/tasklist.py`, backed by a JSON array in a configurable file path. Test the CLI entry point with pytest and a temporary `TASKLIST_DATA_FILE` path so real user data is never touched.

**Tech Stack:** Python 3.11+, Python standard library, pytest for tests.

**Spec:** `docs/superpowers/specs/2026-09-20-codex-loop-lab-design.md`

## Global Constraints

- Python 3.11+
- No database and no web framework
- No third-party runtime dependencies
- Tests use pytest
- User-facing CLI output is Chinese
- IDs are permanent and must never be reused
- Do not silently change existing CLI behavior
- Implement only `add` and `list` in this PR

## Review Focus

- A missing data file should behave as an empty task list; test this through the first `add`.
- A second `add` must continue IDs from the persisted maximum; test persistence and incrementing.
- `list` must read the saved JSON and render Chinese output; test both empty and populated output.
- Tests must use a temporary path rather than the default `tasks.json`; test setup must prove isolation.
- Unsupported later commands must not be added; review the CLI parser and PR diff for scope.

### Task 1: Main branch project baseline

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `src/tasklist.py`

**Interfaces:**
- Produces the project metadata, documentation, and empty production-module location used by Task 2.

- [ ] **Step 1: Create the baseline files**

Create the exact long-term rules in `AGENTS.md`, describe the project and JSON task shape in `README.md`, configure Python 3.11 and pytest test discovery in `pyproject.toml`, ignore generated files, and leave `src/tasklist.py` as a module docstring only so no first-round behavior exists on `main`.

- [ ] **Step 2: Verify the baseline shape**

Run `Get-ChildItem -Recurse -File | Select-Object FullName` and confirm the requested baseline files exist, with no database, framework, or runtime dependency declared.

- [ ] **Step 3: Commit the baseline**

Run:

```powershell
git add AGENTS.md README.md pyproject.toml .gitignore src/tasklist.py
git commit -m "chore: initialize codex loop lab"
```

### Task 2: First-round add and list

**Files:**
- Modify: `src/tasklist.py`
- Create: `tests/test_tasklist.py`
- Modify: `README.md`

**Interfaces:**
- Consumes the baseline module path and pytest configuration from Task 1.
- Produces `main(argv: list[str] | None = None) -> int`, plus the `add` and `list` CLI behavior used by the tests.

- [ ] **Step 1: Create failing tests for add and list**

Write pytest tests that set `TASKLIST_DATA_FILE` to `tmp_path / "tasks.json"`, call `tasklist.main(["add", "买牛奶"])`, assert Chinese confirmation, assert the JSON object has `id: 1`, `title: "买牛奶"`, and `done: False`, then add a second task and assert `id: 2`. Add a list test that writes two task objects to the temporary file, calls `tasklist.main(["list"])`, and asserts both Chinese-rendered task titles and status markers. Add an empty-list test asserting `暂无任务`.

- [ ] **Step 2: Run tests to verify they fail**

Run `pytest -q`. Expected: collection or assertion failures because `tasklist.main` and the CLI behavior do not yet exist.

- [ ] **Step 3: Implement the minimal CLI**

Use only `argparse`, `json`, `os`, and `pathlib`. Load a missing file as `[]`, append the next task ID as `max(existing ids, default=0) + 1`, save UTF-8 JSON with `ensure_ascii=False`, and render Chinese output. Parse only `add` and `list`; do not add `done`, `delete`, `edit`, renumbering, or other second-round features.

- [ ] **Step 4: Run the full test suite**

Run `pytest -q`. Expected: all tests pass with zero failures.

- [ ] **Step 5: Commit the feature**

Run:

```powershell
git add src/tasklist.py tests/test_tasklist.py README.md
git commit -m "feat: add and list tasks"
```

### Task 3: GitHub delivery

**Files:**
- No source changes.

**Interfaces:**
- Consumes the verified `feature/add-and-list` commit from Task 2.
- Produces the pushed branch and PR `feature/add-and-list` → `main` titled `Round 1: implement add and list`.

- [ ] **Step 1: Verify branch and tests**

Run `git status --short --branch` and `pytest -q`; require a clean feature branch and a passing suite.

- [ ] **Step 2: Push the branch**

Run `git push -u origin feature/add-and-list`. If GitHub credentials or repository permissions are unavailable, preserve the local commits and report this exact blocked step.

- [ ] **Step 3: Create the PR and stop**

Create the PR with the required title and a description covering implemented behavior, test results, and that `done/delete/edit` remain unimplemented. After PR creation, do not make any additional code or architecture changes.
