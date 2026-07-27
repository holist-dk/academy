# The Academy - Architecture

## Core Idea
The Academy rejects the "God Agent" pattern - one large AI model responsible for search, read, write, execute, and remember all in a single prompt. Instead it is built as a colony of small specialist agents ("Departments") that cooperate indirectly through shared state, the same way ants coordinate through pheromone trails rather than direct communication.

## Why Not One Big Agent
- Prompt bloat: every tool needs in-context documentation; large tool sets produce oversized, unreliable prompts.
- Diluted attention: the model spends reasoning capacity choosing between many tools instead of doing the task.
- Undebuggable failures: when a single monolithic agent fails, it is unclear whether the cause was memory, tool choice, prompt, hallucination, or parsing.

## Three Pillars

### 1. Kairos Flow
Every agent has exactly one responsibility. A Reader only reads. A Writer only writes. A Runner only executes. No department performs another department's job.

### 2. Stigmergy
Departments never call each other directly. They read and write to shared state - the Institutional Learner Record (ILR) and the Blackboard. A Reader department does not know a Writer department exists; they only interact through what is written to shared state.

### 3. LangGraph (Orchestrator Pattern)
LangGraph is the control tower. It decides which department runs next, based on the current task Phase (PLANNING -> READY -> READ_DONE -> WRITE_DONE -> VERIFIED -> COMPLETE). No department decides what happens next - only the graph does. This is the Orchestrator Pattern: the graph does not do the work itself, it coordinates specialists that do.

## The Departments
| Department | Job | Never does |
|---|---|---|
| Manager | Turns a request into a Blueprint (goal, constraints, expected output) | Execute or write |
| Planner | Breaks the Blueprint into ordered steps | Execute |
| Reader | Gathers information (web, files, memory, ILR) | Writes or modifies anything |
| Writer | Modifies things (ILR writes, files, email) | Reads or searches |
| Runner | Executes commands or code | Edits files directly |
| Verifier | Pure Python. Validates output against expected schema. Never AI. | Any AI reasoning |
| Logger | Pure Python. Stores completed tasks into long-term memory. | Any AI reasoning |

Departments may be further subdivided into squads (e.g. Reader-Web, Reader-Memory, Writer-Email) so each sees only 2-4 tools, reducing confusion and hallucination risk.

## Engineering Principles

### Dependency Inversion
High-level code never depends on a specific vendor's implementation. Departments depend on abstractions (LLMProvider, VectorStoreProvider, EmbeddingProvider), not directly on OpenAI, Anthropic, or Google SDKs. Swapping a model or provider should be a config change, never a code change.

### Factory Pattern
A factory assembles each department's components (LLM + prompt + tools + contract) from independent, swappable pieces.

### Registry Pattern
Departments register themselves (e.g. via a decorator) rather than being wired together with manual if/elif routing. This lets LangGraph's router discover departments automatically as new ones are added.

### Prompt Engineering as Constraint-Writing
Prompts are not English descriptions - they are behavior specifications. Every department prompt should remove decision freedom, not add flavor. Example: "Use ONLY evidence already in the ILR" is a constraint, not a suggestion.

### Graceful Degradation
No single failure should collapse the whole system. If the Verifier fails, or shared state is unreachable, the system should degrade a specific feature (e.g. skip a recommendation this session) rather than crash the whole interaction.

### Async I/O
Reader departments performing web search, file reads, or memory queries are I/O-bound and should run asynchronously so the system can serve other work while waiting.

### Lazy Initialization and Caching
Providers (LLM, vector store, embeddings) are not created until first used, and are cached/reused rather than recreated per call.

### Idempotency
Writes to the ILR must be safe to retry. A retried write (e.g. after a network blip or LangGraph retry-on-failure) must never duplicate the same evidence twice. Evidence entries should be checked or deterministically identified before insert.

## Anti-Hallucination Measures
- Small tool sets per department (a Reader sees ~3 tools, never 30).
- Temperature = 0 for deterministic behavior.
- Verification is always pure Python, never another AI grading the first.
- Retry limit of 3 attempts before LangGraph halts and reports the error rather than looping forever.

## Memory Types (shared state)
| Type | Contents |
|---|---|
| STATE | Current task, temporary, deleted after completion |
| EPISODIC | Past conversations and completed jobs |
| SEMANTIC | Stable facts about the learner |
| PROCEDURAL | Reusable successful workflows |

## Naming Standards
Always say: Department, Institutional Learner Record, Evidence, Learner Model, Knowledge Map, World Engagement, Active Session.
Never say: Agents, Workers, Processors, Bots, as generic substitutes for Department.