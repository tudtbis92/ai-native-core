# Scorecard — Copilot Draft Review (Lab 2.1 Step 4)

**Target:** `docs/drafts/workorder-handler-draft.py` (Vd 1 prompt)
**Reviewer:** human | **Date:** 2026-09-22
**Verdict scale:** Pass / Partial / Fail per criterion.

| # | Criterion (source rule) | Result | Evidence / note |
|---|---|---|---|
| 1 | Plural resource path (`api-rules.md` §1) | Pass | `/api/v1/work-orders` |
| 2 | POST create → 201 with resource (`api-rules.md` §2, §6) | Pass | `status_code=201`, returns `id/status/created_at` |
| 3 | No invented JSON fields (`api-rules.md` §3) | Pass | Request = exact WO-201 fields; `extra="forbid"` |
| 4 | RFC 7807 error shape (`api-rules.md` §4) | Pass | `_problem()` returns `type/title/status/detail` |
| 5 | Pydantic v2 constraints (`api-rules.md` §5) | Pass | `min_length`, `Enum`, `UUID` |
| 6 | 400 malformed / 422 validation split (`api-rules.md` §5) | Partial | 422 explicit; malformed JSON falls to FastAPI default (also 422, not 400) |
| 7 | Auth scope enforced (`api-rules.md` §6, `security-rules.md` §4) | Fail | `require_write_scope()` is a TODO stub, no real OAuth2 check |
| 8 | No PII in logs (`coding-rules.md` §4, `security-rules.md` §5) | Pass | Logs `title_len` + `priority` only |
| 9 | stdlib logger, step lines (`coding-rules.md` §4) | Pass | `getLogger(__name__)`, attempt/ok lines |
| 10 | Naming conventions (`coding-rules.md` §2) | Pass | PascalCase models, snake_case funcs |
| 11 | No hardcoded secrets (`security-rules.md` §1) | Pass | None present |
| 12 | No hallucinated deps (`coding-rules.md` §10) | Pass | Only `fastapi` + `pydantic` + stdlib |

**Summary:** 10 Pass / 1 Partial / 1 Fail.
**Required follow-up before use:** implement real OAuth2 scope check (criterion 7); decide 400-vs-422 malformed handling (criterion 6). Draft must NOT be wired into an app as-is.
