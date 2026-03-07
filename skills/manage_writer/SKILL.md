---
name: manage_writer
description: A command-line skill for the Master Agent to dynamically spawn and archive Writer Agents within the OpenClaw environment.
---

# Manage Writer Skill

This skill is designed specifically for the Master Agent to oversee its fleet of Writer Agents. Instead of relying on a static python script, you should execute these steps sequentially using your core shell capabilities.

## Important Notes

### ⚠️ Critical Corrections from Session Experience:
- **Use `openclaw agents add`** (NOT `openclaw agent add`) - plural "agents" is correct

### 📋 Prerequisites:
- Workspace folder must exist (created via `cp -r`)
- Agent files (`agent.md`, `SOUL.md`) must be properly configured with theme/personality
- Environment variable `$DISCORD_WEBHOOK_URL` should be set for Discord announcements

## Commands

### Spawn
To spawn a new autonomous Writer Agent, execute the following bash commands:

1. **Provision Workspace:**
   Copy the default template to a new workspace folder for the agent.
   ```bash
   cp -r agents/nnw_writer_template agents/nnw_writer_<AGENT_NAME>
   ```

2. **Configure Files:**
   Replace the placeholders `{{theme}}` and `{{writer_name}}` in the newly created `agent.md`, and `{{personality}}` in `SOUL.md`. 
   You can use `sed` for this:
   ```bash
   # Replace theme placeholder
   sed -i 's/{{theme}}/<THEME>/g' agents/nnw_writer_<AGENT_NAME>/agent.md
   
   # Replace writer name placeholder
   sed -i 's/{{writer_name}}/<AGENT_NAME>/g' agents/nnw_writer_<AGENT_NAME>/agent.md
   
   # Replace personality placeholder in SOUL.md
   sed -i 's/{{personality}}/<TRAITS>/g' agents/nnw_writer_<AGENT_NAME>/SOUL.md
   ```

3. **Register Agent:**
   Register the newly provisioned workspace to the OpenClaw environment.
   **Use absolute paths** and use `agents` (plural) subcommand:
   ```bash
   openclaw agents add <AGENT_NAME> --workspace /absolute/path/to/workspace --model <the model you are using or user specified model>
   
   # Example:
   openclaw agents add ancientworldaffections --workspace /mnt/e/NetNovelWriter/agents/nnw_writer_AncientWorldAffections --model ollama/qwen3.5
   ```

4. **Discord Webhook (Introduce Agent):**
   
   **Option A**: Use `discord_webhook` skill if webhook URL is configured:
   ```bash
   curl -H "Content-Type: application/json" \
        -d '{"username": "<AGENT_NAME>", "content": "Welcome message..."}' \
        $DISCORD_WEBHOOK_URL
   ```
   
   **Option B**: Alternatively, use OpenClaw's internal routing:
   ```bash
   openclaw agent --to discord --message "Introduction message for the new agent"
   ```

5. **Assign Task to New Agent:**
   Finally, use OpenClaw messaging to ask the new agent to begin working, which will spin up the process properly:
   ```bash
   openclaw agent --to <AGENT_NAME> --message "Please introduce yourself to the discord channel using the discord_webhook skill and begin your writing task."
   ```

### Kill
To terminate and archive a failing Writer Agent:

1. **Remove Workspace:**
   ```bash
   rm -rf agents/nnw_writer_<AGENT_NAME>
   ```

2. **Unregister Agent:**
   Remove the agent from the OpenClaw registry.
   ```bash
   openclaw agent remove <AGENT_NAME>
   ```

## Troubleshooting

### Common Errors:

- **"too many arguments for 'agent'"**: You used `openclaw agent add` instead of `openclaw agents add` (plural)
- **Folder not found**: Ensure you created the workspace folder with `cp -r` before attempting to register
- **"Agent already exists"**: Check if an agent with that ID is already registered using `openclaw status`

### Agent Naming:
- Agent IDs will be normalized to lowercase (e.g., `AncientWorldAffections` → `ancientworldaffections`)
- Consider using English names for better cross-platform compatibility
