"""
Learner Model for the Institutional Learner Record.

The Learner Model is a collection of hypotheses the Academy holds
about a learner - motivation, confidence, curiosity, momentum,
frustration, and independence. Every hypothesis is represented by
the same generic structure (EvidenceBackedHypothesis) because they
are all fundamentally the same kind of thing: a current best
understanding, always traceable to evidence, always open to revision.

The Learner Model never invents truth. Every estimate must reference
one or more entries in the Evidence Ledger (app/state/evidence.py).
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.state.evidence import ConfidenceLevel

EvidenceId = uuid.UUID
"""
Semantic alias for a UUID that specifically identifies an Evidence
entry. Purely an alias today - if stronger typing is ever needed
(e.g. via typing.NewType), only this line changes.
"""


class EvidenceBackedHypothesis(BaseModel):
    """
    A single hypothesis the Academy holds, backed by evidence.

    This is a domain concept, not a per-attribute model - the same
    structure is reused for motivation, confidence, curiosity,
    momentum, frustration, and independence. Only the subject
    changes; the reasoning shape stays identical.
    """

    estimate: str = "unknown"
    certainty: ConfidenceLevel = ConfidenceLevel.LOW
    supported_by: list[EvidenceId] = Field(default_factory=list)
    competing_evidence: list[EvidenceId] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    notes: str | None = None


class LearnerModel(BaseModel):
    """
    The Academy's current hypotheses about a learner.

    Each field is a living estimate, not a fixed trait. Departments
    update these by writing new Evidence and revising the relevant
    hypothesis - they do not overwrite understanding without evidence
    behind the change.
    """

    motivation: EvidenceBackedHypothesis
    confidence: EvidenceBackedHypothesis
    curiosity: EvidenceBackedHypothesis
    momentum: EvidenceBackedHypothesis
    frustration: EvidenceBackedHypothesis
    independence: EvidenceBackedHypothesis
    
    @classmethod
    def new_unknown(cls) -> "LearnerModel":
        """
        Construct a LearnerModel with all six hypotheses in their
        default unknown state - no evidence, no assumptions. Use this
        for a brand-new student before Student Intake has run.
        """
        return cls(
            motivation=EvidenceBackedHypothesis(),
            confidence=EvidenceBackedHypothesis(),
            curiosity=EvidenceBackedHypothesis(),
            momentum=EvidenceBackedHypothesis(),
            frustration=EvidenceBackedHypothesis(),
            independence=EvidenceBackedHypothesis(),
        )