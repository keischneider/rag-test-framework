from openai import OpenAI
import os

def query_llm(prompt):
    response = OpenAI(api_key=os.getenv("OPENAI_API_KEY")).responses.create(
        model="gpt-5-mini",
        input=prompt
    )
    return response.output_text