"""Scheduler — runs the content agent on a recurring schedule using APScheduler"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from main import run_weekly_production
from src.utils.logger import get_logger

logger = get_logger("scheduler")

scheduler = BlockingScheduler(timezone="Asia/Kolkata")

# Run every Monday at 9:00 AM IST
scheduler.add_job(
    run_weekly_production,
    CronTrigger(day_of_week="mon", hour=9, minute=0),
    id="weekly_content_production",
    name="Weekly Content Production",
    misfire_grace_time=3600
)

if __name__ == "__main__":
    logger.info("Scheduler started — will run every Monday at 9:00 AM IST")
    logger.info("Press Ctrl+C to stop")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")
