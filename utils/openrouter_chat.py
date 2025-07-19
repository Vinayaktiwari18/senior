import requests
import os

def get_ai_reply(user_input: str, system_prompt: str = "") -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ API key is missing.")
        return "❌ No API key found in environment."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # Replace with your domain if needed
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("🔴 OpenRouter error:", response.status_code, response.text)
            return "Sorry, I'm having trouble replying right now."
    except Exception as e:
        print("❌ Exception while calling OpenRouter:", str(e))
        return "Sorry, I'm having trouble replying right now."
