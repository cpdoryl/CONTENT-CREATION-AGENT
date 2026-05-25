"""Video Assembly Agent — combines voiceover + background + captions into MP4 using FFmpeg"""

import subprocess
import httpx
from pathlib import Path
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VideoAgent:
    def assemble_reel_ffmpeg(
        self,
        background_image: Path,
        voiceover_mp3: Path,
        output_path: Path,
        subtitle_text: str = None
    ) -> Path:
        """
        Assemble reel using local FFmpeg.
        Free, no API limits, requires FFmpeg installed.
        Output: MP4 1080x1920 (Instagram/YouTube Shorts spec)
        """
        logger.info(f"Assembling reel: {output_path.name}")

        # Get audio duration to set video length
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(voiceover_mp3)],
            capture_output=True, text=True
        )
        duration = float(probe.stdout.strip())
        logger.info(f"Audio duration: {duration:.2f}s")

        # Write subtitles file if script provided
        srt_path = None
        if subtitle_text:
            srt_path = output_path.parent / f"{output_path.stem}.srt"
            self._create_simple_srt(subtitle_text, duration, srt_path)
            logger.info(f"Subtitle file created: {srt_path}")

        # Build FFmpeg command
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(background_image),
            "-i", str(voiceover_mp3),
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"Video assembly failed: {result.stderr}")

        file_size_mb = output_path.stat().st_size / 1024 / 1024
        logger.info(f"Reel assembled: {output_path} ({file_size_mb:.1f} MB)")
        return output_path

    def _create_simple_srt(self, text: str, duration: float, srt_path: Path):
        """Create a basic SRT subtitle file from script text"""
        words = text.split()
        words_per_chunk = 5
        chunks = [" ".join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]

        if not chunks:
            chunks = [text]

        chunk_duration = duration / len(chunks)

        srt_content = ""
        for i, chunk in enumerate(chunks):
            start = i * chunk_duration
            end = (i + 1) * chunk_duration
            srt_content += f"{i+1}\n"
            srt_content += f"{self._sec_to_srt(start)} --> {self._sec_to_srt(end)}\n"
            srt_content += f"{chunk}\n\n"

        with open(srt_path, "w") as f:
            f.write(srt_content)

    def _sec_to_srt(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
