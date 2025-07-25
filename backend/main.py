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
from moviepy.editor import AudioFileClip  

load_dotenv()

app = FastAPI()

# ✅ Serve audio replies
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def root():
    return {"msg": "YAAR backend is live 💖"}

# ✅ Voice message chat
@app.post("/chat")
async def chat_voice(file: UploadFile = File(...), mood: str = Form("sweet")):
    try:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Convert to WAV
        wav_path = f"{uuid.uuid4().hex}_voice.wav"
        clip = AudioFileClip(tmp_path)
        clip.write_audiofile(wav_path, codec='pcm_s16le')
        clip.close()

        # Transcribe
        user_text = transcribe_audio(wav_path)
        print("You said:", user_text)

        # Language detection
        lang = detect_language(user_text)
        print("Language:", lang)

        # AI reply
        system_prompt = get_prompt(mood, lang)
        reply = get_ai_reply(user_text, system_prompt)
        print("AI says:", reply)

        # Voice generation
        voice_filename = f"{uuid.uuid4().hex}_response.mp3"
        voice_path = os.path.join("media", voice_filename)
        await generate_voice(text=reply, output_path=voice_path)

        return {
            "text_reply": reply,
            "audio_url": f"/media/{voice_filename}",
            "mood": mood,
            "language": lang
        }

    finally:
        for f in [tmp_path, wav_path]:
            try:
                os.remove(f)
            except Exception:
                pass

# ✅ Text message chat
@app.post("/chat-text")
async def chat_text(
    text: str = Form(...),
    mood: str = Form("sweet")
):
    try:
        print("You typed:", text)

        # Language detection
        lang = detect_language(text)
        print("Language:", lang)

        # AI reply
        system_prompt = get_prompt(mood, lang)
        reply = get_ai_reply(text, system_prompt)
        print("AI says:", reply)

        # Voice generation
        voice_filename = f"{uuid.uuid4().hex}_response.mp3"
        voice_path = os.path.join("media", voice_filename)
        await generate_voice(text=reply, output_path=voice_path)

        return {
            "text_reply": reply,
            "audio_url": f"/media/{voice_filename}",
            "mood": mood,
            "language": lang
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ For direct run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)