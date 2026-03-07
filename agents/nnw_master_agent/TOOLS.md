# Tool Conventions & Context

## 1. Discord Skill
- You share a discord channel with all Writer Agents.
- **Discord Server ID**: 1479013060084502682
- **Discord Channel ID**: 1479013060705521863
- Always use the built-in Discord skill to broadcast global metric updates or announce the spawning/killing of a Writer Agent to the team.

## 2. Manage Writer Skill (`skills/manage_writer`)
- You are strictly required to use this skill to spawn or kill Writer Agents.
- **CRITICAL**: The manage writer skill does NOT use a Python script. Instead, it relies on a specific sequence of agentic shell commands.
- You **MUST** read `skills/manage_writer/SKILL.md` every single time before attempting to spawn or kill a writer agent, as the exact commands and steps may change over time.
- Use `cat skills/manage_writer/SKILL.md` (or your preferred file reading tool) to understand the current procedure for provisioning, configuring, and registering the agent.
