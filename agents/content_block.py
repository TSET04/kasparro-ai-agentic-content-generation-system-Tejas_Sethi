import logging

logger = logging.getLogger()

# Content Block Node
class ContentBlockAgent:
    """Content Block Agent: Generates structured content blocks for a product"""
    
    def run(self, state):
        """LangGraph Node: Generate content blocks for Product A"""
        logger.info("Content Block Node loaded successfully")
        
        try:
            product = state.get('product_a', {})
            
            # Function to create summary block for the product
            def create_summary() -> str:
                name = product.get('name', '')
                conc = product.get('concentration', '')
                skins = ", ".join(product.get('skin_type', []))
                benefits = product.get('benefits', [])
                main_benefit = benefits[0] if benefits else ""
                return f"{name} with {conc} is suitable for {skins.lower()} skin and helps with {main_benefit.lower()}."
            
            # Function to create benefits block for the product
            def create_benefits() -> list:
                return [
                    {
                        "benefit": b,
                        "explanation": f"This product supports {b.lower()} based on the provided product details."
                    }
                    for b in product.get('benefits', [])
                ]
            
            # Function to create usage block for the product
            def create_usage() -> list:
                raw = product.get('use', '')
                steps = [s.strip() for s in raw.replace("•", ".").split(".") if s.strip()]
                return [{"step_number": i+1, "instruction": step} for i, step in enumerate(steps)]
            
            # Function to create ingredients block for the product
            def create_ingredients() -> list:
                return [{"ingredient": ing} for ing in product.get('ingredients', [])]
            
            # Function to create side-effects block for the product
            def create_side_effects() -> dict:
                text = product.get('side_effects', '')
                severity = "low" if any(word in text.lower() for word in ["tingling", "mild"]) else \
                          "high" if any(word in text.lower() for word in ["rash", "burn"]) else "medium"
                return {"description": text, "severity": severity}
            
            # Function to create price block for the product
            def create_price() -> dict:
                price_str = product.get('price', '')
                digits = "".join(ch for ch in price_str if ch.isdigit())
                value = int(digits) if digits else None
                return {"value": value, "currency": "INR"}
            
            content_blocks = {
                "summary_block": create_summary(),
                "benefits_block": create_benefits(),
                "usage_block": create_usage(),
                "ingredients_block": create_ingredients(),
                "side_effects_block": create_side_effects(),
                "price_block": create_price(),
            }
            
            state['content_a'] = content_blocks
            logger.info("Content blocks generated successfully")
            return state
        
        except Exception as e:
            error_msg = f"Error generating content blocks: {e}"
            logger.error(error_msg)
            state['error'] = error_msg
            state['content_a'] = {}
            return state