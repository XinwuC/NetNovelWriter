import sys
import os

# Ensure the tests directory is in the path so we can import the test modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import test_manage_writer
import test_fanqie_integration

def main():
    try:
        print("Running test_manage_writer.test_spawn_and_kill_writer...")
        test_manage_writer.test_spawn_and_kill_writer()
        
        print("Running test_fanqie_integration.test_fanqie_scraper_top_rankings...")
        test_fanqie_integration.test_fanqie_scraper_top_rankings()
        
        print("Running test_fanqie_integration.test_fanqie_scraper_read_comments...")
        test_fanqie_integration.test_fanqie_scraper_read_comments()
        
        print("Running test_fanqie_integration.test_fanqie_publisher...")
        test_fanqie_integration.test_fanqie_publisher()
        
        print("\n✅ All unit tests passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed with AssertionError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
