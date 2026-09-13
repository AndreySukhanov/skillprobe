# skillprobe report

Target skill: `commit-message` - 10 cases, 3 repeat(s) per case, 300 trials. Started 2026-09-13T14:18:41+00:00, finished 2026-09-13T14:18:41+00:00.

## Summary

| variant | pass | 95% CI | trigger precision | trigger recall | flaky cases | errors | cost | avg latency |
|---|---|---|---|---|---|---|---|---|
| gpt-5.6-luna | 30/30 (100%) | 89-100% | 100% | 100% | 0 | 0 | $0.0067 | 2.5s |
| gpt-5.6-luna (no skills) | 15/30 (50%) | 33-67% | - | - | 0 | 0 | $0.0031 | 1.7s |
| qwen3.8-flash | 24/30 (80%) | 63-90% | 100% | 100% | 2 | 0 | $0.0070 | 12.8s |
| qwen3.8-flash (no skills) | 15/30 (50%) | 33-67% | - | - | 0 | 0 | $0.0061 | 8.2s |
| deepseek-v4.1-flash | 19/30 (63%) | 46-78% | 100% | 100% | 4 | 0 | $0.0110 | 3.2s |
| deepseek-v4.1-flash (no skills) | 15/30 (50%) | 33-67% | - | - | 0 | 0 | $0.0183 | 13.8s |
| glm-5.3-flash | 23/30 (77%) | 59-88% | 100% | 100% | 5 | 0 | $0.0077 | 17.6s |
| glm-5.3-flash (no skills) | 15/30 (50%) | 33-67% | - | - | 0 | 0 | $0.0091 | 9.0s |
| kimi-k3 | 29/30 (97%) | 83-99% | 100% | 100% | 1 | 0 | $0.1942 | 30.4s |
| kimi-k3 (no skills) | 2/15 (13%, 15 not run) | 4-38% | - | - | 0 | 0 | $0.1137 | 29.9s |

Trigger precision: of the runs that loaded the target skill, how many should have. Trigger recall: of the runs that should load it, how many did. A case is flaky when its repeats disagree.

## Cases

| case | expects trigger | gpt-5.6-luna | gpt-5.6-luna (no skills) | qwen3.8-flash | qwen3.8-flash (no skills) | deepseek-v4.1-flash | deepseek-v4.1-flash (no skills) | glm-5.3-flash | glm-5.3-flash (no skills) | kimi-k3 | kimi-k3 (no skills) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `fix-in-auth` | yes | 3/3 | 0/3 | 1/3 | 0/3 | 1/3 | 0/3 | 2/3 | 0/3 | 3/3 | 0/3 |
| `ticket-from-branch` | yes | 3/3 | 0/3 | 3/3 | 0/3 | 1/3 | 0/3 | 1/3 | 0/3 | 2/3 | 0/3 |
| `root-file-no-scope` | yes | 3/3 | 0/3 | 2/3 | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 3/3 | 0/2 |
| `reason-not-stated` | yes | 3/3 | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 2/3 | 0/3 | 3/3 | 0/3 |
| `request-in-russian` | yes | 3/3 | 0/3 | 3/3 | 0/3 | 1/3 | 0/3 | 2/3 | 0/3 | 3/3 | 0/2 |
| `review-is-not-commit` | no | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/1 |
| `release-note-summary` | no | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/1 |
| `how-to-amend` | no | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | - |
| `merge-vs-rebase` | no | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | - |
| `unrelated-haiku` | no | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | - |

## Failures

### gpt-5.6-luna (no skills)

- `fix-in-auth` #1: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Reject expired sessions immediately Remove the one-minute grace period from session validation so tokens are rejected once `expires_at` is reached, preventing sessions from remaining active after logout on another device.
- `fix-in-auth` #2: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Reject expired sessions immediately Remove the one-minute grace period from session validation so tokens are rejected at their exact expiration time, preventing sessions from remaining usable after logout on another device.
- `fix-in-auth` #3: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Enforce immediate session token expiration Remove the one-minute grace period when validating sessions so expired tokens are rejected immediately, including after logout on another device.
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Use: ```text feat(invoice): add PDF rendering for invoices ``` Optional body: ```text feat(invoice): add PDF rendering for invoices Expose Invoice.to_pdf() using the invoice template and calculated total so customers can download invoices f
- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Use: ```text feat(invoice): add PDF rendering for invoices ``` Optional body: ```text feat(invoice): add PDF rendering for invoices Expose Invoice.to_pdf() to generate downloadable invoice PDFs using the invoice template, line items, and to
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Use: ```text feat(invoice): add PDF rendering for invoices ``` Optional body: ```text feat(invoice): add PDF rendering for invoices Expose Invoice.to_pdf() using the invoice template and calculated total so customers can download invoices f
- `root-file-no-scope` #1: contains 'Why:'
  > docs: update installation instructions for Python 3.11+ - Document the `tomllib` Python version requirement - Replace requirements installation with editable install - Add `.env` setup instructions
- `root-file-no-scope` #2: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > docs: update installation instructions for Python 3.11+ and editable setup
- `root-file-no-scope` #3: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > docs: update installation instructions for Python 3.11+ and editable setup
- `reason-not-stated` #1: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45 seconds
- `reason-not-stated` #2: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45 seconds
- `reason-not-stated` #3: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45 seconds
- `request-in-russian` #1: contains 'Why:'
  > fix(auth): reject expired sessions immediately Remove the one-minute grace period when validating session tokens to ensure expired or remotely logged-out sessions are rejected without delay.
- `request-in-russian` #2: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > Исправить проверку срока действия сессии Убрать дополнительную минуту допуска для просроченных токенов, чтобы они отклонялись сразу после `expires_at` и не позволяли продолжать сессию после выхода на другом устройстве.
- `request-in-russian` #3: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > Исправить проверку срока действия сессии Убрать минутный grace period для истёкших токенов и отклонять их сразу после `expires_at`. Это предотвращает сохранение сессии после выхода на другом устройстве.

### qwen3.8-flash

- `fix-in-auth` #1: not_contains 'Refs:'
  > fix(auth): reject expired tokens immediately without grace period Why: the one-minute grace period let users keep a session alive after logging out on another device Refs:
- `fix-in-auth` #2: not_contains 'Refs:'
  > fix(auth): reject expired tokens immediately by dropping grace minute Why: the one-minute grace period let users keep a session alive after logging out on another device Refs:
- `root-file-no-scope` #2: not_contains 'Refs:'
  > docs: update install instructions for python 3.11+ setup Why: the service relies on tomllib, so the README must state the Python 3.11+ requirement and the editable-install steps Refs:
- `reason-not-stated` #1: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > config: raise payment gateway timeout to 45 seconds Why: unknown - ask the author
- `reason-not-stated` #2: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > config: raise payment gateway timeout to 45 seconds Why: unknown - ask the author
- `reason-not-stated` #3: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > config: raise payment gateway timeout to 45s Why: unknown - ask the author

### qwen3.8-flash (no skills)

- `fix-in-auth` #1: regex '^Why: (?!unknown)\\S'
  > fix(auth): remove one-minute grace period from session expiry Expired tokens are now rejected immediately instead of being accepted for an extra minute. This prevents users from keeping a session active after expiry, especially following lo
- `fix-in-auth` #2: regex '^Why: (?!unknown)\\S'
  > fix(auth): reject expired session tokens immediately Remove the one-minute grace period that allowed sessions to remain valid after token expiry. This prevents revoked or logged-out sessions from staying active briefly due to stale token ex
- `fix-in-auth` #3: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > fix: reject expired auth sessions immediately Remove the one-minute grace period from `is_session_valid()` so that expired tokens are rejected as soon as `expires_at` is reached. This prevents a stale session from remaining valid after logo
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Use a commit message that mentions the ticket and the change clearly. Example: ```bash git commit -m "PAY-482: Add Invoice.to_pdf to render invoice PDFs" ``` If you prefer a conventional commit style: ```bash git commit -m "feat(billing): a
- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Use a commit message that states the new behavior and references the ticket. For example: ```bash git commit -m "Add Invoice.to_pdf to generate PDF invoices" -m "Implements PAY-482 by rendering invoice.html with invoice number, lines, and t
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Since this change adds a new feature—`Invoice.to_pdf()`—use a commit message that mentions the ticket, the new capability, and why it exists. ## Recommended commit message ```text feat(billing): add Invoice.to_pdf Adds Invoice.to_pdf so inv
- `root-file-no-scope` #1: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ```text docs(readme): update installation instructions Require Python 3.11+ for tomllib and replace the requirements.txt install step with editable package installation and copying .env.example. ```
- `root-file-no-scope` #2: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ```commit docs: update README installation instructions Require Python 3.11+ because the service uses tomllib. Switch installation to `pip install -e .` and add copying `.env.example` to `.env`. ```
- `root-file-no-scope` #3: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ```text docs: update installation instructions in README Mention Python 3.11+ requirement and replace requirements.txt installation with an editable install plus .env example copy. ```
- `reason-not-stated` #1: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ```text fix(config): increase payment gateway timeout to 45 seconds Raise PAYMENT_GATEWAY_TIMEOUT_S from 30 to 45 seconds to allow longer gateway response times. ```
- `reason-not-stated` #2: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ```text chore(config): increase payment gateway timeout to 45s ```
- `reason-not-stated` #3: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` Increase payment gateway timeout from 30s to 45s The previous 30-second timeout was too aggressive, causing preemptive cancellations on slower gateway responses. Bumping to 45s gives the payment provider adequate time to respond while s
- `request-in-russian` #1: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ```text fix(auth): reject expired tokens immediately Remove the one-minute grace period in is_session_valid(). Expired tokens are now always rejected, preventing sessions from staying alive after logout on another device. ```
- `request-in-russian` #2: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ```text fix(auth): reject expired sessions immediately Remove the one-minute grace period from is_session_valid(). Expired tokens are now considered invalid immediately, preventing sessions from remaining active after logout on another devi
- `request-in-russian` #3: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > Рекомендуемый вариант в стиле Conventional Commits: ```text fix(auth): reject expired tokens immediately Remove the one-minute grace period from session validation. Expired sessions are now rejected as soon as expires_at is reached, prevent

### deepseek-v4.1-flash

- `fix-in-auth` #1: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): reject expired sessions immediately Why: the one-minute grace period let users keep a session alive after logout on another device ```
- `fix-in-auth` #3: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): reject expired sessions immediately Why: the one-minute grace period let users keep a session alive after logging out on another device ```
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` feat(billing): add to_pdf export for invoices Why: customers asked to download invoices for their accountants Refs: PAY-482 ```
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` feat(billing): add to_pdf method to Invoice Why: customers asked to download invoices for their accountants Refs: PAY-482 ```
- `root-file-no-scope` #1: regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions Why: the service requires Python 3.11+ for `tomllib`, so the install steps now use an editable install and copy the example env file. ```
- `root-file-no-scope` #2: regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: document python 3.11+ requirement and editable install Why: the service uses tomllib, which requires Python 3.11 or newer ```
- `root-file-no-scope` #3: regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: document editable install and env setup Why: unknown - ask the author ```
- `reason-not-stated` #1: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` chore(config): increase payment gateway timeout to 45s Why: unknown - ask the author ```
- `reason-not-stated` #3: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` chore(config): increase payment gateway timeout to 45 seconds Why: unknown - ask the author ```
- `request-in-russian` #2: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): reject expired sessions immediately Why: the one-minute grace period let users keep a session alive after logging out on another device. ```
- `request-in-russian` #3: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): reject expired sessions immediately Why: the one-minute grace period let users keep a session alive after logging out on another device ```

### deepseek-v4.1-flash (no skills)

- `fix-in-auth` #1: regex '^Why: (?!unknown)\\S'
  > fix(auth): reject expired sessions immediately Remove the one-minute grace period after session expiry in `is_session_valid`. The grace period allowed a session to remain valid after logout on another device; sessions are now invalid once `
- `fix-in-auth` #2: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Reject expired sessions immediately Remove the one-minute grace period after session expiration. The grace period allowed a session to remain valid after logout on another device. Expired sessions are now rejected as soon as `expires_at` is
- `fix-in-auth` #3: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ```text fix(auth): reject expired sessions immediately Remove the one-minute post-expiry grace period in is_session_valid. Sessions are now valid only while now < expires_at, preventing expired tokens from remaining usable after logout on a
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Use a commit message that references the ticket and describes the new capability. Since this adds a feature, something like: ```text PAY-482 Add invoice PDF export Add Invoice.to_pdf() using billing.pdf.render_pdf so customers can download 
- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Suggested commit message: ```text PAY-482: Add invoice PDF export Add Invoice.to_pdf() to render invoices as PDF using billing.pdf.render_pdf and the invoice.html template. This lets customers download invoices for their accountants. ``` If
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > Given the diff, this is a new feature: it adds `Invoice.to_pdf()` using `render_pdf`. Recommended commit message if your team uses Conventional Commits: ```text feat(invoice): add PDF export Add Invoice.to_pdf() using billing.pdf.render_pdf
- `root-file-no-scope` #1: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions Replace the requirements.txt-based install steps with an editable install (`pip install -e .`) and note the Python 3.11+ requirement due to the `tomllib` dependency. Also add a step to copy `.env.exampl
- `root-file-no-scope` #2: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions for Python 3.11+ and editable install ``` Or if you prefer a body: ``` docs: update install instructions in README - Note Python 3.11+ requirement (uses tomllib) - Replace requirements.txt install with 
- `root-file-no-scope` #3: contains 'Why:'
  > docs: update installation instructions Require Python 3.11+ for `tomllib`, switch to editable install with `pip install -e .`, and add `.env` setup via `cp .env.example .env`.
- `reason-not-stated` #1: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45s Raise `PAYMENT_GATEWAY_TIMEOUT_S` from 30 to 45 to allow more time for slow payment gateway responses.
- `reason-not-stated` #2: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45s
- `reason-not-stated` #3: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > Increase payment gateway timeout to 45s
- `request-in-russian` #1: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ```text fix(auth): немедленно отклонять истёкшие сессии Убран grace-период в 1 минуту после expires_at, в течение которого токен всё ещё считался действительным. Это позволяло сохранять сессию после выхода на другом устройстве. Теперь прове
- `request-in-russian` #2: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ```text fix(auth): отклонять истёкшие сессии сразу Убрано минутное окно отсрочки после истечения срока действия токена. Теперь is_session_valid считает сессию недействительной при now >= session.expires_at, а не через минуту после expires_a
- `request-in-russian` #3: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ```text fix(auth): отклонять истёкшие сессии сразу Убран минутный льготный период после `expires_at`: теперь проверка использует строгое `now < session.expires_at`. Ранее grace-минута позволяла сессии оставаться активной после выхода на дру

### glm-5.3-flash

- `fix-in-auth` #2: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): reject expired tokens immediately Why: the one-minute grace period let users keep a session alive after logout on another device ```
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` feat(billing): add pdf export for invoices Why: customers asked to download invoices for their accountants Refs: PAY-482 ```
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` feat(billing): add pdf export for invoices Why: Customers asked to download invoices for their accountants Refs: PAY-482 ```
- `root-file-no-scope` #1: regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: document editable install and python 3.11 requirement Why: the service uses tomllib, so Python 3.11+ is required ```
- `root-file-no-scope` #2: regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions for editable setup Why: document the Python 3.11+ requirement and switch to `pip install -e .` with a .env setup step ```
- `reason-not-stated` #3: regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` chore(config): increase payment gateway timeout to 45s Why: unknown - ask the author ```
- `request-in-russian` #2: regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` fix(auth): remove one-minute grace period for expired tokens Why: the grace minute let users keep a session alive after logout on another device ```

### glm-5.3-flash (no skills)

- `fix-in-auth` #1: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` fix(auth): reject expired session tokens immediately is_session_valid previously allowed a one-minute grace period after expires_at, during which expired tokens were still accepted. This meant a session could remain alive even after the
- `fix-in-auth` #2: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` Reject expired auth tokens immediately The one-minute grace period in is_session_valid allowed a session to stay valid for up to a minute past expires_at, which kept it usable after logout on another device. Require now < expires_at so 
- `fix-in-auth` #3: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` fix(auth): reject expired session tokens immediately Remove the one-minute grace period from session expiry validation. The extra minute allowed tokens to remain valid after logout on another device, so a session could outlive the user'
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Here's a commit message that follows the usual conventions (imperative mood, ticket ID for traceability, body explaining the "why"): ``` PAY-482: Add PDF export for invoices Customers asked to download invoices for their accountants. Adds I
- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Here's a commit message for that diff: ``` PAY-482: Add PDF export for invoices Add Invoice.to_pdf(), which renders the invoice through billing.pdf.render_pdf so customers can download invoices for their accountants. ``` You can apply it di
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Here's a commit message that follows common conventions: ``` feat(billing): add PDF export for invoices Customers need to download invoices as PDFs for their accountants. Invoice.to_pdf() renders the invoice.html template with the invoice n
- `root-file-no-scope` #1: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions in README - Note Python 3.11+ requirement (project uses tomllib) - Replace `pip install -r requirements.txt` with `pip install -e .` - Add step to copy .env.example to .env ```
- `root-file-no-scope` #2: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update README install instructions - Note Python 3.11+ requirement (project uses stdlib tomllib) - Install via `pip install -e .` instead of requirements.txt - Add step to create .env from .env.example ``` Shorter alternative if y
- `root-file-no-scope` #3: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions in README Replace the requirements.txt workflow with `pip install -e .` and document copying `.env.example` to `.env`. Note that Python 3.11+ is required since the service uses `tomllib`. ``` Shorter al
- `reason-not-stated` #1: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > **Commit message:** ``` Increase payment gateway timeout from 30s to 45s ``` If you want a message with a body explaining the rationale (adjust the reason to match your actual motivation): ``` Increase payment gateway timeout from 30s to 45
- `reason-not-stated` #2: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` Increase payment gateway timeout from 30s to 45s ``` If you want a fuller message with a body: ``` Increase payment gateway timeout from 30s to 45s <Why: e.g., gateway requests were intermittently timing out at 30s under peak load, caus
- `reason-not-stated` #3: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > **Suggested commit message:** ``` Increase payment gateway timeout from 30s to 45s ``` **With a body (if you want more context):** ``` Increase payment gateway timeout from 30s to 45s Raises PAYMENT_GATEWAY_TIMEOUT_S to reduce premature req
- `request-in-russian` #1: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > Вот вариант сообщения коммита: ``` Убрать минутный льготный период при проверке срока сессии is_session_valid принимала токены ещё минуту после expires_at. Из-за этого сессия оставалась активной после логаута на другом устройстве. Теперь ис
- `request-in-russian` #2: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ``` fix(auth): reject expired session tokens immediately Remove the 1-minute grace period after token expiry in is_session_valid(). Tokens were accepted for up to 60 seconds past expires_at, which allowed a session to stay alive after the u
- `request-in-russian` #3: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > Вот вариант сообщения коммита: ``` fix(auth): reject expired session tokens immediately Remove the one-minute grace period in is_session_valid() that kept tokens valid for 60 seconds past expires_at. During that window a session could stay 

### kimi-k3

- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` feat(billing): add pdf export to invoice Why: customers asked to download invoices for their accountants Refs: PAY-482 ```

### kimi-k3 (no skills)

- `fix-in-auth` #1: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` Remove grace period for expired session tokens Sessions were considered valid for one extra minute after their expiry time. This let a session stay alive briefly after the user logged out on another device. Expired tokens are now reject
- `fix-in-auth` #2: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` Reject sessions immediately at expiry The one-minute grace period in is_session_valid allowed tokens to remain valid after their expiry time. This let a session stay alive briefly after the user logged out on another device, since revoc
- `fix-in-auth` #3: not_contains '```'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Why: (?!unknown)\\S'
  > ``` fix(auth): reject expired session tokens immediately Remove the one-minute grace period after session expiry. The grace window kept sessions usable for up to 60 seconds after a user logged out on another device. Tokens are now invalid a
- `ticket-from-branch` #1: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Here's a solid commit message for that change: ``` PAY-482: Add PDF export to Invoice Customers need to download invoices for their accountants. Adds an Invoice.to_pdf() method that renders the invoice.html template with the invoice number,
- `ticket-from-branch` #2: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Something like this: ``` Add downloadable PDF invoices (PAY-482) Customers need to download invoices for their accountants. Adds Invoice.to_pdf(), which renders invoice.html with the invoice number, line items, and total via billing.pdf.ren
- `ticket-from-branch` #3: regex '\\Afeat\\(billing\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '^Refs: PAY-482\\s*$'; regex '^Why: (?!unknown)\\S'
  > Here's a solid option: ``` Add Invoice.to_pdf() for downloadable invoices Customers need to download invoices as PDFs for their accountants. Renders the existing invoice template via billing.pdf.render_pdf. Closes PAY-482 ``` A few variatio
- `root-file-no-scope` #1: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update README install instructions - Note Python 3.11+ requirement (service uses tomllib) - Switch to editable install (pip install -e .) - Add .env setup step ``` Or a one-liner if you prefer: ``` docs: update install steps — edi
- `root-file-no-scope` #2: contains 'Why:'; regex '\\Adocs: (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'
  > ``` docs: update install instructions in README Note Python 3.11+ requirement (tomllib), switch to editable install, and add .env setup step. ``` Or if you prefer a one-liner: ``` docs: update README install steps (Python 3.11+, editable in
- `reason-not-stated` #1: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` Increase payment gateway timeout from 30s to 45s ``` Or if you're using conventional commits: ``` chore(config): increase payment gateway timeout to 45s ``` If this change was motivated by a specific issue (e.g., timeouts under load), i
- `reason-not-stated` #2: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` Increase payment gateway timeout from 30s to 45s ``` If your project uses Conventional Commits: ``` chore(config): increase payment gateway timeout from 30s to 45s ``` Since this is a single-value change, a subject line alone is suffici
- `reason-not-stated` #3: contains 'Why: unknown - ask the author'; regex '\\A(chore|fix|perf|refactor|feat)\\(config\\): '
  > ``` config: increase payment gateway timeout from 30s to 45s ``` If your team doesn't use conventional prefixes, this works too: ``` Increase payment gateway timeout from 30s to 45s ``` If you want a body explaining the motivation (e.g., in
- `request-in-russian` #1: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ``` fix(auth): reject expired session tokens immediately Remove the one-minute grace period in session validation. The extra minute allowed sessions to stay valid after logout on another device, which is a security risk. Tokens are now reje
- `request-in-russian` #3: contains 'Why:'; regex '\\Afix\\(auth\\): (?=[^\\n]{1,60}(\\n|\\Z))[a-z][^\\n]*[^.\\n](\\n|\\Z)'; regex '\\A[^Ѐ-ӿ]*\\Z'
  > ``` fix(auth): отклонять просроченные токены сразу после истечения Убрана минутная отсрочка при проверке expires_at: из-за неё сессия оставалась активной даже после выхода пользователя на другом устройстве. Теперь токен считается невалидным
