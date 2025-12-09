import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Class to generate FAQs out of MistralAI for a single product
class QuestionGenerationAgent:
    def run(self, product):
        product = product.__dict__
        api_key = os.environ.get('MISTRAL_API_KEY')
        client = Mistral(api_key=api_key)
        try:
            prompt = f"""
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
                {product}

                Output Structure - 
                FAQs:
                    Id - "integer"
                    Question - "string"
                    Answer - "string"
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