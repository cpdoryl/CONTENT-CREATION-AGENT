"""Test approval metrics fix - quick focused test"""
import asyncio
import time
from playwright.async_api import async_playwright

async def test_approval_metrics():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print("[INFO] Starting approval metrics test...")
        print("[INFO] Note: App must already be in Stage 4 for this test to work")

        # Navigate to app
        await page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(3)

        # Get the page content
        content = await page.content()

        # Check for Stage 4
        if "Stage 4" in content or "Review & Approve Content" in content:
            print("[PASS] Stage 4 is loaded")

            # Look for the metrics
            if "Total Items" in content:
                print("[PASS] Metrics section found")

            # Check if items show as approved (look for green checkmarks)
            if "APPROVED" in content:
                approved_count = content.count("APPROVED")
                print(f"[PASS] Found {approved_count} approved items")

            # Take screenshot
            screenshot = await page.screenshot(path="approval_metrics_check.png")
            print("[INFO] Screenshot saved: approval_metrics_check.png")

        else:
            print("[WARN] Stage 4 not yet loaded - app may still be generating")
            screenshot = await page.screenshot(path="current_stage.png")
            print("[INFO] Current stage screenshot saved: current_stage.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_approval_metrics())
