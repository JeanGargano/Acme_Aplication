import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
print(f"API_KEY: {api_key}")

if not api_key:
    raise Exception("API_KEY no encontrada")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "Dame un ejemplo de plan de acción"
response = model.generate_content(prompt)
print(response.text)
