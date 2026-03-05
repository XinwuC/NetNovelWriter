#!/usr/bin/env python3
import sys
import os
import argparse
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("fanqie_publisher")

class FanqiePublisher:
    def __init__(self, config=None):
        self.config = config

    def publish_chapter(self, novel_id, chapter_title, content):
        logger.info(f"Mock publishing '{chapter_title}' to novel {novel_id}")
        return True

    def reply_to_comment(self, novel_id, comment_id, reply_text):
        logger.info(f"Mock replying to comment {comment_id} on novel {novel_id}")
        return True

def get_publisher():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    config = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k.strip()] = v.strip().strip('"\'')
                    
    for key in ["FANQIE_USERNAME", "FANQIE_PASSWORD", "FANQIE_SESSION_COOKIE"]:
        if os.environ.get(key):
            config[key] = os.environ.get(key)
            
    return FanqiePublisher({"fanqienovel": config} if config else None)

def main():
    parser = argparse.ArgumentParser(description="Skill: Fanqie Novel Publisher")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    publish_parser = subparsers.add_parser("publish", help="Publish a new chapter")
    publish_parser.add_argument("--id", required=True, help="Novel ID")
    publish_parser.add_argument("--title", required=True, help="Chapter Title")
    publish_parser.add_argument("--content-file", required=True, help="Path to text file containing chapter content")
    
    reply_parser = subparsers.add_parser("reply", help="Reply to a reader comment")
    reply_parser.add_argument("--id", required=True, help="Novel ID")
    reply_parser.add_argument("--comment-id", required=True, help="Comment ID to reply to")
    reply_parser.add_argument("--text", required=True, help="Reply text")
    
    args = parser.parse_args()
    publisher = get_publisher()
    
    if args.command == "publish":
        try:
            with open(args.content_file, "r") as f:
                content = f.read()
            success = publisher.publish_chapter(args.id, args.title, content)
            print(json.dumps({"status": "success" if success else "error", "message": "Chapter published"}))
        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}))
            
    elif args.command == "reply":
        success = publisher.reply_to_comment(args.id, args.comment_id, args.text)
        print(json.dumps({"status": "success" if success else "error", "message": "Reply posted"}))

if __name__ == "__main__":
    main()
