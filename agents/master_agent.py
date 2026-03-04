import logging
from .writer_agent import WriterAgent

logger = logging.getLogger(__name__)

class MasterAgent:
    def __init__(self, config):
        self.config = config
        self.writer_agents = []

    def spawn_writer(self, theme):
        logger.info(f"Spawning new WriterAgent for theme: {theme}")
        writer = WriterAgent(self.config, theme)
        self.writer_agents.append(writer)
        return writer

    def check_rankings(self):
        logger.info("Checking rankings of all WriterAgents on fanqienovel...")
        # Plugin scraper logic later
        pass

    def terminate_underperforming(self):
        # Plugin termination logic
        pass
