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

## WhatsApp Messaging
- You can send notifications to the user via WhatsApp.
```bash
openclaw message send --channel whatsapp --target "<phone_number>" --message "<message>"
```