import os
import json
import logging
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()

# Comparison Agent - LangGraph Node Function
class ComparisonAgent:
    """Comparison Agent: Compares two products using LangChain + Mistral AI"""
    
    def run(self, state):
        """LangGraph Node: Compare Product A and B using LangChain + Mistral AI"""
        logger.info("Comparison Node Loaded successfully")
        
        # LLM call to compare both the products
        try:
            product_a = state.get('product_a', {})
            product_b = state.get('product_b', {})
            api_key = os.environ.get('MISTRAL_API_KEY')
            
            if not api_key:
                logger.warning("MISTRAL_API_KEY not set. Skipping comparison.")
                state['comparison'] = {}
                return state
            
            # Initialize LangChain ChatMistralAI
            llm = ChatMistralAI(api_key=api_key, model="mistral-large-latest", temperature=0.4)
            
            prompt_text = f"""
You are an expert product review agent with overall 15+ years of experience. You have a sharp eye for details and is able to 
extract meaningful and smart insights from a product. Your task is to compare the following 2 products and then give the json output
as per the desired output structure.

Products to Compare - 
Product A - {json.dumps(product_a, indent=2)}
Product B - {json.dumps(product_b, indent=2)}

Output Structure - 
{product_a} - Summarise the Product A 
{product_b} - Summarise the Product B
Comparison - 3 points of differentation between both the products along with conclusion of that point
Recommendation - Recommend the right product for a user

Guardrails:
1. Give factual and concise answers only.
2. Use the names of products at the place of "Product A" and "Product B"
3. Do not assume anything.
4. The summary and recommendation must be strictly less than 200 words.
5. Give a proper JSON output and do not include "```JSON" or "```" in the output.
"""
            
            message = HumanMessage(content=prompt_text)
            response = llm.invoke([message])
            content = response.content
            
            comparison_data = json.loads(content)
            state['comparison'] = comparison_data
            logger.info("Comparison generated successfully")
            return state
        
        except Exception as e:
            error_msg = f"Error comparing products: {e}"
            logger.error(error_msg)
            state['error'] = error_msg
            state['comparison'] = {}
            return state