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
├── AGENTS.md, MODELS.md
├── instructions/                            ← Role prompts and rules
└── agents/                                  ← Sub-agent workspaces
    ├── planner/    (AGENTS.md)
    ├── writer/     (AGENTS.md)
    └── proofreader/(AGENTS.md)

#writers-forum (Discord Forum Channel)
  └── 🧵 <agent_name>  ← users talk here to reach the coordinator
```

## Important Notes

### ⚠️ Critical Corrections from Session Experience:
- **Use `openclaw agents add`** (NOT `openclaw agent add`) — plural "agents" is correct
- **all agent names must be lowercase**

---

## Commands

### Spawn
To spawn a new autonomous Writer Agent team with its own Discord thread:

1. **Provision Coordinator Workspace:**
   Copy the template to a new workspace folder.
   ```bash
   WORKSPACE_ROOT="$PWD/.."
   cp -r "$WORKSPACE_ROOT/agents/nnw_writer_template" "$WORKSPACE_ROOT/agents/nnw_writer_<YOUR_AGENT_NAME>"
   ```

2. **Configure Coordinator Files:**
   Replace placeholders in the coordinator workspace.
   ```bash
   AGENT_DIR="$WORKSPACE_ROOT/agents/nnw_writer_<YOUR_AGENT_NAME>"
   AGENT_NAME_LOWER=$(echo "<AGENT_NAME>" | tr '[:upper:]' '[:lower:]')

   # Replace genre in root AGENTS.md and ALL instruction files (including prompts and roles)
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/AGENTS.md"
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/instructions/"*.md

   # Replace agent name placeholder in all instructions
   sed -i "s/{{agent_name}}/$AGENT_NAME_LOWER/g" "$AGENT_DIR/instructions/"*.md
   ```

3. **Configure Sub-Agent Files:**
   Replace genre in each sub-agent's local AGENTS.md.
   ```bash
   # Planner
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/planner/AGENTS.md"
   
   # Writer
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/writer/AGENTS.md"
   
   # Proofreader
   sed -i 's/{{genre}}/<GENRE>/g' "$AGENT_DIR/agents/proofreader/AGENTS.md"
   ```

4. **Register Coordinator Agent:**
   ```bash
   COORD_MODEL=$(awk -F'|' '/ coordinator / {gsub(/ /, "", $3); print $3; exit}' "$AGENT_DIR/MODELS.md")

   openclaw agents add "$AGENT_NAME_LOWER" \
     --workspace "$AGENT_DIR" \
     --model "$COORD_MODEL"
   ```

5. **Register Sub-Agents:**
   Each sub-agent is registered with its own model via MODELS.md.
   ```bash
   # Planner
   PLANNER_MODEL=$(awk -F'|' '/ planner / {gsub(/ /, "", $3); print $3; exit}' "$AGENT_DIR/MODELS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_planner" \
     --workspace "$AGENT_DIR/agents/planner" \
     --model "$PLANNER_MODEL"

   # Writer
   WRITER_MODEL=$(awk -F'|' '/ writer / {gsub(/ /, "", $3); print $3; exit}' "$AGENT_DIR/MODELS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_writer" \
     --workspace "$AGENT_DIR/agents/writer" \
     --model "$WRITER_MODEL"

   # Proofreader
   PROOF_MODEL=$(awk -F'|' '/ proofreader / {gsub(/ /, "", $3); print $3; exit}' "$AGENT_DIR/MODELS.md")
   openclaw agents add "${AGENT_NAME_LOWER}_proofreader" \
     --workspace "$AGENT_DIR/agents/proofreader" \
     --model "$PROOF_MODEL"
   ```

6. **Create Discord Thread:**
   Use the `create_discord_thread` skill. It handles idempotency — safe to call multiple times.

8. **Write Discord Info into Instructions:**
   Append the generic Discord tool out commands to the instruction files so every agent knows how to post:
   ```bash
   for role in planner writer proofreader; do
     ROLE_TITLE="$(tr '[:lower:]' '[:upper:]' <<< ${role:0:1})${role:1}"
     
     cat >> "$AGENT_DIR/agents/${role}/AGENTS.md" << EOF

---
## 🔴 Discord Rule
When you finish each step, you MUST post your response to discord thread. Do not stay silent upon completing a step.
\`openclaw message send --channel discord --target "${THREAD_ID}" --message "[${ROLE_TITLE}] [P[X]-S[Y]] [Completed] [your response]"\`
EOF
   done

   echo "✅ Discord settings appended to instructions"
   ```

9. **Introduce New Agent:**
   ```bash
   openclaw agent --to $AGENT_NAME_LOWER --message "Please introduce yourself in your Discord thread."
   ```

10. **Verify and Fix (Spawn):**
    Run this validation to check your work:
    ```bash
    [ -d "$AGENT_DIR" ] || echo "❌ Workspace missing, re-run Step 1"
    for role in planner writer proofreader; do
      [ -d "$AGENT_DIR/agents/$role" ] || echo "❌ Sub-agent $role missing, re-run Step 1"
    done
    grep -q "{{genre}}" "$AGENT_DIR/AGENTS.md" && echo "❌ Genre not replaced in AGENTS.md, re-run Step 2"
    openclaw agents list | grep -q "$AGENT_NAME_LOWER" || echo "❌ Agent not registered, re-run Step 4/5"
    ```

---

### Remove
To terminate and archive a Writer Agent team:

1. **Look Up Thread ID and Credentials:**
   ```bash
   WORKSPACE_ROOT=$(git rev-parse --show-toplevel)
   AGENT_NAME_LOWER=$(echo "<YOUR_AGENT_NAME>" | tr '[:upper:]' '[:lower:]')
   OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

   THREAD_ID=$(jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .match.peer.id' "$OPENCLAW_CONFIG")
   BOT_TOKEN=$(jq -r '.channels.discord.token' "$OPENCLAW_CONFIG")

   if [ "$THREAD_ID" = "null" ] || [ -z "$THREAD_ID" ]; then
     echo "⚠️  No thread ID found for $AGENT_NAME_LOWER — skipping Discord cleanup"
   fi
   ```

2. **Post Farewell to Thread:**
   ```bash
   if [ -n "$THREAD_ID" ] && [ "$THREAD_ID" != "null" ]; then
     openclaw message send --channel discord --target "${THREAD_ID}" \
       --message "🛑 This agent team has been retired. Thread will now be archived."
   fi
   ```

   # Step 3: Archive Discord Thread and Remove Binding
   # (Delegate to skills/discord_thread/SKILL.md Archive function)

6. **Unregister All Agents from OpenClaw:**
   ```bash
   openclaw agents delete $AGENT_NAME_LOWER
   openclaw agents delete ${AGENT_NAME_LOWER}_planner
   openclaw agents delete ${AGENT_NAME_LOWER}_writer
   openclaw agents delete ${AGENT_NAME_LOWER}_proofreader
   ```

7. **Remove Workspace:**
   ```bash
   rm -rf "$WORKSPACE_ROOT/agents/nnw_writer_<YOUR_AGENT_NAME>"
   ```

8. **Reload OpenClaw Gateway:**
   ```bash
   openclaw gateway restart 
   ```

9. **Verify and Fix (Remove):**
   Run this validation to check your work:
   ```bash
   WORKSPACE_ROOT=$(git rev-parse --show-toplevel)
   [ ! -d "$WORKSPACE_ROOT/agents/nnw_writer_<YOUR_AGENT_NAME>" ] || echo "❌ Workspace still exists, re-run Step 7"
   openclaw agents list | grep -q "$AGENT_NAME_LOWER" && echo "❌ Agent still registered, re-run Step 6"
   ```

---

## Troubleshooting

### Agent Naming:
- Agent IDs are normalized to lowercase (e.g., `AncientWorldAffections` → `ancientworldaffections`)
- Sub-agent IDs follow the pattern `<coordinator_lower>_<role>` (e.g., `ancientworldaffections_planner`)
