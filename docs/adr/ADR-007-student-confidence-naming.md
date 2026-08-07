# ADR-007: Student Confidence Is a Separate Field From Certainty

## Status
Accepted

## Problem
"Confidence" was being used to mean two unrelated things in the same codebase: the Academy's epistemic confidence in a hypothesis (EvidenceBackedHypothesis.certainty), and the student's own psychological confidence as a learner (originally LearnerModel.confidence). Naming both "confidence" risked genuine confusion once department code and prompts started referencing these fields - "update the student's confidence" is ambiguous between "the Academy should believe this more strongly" and "the student feels more self-assured using Japanese."

## Decision
LearnerModel.confidence is renamed to LearnerModel.student_confidence.

EvidenceBackedHypothesis.certainty is unchanged - it already used a distinct name from the field being renamed, so no change was needed there.

Student confidence is never stored as a raw measurement (e.g. response_time, hesitation_score). It is represented the same way as every other Learner Model field: as an EvidenceBackedHypothesis, where the estimate describes the student ("Growing") and the certainty describes how sure the Academy is of that estimate.

Raw signals (e.g. "answered in 14.2 seconds") are Facts. A department's interpretation of those signals ("student hesitated significantly compared to their recent average") is Evidence. Only the resulting hypothesis lives in the Learner Model.

## Alternatives Rejected
- Keeping LearnerModel.confidence and relying on documentation to clarify the distinction. Rejected - naming collisions in a shared codebase get missed regardless of documentation quality, especially once multiple departments and prompts reference these fields independently.
- Adding raw fields like response_time or hesitation_score directly to the schema now. Rejected per the project's existing principle: don't model complexity until something actually uses it. These remain Facts/Evidence today; a structured field is only justified once a department is producing this kind of signal repeatedly.

## Consequences
- LearnerModel.student_confidence is the field departments write to when recording a hypothesis about how confident the student feels.
- EvidenceBackedHypothesis.certainty remains the field that expresses the Academy's confidence in any hypothesis, including this one.
- Future evidence about response time, self-correction, hesitation, or willingness to attempt difficult questions should be recorded as ordinary Evidence Ledger entries (observation + confidence + signal_strength) that support or challenge the student_confidence hypothesis - not as new schema fields, unless this pattern becomes common enough to justify structure.