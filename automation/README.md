# NIMO-Agent Automations

The automation layer supports:
- Schedule triggers for timed or recurring actions.
- Event triggers for external events such as incoming email.

Planned email workflows:
1. Automatic receipt acknowledgement.
2. Scheduled outgoing email.
3. AI-assisted reply drafting.
4. Optional automatic AI replies when explicitly enabled.
5. Follow-up reminders and escalation rules.

Provider credentials stay behind an adapter boundary. Gmail, Outlook, Resend, or another provider can implement the email interface without putting credentials inside the agent core.

AI replies should pass through policy before sending. Policy can require confirmation, limit recipients/domains, prevent sensitive-data disclosure, and keep an audit record.
