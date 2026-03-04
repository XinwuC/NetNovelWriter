from litellm import completion
import logging
from tools.fanqie_scraper import FanqieScraper
from tools.fanqie_publisher import FanqiePublisher

logger = logging.getLogger(__name__)

class WriterAgent:
    def __init__(self, config, theme, novel_id=None):
        self.config = config
        self.theme = theme
        self.novel_id = novel_id
        self.primary_model = self.config.get("llm", {}).get("primary_model", "ollama/qwen2")
        self.fallback_model = self.config.get("llm", {}).get("fallback_model", "groq/llama3-70b-8192")
        self.scraper = FanqieScraper(self.config)
        self.publisher = FanqiePublisher(self.config)

    def read_top_novels_deeply(self):
        logger.info("Reading top novels deeply to learn character and plot structure...")
        top_rankings = self.scraper.scrape_top_rankings()
        for novel in top_rankings:
            full_text = self.scraper.read_entire_novel(novel["novel_id"])
            # In a real implementation, we would summarize this using LLM and store in a local knowledge base

    def generate_text(self, prompt):
        try:
            response = completion(model=self.primary_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"Primary model {self.primary_model} failed: {e}. Falling back to {self.fallback_model}")
            try:
                response = completion(model=self.fallback_model, messages=[{"role": "user", "content": prompt}])
                return response.choices[0].message.content
            except Exception as fallback_e:
                logger.error(f"Fallback model also failed: {fallback_e}")
                return "Error generating content."

    def draft_chapter(self):
        prompt = f"Please draft a compelling chapter for a Chinese novel with the theme: {self.theme}. Make sure to include proper character growth and plot development."
        return self.generate_text(prompt)

    def publish_chapter(self, chapter_title, content):
        if not self.novel_id:
            logger.error("No novel_id assigned to this writer agent. Cannot publish.")
            return False
        return self.publisher.publish_chapter(self.novel_id, chapter_title, content)

    def read_and_incorporate_feedback(self):
        if not self.novel_id:
            return
        comments = self.scraper.read_comments(self.novel_id)
        if comments:
            prompt = f"Here is recent reader feedback: {comments}. How should I adjust the plot for the next chapter?"
            strategy = self.generate_text(prompt)
            logger.info(f"Adjusted strategy based on feedback: {strategy}")
            # The strategy can be saved or appended to self.theme or a context window.
