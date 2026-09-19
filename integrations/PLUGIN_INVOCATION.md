# @ Plugin Invocation

NIMO-Agent supports an explicit `@` syntax for selecting an integration/provider in a user request.

Examples:

- `@gmail summarize unread mail`
- `@github inspect the latest PR`
- `@calendar schedule a meeting tomorrow`
- `@nimo-core explain the model/API status`
- `@autolab open the lab workflow`

## Invocation contract

The first `@` token selects a registered provider. The remaining text is the task.

The router must:
1. Parse the provider token.
2. Resolve it against the plugin registry.
3. Reject unknown or disabled providers.
4. Pass only the task payload to the selected adapter.
5. Apply the normal Agent permission/risk policy before external side effects.
6. Record provider selection and action in the audit log.

Multiple providers can be explicitly requested in one command, for example:

`@gmail find unread mail @calendar schedule a follow-up`

Multi-provider workflows must execute as separate planned steps and preserve each provider's permission and audit boundary.

The `@` selector chooses the integration; it does not grant extra privileges.