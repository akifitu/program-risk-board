# Step-By-Step Plan

## Phase 1: Define the board

1. Decide which program-level risks matter to the portfolio story.
2. Define ownership, gate, and status fields.
3. Choose a repeatable scoring model.

## Phase 2: Build the data model

1. Store open risks in machine-readable form.
2. Link every risk to at least one workstream or repository.
3. Capture mitigation actions and residual scoring.

## Phase 3: Implement the analytics

1. Validate scale values and required fields.
2. Calculate initial and residual RPN values.
3. Export gate-level and risk-level summary artifacts.

## Phase 4: Debug and verify

1. Add tests for invalid scores and missing owners.
2. Confirm residual rankings match the input data.
3. Fix exporter gaps until the repo audits cleanly.

## Phase 5: Publish professionally

1. Write a clear README and documentation index.
2. Commit generated outputs for reviewers.
3. Push publicly and keep CI green.

## To-Do

- [x] define the risk schema
- [x] create a realistic program-level dataset
- [x] implement validation and export logic
- [x] add regression tests
- [x] publish the repository
