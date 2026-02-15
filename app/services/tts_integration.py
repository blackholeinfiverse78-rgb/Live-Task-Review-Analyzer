import sys
import os
import logging

logger = logging.getLogger("task_review_system.tts")

# Locate VaaniTTS Standalone directory
# Expected structure:
# Root
# |- app
# |- VaaniTTS_Standalone
#    |- VaaniTTS_Standalone
#       |- tts_service.py

# Current file: app/services/tts_integration.py
# Root is 3 levels up from this file (app/services/tts_integration.py -> app/services -> app -> root)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAANI_DIR = os.path.join(ROOT_DIR, "VaaniTTS_Standalone", "VaaniTTS_Standalone")

if os.path.exists(VAANI_DIR):
    if VAANI_DIR not in sys.path:
        sys.path.append(VAANI_DIR)
        logger.info(f"Added VaaniTTS path: {VAANI_DIR}")
else:
    logger.warning(f"VaaniTTS directory not found at: {VAANI_DIR}. Please ensure the submodule/folder is present.")

try:
    # Attempt to import the service
    # Since we added the path, we can import directly
    from tts_service import text_to_speech_stream, speak_text_directly, initialize_tts_engine
    TTS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import VaaniTTS modules: {e}")
    TTS_AVAILABLE = False
    text_to_speech_stream = None
    speak_text_directly = None
    initialize_tts_engine = None

def generate_audio_stream(text: str, language: str = 'en') -> bytes:
    """
    Generates audio stream from text using VaaniTTS.
    Returns raw bytes of WAV (or other format) audio.
    """
    if not TTS_AVAILABLE:
        raise RuntimeError("VaaniTTS service is not available (Import Error)")
    
    try:
        # Generate audio using the standalone service
        # It handles buffering and cleanup
        audio_data = text_to_speech_stream(text, language=language)
        return audio_data
    except Exception as e:
        logger.error(f"Error generating audio stream: {e}")
        raise e

def speak_on_server(text: str):
    """
    Speaks text immediately on the server (local playback).
    Useful for local debugging or if the agent is running on the user's machine.
    """
    if not TTS_AVAILABLE:
        logger.warning("TTS not available, cannot speak")
        return
    
    try:
        # Initialize COM library for Windows if running in a thread
        if sys.platform == 'win32':
             try:
                 import pythoncom
                 pythoncom.CoInitialize()
             except ImportError:
                 pass

        speak_text_directly(text)
    except Exception as e:
        logger.error(f"Error speaking text on server: {e}")
