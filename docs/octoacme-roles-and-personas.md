# OctoAcme Roles and Personas

## Purpose

This document expands role clarity in the OctoAcme project management process so ownership is explicit from planning to delivery, release, and follow-up.

## Why this matters

- Reduces handoff gaps by defining who owns each decision.
- Improves accountability by mapping responsibilities to named roles.
- Speeds up delivery by clarifying escalation and communication paths.
- Improves quality by giving testing, release readiness, and operational feedback a clear owner.

## Existing Core Roles (Reference)

These existing roles are already part of the process and are referenced by the added personas below:

- Product Manager (PM): Prioritizes backlog, defines outcomes, and approves scope.
- Engineering Lead (Eng Lead): Owns technical direction, architecture alignment, and implementation quality.
- Developer: Implements features and fixes, writes tests, and addresses review feedback.
- Reviewer: Reviews code quality, maintainability, and correctness before merge.

## Proposed New Personas and Roles

### 1) Delivery Manager

Responsibilities:
- Tracks milestone progress and delivery risk across active work items.
- Runs weekly delivery checkpoints and keeps dependencies visible.
- Flags scope creep and coordinates re-planning with PM and Eng Lead.

Interactions with existing roles:
- PM: Aligns delivery plan with priority and release goals.
- Eng Lead: Aligns timeline with technical constraints and sequencing.
- Developer: Resolves blockers and confirms realistic completion forecasts.

### 2) Quality Champion

Responsibilities:
- Defines test strategy for each iteration (unit, integration, and regression coverage).
- Verifies acceptance criteria are testable and measurable.
- Curates quality gates before merge and before release.

Interactions with existing roles:
- PM: Converts product acceptance criteria into test scenarios.
- Eng Lead: Aligns quality gates with architecture and risk profile.
- Developer and Reviewer: Ensures test evidence exists for critical changes.

### 3) Release Coordinator

Responsibilities:
- Owns release readiness checklist and go/no-go coordination.
- Confirms changelog completeness, rollback plan, and communication readiness.
- Coordinates release window activities and post-release verification.

Interactions with existing roles:
- PM: Confirms business readiness and stakeholder communication.
- Eng Lead: Confirms technical readiness and rollback safety.
- Developer: Verifies deployment tasks and production checks are complete.

### 4) Stakeholder Liaison

Responsibilities:
- Captures operational and user feedback for planning input.
- Maintains traceability between reported issues and roadmap items.
- Coordinates expectation-setting with non-engineering stakeholders.

Interactions with existing roles:
- PM: Feeds validated stakeholder needs into backlog prioritization.
- Eng Lead: Communicates technical trade-offs in stakeholder-friendly terms.
- Developer: Clarifies issue context and expected behavior for fixes.

### 5) Metrics Analyst

Responsibilities:
- Defines delivery and quality metrics (lead time, defect leakage, cycle time).
- Publishes iteration reports with trends and improvement recommendations.
- Helps the team evaluate process changes using measurable outcomes.

Interactions with existing roles:
- PM: Aligns metrics with product outcomes and planning decisions.
- Eng Lead: Uses technical metrics to target systemic improvements.
- Reviewer and Developer: Highlights recurring defects and rework patterns.

## Accountability Improvements

With these added personas, the process gains explicit ownership for:

- Delivery predictability: Delivery Manager
- Quality governance: Quality Champion
- Release safety: Release Coordinator
- Stakeholder alignment: Stakeholder Liaison
- Continuous improvement through data: Metrics Analyst

## Expected Project Outcome Improvements

- Fewer missed deadlines due to proactive risk tracking.
- Better release stability with ownership of readiness and rollback.
- Clearer requirements-to-test traceability, reducing rework.
- Faster response to stakeholder needs with a dedicated communication role.
- Better decision-making with process and quality metrics.