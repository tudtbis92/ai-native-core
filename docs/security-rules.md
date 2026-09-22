# Security Rules

1. **No Hardcoded Secrets:** Never hardcode API keys, passwords, connection strings, or tokens in code or comments. Env vars only (see `.copilotignore`/`.gitignore`: `.env*`, `secrets/`).
2. **Input Validation:** Validate + sanitize at the controller boundary with Pydantic. Never trust client payloads.
3. **Injection Protection:** Use SQLAlchemy parameterized queries / ORM methods. Never concatenate strings into raw SQL.
4. **Authorization:** Enforce RBAC on endpoints (e.g. require `workorders:write` scope for creation; technicians read only assigned orders).
5. **PII Handling:** `customer_id` is internal PII. Audit logs must be sanitized (no raw IDs). Error responses must not leak internal details.
6. **Prompt Hygiene:** No production keys, DB credentials, or customer data in AI prompts or committed files.
