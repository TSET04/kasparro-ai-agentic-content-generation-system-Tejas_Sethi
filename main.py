import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from agents.parser import ParserAgent
from agents.content_block import ContentBlockAgent
from agents.question_gen import QuestionGenerationAgent
from agents.page_assembler import PageAssemblerAgent
from agents.comparison import ComparisonAgent

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Safe JSON save
def save_json(data, path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved JSON successfully: {path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {path}: {e}")

# Safe agent run for parallel runs
def safe_run(agent, data, name="",):
    try:
        if isinstance(data, (tuple, list)):
            result = agent.run(*data)  # unpack the tuple/list
        else:
            result = agent.run(data)
        logger.info(f"{name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"{name} failed: {e}")
        return None

# Main Pipeline
def main():
    # Load template
    try:
        with open('template.json', 'r', encoding='utf-8') as f:
            template = json.load(f)
        if len(template) < 2:
            logger.error("Template JSON must contain at least 2 products.")
            return
        a, b = template[0], template[1]
        logger.info("Template loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load template.json: {e}")
        return

    # Initialize agents
    parser_a = ParserAgent()
    parser_b = ParserAgent()
    faq_agent = QuestionGenerationAgent()
    content_agent = ContentBlockAgent()
    page_agent = PageAssemblerAgent()
    compare_agent = ComparisonAgent()


    # Step 1: Parse Products in parallel
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_parser_a = executor.submit(safe_run, parser_a, a, "ParserAgent A")
            future_parser_b = executor.submit(safe_run, parser_b, b, "ParserAgent B")
            product_a = future_parser_a.result()
            product_b = future_parser_b.result()
    except Exception as e:
        logger.error(f"Error running ParserAgents: {e}")
        return

    if product_a is None or product_b is None:
        logger.error("Parsing failed. Cannot continue pipeline.")
        return


    # Step 2: Generate FAQs and Content Blocks in parallel
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_faq = executor.submit(safe_run, faq_agent, product_a, "FAQ Agent A")
            future_content = executor.submit(safe_run, content_agent, product_a, "ContentBlockAgent A")
            faq_a = future_faq.result()
            content_a = future_content.result()
    except Exception as e:
        logger.error(f"Error running FAQ/ContentBlock agents: {e}")
        return

    if faq_a is None:
        logger.warning("FAQ generation failed. Proceeding with empty FAQ.")
        faq_a = {}
    else:
        save_json(faq_a, os.path.join('output', 'faq.json'))

    if content_a is None:
        logger.warning("ContentBlock generation failed. Proceeding with empty content.")
        content_a = {}


    # Step 3: Product Page Generation 
    try:
        page_a = safe_run(page_agent, (product_a, content_a, faq_a), "PageAssemblerAgent A")
        if page_a:
            save_json(page_a, os.path.join('output', 'product_page.json'))
    except Exception as e:
        logger.error(f"Error creating product page: {e}")


    # Step 4: Products Comparison
    try:
        comparison = safe_run(compare_agent, (product_a, product_b), "ComparisonAgent A&B")
        if comparison:
            save_json(comparison, os.path.join('output', 'comparison_page.json'))
    except Exception as e:
        logger.error(f"Error creating comparison page: {e}")

# Entry Point
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Pipeline failed unexpectedly: {e}")
