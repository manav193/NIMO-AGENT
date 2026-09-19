# NIMO Automation Provider Manifest

Provider-neutral adapters allow integrations to be added without changing the agent runtime.

Provider families:
- Email: Gmail, Outlook, Resend
- Calendar: Google Calendar, Outlook Calendar
- Messaging: Slack, Discord, Teams
- Productivity: Notion, Google Drive, Dropbox
- Developer: GitHub, GitLab
- Project management: Jira, Linear, Trello
- CRM/support: Salesforce, HubSpot, Zendesk
- Meetings: Zoom, Calendly
- Commerce/operations: Shopify and other authorized provider APIs

Standard adapter contract:
1. Authentication/credential boundary
2. Read/search operations
3. Create/update operations
4. Event/webhook ingestion
5. Scheduled actions
6. Idempotency/deduplication
7. Retry/backoff
8. Audit events
9. Permission/risk classification
10. Rate-limit handling

AI-generated messages are distinct from deterministic acknowledgements. Sending AI-generated content is an external side effect and follows the active Agent mode and provider policy.
