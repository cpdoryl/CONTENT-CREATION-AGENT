"""Packager Agent — organises outputs, uploads to Google Drive, and sends notifications"""

import httpx
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class PackagerAgent:
    def __init__(self):
        self.drive_service = self._get_drive_service()
        self.week_label = datetime.now().strftime("%Y-W%V")

    def _get_drive_service(self):
        """Authenticate with Google Drive"""
        creds = None
        token_path = Path("credentials/token.json")

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, "w") as f:
                f.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def create_week_folder(self, parent_folder_id: str, subfolder: str) -> str:
        """Create week/subfolder in Drive, return folder ID"""
        metadata = {
            "name": subfolder,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id]
        }
        folder = self.drive_service.files().create(
            body=metadata, fields="id"
        ).execute()
        logger.info(f"Created Drive folder: {subfolder}")
        return folder["id"]

    def upload_file(self, file_path: Path, folder_id: str) -> str:
        """Upload file to Google Drive folder, return file URL"""
        mime_types = {
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".txt": "text/plain"
        }
        mime_type = mime_types.get(file_path.suffix.lower(), "application/octet-stream")

        metadata = {"name": file_path.name, "parents": [folder_id]}
        media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)

        file = self.drive_service.files().create(
            body=metadata, media_body=media, fields="id,webViewLink"
        ).execute()

        logger.info(f"Uploaded: {file_path.name}")
        return file.get("webViewLink", "")

    def save_caption_file(self, topic_slug: str, caption: str, hashtags: list, output_dir: Path) -> Path:
        """Save caption and hashtags as text file"""
        caption_path = output_dir / f"{topic_slug}_caption.txt"
        hashtag_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)

        with open(caption_path, "w") as f:
            f.write(f"CAPTION:\n{caption}\n\n")
            f.write(f"HASHTAGS:\n{hashtag_str}\n")

        logger.info(f"Caption saved: {caption_path}")
        return caption_path

    def send_telegram_notification(self, summary: dict):
        """Send Telegram message when content is ready"""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram not configured — skipping notification")
            return

        lines = [
            f"✅ *Week {self.week_label} content is ready*",
            "",
            f"📱 *Reels/Shorts:* {summary.get('reels', 0)}",
            f"📊 *Carousels:* {summary.get('carousels', 0)}",
            f"🖼 *Static posts:* {summary.get('posts', 0)}",
            "",
            "📁 Check your Google Drive folder to review.",
            "",
            "_Open Drive → review → paste captions → schedule in Buffer_"
        ]

        message = "\n".join(lines)

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
            logger.info("Telegram notification sent")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
