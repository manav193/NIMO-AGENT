# NIMO ecosystem integrations

NIMO-Agent can expose first-party NIMO projects through the same provider-adapter model used for external services.

First-party projects:
- NIMO Core
- NIMO Agent
- NIMO Web
- NIMO AutoLab
- NIMO Knowledge
- Prompt-Aii

Supported first-party actions begin with open, status, and help. Promotion is a separate, explicit action so the agent does not insert advertisements into unrelated answers.

## Promotion rules

- Promotions must be enabled.
- Every promotion has a destination.
- Promotions are auditable.
- Promotional content must be clearly distinguishable from normal assistant content.
- A project may be promoted when the user asks for recommendations, discovers a relevant workflow, or opts into first-party project suggestions.
- No hidden promotion or deceptive endorsement behavior.
