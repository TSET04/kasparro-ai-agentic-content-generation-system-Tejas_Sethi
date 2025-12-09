import random

class PageAssemblerAgent:
    
    def run(self, product, content_block, faqs):
        try:
            # Converting product object to dictionary
            product_dict = product.__dict__
            
            # Generating random number for Id
            id = random.randint(1000000, 10000000)
            result = {'id': id}
            result.update({'product_name': product_dict.get('name', '')})

            # Error handling for content block and faqs
            if not isinstance(content_block, dict):
                print("Warning: content_block is not a dict. Using empty dict.")
                content_block = {}
            if not isinstance(faqs, dict):
                print("Warning: faqs is not a dict. Using empty dict.")
                faqs = {}

            # Appending dictionaries
            result = result | content_block
            result = result | faqs

            return result
        except Exception as e:
            print(f"PageAssemblerAgent.run failed: {e}")
            return {'id': None, 'product_name': '', **(content_block if isinstance(content_block, dict) else {}), **(faqs if isinstance(faqs, dict) else {})}