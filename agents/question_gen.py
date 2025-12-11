import os
import json
import logging
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()

# FAQ Generation Node 
class QuestionGenerationAgent:
    """FAQ Generation Agent: Generates FAQs using LangChain + Mistral AI"""
    
    def run(self, state):
        """LangGraph Node: Generate FAQ using LangChain + Mistral AI"""
        logger.info("FAQ Generation Node loaded successfully")
        
        try:
            product = state.get('product_a', {})
            api_key = os.environ.get('MISTRAL_API_KEY')
            
            if not api_key:
                logger.warning("MISTRAL_API_KEY not set. Skipping FAQ generation.")
                state['faq_a'] = {}
                return state
            
            # Initialize LangChain ChatMistralAI
            llm = ChatMistralAI(api_key=api_key, model="mistral-large-latest", temperature=0.4)
            
            prompt_text = f"""
You are an AI FAQ Generator. You must create FAQs ONLY using the information
from the product data below. You are NOT allowed to add external facts.

STRICT RULES:
- Use ONLY the information provided.
- No outside knowledge.
- No invented benefits or ingredients.
- 15 Q&A pairs.
- Keep answers factual, grounded.
- Give a proper JSON output and do not include "```JSON" or "```" in the output.

PRODUCT DATA:
{json.dumps(product, indent=2)}

Output Structure - 
FAQs:
    Id - "integer"
    Question - "string"
    Answer - "string"
"""
            
            message = HumanMessage(content=prompt_text)
            response = llm.invoke([message])
            content = response.content
            
            faq_data = json.loads(content)
            state['faq_a'] = faq_data
            logger.info("FAQ generated successfully")
            return state
        
        except Exception as e:
            error_msg = f"Error generating FAQ: {e}"
            logger.error(error_msg)
            logger.warning("Proceeding with empty FAQ.")
            state['error'] = error_msg
            state['faq_a'] = {}
            return state