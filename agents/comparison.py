import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Comparison Agent class
class ComparisonAgent:
    def run(self, product1, product2):
        # Converting Objects into dictionaries
        product1 = product1.__dict__
        product2 = product2.__dict__

        # Mistral AI client
        api_key = os.environ.get('MISTRAL_API_KEY')
        client = Mistral(api_key=api_key)

        try:
            prompt = f"""
                You are an expert product review agent with overall 15+ years of experience. You have a sharp eye for details and is able to 
                extract meaningful and smart insights from a product. Your task is to compare the following 2 products and then give the json output
                as per the desired output structure.

                Products to Compare - 
                Product A - {product1}
                Product B - {product2}

                Output Structure - 
                Product A - Summarise the Product A 
                Product B - Summarise the Product B
                Comparison - 3 points of differentation between both the products along with conclusion of that point
                Recommendation - Recommend the right product for a user

                Guardrails:
                1. Give factual and concise answers only.
                2. Use the names of products at the place of "Product A" and "Product B"
                3. Do not assume anything.
                4. The summary and recommendation must be strictly less than 200 words.
                5. Give a proper JSON output and do not include "```JSON" or "```" in the output.
            """

            response = client.chat.complete(
            model='mistral-large-latest',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            )

            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception as e:
            print("Caught an Exception: ", e)