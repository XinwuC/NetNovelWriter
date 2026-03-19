#!/bin/bash
# tests/test_skills_bash.sh

# Setup Mock openclaw.json
MOCK_CONFIG="/tmp/mock_openclaw.json"
echo '{
  "channels": {
    "discord": {
      "token": "secret_token",
      "guilds": {
        "guild_123": {
          "channels": {
            "forum_456": { "allow": true, "requireMention": false }
          }
        }
      }
    }
  },
  "bindings": []
}' > "$MOCK_CONFIG"

echo "✅ Created mock openclaw.json"

# 1. Test Adding Binding (Create Function)
AGENT_NAME_LOWER="test_writer"
THREAD_ID="thread_789"
GUILD_ID="guild_123"

# Run jq command from discord_thread/SKILL.md
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
   }]' "$MOCK_CONFIG" > /tmp/openclaw_updated.json && mv /tmp/openclaw_updated.json "$MOCK_CONFIG"

# Verify Binding Exists
if jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .agentId' "$MOCK_CONFIG" | grep -q "$AGENT_NAME_LOWER"; then
  echo "✅ Test Add Binding: PASS"
else
  echo "❌ Test Add Binding: FAIL"
  exit 1
fi

# 2. Test Lookup Thread ID (Remove Step 1)
# Run jq command from manage_writer/SKILL.md
LOOKUP_THREAD_ID=$(jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .match.peer.id' "$MOCK_CONFIG")

if [ "$LOOKUP_THREAD_ID" = "thread_789" ]; then
  echo "✅ Test Lookup Thread ID: PASS"
else
  echo "❌ Test Lookup Thread ID: FAIL (Got: $LOOKUP_THREAD_ID)"
  exit 1
fi

# 3. Test Removing Binding (Archive Function)
# Run jq command from discord_thread/SKILL.md
jq --arg agentId "$AGENT_NAME_LOWER" \
   'del(.bindings[]? | select(.agentId == $agentId))' \
   "$MOCK_CONFIG" > /tmp/openclaw_updated.json && mv /tmp/openclaw_updated.json "$MOCK_CONFIG"

# Verify Binding is Gone
if jq -r --arg agent "$AGENT_NAME_LOWER" '.bindings[]? | select(.agentId == $agent) | .agentId' "$MOCK_CONFIG" | grep -q "$AGENT_NAME_LOWER"; then
  echo "❌ Test Remove Binding: FAIL (Still exists)"
  exit 1
else
  echo "✅ Test Remove Binding: PASS"
fi

# Cleanup
rm "$MOCK_CONFIG"
echo "✅ All Bash Skill Tests Passed!"
