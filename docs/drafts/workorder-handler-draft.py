"""DRAFT per Lab 2.1 Step 3 (Vd 1). Not wired into any app — scoring target only.

Prompt used:
  Role: Senior Engineer. Task: Write a POST /api/workorders handler.
  Context files: docs/coding-rules.md, docs/api-rules.md, docs/security-rules.md.
  Constraints: Do not invent extra JSON fields not specified in requirements,
  use standard validation, return 400 on malformed input / 422 on validation
  failure. Match repo style. Spec: docs/work-order-decomposition.md (WO-201).
"""

import logging
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/work-orders", tags=["work-orders"])


class Priority(str, Enum):
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class WorkOrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5, max_length=255)
    description: str = Field(default="", max_length=2000)
    priority: Priority = Priority.MED
    customer_id: UUID


class WorkOrderCreated(BaseModel):
    id: UUID
    status: str
    created_at: datetime


def _problem(status_code: int, title: str, detail: str) -> dict:
    return {
        "type": f"https://api.example.com/problems/{title.lower().replace(' ', '-')}",
        "title": title,
        "status": status_code,
        "detail": detail,
    }


def require_write_scope() -> None:
    # TODO: enforce OAuth2 Bearer scope workorders:write via Depends(security).
    return None


@router.post("", status_code=status.HTTP_201_CREATED, response_model=WorkOrderCreated)
def create_work_order(payload: WorkOrderCreate, _: None = Depends(require_write_scope)):
    log.info("workorder.create attempt title_len=%d priority=%s", len(payload.title), payload.priority)
    created = WorkOrderCreated(
        id=uuid4(),
        status="DRAFT",
        created_at=datetime.now(timezone.utc),
    )
    log.info("workorder.create ok status=%s", created.status)
    return created


@router.post("/validate-title")
def validate_title_example(title: str = ""):
    if len(title) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_problem(422, "Validation Failed", "title field required (min 5 chars)"),
        )
    return {"ok": True}
