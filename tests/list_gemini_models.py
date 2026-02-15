import os
from dotenv import load_dotenv

load_dotenv()

print("Listing available Gemini models...")

try:
    from google import genai
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # List available models
    models = client.models.list()
    
    print("\nAvailable models:")
    for model in models:
        if 'gemini' in model.name.lower():
            print(f"  - {model.name}")
    
except Exception as e:
    print(f"Error: {e}")
