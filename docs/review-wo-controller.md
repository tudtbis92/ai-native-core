# AI-Assisted Code Review — WorkOrderController sample (Lab 2.2 Step 3)

**Target:** `docs/drafts/posco-workorder-sample.java` | **Reviewer:** human + AI
**Priority order:** Spec delta → Security → Testing/Validation → Complexity → Style.

## Comments

### 1. Spec delta
- **[C1] Non-REST path.** `POST /api/work-orders/create-wo` invents a verb-style path; spec uses `POST /api/v1/work-orders`. Fix: collection POST, return `201`.
- **[C2] No input validation.** `equipment_id`/priority/description unchecked (null, blank, unknown enum). Fix: Bean Validation (`@NotBlank`, enum) → `422` Problem Details.
- **[C3] Bespoke response types.** `ApiResponse`/`ErrorResponse` instead of RFC 7807 (`type/title/status/detail`). Fix: Problem Details on all errors.

### 2. Security
- **[C4] SQL injection (CRITICAL).** String-concatenated `INSERT` with raw request fields. Fix: `PreparedStatement` / JPA parameterized query.
- **[C5] Hardcoded JWT secret (CRITICAL).** `JWT_SECRET` in source. Fix: env var / secret manager, rotate the leaked value.
- **[C6] No authentication/authorization.** Anyone can insert rows. Fix: authenticate + require `workorders:write` (see BR Q2 decision).
- **[C7] Error oracle.** `catch` returns `e.getMessage()` + full SQL `query` with HTTP 500 — leaks internals. Fix: log server-side, return generic Problem Details.
- **[C8] PII-adjacent logging.** `System.out` prints equipment ID to stdout, no sanitization, no logger. Fix: SLF4J, sanitized fields.

### 3. Testing & Validation
- **[C9] Generic `catch (Exception ...)`.** Swallows `SQLException`, validation, NPE alike; untestable branches. Fix: catch specific exceptions; map to 4xx/5xx.
- **[C10] Untestable design.** Field injection (`@Autowired`) + static secret + `System.out` block unit tests. Fix: constructor injection, injectable clock/ID generator.

### 4. Complexity
- **[C11] Controller does SQL.** Persistence logic inline in the endpoint. Fix: service + repository layers.

### 5. Style
- **[C12] `System.out` instead of logger; field injection over constructor injection.** Fix per `coding-rules.md` §§4–5.

**Tally:** 12 comments (≥8 required). **Blockers:** C4, C5, C6 — must fix before any deploy.

## Fixed structure (equivalent, Java/Spring)

```java
@RestController
@RequestMapping("/api/v1/work-orders")
public class WorkOrderController {
    private static final Logger log = LoggerFactory.getLogger(WorkOrderController.class);
    private final WorkOrderService service;
    public WorkOrderController(WorkOrderService service) { this.service = service; }

    @PostMapping
    public ResponseEntity<?> create(@Valid @RequestBody WorkOrderRequest req) {
        // service: validate equipment active, PreparedStatement/JPA insert,
        // sanitized log, return 201 + resource; errors as Problem Details.
        return ResponseEntity.status(201).body(service.create(req));
    }
}
// JWT secret: ${JWT_SECRET} env only. Endpoint: @PreAuthorize("hasAuthority('workorders:write')").
```
