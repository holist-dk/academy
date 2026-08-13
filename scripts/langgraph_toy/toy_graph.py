"""
Throwaway LangGraph example - NOT part of the Academy's real code.
Purpose: see state flow through nodes, and watch an iteration limit
actually stop a loop, before building the real Phase 9 scaffolding.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, END


# 1. STATE
# The one shared object every node reads and writes to.
# In the real Academy, this will be (a wrapper around) the ILR.
class ToyState(TypedDict):
    counter: int
    log: list[str]


# 2. NODES
# Each node is just a function: (state) -> partial state update.
# Nodes never call each other directly - they only return changes.
def department_a(state: ToyState) -> dict:
    print(f"[Department A] saw counter={state['counter']}")
    return {
        "counter": state["counter"] + 1,
        "log": state["log"] + ["Department A ran"],
    }


def department_b(state: ToyState) -> dict:
    print(f"[Department B] saw counter={state['counter']}")
    return {
        "counter": state["counter"] + 1,
        "log": state["log"] + ["Department B ran"],
    }


# 3. ROUTING
# This function decides what runs next - this IS the Control Shell
# (ADR-008 Law 2: the graph alone decides, no department decides for itself).
def route_after_a(state: ToyState) -> str:
    if state["counter"] >= 6:
        # Fixed point reached / iteration limit hit - stop (ADR-008 Law 3)
        print(f"[Control Shell] counter={state['counter']} - limit reached, stopping.")
        return END
    return "department_b"


def route_after_b(state: ToyState) -> str:
    if state["counter"] >= 6:
        print(f"[Control Shell] counter={state['counter']} - limit reached, stopping.")
        return END
    return "department_a"


# 4. BUILD THE GRAPH
builder = StateGraph(ToyState)
builder.add_node("department_a", department_a)
builder.add_node("department_b", department_b)
builder.set_entry_point("department_a")
builder.add_conditional_edges("department_a", route_after_a)
builder.add_conditional_edges("department_b", route_after_b)

graph = builder.compile()


# 5. RUN IT
if __name__ == "__main__":
    initial_state: ToyState = {"counter": 0, "log": []}
    final_state = graph.invoke(initial_state)

    print("\n--- Final state ---")
    print(f"counter: {final_state['counter']}")
    print("log:")
    for entry in final_state["log"]:
        print(f"  - {entry}")