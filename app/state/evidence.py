"""
Evidence Ledger models for the Institutional Learner Record.

Evidence entries are observations only - never conclusions. Every
hypothesis in the Learner Model must trace back to one or more
Evidence entries by id.

Evidence is append-only (ADR-005). Departments never edit or delete
evidence after creation. Corrections are represented by new evidence,
or - in exceptional technical cases - by superseding prior evidence.
Superseding is not yet implemented; deferred until a real need appears.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

DepartmentName = Literal[
    "student_intake",
    "conversation",
    "reflection",
    "curriculum",
    "assessment",
]
"""
Currently recognized departments. This is intentionally a Literal, not
an Enum - the Academy's organizational structure is still being
discovered (Day 0). Add new department names here as they are built.
Migrate to a proper Department enum once the org structure stabilizes,
and consider a DepartmentRegistry if departments become dynamically
loaded plugins.
"""


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EvidenceEntry(BaseModel):
    """
    A single observation recorded by a department.

    No conclusions live here - only what was observed, who observed
    it, and how strongly the Academy trusts the observation itself.
    Immutable after creation.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    department: DepartmentName
    observation: str
    confidence: ConfidenceLevel
    signal_strength: int = Field(
        ge=0,
        le=100,
        description="Relative weight this evidence contributes during reasoning.",
    )
    supporting_data: str | None = None

    class Config:
        frozen = True