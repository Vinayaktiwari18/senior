import edge_tts

async def generate_voice(*, text: str, output_path: str = "response.mp3", voice: str = "hi-IN-SwaraNeural") -> str:
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        print(f"[generate_voice] Error: {e}")
        raise
