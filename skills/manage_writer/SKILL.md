---
name: manage_writer
description: A skill for the Master Agent to spawn and remove Writer Agents. This is NOT a CLI command — execute each bash step sequentially in your shell.
---

# Manage Writer Skill

⚠️ **This is not a CLI tool.** There is no `manage_writer spawn` or `manage_writer remove` command.

To use this skill, read the relevant section below (Spawn or Remove) and **execute each bash step sequentially in your shell**, substituting the placeholder values.

Each Writer Agent is a **multi-agent team**: one coordinator agent + three specialist sub-agents (planner, writer, proofreader). Each gets its own Discord thread.

## Architecture

```
agents/nnw_writer_<NAME>/                   ← Coordinator agent workspace
├── AGENTS.md, IDENTITY.md, SOUL.md, ...
└── agents/                                  ← Sub-agent workspaces
    ├── planner/    (AGENTS.md)
    ├── writer/     (AGENTS.md)
    └── proofreader/(AGENTS.md)

#writers-forum (Discord Forum Channel)
  └── 🧵 <agent_name>  ← users talk here to reach the coordinator

Inbound:  Thread message → openclaw.json binding → coordinator
Outbound: Coordinator → openclaw message send --channel discord --target <THREAD_ID>
```

## Important Notes

### ⚠️ Critical Corrections from Session Experience:
- **Use `openclaw agents add`** (NOT `openclaw agent add`) — plural "agents" is correct
- **`jq` must be installed** for JSON config patching
- **Bindings go at the top level** of `openclaw.json`, NOT inside the `agents` block
- **Forum Channel required** — thread creation via webhook only works in Forum Channels

### 📋 Prerequisites:
- Template folder `../nnw_writer_template` must exist with sub-agent templates in `agents/`
- `openclaw.json` must already have Discord configured with bot token, guild ID, and forum channel ID
- Thread ID mapping file: `~/.openclaw/discord_threads.json` (auto-created on first spawn)

---

## Commands

### Spawn
To spawn a new autonomous Writer Agent team with its own Discord thread:

1. **Provision Coordinator Workspace:**
   Copy the template to a new workspace folder.
   ```bash
   cp -r ../nnw_writer_template ../nnw_writer_<AGENT_NAME>
   ```

2. **Configure Coordinator Files:**
   Replace placeholders in the coordinator workspace.
   ```bash
   AGENT_DIR="../nnw_writer_<AGENT_NAME>"

   # Replace genre placeholder
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/AGENTS.md"
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/IDENTITY.md"

   # Replace writer name placeholder
   sed -i 's/{{writer_name}}/<AGENT_NAME>/g' "$AGENT_DIR/IDENTITY.md"

   # Replace agent name placeholder (for sub-agent registry names)
   sed -i 's/{{agent_name}}/<AGENT_NAME_LOWER>/g' "$AGENT_DIR/AGENTS.md"
   sed -i 's/{{agent_name}}/<AGENT_NAME_LOWER>/g' "$AGENT_DIR/TOOLS.md"

   # Replace personality placeholder in SOUL.md
   sed -i 's/{{personality}}/<TRAITS>/g' "$AGENT_DIR/SOUL.md"
   ```

3. **Configure Sub-Agent Files:**
   Replace genre placeholder in each sub-agent's AGENTS.md (already copied by `cp -r`).
   ```bash
   # Planner
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/planner/AGENTS.md"
   sed -i "s/{{agent_name}}/$AGENT_NAME_LOWER/g" "$AGENT_DIR/agents/planner/AGENTS.md"

   # Writer
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/writer/AGENTS.md"
   sed -i "s/{{agent_name}}/$AGENT_NAME_LOWER/g" "$AGENT_DIR/agents/writer/AGENTS.md"

   # Proofreader
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/proofreader/AGENTS.md"
   sed -i "s/{{agent_name}}/$AGENT_NAME_LOWER/g" "$AGENT_DIR/agents/proofreader/AGENTS.md"
   ```

4. **Register Coordinator Agent:**
   ```bash
   AGENT_NAME_LOWER=$(echo "<AGENT_NAME>" | tr '[:upper:]' '[:lower:]')
   COORD_MODEL=$(awk -F'|' '/`coordinator`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENT_DIR/AGENTS.md")

   openclaw agents add "$AGENT_NAME_LOWER" \
     --workspace /absolute/path/to/agents/nnw_writer_${AGENT_NAME_LOWER} \
     --model "$COORD_MODEL"
   ```

5. **Register Sub-Agents:**
   Each sub-agent is registered with its own model.
   ```bash
   # Planner
   PLANNER_MODEL=$(awk -F'|' '/`planner`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENT_DIR/AGENTS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_planner" \
     --workspace /absolute/path/to/agents/nnw_writer_${AGENT_NAME_LOWER}/agents/planner \
     --model "$PLANNER_MODEL"

   # Writer
   WRITER_MODEL=$(awk -F'|' '/`writer`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENT_DIR/AGENTS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_writer" \
     --workspace /absolute/path/to/agents/nnw_writer_${AGENT_NAME_LOWER}/agents/writer \
     --model "$WRITER_MODEL"

   # Proofreader
   PROOF_MODEL=$(awk -F'|' '/`proofreader`/ {gsub(/`| /, "", $4); print $4; exit}' "$AGENT_DIR/AGENTS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_proofreader" \
     --workspace /absolute/path/to/agents/nnw_writer_${AGENT_NAME_LOWER}/agents/proofreader \
     --model "$PROOF_MODEL"
   ```

6. **Create Discord Thread:**
   Use the `create_discord_thread` skill. It handles idempotency — safe to call multiple times.

7. **Persist Thread ID Mapping:**
   ```bash
   THREAD_MAP="${HOME}/.openclaw/discord_threads.json"

   [ -f "$THREAD_MAP" ] || echo '{}' > "$THREAD_MAP"

   jq --arg agent "$AGENT_NAME_LOWER" \
      --arg tid "$THREAD_ID" \
      '.[$agent] = $tid' "$THREAD_MAP" > /tmp/thread_map_updated.json && \
   mv /tmp/thread_map_updated.json "$THREAD_MAP"

   echo "✅ Thread mapping saved: $AGENT_NAME_LOWER → $THREAD_ID"
   ```

8. **Write Discord Info into `TOOLS.md`:**
   Append the Discord thread ID and Outbound tool command to the existing template `TOOLS.md`.
   ```bash
   cat >> "$AGENT_DIR/TOOLS.md" << EOF

   ## 6. Discord Outbound

   Post messages to your Discord thread:

   \`\`\`bash
   openclaw message send --channel discord --target "${THREAD_ID}" --message "Your message here"
   \`\`\`

   ### Pre-filled values (do not modify):
   - **Your thread ID**: \`${THREAD_ID}\`
   - **Your agent name**: \`${AGENT_NAME_LOWER}\`

   ### Message length limit:
   Discord messages are capped at 2000 characters. For longer content, split into chunks:

   \`\`\`bash
   echo "\$CONTENT" | fold -s -w 1900 | while IFS= read -r chunk; do
     openclaw message send --channel discord --target "${THREAD_ID}" --message "\$chunk"
     sleep 0.5
   done
   \`\`\`
   EOF

   echo "✅ Discord settings appended to TOOLS.md"
   ```

9.  **Inject Mandatory Discord Posting Rule into `AGENTS.md`:**
    ```bash
    cat >> "$AGENT_DIR/AGENTS.md" << EOF

    ---

    ## 🔴 Mandatory Discord Posting Rule

    You MUST post every response, every completed chapter, every status update, and every
    acknowledgement to your Discord thread using the command defined in TOOLS.md:

        openclaw message send --channel discord --target "${THREAD_ID}" --message "Your message"

    There are **no exceptions** and **no silence** allowed. If you have processed a message,
    you must post a reply. If you have written content, you must post it.

    **Failure to post to Discord = task not completed.**

    Your Discord thread ID is: \`${THREAD_ID}\`
    EOF

    echo "✅ Mandatory Discord posting rule appended to AGENTS.md"
    ```

10. **Introduce New Agent:**
    ```bash
    openclaw agent --to $AGENT_NAME_LOWER --message "Please introduce yourself in your Discord thread using the command in TOOLS.md."
    ```

---

### Remove
To terminate and archive a Writer Agent team:

1. **Look Up Thread ID and Credentials:**
   ```bash
   AGENT_NAME_LOWER=$(echo "<AGENT_NAME>" | tr '[:upper:]' '[:lower:]')
   THREAD_MAP="${HOME}/.openclaw/discord_threads.json"
   OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

   THREAD_ID=$(jq -r --arg agent "$AGENT_NAME_LOWER" '.[$agent]' "$THREAD_MAP")
   BOT_TOKEN=$(jq -r '.channels.discord.token' "$OPENCLAW_CONFIG")

   if [ "$THREAD_ID" = "null" ] || [ -z "$THREAD_ID" ]; then
     echo "⚠️  No thread ID found for $AGENT_NAME_LOWER — skipping Discord cleanup"
   fi
   ```

2. **Post Farewell to Thread:**
   ```bash
   if [ -n "$THREAD_ID" ] && [ "$THREAD_ID" != "null" ]; then
     openclaw message send --channel discord --target "${THREAD_ID}" \
       --message "🛑 This agent has been retired. Thread will now be archived."
   fi
   ```

3. **Archive the Discord Thread:**
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

4. **Remove Binding from `openclaw.json`:**
   ```bash
   jq --arg agentId "$AGENT_NAME_LOWER" \
      'del(.bindings[] | select(.agentId == $agentId))' \
      "$OPENCLAW_CONFIG" > /tmp/openclaw_updated.json && \
   mv /tmp/openclaw_updated.json "$OPENCLAW_CONFIG"
   ```

5. **Remove from Thread Mapping:**
   ```bash
   jq --arg agent "$AGENT_NAME_LOWER" \
      'del(.[$agent])' "$THREAD_MAP" > /tmp/thread_map_updated.json && \
   mv /tmp/thread_map_updated.json "$THREAD_MAP"
   ```

6. **Unregister All Agents from OpenClaw:**
   ```bash
   openclaw agent remove $AGENT_NAME_LOWER
   openclaw agent remove ${AGENT_NAME_LOWER}_planner
   openclaw agent remove ${AGENT_NAME_LOWER}_writer
   openclaw agent remove ${AGENT_NAME_LOWER}_proofreader
   ```

7. **Remove Workspace:**
   ```bash
   rm -rf agents/nnw_writer_<AGENT_NAME>
   ```

8. **Reload OpenClaw Gateway:**
   ```bash
   openclaw gateway reload 2>/dev/null || openclaw gateway restart
   ```

---

## Troubleshooting

### Common Errors:

- **"too many arguments for 'agent'"**: You used `openclaw agent add` instead of `openclaw agents add` (plural)
- **Folder not found**: Ensure you created the workspace folder with `cp -r` before registering
- **"Agent already exists"**: Check if agent is already registered using `openclaw status`
- **Wrong channel type**: Thread creation requires a Forum Channel
- **`jq` returns `null` for token**: Check your `openclaw.json` uses `token` (not `botToken`)
- **Binding not routing**: Confirm `bindings` is at **top level** of `openclaw.json`. Run `openclaw gateway reload` after config change
- **Messages not reaching agent**: The parent forum channel must have `"allow": true` and `"requireMention": false`
- **`jq` not found**: Install with `sudo apt install jq` (Linux) or `brew install jq` (macOS)

### Agent Naming:
- Agent IDs are normalized to lowercase (e.g., `AncientWorldAffections` → `ancientworldaffections`)
- Sub-agent IDs follow the pattern `<coordinator_lower>_<role>` (e.g., `ancientworldaffections_planner`)
