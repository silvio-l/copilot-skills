---
name: codebase-map
description: Understand an unfamiliar codebase in a structured way, find relevant entry points, data flows, module boundaries, and the areas most likely affected by a problem or initiative.
---

# Codebase Map Skill

Use this skill when you need to understand how a codebase is structured before analyzing or making changes.

## Goal
Produce a reliable, concise architecture and navigation map of the relevant codebase.

## Workflow
1. Clarify the goal:
   - Bug?
   - Feature?
   - Refactoring?
   - Architecture understanding?
2. Find relevant entry points:
   - UI / CLI / API / Events / Scheduler / Background Jobs
3. Trace call chains, data flows, and state transitions.
4. Categorize key files and modules:
   - directly relevant
   - potentially relevant
   - likely irrelevant
5. Identify boundaries:
   - Layers
   - Feature slices
   - Adapters / Ports
   - Shared modules
6. Name uncertainties explicitly.

## Output Format
1. Goal / question
2. Relevant entry points
3. Key modules / files
4. Data flow / control flow
5. Architecture and boundary observations
6. Open questions / uncertainties
