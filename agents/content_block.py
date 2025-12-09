class ContentBlockAgent:
    def run(self, product):
        try:
            return {
                "summary_block": self.create_summary(product),
                "benefits_block": self.create_benefits(product),
                "usage_block": self.create_usage(product),
                "ingredients_block": self.create_ingredients(product),
                "side_effects_block": self.create_side_effects(product),
                "price_block": self.create_price(product),
            }
        except Exception as e:
            print(f"ContentBlockAgent.run failed: {e}")
            return {}

    # Function to create summary block
    def create_summary(self, product):
        try:
            name = product.name
            conc = product.concentration
            skins = ", ".join(product.skin_type)
            main_benefit = product.benefits[0] if product.benefits else ""
            summary = f"{name} with {conc} is suitable for {skins.lower()} skin and helps with {main_benefit.lower()}."
            return summary.strip()
        except Exception as e:
            print(f"create_summary failed: {e}")
            return ""

    # Function to create benefits block
    def create_benefits(self, product):
        try:
            return [
                {
                    "benefit": b,
                    "explanation": f"This product supports {b.lower()} based on the provided product details."
                }
                for b in product.benefits
            ]
        except Exception as e:
            print(f"create_benefits failed: {e}")
            return []

    # Function to create usage block
    def create_usage(self, product):
        try:
            raw = product.use
            steps = [s.strip() for s in raw.replace("•", ".").split(".") if s.strip()]
            return [{"step_number": i+1, "instruction": step} for i, step in enumerate(steps)]
        except Exception as e:
            print(f"create_usage failed: {e}")
            return []

    # Function to create ingredients block
    def create_ingredients(self, product):
        try:
            return [{"ingredient": ing} for ing in product.ingredients]
        except Exception as e:
            print(f"create_ingredients failed: {e}")
            return []
        
    # Function to create side effects block
    def create_side_effects(self, product):
        try:
            text = product.side_effects
            return {
                "description": text,
                "severity": self._severity(text),
            }
        except Exception as e:
            print(f"create_side_effects failed: {e}")
            return {"description": "", "severity": "medium"}

    # Helper function to assign the severity of the side effects
    def _severity(self, text):
        try:
            text = text.lower()
            if "tingling" in text or "mild" in text:
                return "low"
            if "rash" in text or "burn" in text:
                return "high"
            return "medium"
        except Exception as e:
            print(f"_severity failed: {e}")
            return "medium"

    # Function to create the price block
    def create_price(self, product):
        try:
            digits = "".join(ch for ch in product.price if ch.isdigit())
            value = int(digits) if digits else None
            return {"value": value, "currency": "INR"}
        except Exception as e:
            print(f"create_price failed: {e}")
            return {"value": None, "currency": "INR"}