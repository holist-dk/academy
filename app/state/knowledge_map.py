"""
Knowledge Map for the Institutional Learner Record.

Tracks the learner's mastery of specific educational concepts across
subjects (grammar, vocabulary, kanji, listening, speaking, reading,
writing, culture). Concepts are tracked individually, not as one
blob per subject - "grammar" is not one thing, "te-form" is.

KnowledgeConcept is a distinct model from EvidenceBackedHypothesis
(app/state/learner_model.py). They share a philosophy - both are
evidence-backed and revisable - but represent different domain
concepts: a hypothesis is a belief about the learner as a person,
a knowledge concept is a measurement of mastery over one specific
piece of content. Do not merge these into a shared base model until
real department code shows the duplication is stable (avoid premature
abstraction).
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, RootModel

from app.state.evidence import ConfidenceLevel
from app.state.learner_model import EvidenceId


class MasteryLevel(str, Enum):
    UNKNOWN = "unknown"
    INTRODUCED = "introduced"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    MASTERED = "mastered"


class KnowledgeConcept(BaseModel):
    """
    Mastery tracking for a single concept (e.g. "te-form", "greetings",
    the kanji "日"). New students start every concept at MasteryLevel.UNKNOWN -
    concepts are added by departments as they are actually introduced,
    not pre-populated in bulk.
    """

    mastery: MasteryLevel = MasteryLevel.UNKNOWN
    certainty: ConfidenceLevel
    retention_score: int = Field(
        ge=0,
        le=100,
        description="How well the student currently retains this concept, independent of overall mastery level. 0 = fully forgotten, 100 = fully retained.",
    )
    supported_by: list[EvidenceId] = Field(default_factory=list)
    competing_evidence: list[EvidenceId] = Field(default_factory=list)
    recommended_next_step: str | None = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    notes: str | None = None


class KnowledgeSubject(RootModel[dict[str, KnowledgeConcept]]):
    """
    A subject (e.g. grammar) is a collection of individually tracked
    concepts, keyed by a short identifier (e.g. "te_form"). Starts
    empty for a new student - the Curriculum Department adds concepts
    as they are introduced.
    """

    root: dict[str, KnowledgeConcept] = Field(default_factory=dict)


class KnowledgeMap(BaseModel):
    """
    The full Knowledge Map: every tracked subject, each a sparse
    collection of concepts. Subjects start empty and grow as the
    learner is actually taught specific content.
    """

    grammar: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    vocabulary: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    kanji: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    listening: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    speaking: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    reading: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    writing: KnowledgeSubject = Field(default_factory=KnowledgeSubject)
    culture: KnowledgeSubject = Field(default_factory=KnowledgeSubject)