# The Academy - Departments

Each department has exactly one responsibility (Kairos Flow). Departments never call each other directly - they communicate only by reading and writing to shared state (Stigmergy). LangGraph decides which department runs next; no department decides for itself.

## Folder Structure Per Department
Every department folder contains the same four files, even if some start empty:
- __init__.py
- prompt.md (the behavior specification - written as constraints, not descriptions)
- contract.py (inputs, outputs, and what this department is and is not allowed to touch)
- node.py (the LangGraph node implementation)

## Initial Departments (Day 0 scaffolding)
- student_intake
- conversation
- reflection
- curriculum
- assessment

## Department Responsibilities (from the agent architecture)

### Manager
Turns a user request into a Blueprint: goal, constraints, expected output, requirements. Never executes or writes.

### Planner
Breaks a Blueprint into ordered steps. Never executes.

### Reader (and squads: Reader-Web, Reader-File, Reader-Memory)
Gathers information only - web search, file reads, memory or ILR search. Never writes or modifies anything. Sees only 2-4 tools per squad.

### Writer (and squads: Writer-Email, Writer-File, Writer-Memory)
Modifies things only - ILR writes, file creation, sending messages. Never reads or searches. Sees only 2-4 tools per squad.

### Runner
Executes commands or code. Never edits files directly.

### Verifier
Pure Python. Never an AI call. Validates department output against an expected schema before it is accepted. If validation fails, the department retries (up to 3 attempts) before LangGraph halts and reports the error.

### Logger
Pure Python. Never an AI call. Records completed tasks into long-term (episodic) memory once verified.

## Rule: Department Boundary Enforcement
A department's allowed tools are a hard restriction, not just documentation. A Reader-role department should not have write-capable tools available to it at all - the boundary should be enforced by what tools exist in its toolset, not by hoping the prompt is followed.

## Adding a New Department
1. Create the folder with the standard four files.
2. Define its contract.py first: what it reads, what it writes, what it is never allowed to touch.
3. Write prompt.md as constraints, not descriptions.
4. Register it (Registry Pattern) so LangGraph's router can discover it - avoid manual if/elif routing.
5. Confirm it fits Kairos Flow: one responsibility only. If it needs more than one, it should be split into multiple departments (as Builder was split into Reader, Writer, and Runner).