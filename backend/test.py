import requests

url = "http://127.0.0.1:8000/chat"
with open("hello.ogg.m4a", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},
        data={"mood": "sweet"}
    )

with open("bot_reply.mp3", "wb") as out:
    out.write(response.content)

print("💬 AI Reply:", response.headers.get("reply-text"))
print("🎭 Mood Used:", response.headers.get("mood-used"))
