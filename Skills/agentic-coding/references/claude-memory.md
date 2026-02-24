# Claude Memory Integration Reference

> Local enhancement — not in upstream repo. Specifies how Claude Memory and the
> Agentic Coding Framework interact to enable persistent cross-session and
> cross-project learning.

---

## Three-Layer Memory Architecture

```
~/.claude/GLOBAL_MEMORY.md                 ← Cross-project (machine-bound)
    USER_PREFS   — user work style, framework usage habits
    PATTERNS     — reusable cross-project technical patterns
    STACK_LIB    — stack-specific pitfalls and conventions

~/.claude/projects/{id}/memory/MEMORY.md   ← Project meta (auto-loaded each turn)
    USER_PREFS   — project-specific overrides of global prefs
    STACK_QUICK  — this project's stack quick reference

~/.claude/projects/{id}/memory/solutions.md ← Blocker archive (load on demand)
    Past Story blockers with solutions, append-only
```

**Key distinction from PROJECT_MEMORY.md:**

| | PROJECT_MEMORY.md | Claude Memory |
|---|---|---|
| What | Project current state (NOW/NEXT/TESTS) | What Claude learns about working with this user |
| Who writes | Skill (Step 8) | Claude (triggered by events) |
| When read | Every turn (auto-resent) | Session start only |

---

## Trigger Matrix

| Event | Action | Target File |
|-------|--------|------------|
| Session start | Read global + project memory | `GLOBAL_MEMORY.md` + `memory/MEMORY.md` |
| max_attempts hit | Append blocker + solution | `memory/solutions.md` |
| User corrects Claude behavior | Append preference | `GLOBAL_MEMORY.md` USER_PREFS |
| Story completed | Scan for cross-project pattern | `GLOBAL_MEMORY.md` PATTERNS (if applicable) |
| New project Bootstrap | Read GLOBAL_MEMORY, inform approach | — |
| Story start (before Step 0) | Scan solutions.md for relevant past blockers | `memory/solutions.md` |

---

## Writing Rules

**GLOBAL_MEMORY.md**
- Keep under 50 lines total — it's read at every session start across ALL projects
- USER_PREFS: one line per preference, imperative style ("always ask before refactoring")
- PATTERNS: one line per pattern + project origin ("Go test races: use t.Parallel() carefully [go-webrtc]")
- STACK_LIB: one line per stack lesson ("gin CORS: include X-Forwarded-* headers")
- Update the `<!-- -->` header when modified (date + projects list)

**memory/MEMORY.md**
- Under 30 lines — auto-loaded every turn, every line costs tokens
- USER_PREFS: project-specific overrides only, not duplicates of GLOBAL_MEMORY
- STACK_QUICK: 3–5 lines of this project's most-needed stack context

**memory/solutions.md**
- Append-only — never modify past entries
- One block per blocker, format:
  ```
  ## [{project}] {short title} — US-{id}, {date}
  Problem: {what broke}
  Solution: {what fixed it}
  Applicable-to: {what kind of future problems this applies to}
  ```

---

## GLOBAL_MEMORY.md Template

```markdown
# Agentic Coding — Global Memory
<!-- Updated: {date} | Projects: {comma-separated list} -->

> Cross-project knowledge base. Maintained by Claude, read at every session start.
> Keep this file under 50 lines — move details to project-level memory/solutions.md.

---

## USER_PREFS
- {preference discovered from user interaction}

---

## PATTERNS
- {technical pattern} [{origin project}]

---

## STACK_LIB
- {stack}: {lesson}
```

---

## memory/MEMORY.md Template (Bootstrap)

```markdown
# Project Memory — {Project Name}
<!-- project: {name} | bootstrapped: {date} -->

## USER_PREFS
(project-specific overrides — global prefs apply by default)

## STACK_QUICK
- Stack: {language}, {framework}, {test library}
- Key conventions: {1-2 lines}
```

---

## memory/solutions.md Template (Bootstrap)

```markdown
# Solutions Archive — {Project Name}

> Append-only. Each entry = one blocker encountered during Story implementation.
> Read at Story start to avoid re-encountering the same problem.
```

---

## When NOT to Write to Claude Memory

- Current story state → goes in `PROJECT_MEMORY.md` NOW
- Test results → goes in `PROJECT_MEMORY.md` TESTS
- Architecture decisions → goes in SDD or `docs/constitution.md`
- Temporary session notes → not worth persisting
- Things that are project-specific AND unlikely to recur in other projects → skip GLOBAL_MEMORY, use `memory/MEMORY.md` instead
