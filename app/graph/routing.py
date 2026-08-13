"""
Routing logic - decides what runs next (ADR-008 Law 2).

This is the only place execution order is decided. Functions here
will implement each department's activation contract (does this
department have new, relevant Blackboard state to act on?), the
iteration limit (Law 3), and fixed-point detection. Left empty until
real departments exist to define activation contracts for.
"""