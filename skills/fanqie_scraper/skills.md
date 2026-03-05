---
name: fanqie_scraper
description: A command-line skill to fetch data from fanqienovel.com, including top rankings, novel content, and audience comments.
---

# Fanqie Scraper Skill

Provides read-only access to fanqienovel.com.

## Commands

### Top Rankings
Retrieves the most popular novels.
`python fanqie_scraper.py top-rankings`

### Read Novel
Gets the full content of a specified novel for learning.
`python fanqie_scraper.py read-novel --id NOVEL_ID`

### Read Comments
Retrieves audience feedback for a specific novel.
`python fanqie_scraper.py read-comments --id NOVEL_ID`
