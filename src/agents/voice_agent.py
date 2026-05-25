"""Voice Agent — converts scripts to MP3 using ElevenLabs TTS API"""

import httpx
import subprocess
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VoiceAgent:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID
        self.base_url = "https://api.elevenlabs.io/v1"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_voiceover(
        self,
        script: str,
        output_path: Path,
        stability: float = 0.5,
        similarity_boost: float = 0.85,
        style: float = 0.4
    ) -> Path:
        """
        Convert script to MP3 voiceover.

        Voice settings guide:
        - stability: 0.3 = expressive/dynamic, 0.8 = consistent/steady
          → Use 0.4 for energetic content, 0.6 for educational content
        - similarity_boost: how close to reference voice (0.75-0.95)
        - style: how dramatic the delivery (0.2 = neutral, 0.8 = theatrical)
          → Use 0.3 for calm educational, 0.5 for motivational reels
        """
        logger.info(f"Generating voiceover: {output_path.name}")

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        payload = {
            "text": script,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": True
            }
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/text-to-speech/{self.voice_id}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)

        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"Voiceover saved: {output_path} ({file_size_kb:.1f} KB)")
        return output_path

    def get_audio_duration(self, mp3_path: Path) -> float:
        """Get duration of MP3 in seconds using ffprobe"""
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
            capture_output=True, text=True
        )
        return float(result.stdout.strip())

    def get_remaining_characters(self) -> dict:
        """Check ElevenLabs quota remaining"""
        headers = {"xi-api-key": self.api_key}
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/user/subscription", headers=headers)
        data = response.json()
        return {
            "used": data.get("character_count", 0),
            "limit": data.get("character_limit", 0),
            "remaining": data.get("character_limit", 0) - data.get("character_count", 0)
        }
