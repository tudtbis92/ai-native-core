# BR Analysis — Mobile Work Order (POSCO MCI track, Lab 2.2 Step 2)

## 0. Raw requirement (Product Owner, verbatim intent)

> Fast mobile Work Order feature for field technicians: enter `equipment_id`,
> pick priority (`low`, `medium`, `high`, `urgent`), write `description`.
> System saves and shows a list for managers. Ship fast this week; no complex
> authorization — anyone on site can create as long as the equipment ID is a
> valid active one.

## 1. Entities & attributes

| Entity | Key attributes | Notes |
|---|---|---|
| WorkOrder | `id` UUID, `equipment_id`, `description`, `priority`, `status`, `created_by`, `created_at` | Status lifecycle TBD (see Q4) |
| Equipment | `equipment_id`, `active` flag, site | Master data source TBD (see Q3) |
| Technician | `id`, site | Creator; identity needed even if "no auth" |
| Manager | `id` | Reads list; filter needs TBD (see Q5) |

## 2. Open Questions / Business risks (need PO decision)

| # | Question / risk | Why it blocks DoR |
|---|---|---|
| Q1 | Priority enum mismatch: PO says `low/medium/high/urgent`, WO-201 spec says `LOW/MED/HIGH(/CRITICAL)` | API contract conflict — must pick one mapping |
| Q2 | "No complex auth" vs `security-rules.md` RBAC + WO-201 `workorders:write` scope | Direct contradiction; PO must sign the risk waiver or scope it (e.g. site-local PIN) |
| Q3 | Where is equipment master data? What does "active" mean, who owns it? | Cannot validate `equipment_id` without a source |
| Q4 | Status lifecycle: is `NEW`/`DRAFT` enough? Who transitions to DONE? | Affects Data + API contract |
| Q5 | Manager list: filters (site/status/priority), pagination, offline mobile? | Affects UI + API scope |
| Q6 | "Ship this week": which DoR items may be deferred without breaking security floor? | Scope negotiation; security items are non-negotiable |

## 3. UI / Data / API decomposition (proposed, pending Q1–Q6)

| Layer | Proposal |
|---|---|
| UI | Mobile form: `equipment_id` (text, required, active-check), `priority` (enum, default per Q1), `description` (text, max 2000); error states per field; manager list view with filters (per Q5) |
| Data | Reuse `work_orders` table; add `equipment_id`, `created_by`; PII: creator identity in audit log (sanitized); no raw secrets |
| API | `POST /api/v1/work-orders` (201 + resource; 400 malformed; 422 validation); `GET /api/v1/work-orders` (filters per Q5); auth per Q2 decision; RFC 7807 errors |

**DoR status:** NOT READY — blocked on Q1, Q2, Q3. Usable as intake draft only.
