---
name: "algorithm-correctness-invariants"
description: "Validates algorithm correctness using invariants, preconditions, and postconditions."
version: "1.0.0"
domain: "math-programming-logic"
quality_tier: "expert"
compatibility:
  - claude-code
  - codex
owner: "yonatanguerrerosoriano"
tags:
  - "logic"
  - "mathematics"
  - "programming-foundation"
foundation_skills:
  - ""
---

# Algorithm Correctness Invariants Skill

## Mission
Validates algorithm correctness using invariants, preconditions, and postconditions.

## When to use
- When the task requires strict logical correctness and defensible reasoning.
- When assumptions, constraints, and proof obligations must be made explicit.

## Inputs expected
- Formal problem statement, constraints, and success criteria.
- Known assumptions, unknowns, and boundary conditions.

## Workflow
1. Translate the task into formal entities, assumptions, and constraints.
2. Derive the solution through explicit logical rules or proof structure.
3. Validate with edge cases, contradiction checks, and consistency tests.

## Output contract
Return: formal framing, reasoning chain, verification evidence, and residual uncertainty.

## Guardrails
- Never skip logical steps or present intuition as proof.
- Never mix assumptions with verified facts.
- Always provide at least one explicit validation or counterexample check.


## Logical reliability checklist
- Assumptions are explicit and separated from verified facts.
- The solution path is justified with clear reasoning steps.
- Edge cases and contradiction checks are included.
- Output is testable, auditable, and reversible when possible.

## Example prompts
- "Apply the algorithm-correctness-invariants skill to handle this task end-to-end."
- "Run algorithm-correctness-invariants and produce a production-ready output with validation notes."
