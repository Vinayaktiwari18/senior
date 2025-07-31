import requests
import os

def get_ai_reply(user_input: str, system_prompt: str = "") -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ API key is missing.")
        return "❌ No API key found in environment."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # Replace with your deployed frontend URL if needed
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ You can change this to claude-3-haiku or gpt-3.5-turbo for faster replies
        "max_tokens": 250,  # ✅ Limit reply length (adjust 50–200 as needed)
        "temperature": 0.7,  # Optional: controls creativity
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )

        if response.status_code == 200:
            json_data = response.json()
            message = json_data.get("choices", [{}])[0].get("message", {}).get("content")
            return message.strip() if message else "🤖 AI replied with nothing."

        print("🔴 OpenRouter API Error:", response.status_code, response.text)
        return f"❌ AI Error: {response.status_code}"

    except requests.exceptions.RequestException as e:
        print("❌ Request Error:", str(e))
        return "❌ Couldn’t reach AI service. Try again later."
