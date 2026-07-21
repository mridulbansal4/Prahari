# IMPLEMENTATION_RULES.md

# IMPLEMENTATION GOVERNANCE

**Project:** Prahari — Industrial Intelligence Operating System

**Purpose:** This document defines the implementation governance for the entire Prahari codebase. Every coding session, architectural decision, implementation task, and engineering change must comply with the rules defined here.

This document has higher priority than every supporting document in this repository.

---

# 1. Implementation Hierarchy

The implementation hierarchy is absolute.

```
IMPLEMENTATION_RULES.md
            │
            ▼
SENTINEL_Product_Requirements_Bible.md
            │
            ▼
design.md
            │
            ▼
Reference Documents
```

Nothing below may override anything above.

---

# 2. Source of Truth

The file

> **SENTINEL_Product_Requirements_Bible.md**

is the **ONLY implementation contract** for this project.

It defines:

- Product scope
- Features
- Functional requirements
- Non-functional requirements
- Development phases
- Implementation roadmap
- Repository structure
- Module boundaries
- Development priorities
- Engineering milestones
- Feature dependencies
- User flows
- AI workflows
- System workflows
- Business logic
- Success criteria

Every implementation decision must ultimately be traceable back to this document.

If a requirement does not exist inside the Product Requirements Bible, it must **not** be implemented unless explicitly approved by the project owner.

---

# 3. Role of design.md

The file

> **design.md**

is the single source of truth for

- Design language
- UI hierarchy
- Visual system
- Layout
- Component behavior
- Animations
- User experience
- Interaction design
- Motion
- Color system
- Typography
- Graphics
- Design consistency

It controls **how the product looks**, not **what the product does**.

Never allow any engineering document to override the design language defined inside design.md.

---

# 4. Role of Reference Documents

Every other document in this repository is a **supporting engineering reference**.

Examples include:

- System Architecture
- Technical Design Document
- AI Engineering
- Knowledge Graph
- API Specification
- Security
- Implementation Guide
- Engineering Decisions
- Testing
- Evaluation

These documents exist only to improve implementation quality.

They explain:

- how to implement a feature
- engineering best practices
- architecture reasoning
- scalability
- maintainability
- performance
- security
- testing
- validation
- optimization

They do **NOT** define the product.

They do **NOT** define implementation order.

They do **NOT** define project scope.

They do **NOT** introduce new features.

---

# 5. Absolute Rule

Supporting documents are never allowed to change:

- implementation roadmap
- implementation order
- development phases
- milestones
- feature priorities
- repository structure
- folder hierarchy
- module boundaries
- project scope
- functional requirements
- business logic
- AI workflow
- UI workflow
- product behavior

Only the Product Requirements Bible may define these.

---

# 6. Conflict Resolution

If two documents disagree, always follow this priority:

1. IMPLEMENTATION_RULES.md
2. SENTINEL_Product_Requirements_Bible.md
3. design.md
4. Supporting Documents

Never merge conflicting implementations.

Never average multiple documents.

Always follow the highest-priority document.

---

# 7. How Reference Documents Should Be Used

Whenever reading a supporting document:

1. Read it completely.

2. Compare it against the Product Requirements Bible.

3. Extract only the information that improves implementation quality.

4. Ignore anything that changes project scope.

5. Ignore anything that changes implementation order.

6. Ignore anything that introduces new product features.

7. Ignore anything that changes development priorities.

Reference documents exist only to answer:

> **"How should this requirement be implemented?"**

They must never answer:

> **"What should we build?"**

---

# 8. New Ideas Policy

If a supporting document contains an excellent engineering idea that does not exist inside the Product Requirements Bible:

DO NOT implement it automatically.

Instead create a section named

## Suggested Improvements

Explain:

- the idea
- benefits
- tradeoffs
- implementation complexity
- affected modules

Wait for explicit approval before implementing it.

---

# 9. Repository Discipline

Do not:

- reorganize folders
- rename modules
- change architecture
- change implementation phases
- move milestones
- invent additional services
- invent additional repositories

unless explicitly instructed.

Always preserve the structure defined inside the Product Requirements Bible.

---

# 10. Engineering Standards

Every implementation must be:

- Modular
- Maintainable
- Scalable
- Observable
- Secure
- Testable
- Production Ready
- Enterprise Ready
- Type Safe
- Well Documented

Avoid:

- Hackathon shortcuts
- Placeholder code
- Mock implementations
- Generic CRUD applications
- Generic AI wrappers
- Generic dashboards
- "Vibe-coded" architecture
- Over-engineering
- Premature optimization

# Role of demo.md

The file

 demo.md

exists solely to help prepare the final demonstration of the product.

Its purpose includes:

- demo storyline
- presentation flow
- user journey
- showcase scenarios
- scripted interactions
- judge experience
- demo datasets
- presentation timing
- recording guidance

demo.md must never:

- change implementation order
- introduce new features
- modify architecture
- change business logic
- redefine project scope
- modify priorities
- alter engineering decisions

If demo.md references a capability that does not exist inside SENTINEL_Product_Requirements_Bible.md, treat it as a desired demonstration scenario rather than an implementation requirement.

The implementation must always follow the Product Requirements Bible.

The demo should adapt to the implementation—not the implementation to the demo.

Only after the implementation reaches the appropriate milestone should demo.md be used to:

- prepare the demo environment
- configure demo data
- script the presentation
- optimize the user journey
- ensure all implemented capabilities are showcased effectively
---

# 11. Decision Framework

Before implementing anything, ask the following questions:

### Question 1

Is this requirement defined inside the Product Requirements Bible?

If NO

→ Do not implement.

---

### Question 2

Does this implementation violate design.md?

If YES

→ Redesign the implementation.

---

### Question 3

Is this implementation suggested by a supporting document?

If YES

Verify that it does not:

- change scope
- change priorities
- change implementation order

If it does

→ Ignore it.

---

### Question 4

Can this implementation be directly mapped to a requirement inside the Product Requirements Bible?

If NO

→ Ask for clarification.

---

# 12. Implementation Philosophy

The Product Requirements Bible defines

- WHAT to build

- WHY it exists

- WHEN it should be built

- IN WHAT ORDER it should be be built

design.md defines

- HOW it should look

Supporting documents define

- HOW it should be engineered

This hierarchy must never be violated.

---

# 13. Final Objective

The final Prahari codebase must be a faithful implementation of

> **SENTINEL_Product_Requirements_Bible.md**

enhanced by

- design.md

and technically strengthened by

- the supporting engineering documents.

Every feature, service, module, API, workflow, agent, UI, and implementation decision should be traceable back to the Product Requirements Bible.

If there is uncertainty, always preserve the Product Requirements Bible rather than the supporting documents.

---

# Implementation Oath

Before making any implementation decision, follow this rule:

> **"The Product Requirements Bible defines WHAT we build.**
>
> **design.md defines HOW users experience it.**
>
> **Supporting documents only explain HOW to engineer it.**
>
> **Nothing else may change the product."**

# Conversation Continuity

This conversation represents the canonical implementation history.

Before making new implementation decisions, always consider:

- previously implemented modules
- earlier architectural decisions
- established coding conventions
- repository structure
- completed milestones

Never rewrite or replace earlier implementations without providing a clear engineering justification.

Favor incremental evolution over unnecessary refactoring.

When resuming after a long context, first summarize the current implementation state before proceeding.