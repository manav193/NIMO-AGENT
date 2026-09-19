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
