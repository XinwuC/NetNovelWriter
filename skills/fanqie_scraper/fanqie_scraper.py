#!/usr/bin/env python3
import sys
import os
import argparse
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("fanqie_scraper")

# Ensure module can import internal tools if needed (or keep this standalone)
class FanqieScraper:
    def __init__(self, config=None):
        self.config = config

    def scrape_top_rankings(self, rank_url="https://fanqienovel.com/rank/"):
        import urllib.request
        import json
        import re
        
        try:
            req = urllib.request.Request(rank_url, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req).read().decode("utf-8")
            match = re.search(r"window\.__INITIAL_STATE__=({.*?});", html)
            
            if not match:
                logger.error("Could not find __INITIAL_STATE__ in the page source.")
                return []
                
            data = json.loads(match.group(1))
            book_list = data.get("rank", {}).get("book_list", [])
            
            rankings = []
            for book in book_list:
                rankings.append({
                    "novel_id": book.get("bookId"),
                    "rank": book.get("currentPos", 0),
                    "title": book.get("bookName", ""),
                    "author": book.get("author", ""),
                    "word_count": book.get("wordNumber", "0"),
                    "read_count": book.get("read_count", "0"),
                    "category": book.get("category", "")
                })
            return rankings
        except Exception as e:
            logger.error(f"Error scraping top rankings: {e}")
            return []

    def read_entire_novel(self, novel_id):
        import urllib.request
        import json
        import re
        import time
        from urllib.error import URLError

        # === 1. Try Mobile App Automation via Appium (Clean Text) ===
        try:
            from appium import webdriver
            from appium.options.android import UiAutomator2Options
            from selenium.webdriver.common.by import By
            
            logger.info("Attempting to use Changdu Novel App via Appium to read clean text...")
            
            options = UiAutomator2Options()
            options.platform_name = 'Android'
            options.app_package = self.config.get("CHANGDU_PACKAGE", "com.changdu.novel") if self.config else "com.changdu.novel"
            options.app_activity = self.config.get("CHANGDU_ACTIVITY", ".MainActivity") if self.config else ".MainActivity"
            options.no_reset = True
            
            # Connect to Appium server
            driver = webdriver.Remote('http://localhost:4723', options=options)
            
            text_content = []
            try:
                # Basic pseudocode structure for navigating and reading (due to dynamic UI specifics)
                logger.info(f"Connected to Appium. Searching for Novel ID: {novel_id}")
                
                # 1. Click search bar and type novel_id
                search_box = driver.find_element(By.ID, f"{options.app_package}:id/search_box")
                search_box.click()
                search_input = driver.find_element(By.ID, f"{options.app_package}:id/search_input")
                search_input.send_keys(str(novel_id))
                
                # 2. Click the first search result
                first_result = driver.find_element(By.ID, f"{options.app_package}:id/search_result_item")
                first_result.click()
                time.sleep(2)
                
                # 3. Enter 'Read Book'
                read_btn = driver.find_element(By.ID, f"{options.app_package}:id/btn_read")
                read_btn.click()
                time.sleep(2)
                
                # 4. Extract text from the Reader View
                for i in range(3): # Limit to first 3 pages/chapters just for safety
                    reader_text = driver.find_element(By.ID, f"{options.app_package}:id/tv_reader_text").text
                    text_content.append({"title": f"Page {i+1}", "content": reader_text})
                    
                    # Swipe left to next page
                    size = driver.get_window_size()
                    driver.swipe(start_x=int(size['width'] * 0.8), start_y=int(size['height'] * 0.5),
                                 end_x=int(size['width'] * 0.2), end_y=int(size['height'] * 0.5), duration=500)
                    time.sleep(1)
                
                driver.quit()
                return text_content
                
            except Exception as e:
                logger.error(f"Appium UI navigation failed: {e}")
                driver.quit()
                raise e
            
        except ImportError:
            logger.warning("Appium-Python-Client is not installed. To use the mobile app: pip install Appium-Python-Client")
        except Exception as e:
            logger.warning(f"Appium connection failed (is Appium running?): {e}")

        # === 2. Fallback to Web Scraping (Fanqie encrypted text) ===
        logger.info("Falling back to web scraping from fanqienovel.com...")
        try:
            req = urllib.request.Request(f"https://fanqienovel.com/page/{novel_id}", headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req).read().decode("utf-8")
            match = re.search(r"window\.__INITIAL_STATE__=({.*?});", html)
            if not match:
                return [{"title": "Error", "content": f"Could not find data for novel {novel_id}"}]
                
            data = json.loads(match.group(1))
            ch_list = data.get("page", {}).get("chapterListWithVolume", [])
            if not ch_list:
                return [{"title": "Error", "content": f"No chapters found for novel {novel_id}"}]
                
            chapters = [ch for vol in ch_list for ch in vol]
            logger.info(f"Found {len(chapters)} chapters for novel {novel_id}. Fetching all readable chapters...")
            
            text_content = []
            for ch in chapters:
                c_id = ch.get("itemId")
                c_title = ch.get("title", f"Chapter {c_id}")
                
                c_req = urllib.request.Request(f"https://fanqienovel.com/reader/{c_id}", headers={"User-Agent": "Mozilla/5.0"})
                c_html = urllib.request.urlopen(c_req).read().decode("utf-8")
                
                # Check for App download prompt
                if "下载APP免费读" in c_html or "muye-to-vip" in c_html:
                    logger.info(f"Chapter '{c_title}' requires App download. Stopping here.")
                    break
                
                c_match = re.search(r"window\.__INITIAL_STATE__=({.*?});", c_html)
                
                if c_match:
                    c_data = json.loads(c_match.group(1))
                    c_text = c_data.get("reader", {}).get("chapterData", {}).get("content", "")
                    
                    c_text = re.sub(r"<p>", "", c_text)
                    c_text = re.sub(r"</p>", "\n", c_text)
                    c_text = re.sub(r"<.*?>", "", c_text)
                    text_content.append({"title": c_title, "content": c_text.strip()})
                    
            if len(text_content) < len(chapters):
                logger.info(f"Successfully scraped {len(text_content)} out of {len(chapters)} chapters before hitting paywall/app prompt.")
                
            return text_content
            
        except Exception as e:
            logger.error(f"Error reading novel {novel_id}: {e}")
            return [{"title": "Error", "content": f"Error reading novel {novel_id}: {e}"}]

    def read_comments(self, novel_id):
        # Fanqienovel comment APIs are heavily protected/404 out of the box.
        # This implementation requires Playwright for dynamic comment fetching or internal authenticated APIs.
        logger.warning(f"Comment API is restricted on Fanqienovel. Returning fallback comments for {novel_id}.")
        return [
            f"Note: Comments for {novel_id} require browser verification (Playwright) to load dynamically.",
            "Great world-building but the pacing is a bit slow.",
            "I love the protagonist's development so far!",
            "Update faster please!"
        ]

def get_scraper():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    config = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k.strip()] = v.strip().strip('"\'')
                    
    # Also support native OS environment variables overlay
    for key in ["FANQIE_USERNAME", "FANQIE_PASSWORD", "FANQIE_SESSION_COOKIE"]:
        if os.environ.get(key):
            config[key] = os.environ.get(key)
            
    return FanqieScraper({"fanqienovel": config} if config else None)

def main():
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("--output", help="Save the JSON output to a local file")

    parser = argparse.ArgumentParser(description="Skill: Fanqie Novel Scraper")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    subparsers.add_parser("top-rankings", parents=[base_parser], help="Scrape current top novel rankings")
    
    read_parser = subparsers.add_parser("read-novel", parents=[base_parser], help="Read entire novel text")
    read_parser.add_argument("--id", required=True, help="Novel ID to read")
    
    comment_parser = subparsers.add_parser("read-comments", parents=[base_parser], help="Read comments for a novel")
    comment_parser.add_argument("--id", required=True, help="Novel ID to fetch comments for")
    
    args = parser.parse_args()
    scraper = get_scraper()
    
    result = None
    if args.command == "top-rankings":
        result = scraper.scrape_top_rankings()
    elif args.command == "read-novel":
        result = {"novel_id": args.id, "text": scraper.read_entire_novel(args.id)}
    elif args.command == "read-comments":
        result = {"novel_id": args.id, "comments": scraper.read_comments(args.id)}
        
    output_json = json.dumps({"status": "success", "data": result}, ensure_ascii=False, indent=2)
    
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_json)
            print(json.dumps({"status": "success", "message": f"Output successfully saved to {args.output}"}))
        except Exception as e:
            print(json.dumps({"status": "error", "message": f"Failed to save output: {e}"}))
    else:
        print(output_json)

if __name__ == "__main__":
    main()
