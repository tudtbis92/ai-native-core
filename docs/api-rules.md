# API Design Rules

1. **REST Resource Naming:** Plural nouns (e.g. `/api/v1/work-orders`, not `/api/workOrder`).
2. **HTTP Verbs:** `POST` create, `GET` retrieve, `PUT`/`PATCH` update, `DELETE` remove.
3. **Strict Schema Conformance:** DO NOT invent JSON fields not defined in the spec (`docs/work-order-decomposition.md`, `docs/api-spec.md`). Pydantic models reject extras (`model_config = ConfigDict(extra="forbid")`).
4. **Error Responses (RFC 7807):** All errors return Problem Details with `type`, `title`, `status`, `detail`.
   - **[GOOD]:** `HTTPException(status_code=422, detail={"type": "...", "title": "Validation Failed", "status": 422, "detail": "title field required"})`
   - **[BAD]:** Returning raw strings or stack traces on validation failure.
5. **Validation:** All request bodies are Pydantic v2 models with constraints (`min_length`, enums, `UUID`). Invalid input → `422`, malformed JSON → `400`.
6. **Auth:** `POST /api/v1/work-orders` requires OAuth2 Bearer (`scope: workorders:write`). Return `201 Created` with the created resource (`id`, `status`, `created_at`).
