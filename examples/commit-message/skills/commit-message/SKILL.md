---
name: commit-message
description: Write a git commit message in this team's convention. Use when the user asks for a commit message or what to put in `git commit` for a diff or a set of changes.
---

# Commit message convention

Output exactly this shape and nothing else - no commentary, no code fences:

```
<type>(<scope>): <summary>

Why: <one sentence with the reason for the change>
Refs: <ticket>
```

Rules:

- `type` is one of: feat, fix, refactor, perf, docs, test, chore.
- `scope` is the top-level directory that the diff touches, e.g. `auth` for `auth/session.py`. If the diff only touches files in the repository root, drop the scope and the parentheses: `docs: <summary>`.
- `summary` is imperative mood, starts with a lowercase letter, has no trailing period, and is at most 60 characters.
- The `Why:` line is mandatory. Take the reason from the diff or the user's words. If the reason is not stated anywhere, write exactly `Why: unknown - ask the author`. Never guess a reason.
- Add `Refs:` only when a ticket id like `PAY-123` appears in the branch name or the request. Otherwise omit the line entirely.
- Write the message in English even if the user writes in another language.
