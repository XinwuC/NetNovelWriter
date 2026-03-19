---
name: create_discord_thread
description: Creates a named thread in a Discord Forum Channel with idempotency check. Can be called by any agent that needs its own Discord thread.
---

# Discord Thread Skill

Creates a named thread in the configured Discord Forum Channel. Safe to call multiple times —
skips creation if a thread with the same name already exists.

## Prerequisites

- `jq` must be installed (`sudo apt install jq` or `brew install jq`)
- `openclaw.json` must contain `channels.discord.token` and `channels.discord.guilds`
- `GUILD_ID` is the **Discord Server ID** (right-click server name → Copy Server ID) — it is NOT the channel ID
- `FORUM_CHANNEL_ID` is the numeric ID of the Forum Channel

## Usage

Set the agent name, then execute the steps below sequentially:

```bash
AGENT_NAME="<YOUR_AGENT_NAME>"
```

---

## Function: Create

1. **Resolve variables:**
   ```bash
   AGENT_NAME_LOWER=$(echo "$AGENT_NAME" | tr '[:upper:]' '[:lower:]')
   OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

   BOT_TOKEN=$(jq -r '.channels.discord.token' "$OPENCLAW_CONFIG")
   GUILD_ID=$(jq -r '.channels.discord.guilds | keys[0]' "$OPENCLAW_CONFIG")
   FORUM_CHANNEL_ID=$(jq -r '.channels.discord.guilds | to_entries[0].value.channels | keys[0]' "$OPENCLAW_CONFIG")
   ```

2. **Check if thread already exists (idempotency):**
   ```bash
   EXISTING_THREAD_ID=$(curl -s \
     -H "Authorization: Bot ${BOT_TOKEN}" \
     "https://discord.com/api/v10/guilds/${GUILD_ID}/threads/active" \
     | jq -r --arg name "$AGENT_NAME_LOWER" \
       '.threads[] | select(.name == $name) | .id' \
     | head -1)

   if [ -n "$EXISTING_THREAD_ID" ] && [ "$EXISTING_THREAD_ID" != "null" ]; then
     echo "⚠️  Thread already exists: $EXISTING_THREAD_ID — skipping creation"
     THREAD_ID="$EXISTING_THREAD_ID"
   fi
   ```

3. **Create thread if it does not exist:**
   ```bash
   if [ -z "$THREAD_ID" ] || [ "$THREAD_ID" = "null" ]; then
     openclaw message thread create --channel discord \
       --target "channel:${FORUM_CHANNEL_ID}" \
       --thread-name "$AGENT_NAME_LOWER" \
       --message "👋 Hi! I'm **${AGENT_NAME_LOWER}**. Post in this thread to talk to me directly."

     # Fetch the newly created thread ID by name
     THREAD_ID=$(curl -s \
       -H "Authorization: Bot ${BOT_TOKEN}" \
       "https://discord.com/api/v10/guilds/${GUILD_ID}/threads/active" \
       | jq -r --arg name "$AGENT_NAME_LOWER" \
         '.threads[] | select(.name == $name) | .id' \
       | head -1)

     if [ -z "$THREAD_ID" ] || [ "$THREAD_ID" = "null" ]; then
       echo "❌ Failed to create or locate thread for $AGENT_NAME_LOWER"
       exit 1
     fi

     echo "✅ Discord thread created: $THREAD_ID"
   fi
   ```

4. **Write binding to `openclaw.json`:**
   Add a peer binding so OpenClaw routes messages from this thread to the correct agent.
   Skips if a binding for this agent already exists (idempotent).
   ```bash
   OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

   # Check if binding already exists for this agent
   EXISTING_BINDING=$(jq -r --arg agentId "$AGENT_NAME_LOWER"      '.bindings[]? | select(.agentId == $agentId) | .agentId' "$OPENCLAW_CONFIG")

   if [ -n "$EXISTING_BINDING" ]; then
     echo "⚠️  Binding already exists for $AGENT_NAME_LOWER — skipping"
   else
     jq --arg agentId "$AGENT_NAME_LOWER" \
        --arg threadId "$THREAD_ID" \
        --arg guildId "$GUILD_ID" \
        '.bindings += [{
          "agentId": $agentId,
          "match": {
            "channel": "discord",
            "guildId": $guildId,
            "peer": {
              "kind": "channel",
              "id": $threadId
            }
          }
        }]' "$OPENCLAW_CONFIG" > /tmp/openclaw_updated.json && \
     mv /tmp/openclaw_updated.json "$OPENCLAW_CONFIG"
     echo "✅ Binding added for $AGENT_NAME_LOWER → thread $THREAD_ID"
   fi
   ```

   > ⚠️ The forum channel (parent) must also be listed in `openclaw.json` with `"allow": true`
   > and `"requireMention": false`, otherwise messages in threads will be silently dropped:
   > ```json
   > "guilds": {
   >   "<YOUR_GUILD_ID>": {
   >     "channels": {
   >       "<YOUR_FORUM_CHANNEL_ID>": { "allow": true, "requireMention": false }
   >     }
   >   }
   > }
   > ```

5. **Reload OpenClaw Gateway:**
   ```bash
   openclaw gateway restart
   ```

6. **Return the thread ID:**
   `$THREAD_ID` is now set and ready for the caller (e.g. `manage_writer`) to use for
   TOOLS.md and agent.md injection.
   ```bash
   echo "THREAD_ID=\$THREAD_ID"
   ```

---

## Function: Archive

To archive an autonomous Writer Agent's Discord thread and remove its binding:

1. **Resolve variables:**
   ```bash
   AGENT_NAME_LOWER=$(echo "$AGENT_NAME" | tr '[:upper:]' '[:lower:]')
   OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

   BOT_TOKEN=$(jq -r '.channels.discord.token' "$OPENCLAW_CONFIG")
   THREAD_ID=$(jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .match.peer.id' "$OPENCLAW_CONFIG")
   ```

2. **Archive the Discord Thread:**
   ```bash
   if [ -n "$THREAD_ID" ] && [ "$THREAD_ID" != "null" ]; then
     curl -s -X PATCH \
       -H "Authorization: Bot ${BOT_TOKEN}" \
       -H "Content-Type: application/json" \
       -d '{"archived": true, "locked": true}' \
       "https://discord.com/api/v10/channels/${THREAD_ID}"

     echo "✅ Discord thread $THREAD_ID archived"
   fi
   ```

3. **Remove Binding from `openclaw.json`:**
   ```bash
   jq --arg agentId "$AGENT_NAME_LOWER" \
      'del(.bindings[]? | select(.agentId == $agentId))' \
      "$OPENCLAW_CONFIG" > /tmp/openclaw_updated.json && \
   mv /tmp/openclaw_updated.json "$OPENCLAW_CONFIG"
   echo "✅ Binding removed for $AGENT_NAME_LOWER"
   ```

4. **Verify and Fix (Archive):**
   Run this validation to check your work:
   ```bash
   # Check if binding is gone
   jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .agentId' "$OPENCLAW_CONFIG" | grep -q "$AGENT_NAME_LOWER" && echo "❌ Binding still exists, re-run Step 3"
   ```

---

## Troubleshooting

- **`{"message": "Unknown Guild", "code": 10004}`**: `GUILD_ID` is wrong — it must be the Discord **server** ID, not a channel ID. Right-click your server name in Discord → Copy Server ID
- **Thread ID is null after creation**: The `openclaw message thread create` call may have failed — check the command output for errors
- **`jq` not found**: Install with `sudo apt install jq` (Linux) or `brew install jq` (macOS)
- **Multiple guilds/channels in config**: The `jq` selectors use `keys[0]`/`to_entries[0]` (first entry). If you have multiple, replace with the specific guild/channel ID string
- **Messages not reaching agent after binding**: The forum channel must be in `guilds.<id>.channels` with `"allow": true` and `"requireMention": false` — OpenClaw matches threads via their parent forum channel ID, not the thread ID itself
