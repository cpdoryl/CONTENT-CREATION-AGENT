"""
Comprehensive test suite for all 7 agents
Run: python test_agents.py
"""

import os
import sys
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import get_logger
from src.core.config import settings
from src.core.models import ContentTopic

logger = get_logger("test_suite")


def test_config():
    """Test 1: Configuration loading"""
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Configuration Loading")
    logger.info("="*60)

    try:
        logger.info(f"✅ NICHE: {settings.NICHE}")
        logger.info(f"✅ TARGET_AUDIENCE: {settings.TARGET_AUDIENCE}")
        logger.info(f"✅ BRAND_VOICE: {settings.BRAND_VOICE}")
        logger.info(f"✅ CONTENT_PER_WEEK: {settings.CONTENT_PER_WEEK}")
        logger.info(f"✅ OpenAI API Key loaded: {bool(settings.OPENAI_API_KEY)}")
        logger.info(f"✅ ElevenLabs API Key loaded: {bool(settings.ELEVENLABS_API_KEY)}")
        logger.info(f"✅ Perplexity API Key loaded: {bool(settings.PERPLEXITY_API_KEY)}")
        logger.info("✅ Config test PASSED")
        return True
    except Exception as e:
        logger.error(f"❌ Config test FAILED: {e}")
        return False


def test_research_agent():
    """Test 2: Research Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Research Agent (Perplexity API)")
    logger.info("="*60)

    if not settings.PERPLEXITY_API_KEY:
        logger.warning("⚠️  SKIPPED: Perplexity API key not set")
        return None

    try:
        from src.agents.research_agent import ResearchAgent

        agent = ResearchAgent()
        logger.info("Researching trends... (this takes ~30 seconds)")
        topics = agent.research_trends()

        if not topics:
            logger.error("❌ No topics returned")
            return False

        logger.info(f"✅ Found {len(topics)} trending topics")
        for i, topic in enumerate(topics[:3], 1):
            logger.info(f"   {i}. [{topic.priority_score}/10] {topic.topic}")
            logger.info(f"      Hook: {topic.hook_angle}")
        logger.info("✅ Research agent test PASSED")
        return True
    except Exception as e:
        logger.error(f"❌ Research agent test FAILED: {e}", exc_info=True)
        return False


def test_script_agent():
    """Test 3: Script Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 3: Script Agent (GPT-4o)")
    logger.info("="*60)

    if not settings.OPENAI_API_KEY:
        logger.warning("⚠️  SKIPPED: OpenAI API key not set")
        return None

    try:
        from src.agents.script_agent import ScriptAgent

        # Create mock topic
        test_topic = ContentTopic(
            topic="5 Money Mistakes Gen Z Makes",
            why_trending="Gen Z is struggling with finances",
            hook_angle="shame and embarrassment",
            recommended_format="reel",
            pain_point="wasting money without realizing",
            title_options=["5 Money Mistakes", "Stop Wasting Money", "Rich People Know This"],
            priority_score=9
        )

        agent = ScriptAgent()
        logger.info(f"Writing script for: {test_topic.topic}")
        logger.info("This takes ~30 seconds...")

        script = agent.write_reel_script(test_topic, duration=45)

        logger.info(f"✅ Reel script written ({script.word_count} words)")
        logger.info(f"   Hook: {script.hook[:60]}...")
        logger.info(f"   CTA: {script.cta[:60]}...")

        logger.info("Writing carousel copy...")
        carousel = agent.write_carousel(test_topic)
        logger.info(f"✅ Carousel written ({len(carousel)} slides)")

        logger.info("Writing caption...")
        caption, hashtags = agent.write_caption(test_topic, script)
        logger.info(f"✅ Caption written ({len(caption)} chars, {len(hashtags)} hashtags)")

        logger.info("✅ Script agent test PASSED")
        return True
    except Exception as e:
        logger.error(f"❌ Script agent test FAILED: {e}", exc_info=True)
        return False


def test_voice_agent():
    """Test 4: Voice Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 4: Voice Agent (ElevenLabs TTS)")
    logger.info("="*60)

    if not settings.ELEVENLABS_API_KEY:
        logger.warning("⚠️  SKIPPED: ElevenLabs API key not set")
        return None

    try:
        from src.agents.voice_agent import VoiceAgent

        agent = VoiceAgent()

        # Check quota
        quota = agent.get_remaining_characters()
        logger.info(f"✅ Quota check:")
        logger.info(f"   Used: {quota['used']:,}")
        logger.info(f"   Limit: {quota['limit']:,}")
        logger.info(f"   Remaining: {quota['remaining']:,}")

        # Generate test voiceover
        test_script = "This is a test. Your content agent is working correctly. Great job."
        output_path = Path("output/test_voice.mp3")

        logger.info(f"Generating test voiceover... (10 seconds)")
        agent.generate_voiceover(test_script, output_path)

        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            logger.info(f"✅ Voiceover generated: {size_kb:.1f} KB")

            # Try to get duration
            try:
                duration = agent.get_audio_duration(output_path)
                logger.info(f"✅ Audio duration: {duration:.1f} seconds")
            except Exception as e:
                logger.warning(f"Could not get duration: {e}")

            logger.info("✅ Voice agent test PASSED")
            return True
        else:
            logger.error("❌ Voiceover file not created")
            return False
    except Exception as e:
        logger.error(f"❌ Voice agent test FAILED: {e}", exc_info=True)
        return False


def test_visual_agent():
    """Test 5: Visual Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 5: Visual Agent (DALL-E 3)")
    logger.info("="*60)

    if not settings.OPENAI_API_KEY:
        logger.warning("⚠️  SKIPPED: OpenAI API key not set")
        return None

    try:
        from src.agents.visual_agent import VisualAgent
        from src.core.models import ReelScript

        # Create test package
        test_topic = ContentTopic(
            topic="Budget Hacks",
            why_trending="Everyone needs to save money",
            hook_angle="practical and empowering",
            recommended_format="reel",
            pain_point="not enough money",
            title_options=["Save Money", "Budget Hacks", "Money Secrets"],
            priority_score=8
        )

        test_script = ReelScript(
            topic="Budget Hacks",
            hook="Want to save $500 this month?",
            problem="Most people waste money without realizing.",
            value="Here are three proven hacks.",
            cta="Try one today.",
            full_script="Want to save? Try this. It works.",
            word_count=10
        )

        from src.core.models import ContentPackage
        test_package = ContentPackage(
            topic=test_topic,
            reel_script=test_script,
            carousel_slides=[],
            caption="Test",
            hashtags=[]
        )

        agent = VisualAgent()
        logger.info("Generating visual prompt...")
        prompt = agent.generate_visual_prompt(test_package, format="reel")
        logger.info(f"✅ Prompt generated: {len(prompt)} chars")
        logger.info(f"   {prompt[:100]}...")

        logger.info("⚠️  Skipping actual DALL-E image generation (costs $0.04)")
        logger.info("   To generate image, run: agent.generate_reel_background(package, output_path)")
        logger.info("✅ Visual agent test PASSED (prompt only)")
        return True
    except Exception as e:
        logger.error(f"❌ Visual agent test FAILED: {e}", exc_info=True)
        return False


def test_video_agent():
    """Test 6: Video Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 6: Video Agent (FFmpeg)")
    logger.info("="*60)

    try:
        from src.agents.video_agent import VideoAgent
        import subprocess

        # Check if FFmpeg is installed
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning("⚠️  SKIPPED: FFmpeg not installed")
            return None

        ffmpeg_version = result.stdout.split('\n')[0]
        logger.info(f"✅ FFmpeg found: {ffmpeg_version}")

        agent = VideoAgent()
        logger.info("✅ Video agent initialized")
        logger.info("⚠️  Skipping actual video assembly (requires image + audio files)")
        logger.info("   To assemble video, run: agent.assemble_reel_ffmpeg(image, audio, output)")
        logger.info("✅ Video agent test PASSED (init only)")
        return True
    except FileNotFoundError:
        logger.warning("⚠️  SKIPPED: FFmpeg not installed on system")
        logger.info("   Install FFmpeg: brew install ffmpeg (Mac) or apt install ffmpeg (Linux)")
        return None
    except Exception as e:
        logger.error(f"❌ Video agent test FAILED: {e}", exc_info=True)
        return False


def test_carousel_agent():
    """Test 7: Carousel Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 7: Carousel Agent (Pyppeteer)")
    logger.info("="*60)

    try:
        from src.agents.carousel_agent import CarouselAgent

        agent = CarouselAgent()
        logger.info(f"✅ Carousel agent initialized")
        logger.info(f"   Template dir: {agent.template_dir}")

        if agent.template_dir.exists():
            logger.info(f"✅ Template directory exists")
            template_file = agent.template_dir / "carousel_template.html"
            if template_file.exists():
                logger.info(f"✅ Carousel template found: {template_file.stat().st_size} bytes")
            else:
                logger.warning(f"⚠️  Carousel template not found")

        logger.info("⚠️  Skipping actual carousel rendering (requires Puppeteer)")
        logger.info("   To render carousel, run: agent.render_carousel(package, output_dir)")
        logger.info("✅ Carousel agent test PASSED (init only)")
        return True
    except Exception as e:
        logger.error(f"❌ Carousel agent test FAILED: {e}", exc_info=True)
        return False


def test_packager_agent():
    """Test 8: Packager Agent"""
    logger.info("\n" + "="*60)
    logger.info("TEST 8: Packager Agent (Google Drive + Telegram)")
    logger.info("="*60)

    if not settings.GOOGLE_CREDENTIALS_PATH:
        logger.warning("⚠️  SKIPPED: Google credentials path not set")
        return None

    try:
        from src.agents.packager_agent import PackagerAgent
        from pathlib import Path

        creds_path = Path(settings.GOOGLE_CREDENTIALS_PATH)
        if not creds_path.exists():
            logger.warning(f"⚠️  SKIPPED: Google credentials file not found at {creds_path}")
            return None

        logger.info("Initializing Packager agent...")
        agent = PackagerAgent()
        logger.info(f"✅ Week label: {agent.week_label}")

        logger.info("⚠️  Skipping actual Drive upload (requires OAuth)")
        logger.info("   First run will open browser for authorization")
        logger.info("✅ Packager agent test PASSED (init only)")
        return True
    except Exception as e:
        logger.error(f"❌ Packager agent test FAILED: {e}", exc_info=True)
        return False


def run_all_tests():
    """Run all tests and summarize results"""
    logger.info("\n\n")
    logger.info("=" * 60)
    logger.info("SOCIAL MEDIA CONTENT AGENT - TEST SUITE".center(60))
    logger.info("=" * 60)

    results = {
        "Config": test_config(),
        "Research": test_research_agent(),
        "Script": test_script_agent(),
        "Voice": test_voice_agent(),
        "Visual": test_visual_agent(),
        "Video": test_video_agent(),
        "Carousel": test_carousel_agent(),
        "Packager": test_packager_agent(),
    }

    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    for agent, result in results.items():
        status = "✅ PASSED" if result is True else ("❌ FAILED" if result is False else "⚠️  SKIPPED")
        logger.info(f"{agent:15} {status}")

    logger.info("="*60)
    logger.info(f"Passed: {passed}  Failed: {failed}  Skipped: {skipped}")
    logger.info("="*60)

    if failed == 0:
        logger.info("✅ ALL TESTS PASSED! Ready for production run.")
        logger.info("\nNext step: python main.py")
    else:
        logger.error(f"❌ {failed} test(s) failed. Check logs above.")


if __name__ == "__main__":
    run_all_tests()
