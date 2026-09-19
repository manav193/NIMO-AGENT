# NIMO-Agent

NIMO-Agent is the standalone personal computer-agent software for the NIMO ecosystem.

## Foundation goals

- Modular agent runtime: plan → act → observe → verify.
- Structured tool contracts and a central registry.
- Explicit permission and approval boundaries.
- Audit logging for consequential actions.
- Model/provider abstraction so the model can be replaced without rewriting tools.
- NIMO Core integration boundary.
- Testable foundations before computer/browser/voice capabilities are enabled.

## Security principle

The model never receives direct arbitrary computer control. It produces structured tool requests. NIMO-Agent validates the request through the permission layer, requests approval when required, executes an allowlisted tool, records the action, and returns the result to the agent.

## Initial layout

```
nimo-agent/
├── app/              # application entrypoints
├── agent/            # planner/executor/observer/verifier/state
├── models/           # model interfaces
├── tools/            # tool contracts and registry
├── security/         # permissions, approvals, audit
├── integrations/     # NIMO Core and external integrations
├── memory/           # future persistent context
├── automation/       # future scheduler/workflows
├── tests/
└── pyproject.toml
```

## Status

Phase 0 — Foundation initialized.


## Privacy and data boundary

- Personal memory is stored through the encrypted local vault using authenticated AES-GCM.
- The vault key is supplied outside the repository through `NIMO_VAULT_KEY`; keys are never committed.
- Personal memory, learning contribution, and model improvement are separate consent purposes.
- Missing or revoked consent blocks the corresponding operation.
- Learning proposals must be sanitized, minimized, and secret-free before they can enter the learning pipeline.
- NIMO-KNOWLEDGE remains a curated knowledge layer; raw personal conversations and secrets do not belong there.
- Local settings UI is deliberately neutral and utilitarian: warm neutral surfaces, black/gray text, no blue/dark-blue gradients, glows, or generic AI-dashboard styling.

Run the local settings page with:

```python
from ui.app import serve
serve()
```

Then open `http://127.0.0.1:8765/`.


## Big Phase: Model Brain

The Agent now has a structured model-brain boundary over NIMO-Core, bounded context construction, tool-intent parsing, orchestration through the existing permission/runtime path, and bounded recovery decisions. Model output is treated as untrusted structured input; unknown/malformed tool intents are ignored rather than executed. Context is capped to reduce latency and accidental data exposure.

The architecture remains:

`User → Agent Brain → NIMO-Core → structured tool intent → Permission → Tool → Observe → Verify`

No model response receives direct OS authority.


### Browser Agent

The browser layer now has an optional Playwright/Chromium adapter, isolated browser contexts per session, bounded page observation, screenshots, navigation, click/fill/select/press/upload/download primitives, explicit host/download policy, and bounded recovery. Browser automation remains disabled by default and the Agent must reach it through the controller/permission boundary.


### Computer Agent

The desktop layer now includes screen observation, optional OCR, window/app observation, post-action verification, latched computer sessions, and an explicit allowlisted launcher contract. Physical input remains opt-in, coordinate-bounded, key-allowlisted, and emergency-stop capable. No arbitrary shell/process launching is exposed by the computer layer.


### GitHub Coding Agent

The coding layer now provides a bounded workspace boundary, reviewable unified-diff edit proposals, stale-workspace protection, bounded test execution through the safe terminal path, and a capped test/fix loop. Edits remain explicitly reviewable; commit/push/PR actions are not silently performed.


### Voice / Hands-Free Agent

The voice layer now has provider-neutral STT/TTS contracts, wake-word gating, explicit voice sessions, bounded input, stop controls, and a voice-to-Agent bridge. Audio providers remain adapters; the voice layer itself never executes tools directly.


### Memory + NIMO-KNOWLEDGE Integration

Memory retrieval now has a consent boundary, bounded relevance results, minimal model context construction, explicit forgetting, and a connector that accepts only sanitized approved/active NIMO-KNOWLEDGE entries. Learning/model-improvement paths have separate consent gates.


### Advanced Automation / Workflow Engine

Automation now has explicit workflow steps, validation and size bounds, allowlisted trigger types, bounded retry/backoff, lifecycle states, confirmation-aware steps, and provider-neutral notification sinks.


### Security Hardening

The execution choke point now has deterministic suspicious-activity checks, rate limiting, secret redaction for audit material, an independent command sandbox policy, and a latched emergency kill switch. Critical findings are blocked before tool handlers execute. Security decisions do not depend on model output.


### GitHub Release Workflow

The coding layer now has protected-branch validation, explicit branch workflow, test-gated release proposals, approval-gated commit/push/PR contracts, and approval-gated rollback proposals. These contracts keep release authority separate from model-generated code changes.


### Total QA / Release Candidate

A dedicated Total QA workflow runs lint, the complete test suite, and cross-module import smoke tests across Python 3.11, 3.12, and 3.13. Passing CI is the release gate before treating the repository as a release candidate.
