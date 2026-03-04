import yaml
import logging
from agents.master_agent import MasterAgent
from tools.discord_integration import DiscordIntegration

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    logger.info("Starting NetNovelWriters...")
    config = load_config()
    
    # Initialize Discord Integration
    discord = DiscordIntegration(config)
    discord.send_message("Master Agent Online. Initializing system...")

    # Initialize Master Agent
    master = MasterAgent(config)
    
    # Example flow
    writer = master.spawn_writer(theme="Cyberpunk Cultivation")
    
    # Note: In a real run, this would be a long-running loop
    logger.info("Running a test cycle for the spawned Writer...")
    writer.read_top_novels_deeply()
    chapter = writer.draft_chapter()
    logger.info(f"Generated Draft Sample:\n{chapter[:200]}...")
    
    discord.send_message("Writer Agent completed a test cycle.")

if __name__ == "__main__":
    main()
