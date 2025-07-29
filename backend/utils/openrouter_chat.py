import requests
import os

def get_ai_reply(user_input: str, system_prompt: str = "") -> str:
    # Load API key from environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ API key is missing.")
        return "❌ No API key found in environment."

    # Headers required by OpenRouter
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # Use your deployed domain in production
        "Content-Type": "application/json"
    }

    # Construct the message payload
    data = {
        "model": "mistralai/mistral-7b-instruct",
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
            timeout=15  # ⏰ Add timeout so it doesn’t hang forever
        )

        # ✅ Success: extract and return AI message
        if response.status_code == 200:
            json_data = response.json()
            message = json_data.get("choices", [{}])[0].get("message", {}).get("content")
            return message if message else "🤖 No reply received from the AI."

        # ❌ API returned error
        print("🔴 OpenRouter API Error:")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return f"❌ OpenRouter error {response.status_code}. Try again later."

    except requests.exceptions.RequestException as e:
        print("❌ Network or request error:", str(e))
        return "❌ Couldn't reach AI service. Check your internet or try again later."
