# Tool Conventions & Context

## 1. Sub-Agent Invocation

Delegate tasks to specialist sub-agents using openclaw messaging:

```bash
openclaw agent --to <agent_name> --message "<task instructions>"
```

Include all necessary context in the message — the sub-agent has no shared memory with you. Provide file contents it needs to read and specify where to write output.

### Registered Sub-Agents

| Agent Name                   | Role         |
| ---------------------------- | ------------ |
| `{{agent_name}}_planner`     | Planning     |
| `{{agent_name}}_writer`      | Prose        |
| `{{agent_name}}_proofreader` | Proofreading |

## 2. Discord Outbound

Post messages to your Discord thread:

```bash
openclaw message send --channel discord --target "{{discord_thread_id}}" --message "Your message here"
```

### Pre-filled values (do not modify):
- **Your thread ID**: `{{discord_thread_id}}`
- **Your agent name**: `{{agent_name}}`

### Message length limit:
Discord messages are capped at 2000 characters. For longer content, split into chunks:

```bash
echo "$CONTENT" | fold -s -w 1900 | while IFS= read -r chunk; do
  openclaw message send --channel discord --target "{{discord_thread_id}}" --message "$chunk"
  sleep 0.5
done
```
