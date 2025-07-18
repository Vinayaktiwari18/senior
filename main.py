from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from utils.stt_google import transcribe_audio
from utils.language import detect_language
from utils.mood_logic import get_prompt
from utils.openrouter_chat import get_ai_reply
from utils.edge_tts import generate_voice
import os
import tempfile
import uuid
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Add this line to serve files from the 'media' folder
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def root():
    return {"msg": "YAAR backend is live 💖"}

@app.post("/chat")
async def chat_voice(file: UploadFile, mood: str = Form("sweet")):
    try:
        # Step 1: Save uploaded voice file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Step 2: Convert to WAV (for STT)
        wav_path = f"{uuid.uuid4().hex}_voice.wav"
        os.system(f"ffmpeg -y -i {tmp_path} {wav_path}")

        # Step 3: Transcribe
        user_text = transcribe_audio(wav_path)
        print("You said:", user_text)

        # Step 4: Detect language
        lang = detect_language(user_text)
        print("Language:", lang)

        # Step 5: Build prompt and get reply
        system_prompt = get_prompt(mood, lang)
        reply = get_ai_reply(user_text, system_prompt)
        print("AI says:", reply)

        # Step 6: Generate voice output
        voice_filename = f"{uuid.uuid4().hex}_response.mp3"
        voice_path = os.path.join("media", voice_filename)
        await generate_voice(text=reply, output_path=voice_path)

        # Step 7: Clean reply and return audio response
        safe_reply = reply.encode("ascii", "ignore").decode("ascii")
        safe_mood = mood.encode("ascii", "ignore").decode("ascii")

    finally:
        for f in [tmp_path, wav_path]:
            try:
                os.remove(f)
            except Exception:
                pass
        return {
    "text_reply": reply,
    "audio_url": f"/media/{voice_filename}",
    "mood": mood,
    "language": lang
}



@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    # Simpler endpoint for Android test (returns text only)
    return {"text": "You said something. Here's a reply!"}

# Optional: if you want to run with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
