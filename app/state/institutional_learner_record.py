"""
The Institutional Learner Record (ILR) - root object.

The Academy's canonical, evidence-backed understanding of a learner
at a specific point in time. Composes every other state model
(Evidence Ledger, Learner Model, Knowledge Map) into one record.

Not a transcript. Not a database dump. A living model that evolves
through observation, evidence, and educational reasoning - see
docs/learner_record.md for the full philosophy behind this schema.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.state.evidence import EvidenceEntry
from app.state.knowledge_map import KnowledgeMap
from app.state.learner_model import EvidenceBackedHypothesis, LearnerModel


class Identity(BaseModel):
    """Stable, rarely-changing facts about who the learner is."""

    student_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    display_name: str
    native_language: str
    target_language: str = "Japanese"
    timezone: str
    occupation: str | None = None
    goals: list[str] = Field(default_factory=list)
    started_learning: datetime | None = None
    joined_academy: datetime = Field(default_factory=datetime.utcnow)


class Facts(BaseModel):
    """
    Objective, stable data. Never inferred - if it requires
    interpretation, it belongs in Evidence or the Learner Model,
    not here.
    """

    jlpt_level: str | None = None
    resources_completed: list[str] = Field(default_factory=list)
    conversation_count: int = 0
    days_active: int = 0
    longest_streak: int = 0
    last_session: datetime | None = None


class EducationalHistoryEntry(BaseModel):
    """
    A single entry in the learner's educational history - a
    milestone, a break, a failed attempt, a strategy that worked
    or was retired, or a reflection worth remembering. Failures are
    deliberately included; they are educationally valuable.
    """

    entry_type: str
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)
    related_evidence: list[uuid.UUID] = Field(default_factory=list)


class WorldEngagementItem(BaseModel):
    """
    A single item tracking the learner's relationship with the real
    Japanese-speaking world - a conversation partner, a community, a
    book, a piece of media, a trip, an external teacher. This is the
    "Recommend the World" principle made concrete data.
    """

    category: str
    description: str
    status: str = "recommended"
    date_added: datetime = Field(default_factory=datetime.utcnow)


class ActiveSession(BaseModel):
    """
    Everything temporary - today's lesson only. This resets; the
    learner's permanent record does not.
    """

    lesson: str | None = None
    current_objective: str | None = None
    pedagogical_strategy: str | None = None
    active_questions: list[str] = Field(default_factory=list)
    pending_hypotheses: list[str] = Field(default_factory=list)
    response_draft: str | None = None


class InstitutionalNote(BaseModel):
    """
    A qualitative, hard-to-quantify observation - e.g. "lights up
    during travel stories." Often the Academy's biggest competitive
    advantage; no textbook captures this.
    """

    note: str
    department: str
    date: datetime = Field(default_factory=datetime.utcnow)


class NorthStar(BaseModel):
    """
    A persistent statement of why this student started learning.
    When momentum drops, every department can ask: how can today's
    lesson reconnect to this?
    """

    purpose: str
    last_reaffirmed: datetime = Field(default_factory=datetime.utcnow)
    confidence_in_goal: EvidenceBackedHypothesis | None = None


class Metadata(BaseModel):
    """Purely technical. No educational meaning lives here."""

    schema_version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_department: str | None = None
    record_version: int = 1


class InstitutionalLearnerRecord(BaseModel):
    """
    The root object. Every department reads from and writes to this
    record - never to each other directly (Stigmergy).
    """

    identity: Identity
    facts: Facts = Field(default_factory=Facts)
    evidence_ledger: list[EvidenceEntry] = Field(default_factory=list)
    learner_model: LearnerModel
    educational_history: list[EducationalHistoryEntry] = Field(default_factory=list)
    knowledge_map: KnowledgeMap = Field(default_factory=KnowledgeMap)
    world_engagement: list[WorldEngagementItem] = Field(default_factory=list)
    active_session: ActiveSession = Field(default_factory=ActiveSession)
    institutional_notes: list[InstitutionalNote] = Field(default_factory=list)
    north_star: NorthStar | None = None
    metadata: Metadata = Field(default_factory=Metadata)