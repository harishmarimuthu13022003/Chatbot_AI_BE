import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Load API keys from env
api_keys = [
    os.getenv("GROK_API_KEY_1"),
    os.getenv("GROK_API_KEY_2"),
    os.getenv("GROK_API_KEY_3"),
    os.getenv("GROK_API_KEY_4"),
    os.getenv("GROK_API_KEY_5"),
]

# Filter out None or empty string keys
VALID_API_KEYS = [key for key in api_keys if key]

async def generate_chat_response(messages: list) -> str:
    """
    Calls the Grok API, looping through valid API keys to handle rate limits or errors.
    """
    if not VALID_API_KEYS:
        return "Error: No valid API keys configured."

    system_message = {
        "role": "system", 
        "content": "You are a professional, highly intelligent, and helpful AI assistant. Provide detailed, accurate, and insightful responses. Maintain a polite and engaging tone."
    }
    formatted_messages = [system_message] + messages

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    for i, api_key in enumerate(VALID_API_KEYS):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile", # High quality model
            "messages": formatted_messages,
            "stream": False
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                elif response.status_code == 429:
                    print(f"Rate limit hit for API Key index {i}. Trying next key...")
                    continue
                else:
                    print(f"Error with API Key index {i}: {response.status_code} - {response.text}")
                    # If it's a 4xx (other than 429) or 5xx, we might want to try next key or just return
                    continue
        except Exception as e:
            print(f"Exception using API Key index {i}: {e}. Trying next key...")
            continue
            
    return "I'm sorry, I couldn't generate a response at this time. All API services appear to be down or rate-limited."
