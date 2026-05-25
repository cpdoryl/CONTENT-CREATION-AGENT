"""Main orchestrator — runs all agents in sequence"""

from pathlib import Path
from datetime import datetime
from src.agents.research_agent import ResearchAgent
from src.agents.script_agent import ScriptAgent
from src.agents.voice_agent import VoiceAgent
from src.agents.visual_agent import VisualAgent
from src.agents.video_agent import VideoAgent
from src.agents.carousel_agent import CarouselAgent
from src.agents.packager_agent import PackagerAgent
from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.file_utils import slugify

logger = get_logger("orchestrator")


def run_weekly_production():
    logger.info("=" * 60)
    logger.info("CONTENT AGENT — WEEKLY PRODUCTION RUN STARTED")
    logger.info("=" * 60)

    week = datetime.now().strftime("%Y-W%V")
    output_base = Path(settings.OUTPUT_DIR) / week

    # Initialize all agents
    research = ResearchAgent()
    script = ScriptAgent()
    voice = VoiceAgent()
    visual = VisualAgent()
    video = VideoAgent()
    carousel = CarouselAgent()

    # PackagerAgent is optional — skip if Google credentials missing
    try:
        packager = PackagerAgent()
    except FileNotFoundError:
        logger.warning("Google credentials not found — skipping Drive upload & Telegram notifications")
        packager = None

    summary = {"reels": 0, "carousels": 0, "posts": 0}

    # Step 1: Research trending topics
    logger.info("\n[1/7] Researching trending topics...")
    try:
        topics = research.research_trends()
        topics = topics[:settings.CONTENT_PER_WEEK]
        logger.info(f"      Found {len(topics)} topics to produce")
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return

    # Steps 2-6: Produce content for each topic
    for i, topic in enumerate(topics):
        logger.info(f"\n[Topic {i+1}/{len(topics)}] {topic.topic}")
        slug = slugify(topic.topic)
        topic_dir = output_base / slug

        try:
            # Step 2: Write all scripts
            logger.info("  [2/7] Writing scripts...")
            package = script.create_content_package(topic)

            # Step 3: Generate voiceover
            logger.info("  [3/7] Generating voiceover...")
            mp3_path = topic_dir / "reels" / f"{slug}-voice.mp3"
            voice.generate_voiceover(
                package.reel_script.full_script,
                mp3_path,
                stability=0.45,
                style=0.45
            )

            # Step 4: Generate background image
            logger.info("  [4/7] Generating background image...")
            bg_path = topic_dir / "reels" / f"{slug}-bg.jpg"
            visual.generate_reel_background(package, bg_path)

            # Step 5: Assemble reel video
            logger.info("  [5/7] Assembling reel video...")
            reel_path = topic_dir / "reels" / f"{slug}-reel.mp4"
            video.assemble_reel_ffmpeg(
                background_image=bg_path,
                voiceover_mp3=mp3_path,
                output_path=reel_path,
                subtitle_text=package.reel_script.full_script
            )
            summary["reels"] += 1

            # Step 6: Build carousel
            logger.info("  [6/7] Building carousel slides...")
            carousel_dir = topic_dir / "carousel"
            carousel.render_carousel(package, carousel_dir)
            summary["carousels"] += 1

            # Save static post image
            logger.info("  Generating static post image...")
            post_path = topic_dir / "post" / f"{slug}-post.jpg"
            visual.generate_post_image(package, post_path)
            summary["posts"] += 1

            # Save caption + hashtags
            logger.info("  Saving caption and hashtags...")
            if packager:
                packager.save_caption_file(
                    slug,
                    package.caption,
                    package.hashtags,
                    topic_dir
                )

            logger.info(f"  ✅ Topic complete: {topic.topic}")

        except Exception as e:
            logger.error(f"  ❌ Failed for topic '{topic.topic}': {e}", exc_info=True)
            continue

    # Step 7: Notify (optional)
    if packager:
        logger.info(f"\n[7/7] Sending notification...")
        packager.send_telegram_notification(summary)
    else:
        logger.info(f"\n[7/7] Skipping notification (Telegram not configured)")

    logger.info("\n" + "=" * 60)
    logger.info(f"PRODUCTION COMPLETE — Week {week}")
    logger.info(f"  Reels: {summary['reels']}  Carousels: {summary['carousels']}  Posts: {summary['posts']}")
    logger.info(f"  Output: {output_base.absolute()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_weekly_production()
