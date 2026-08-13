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

## Blackboard Execution Model (preventing death spirals)
Four laws govern how the Blackboard executes - see ADR-008 for full rationale:
1. Departments communicate only through the Blackboard. They never invoke, schedule, or reference other departments directly.
2. LangGraph (the Control Shell) is the only scheduler. No department decides what runs next.
3. A cycle terminates at a fixed point (no department has anything meaningful left to contribute) or at a hard iteration limit, whichever comes first. On hitting the limit, the system halts and surfaces to a human rather than looping silently.
4. Blackboard entries describe reality, never intent. An entry states what is true, never what should happen next or which department should act on it - that would smuggle a scheduling decision into shared state.

Departments only activate on new user input or a specific named condition (e.g. "new evidence since my last run"), never a background tick. Once no department has anything left to add, execution stops and waits for the student.

## Information Lifecycle: Event, Blackboard State, or Institutional Memory
Every piece of information the Academy handles belongs to exactly one of three tiers. Getting this sort right determines what gets persisted, in what shape, and for how long (this directly drives the Phase 10 database schema).

### 1. Event (transient - deferred, not currently implemented)
Something that happened, with no independent lifespan of its own - e.g. "student clicked next." In an event-driven layer, this would fire, trigger a reaction, and be discarded; it is not meant to be queried later as its own record. The Academy does not yet have a separate event layer (see Deferred Ideas in docs/roadmap.md) - today, what would be an "event" is simply a function call within a single LangGraph run. Revisit only once multiple departments need to react to the same happening independently and asynchronously.

### 2. Blackboard state (working memory - in-session, not necessarily durable)
What is true right now, during an active cycle. This is ActiveSession on the ILR (lesson, current_objective, pending_hypotheses, response_draft) - explicitly temporary, resets, does not need to survive a server restart or a day boundary. Test: is this just scratch space for the current interaction, or does it tell us something about the student worth keeping? If it is scratch space, it belongs here, not in durable storage.

### 3. Institutional memory (durable - the rest of the ILR)
Evidence Ledger, Learner Model, Knowledge Map, Educational History. The existing test from docs/learner_record.md applies directly: "Will remembering this make us a better teacher for this student in the future?" If yes, it belongs here, and (for Evidence specifically) it is append-only per ADR-005.

### The Sorting Rule
- Does it need to survive a network blip, restart, or day boundary? If no, it is Blackboard/Active Session scratch space.
- Does remembering it forever make the Academy a better teacher later? If yes, it is institutional memory.
- Is it "something happened, react now, then discard"? If yes, it belongs to the deferred event tier - not needed until multiple departments require independent, asynchronous reaction to the same happening.

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