## Post a Message to Your Discord Thread
```bash
openclaw message send --channel discord --target "1481874596780183632" --message "Your message here"
```

### For long messages (over 2000 characters):
```bash
echo "$CONTENT" | fold -s -w 1900 | while IFS= read -r chunk; do
  openclaw message send --channel discord --target "1481874596780183632" --message "$chunk"
  sleep 0.5
done
```

---

## Post a Message to the Main Discord Channel

Read channel ID from `openclaw.json`:
```bash
CHANNEL_ID=$(jq -r '.channels.discord.guilds | to_entries[0].value.channels | keys[0]' \
  "$HOME/.openclaw/openclaw.json")

openclaw message send --channel discord --target "$CHANNEL_ID" --message "Your message here"
```

---

## Spawn or Remove a Writer Agent

Refer to the `create_discord_thread` skill and `manage_writer` skill in your skills directory.

## WhatsApp Messaging
- You can send notifications to the user via WhatsApp.
- When you need to notify the user, send a message through the WhatsApp channel