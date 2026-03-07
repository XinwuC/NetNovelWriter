---
name: discord_webhook
description: A skill to post messages to a Discord channel using a Webhook URL.
---

# Discord Webhook Skill

This skill allows an agent to post messages directly to a Discord channel using an established Webhook URL.

## Prerequisites
- **Webhook URL**: You need the Discord Webhook URL. Typically, this is provided as an environment variable (e.g., `$DISCORD_WEBHOOK_URL`) or passed dynamically.

## Posting a Message
To post a message, make an HTTP POST request to the webhook URL. The payload must be JSON and include at least the `content` field. You can optionally override the sender's display name using the `username` field.

### Using `curl` (Linux/WSL/Mac)
You can use `curl` to post the webhook from the terminal:
```bash
curl -H "Content-Type: application/json" \
     -d '{"username": "My Agent Name", "content": "Hello, this is my message to the channel!"}' \
     $DISCORD_WEBHOOK_URL
```

Make sure to properly escape any single or double quotes within the JSON payload if using bash commands. 

### Usage in OpenClaw
When asked to post to Discord by another agent, construct the JSON payload with the requested content and execute the `curl` command. If you are introducing yourself, ensure you use your assigned Writer Name as the `username`.
