import logging

logger = logging.getLogger()

class Product:
    """Template class for product's json"""
    def __init__(self, name="", concentration="", skin_type=None, ingredients=None, 
                 use="", benefits=None, price="", side_effects=""):
        try:
            self.name = name
            self.concentration = concentration
            self.skin_type = skin_type if skin_type is not None else []
            self.ingredients = ingredients if ingredients is not None else []
            self.use = use
            self.benefits = benefits if benefits is not None else []
            self.price = price
            self.side_effects = side_effects
        except Exception as e:
            logger.error(f"Error initializing Product: {e}")

# Parser Node Function
class ParserAgent:
    """Parser Agent: Converts raw JSON product data to structured Product objects"""
    
    def run_product_a(self, state):
        """LangGraph Node: Parse Product A from template"""
        logger.info("Parser Node for Product A loaded successfully")
        
        try:
            template = state.get('template', [])
            if len(template) < 1:
                raise ValueError("Template must contain at least 1 product for Product A")
            
            product_dict = template[0]
            
            product = Product(
                name=product_dict.get("product_name", ""),
                concentration=product_dict.get("concentration", ""),
                skin_type=product_dict.get("skin_type", []),
                ingredients=product_dict.get("key_ingredients", []),
                use=product_dict.get("how_to_use", ""),
                benefits=product_dict.get("benefits", []),
                price=product_dict.get("price", ""),
                side_effects=product_dict.get("side_effects", "")
            )
            
            state['product_a'] = product.__dict__
            logger.info(f"Product A parsed: {product.name}")
            return state
        
        except Exception as e:
            error_msg = f"Error parsing Product A: {e}"
            logger.error(error_msg)
            state['error'] = error_msg
            return state

    def run_product_b(self, state):
        """LangGraph Node: Parse Product B from template"""
        logger.info("Parser Node for Product B loaded successfully")
        
        try:
            template = state.get('template', [])
            if len(template) < 2:
                raise ValueError("Template must contain at least 2 products for Product B")
            
            product_dict = template[1]
            
            product = Product(
                name=product_dict.get("product_name", ""),
                concentration=product_dict.get("concentration", ""),
                skin_type=product_dict.get("skin_type", []),
                ingredients=product_dict.get("key_ingredients", []),
                use=product_dict.get("how_to_use", ""),
                benefits=product_dict.get("benefits", []),
                price=product_dict.get("price", ""),
                side_effects=product_dict.get("side_effects", "")
            )
            
            state['product_b'] = product.__dict__
            logger.info(f"Product B parsed: {product.name}")
            return state
        
        except Exception as e:
            error_msg = f"Error parsing Product B: {e}"
            logger.error(error_msg)
            state['error'] = error_msg
            return state
