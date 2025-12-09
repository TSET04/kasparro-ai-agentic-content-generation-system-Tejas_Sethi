# Template class for product's json 
class Product:
    def __init__(self, name="", concentration="", skin_type=None, ingredients=None, use="", benefits=None, price="", side_effects=""):
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
            print(f"Error initializing Product: {e}")

class ParserAgent:
    def run(self, template):
        try:
            name = template.get("product_name", "")
            concentration = template.get("concentration", "")
            skin_type = template.get("skin_type", [])
            ingredients = template.get("key_ingredients", [])
            use = template.get("how_to_use", "")
            benefits = template.get("benefits", [])
            price = template.get("price", "")
            side_effects = template.get("side_effects", "")

            product = Product(
                name=name,
                concentration=concentration,
                skin_type=skin_type,
                ingredients=ingredients,
                use=use,
                benefits=benefits,
                price=price,
                side_effects=side_effects
            )

            return product
        except Exception as e:
            print(f"Error in ParserAgent.run Method: {e}")
            return None
