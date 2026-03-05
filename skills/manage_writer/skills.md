---
name: manage_writer
description: A command-line skill for the Master Agent to dynamically spawn and archive Writer Agents within the OpenClaw environment.
---

# Manage Writer Skill

This skill is designed specifically for the Master Agent to oversee its fleet of Writer Agents.

## Commands

### Spawn
Copies the default template to spawn a new autonomous Writer Agent.
`python manage_writer.py spawn --theme "THEME" --name "AGENT_NAME" --personality "TRAITS"`

### Kill
Terminates and archives a failing Writer Agent.
`python manage_writer.py kill --name "AGENT_NAME"`
