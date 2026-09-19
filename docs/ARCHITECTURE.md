# NIMO-Agent Foundation Architecture

## Runtime boundary

```
User
  ↓
Agent Runtime
  ↓
Structured Tool Request
  ↓
Permission Engine
  ↓
Approval (when required)
  ↓
Tool Execution
  ↓
Observation / Result
  ↓
Verifier
  ↓
Agent
```

The model is never the execution authority.

## Risk levels

- **read** — inspection/search operations.
- **safe** — reversible local actions.
- **confirmed** — consequential external/destructive actions requiring approval.
- **restricted** — blocked by default.

## Extension points

Future phases attach filesystem, terminal, browser, computer-control, GitHub, voice, memory and automation tools behind the same contracts.
