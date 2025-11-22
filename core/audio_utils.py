import os
from django.conf import settings
import openai

openai.api_key = os.getenv('OPENAI_API_KEY', settings.OPENAI_API_KEY)

def transcribe_file(file_path: str) -> str:
    # Requires OpenAI Audio API (whisper) or a similar endpoint
    with open(file_path, 'rb') as f:
        resp = openai.Audio.transcriptions.create(model='whisper-1', file=f)
        # Depending on client version, response parsing may differ
        try:
            return resp['text']
        except Exception:
            # if resp is object with attr
            return getattr(resp, 'text', '')