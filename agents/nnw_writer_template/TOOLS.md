# Tool Conventions & Context

## 1. Discord Skill
- You use Discord to discuss plot points and ask for advice from the Master Agent or your peers.
- **Discord Server ID**: <INSERT_SERVER_ID>
- **Discord Channel ID**: <INSERT_CHANNEL_ID>
- Use the built-in OpenClaw discord skill to post these messages.

## 2. Fanqie Scraper Skill (`fanqie_scraper.py`)
- Used to research metrics and novels to learn what currently ranks highest.
- Fetch top rankings: `python skills/fanqie_scraper/fanqie_scraper.py top-rankings`
- Read your novel's comments: `python skills/fanqie_scraper/fanqie_scraper.py read-comments --id YOUR_NOVEL_ID`
- Read full novel content: `python skills/fanqie_scraper/fanqie_scraper.py read-novel --id NOVEL_ID`

## 3. Fanqie Publisher Skill (`fanqie_publisher.py`)
- You must write your drafted chapter to a local file before publishing.
- Publish a chapter: `python skills/fanqie_publisher/fanqie_publisher.py publish --id YOUR_NOVEL_ID --title "Chapter Title" --content-file "path/to/draft.txt"`
- Reply to a comment: `python skills/fanqie_publisher/fanqie_publisher.py reply --id YOUR_NOVEL_ID --comment-id ID --text "Response text"`

## 4. Web Browser Skill (`agent-browser`)
- Use the built-in browser skill ONLY if you need to browse websites manually outside the scope of your custom Python scraper capabilities.
