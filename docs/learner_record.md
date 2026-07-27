# The Academy - Institutional Learner Record (ILR)

## Definition
The Institutional Learner Record is the Academy's canonical, evidence-backed understanding of a learner at a specific point in time. It is not a transcript of conversations, nor merely a database record. It is a living model that evolves through observation, evidence, and educational reasoning.

## Six Governing Principles
1. Explainable - every conclusion traces to evidence. Never a bare confidence score; always "confidence is increasing because [specific evidence]."
2. Evolvable - the Academy is allowed to change its mind as new evidence appears. Only Facts are permanent.
3. Department Neutral - no single department owns the ILR (Blackboard Architecture). Every department can contribute.
4. Human Readable - a teacher should be able to understand a learner from the ILR within five minutes.
5. LLM Friendly - JSON is preferred over deeply relational tables early on, for both prompting and reasoning.
6. Institution First - store what is educationally meaningful, never chat logs or raw token history.

## Storage Philosophy
Store evidence and current understanding, not conclusions.

Every piece of information entering the record must pass this test:
"Will remembering this make us a better teacher for this student in the future?"
If the answer is no, it is not stored. This keeps the record meaningful rather than an ever-growing transcript.

### Three Internal Layers
- Facts: objective and stable (name, native language, JLPT level, session dates). Never inferred.
- Evidence: observations (hesitated during speaking, returned after 60 days, used a new grammar point correctly).
- Understanding: the Academy's current hypotheses, always traceable to specific evidence IDs.

## Schema

### Identity (stable)
student_id, display_name, native_language, target_language, timezone, occupation, goals, started_learning, joined_academy.

### Facts (objective, never inferred)
jlpt_level, resources_completed, conversation_count, days_active, longest_streak, last_session.

### Evidence Ledger (the heart of the record)
Every entry: timestamp, department, type (observation), confidence, evidence text, source. No conclusions are stored here - only observations.

### Learner Model (hypotheses)
motivation, confidence, curiosity, momentum, frustration, independence, preferred_learning_methods.
Each field carries: estimate, certainty, last_updated, supported_by (a list of Evidence Ledger IDs).
The Learner Model never invents truth - every value must reference evidence.

### Educational History
major_milestones, long_breaks, failed_attempts, successful_strategies, retired_strategies, reflection_highlights.
Failures are deliberately included - they are educationally valuable, not something to hide.

### Knowledge Map
grammar, vocabulary, kanji, listening, speaking, reading, writing, culture.
Each concept: estimated_mastery, retention, evidence, recommended_next_step. Never raw percentages without evidence behind them.

### World Engagement (the "Recommend the World" principle made concrete)
conversation_partners, communities, books, videos, articles, travel, teachers, recommended_external_resources, completed_external_resources.
This tracks the learner's relationship with the real Japanese-speaking world, not just their activity inside the Academy.

### Active Session (temporary - resets daily)
lesson, current_objective, pedagogical_strategy, active_questions, pending_hypotheses, response_draft.

### Institutional Notes (qualitative, hard to quantify)
Free-form educationally significant observations, e.g. "lights up during travel stories," "prefers authentic conversation over drills." Often the Academy's biggest competitive advantage - no textbook captures this.

### North Star (persistent motivation anchor)
purpose, last_reaffirmed, confidence_in_goal.
A persistent statement of why the student started learning. When momentum drops, every department can ask: "How can I reconnect today's lesson to this person's original reason for learning?"

### Metadata (purely technical)
schema_version, created_at, updated_at, last_department, record_version.

## The Academy's Own Confidence
Separately from confidence about the student, the Academy tracks how confident it is in its own understanding. If certainty is low, departments should gather more evidence rather than make bold assumptions. This keeps the Academy intellectually honest.

## Representation Decision
Human-first JSON, not database-first normalized tables, for the initial build.
Rationale: readable, debuggable, ideal for LLM prompting, and allows the schema to evolve before locking into a relational structure. Pydantic will validate it. PostgreSQL normalization happens later, once real usage reveals what actually needs to be relational - no fixed trigger point has been set for when that migration happens.

## Open Questions (not yet decided)
- Concurrency and conflict management for multiple simultaneous Readers or Writers.
- Whether ChromaDB remains suitable as shared state at scale, and what would replace it if not.
- Evidence Ledger retention or pruning policy for long-term growth over months and years.
- Trigger condition for when ILR data should be normalized into PostgreSQL tables.