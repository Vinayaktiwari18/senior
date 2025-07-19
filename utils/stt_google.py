import subprocess
import speech_recognition as sr

def transcribe_audio(file_path: str) -> str:
    # Convert .ogg to .wav using ffmpeg
    subprocess.run([
        "ffmpeg", "-y", "-i", file_path, "voice.wav"
    ])

    # Transcribe using Google STT
    recognizer = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language="en-IN")
