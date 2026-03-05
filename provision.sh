#!/bin/bash

echo "=== Provisioning NetNovelWriters OpenClaw Environment ==="

# 1. Check if OpenClaw CLI is installed in the environment
if ! command -v openclaw &> /dev/null
then
    echo "⚠️  OpenClaw CLI is not found in PATH."
    echo "Make sure you are running this in your shared openclaw environment."
else
    echo "✅ OpenClaw CLI is available."
fi

# 2. Re-affirm required skills presence
echo "Checking required skills..."
echo "ℹ️  Note: Please ensure that 'agent-browser' and the built-in discord skills are installed globally."

# 3. Setup Environment Variables
echo "Checking for .env configuration file..."
if [ ! -f ".env" ]; then
    echo "ℹ️  Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please remember to edit .env with your Fanqie credentials before starting the agent!"
else
    echo "✅ .env file already exists."
fi

# 4. Setup permissions for custom skills
echo "Setting executable permissions for custom skills..."
chmod +x skills/*/*.py

# 4. Success message
echo "✅ Custom NetNovelWriters skills and agent workspaces have been configured."
echo ""
echo "You can now boot up the master agent by running:"
echo "  openclaw start ./agents/nnw_master_agent"
echo "========================================================="
