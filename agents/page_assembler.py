import random
import logging

logger = logging.getLogger()

# Page Assembler Node
class PageAssemblerAgent:
    """Page Assembler Agent: Assembles product page from product, content, and FAQ data"""
    
    def run(self, state):
        """LangGraph Node: Assemble product page from product, content, and FAQ"""
        logger.info("Page Assemble Node loaded successfully")
        
        try:
            product = state.get('product_a', {})
            content_block = state.get('content_a', {})
            faqs = state.get('faq_a', {})
            
            # Ensure dictionaries are properly formatted
            if not isinstance(content_block, dict):
                logger.warning("content_block is not a dict. Using empty dict.")
                content_block = {}
            if not isinstance(faqs, dict):
                logger.warning("faqs is not a dict. Using empty dict.")
                faqs = {}
            
            # Assemble the final product page
            page_id = random.randint(1000000, 10000000)
            product_page = {
                'id': page_id,
                'product_name': product.get('name', '')
            }
            
            product_page.update(content_block)
            product_page.update(faqs)
            
            state['product_page'] = product_page
            logger.info("Product page assembled successfully")
            return state
        
        except Exception as e:
            error_msg = f"Error assembling product page: {e}"
            logger.error(error_msg)
            state['error'] = error_msg
            state['product_page'] = {}
            return state