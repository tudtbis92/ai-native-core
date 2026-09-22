# Coding & Logging Rules (AI-Native Core Service — Python/FastAPI track)

> Rules Pack per Lab 2.1. Ported from the Java/Spring sample to this repo's stack:
> Python 3.11 / FastAPI / Pydantic v2 / PostgreSQL 16.

1. **Language & Framework:** Use Python 3.11+ and FastAPI. Type-annotate all public functions.
2. **Naming Conventions:** `PascalCase` for classes, `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants.
3. **Exception Handling:** Never raise bare `Exception`. Use specific errors (`ValueError`, `KeyError`) or `fastapi.HTTPException` with a proper status code.
4. **Logging Standards:**
   - DO NOT log PII (raw customer IDs, emails, tokens, passwords).
   - Use stdlib `logging.getLogger(__name__)`; one log line per operation step (action, inputs hash, outcome).
   - **[BAD]:** `log.info(f"creating order for {customer_id}")`
   - **[GOOD]:** `log.info("workorder.create attempt title_len=%d priority=%s", len(title), priority)`
5. **Dependency Injection:** Use FastAPI `Depends()` for DB sessions and auth. No global session objects.
6. **Code Simplicity:** No speculative abstractions or factories. Flat vertical slices per feature.
7. **Variable Declaration Scope:** Declare loop temporaries in the smallest scope that is correct; prefer `const`-like single assignment (no rebinding). Never use a shared mutable accumulator across iterations when a comprehension/`join` suffices.
8. **String Building:** No `s = chunk + s` prepend in loops. Collect with `list.append()` and `"".join()` once (or pre-sized index fill).
9. **Validation Location:** Validate at the boundary with Pydantic models. Domain functions may assume validated input; document it.
10. **No Hallucinated Dependencies:** Only stdlib + declared `requirements.txt` packages. Verify every import exists.
11. **AI Output Policy:** All AI-generated code is UNTRUSTED until human-read and covered by tests (`pytest`, target >= 80%).
12. **Secrets:** No secret, token, or connection string in code, comments, logs, or prompts. Env vars only.
