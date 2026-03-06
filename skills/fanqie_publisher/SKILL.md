---
name: fanqie_publisher
description: A command-line skill for publishing chapters and replying to comments on fanqienovel.com.
---

# Fanqie Publisher Skill

Provides write access to fanqienovel.com using configured credentials.

## Commands

### Publish
Uploads a drafted chapter from a local file to Fanqie.
`python fanqie_publisher.py publish --id NOVEL_ID --title "TITLE" --content-file "PATH/TO/FILE"`

### Reply
Responds to a specific reader's comment.
`python fanqie_publisher.py reply --id NOVEL_ID --comment-id COMMENT_ID --text "TEXT"`
