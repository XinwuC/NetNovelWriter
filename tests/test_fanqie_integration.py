import subprocess
import json
import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_fanqie_scraper_top_rankings():
    script_path = os.path.join(BASE_DIR, "skills", "fanqie_scraper.py")
    result = subprocess.run([script_path, "top-rankings"], capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], list)

def test_fanqie_scraper_read_comments():
    script_path = os.path.join(BASE_DIR, "skills", "fanqie_scraper.py")
    result = subprocess.run([script_path, "read-comments", "--id", "123"], capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "success"
    assert data["data"]["novel_id"] == "123"

def test_fanqie_publisher():
    script_path = os.path.join(BASE_DIR, "skills", "fanqie_publisher.py")
    test_content_file = os.path.join(BASE_DIR, "tests", "dummy_content.txt")
    with open(test_content_file, "w") as f:
        f.write("Chapter content for testing.")

    result = subprocess.run([
        script_path, "publish", 
        "--id", "123", 
        "--title", "Chapter 1", 
        "--content-file", test_content_file
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "success"

    os.remove(test_content_file)
