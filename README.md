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
