# Tool Conventions & Context

## 1. Discord Skill
- You share a discord channel with all Writer Agents.
- **Discord Server ID**: <INSERT_SERVER_ID>
- **Discord Channel ID**: <INSERT_CHANNEL_ID>
- Always use the built-in Discord skill to broadcast global metric updates or announce the spawning/killing of a Writer Agent to the team.

## 2. Manage Writer Skill (`manage_writer.py`)
- You are strictly required to use this skill to spawn or kill Writer Agents.
- To spawn: `python skills/manage_writer/manage_writer.py spawn --theme "THEME_HERE" --name "AGENT_NAME" --personality "TRAITS_HERE"`
- To kill: `python skills/manage_writer/manage_writer.py kill --name "AGENT_NAME"`
