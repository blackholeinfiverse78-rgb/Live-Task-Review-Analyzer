from fastapi import APIRouter, HTTPException, BackgroundTasks, Response, Query
from pydantic import BaseModel
from app.services.tts_integration import generate_audio_stream, speak_on_server, TTS_AVAILABLE

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    mode: str = "stream"  # 'stream' (return file) or 'server_play' (play on host)

@router.post("/speak")
async def speak_text(request: TTSRequest, background_tasks: BackgroundTasks):
    """
    Generates speech from text using the integrated VaaniTTS engine.
    
    - **text**: The text to speak.
    - **language**: Language code (default: 'en').
    - **mode**: 
        - 'stream': Returns audio file (wav).
        - 'server_play': Plays audio on the server speakers (local agent mode).
    """
    if not TTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="TTS Service is not available (Module not found or dependencies missing)")

    if request.mode == "server_play":
        # Play on server in background to avoid blocking
        background_tasks.add_task(speak_on_server, request.text)
        return {"status": "queued", "message": f"Speaking: {request.text[:20]}..."}
    
    try:
        # Stream audio back to client
        audio_data = generate_audio_stream(request.text, request.language)
        return Response(content=audio_data, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_tts_status():
    """Check if TTS service is operational."""
    return {
        "available": TTS_AVAILABLE,
        "service": "VaaniTTS_Standalone"
    }
