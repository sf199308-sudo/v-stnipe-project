import os
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from groq import Groq

app = FastAPI()

# السيرفر بيقرا المفتاح السري تلقائياً من إعدادات ريندر
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.get("/")
def read_root():
    return {"status": "سيرفر V-Stnipe شغال على ريندر وزي الفل ومستني الفويسات يا أسطى!"}

@app.post("/api/voice-to-voice")
async def voice_to_voice(voice_input: UploadFile = File(...)):
    audio_bytes = await voice_input.read()
    
    # 1. جروك بيسمع الفويس ويحوله لنص
    transcription = client.audio.transcriptions.create(
        file=("recording.webm", audio_bytes),
        model="whisper-large-v3",
        language="ar"
    )
    user_text = transcription.text

    # 2. جروك بيفكر ويرد بالعامية المصرية الروشة
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "أنت مساعد صوتي مصري روش، بتعمل محاكاة كاملة للهجة المستخدم. لو قالك يا أسطى رد عليه بيا أسطى وخليك خفيف الدم جداً."},
            {"role": "user", "content": user_text}
        ],
        model="llama3-8b-8192",
    )
    ai_reply_text = chat_completion.choices.message.content
    ai_voice_bytes = b"raw_audio_bytes_here"

    return StreamingResponse(io.BytesIO(ai_voice_bytes), media_type="audio/webm")
