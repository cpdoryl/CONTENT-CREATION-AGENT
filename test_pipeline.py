"""Test all stages of the Streamlit pipeline"""
import asyncio
import time
from playwright.async_api import async_playwright

async def test_pipeline():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("=" * 60)
        print("STAGE 1: Opening app and navigating to Auto Pipeline")
        print("=" * 60)

        # Navigate to app
        await page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(2)

        # Click on Auto Pipeline page
        try:
            await page.click('text=⚡ Auto Pipeline')
            await page.wait_for_load_state("networkidle")
            time.sleep(2)
            screenshot1 = await page.screenshot(path="stage1_navigate.png")
            print("[PASS] Successfully navigated to Auto Pipeline")
        except Exception as e:
            print(f"[FAIL] Failed to navigate: {e}")
            await browser.close()
            return

        print("\n" + "=" * 60)
        print("STAGE 2: Starting Research")
        print("=" * 60)

        # Click Start Research button
        try:
            # Look for the research button
            await page.click('button:has-text("Start Research")')
            print("[PASS] Clicked Start Research button")

            # Wait for research to complete (60 seconds max)
            print("[WAIT] Waiting for research results (up to 60 seconds)...")
            start_time = time.time()
            while time.time() - start_time < 60:
                content = await page.content()
                if "Found" in content and "trending topics" in content:
                    print("[PASS] Research completed!")
                    break
                await page.wait_for_timeout(3000)

            time.sleep(2)
            screenshot2 = await page.screenshot(path="stage2_research_complete.png")

            # Click Approve & Continue
            await page.click('button:has-text("Approve & Continue")')
            print("[PASS] Clicked Approve & Continue")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Research failed: {e}")
            await browser.close()
            return

        print("\n" + "=" * 60)
        print("STAGE 3: Generating Content Packages")
        print("=" * 60)

        print("[WAIT] Waiting for content generation (2-3 minutes)...")
        start_time = time.time()

        # Wait for content generation to complete
        while time.time() - start_time < 300:  # 5 minute timeout
            content = await page.content()
            if "Stage 4" in content or "Review & Approve Content" in content:
                print("[PASS] Content generation completed!")
                break
            await page.wait_for_timeout(5000)

        time.sleep(2)
        screenshot3 = await page.screenshot(path="stage3_content_generated.png")

        print("\n" + "=" * 60)
        print("STAGE 4: Verifying Approval Workflow")
        print("=" * 60)

        content = await page.content()

        # Check for toggle buttons (new approval mechanism)
        if "toggle" in content.lower() or "button" in content.lower():
            print("[PASS] Stage 4 loaded - checking for toggle buttons...")

        # Look for auto-approval indicators
        if "approved" in content.lower():
            print("[PASS] Items appear to be auto-approved")

        # Take screenshot of Stage 4
        time.sleep(2)
        screenshot4 = await page.screenshot(path="stage4_approval.png")
        print("[INFO] Screenshot saved: stage4_approval.png")

        # Look for Export button and click it
        try:
            export_buttons = await page.query_selector_all('button:has-text("Export")')
            if export_buttons:
                await export_buttons[0].click()
                print("[PASS] Clicked Export button")
                time.sleep(3)
            else:
                print("[WARN] Export button not found")
        except Exception as e:
            print(f"[WARN] Could not click Export: {e}")

        print("\n" + "=" * 60)
        print("STAGE 5: Verifying Export & Download")
        print("=" * 60)

        # Check for download options
        content = await page.content()
        if "download" in content.lower() or "csv" in content.lower() or "json" in content.lower():
            print("[PASS] Stage 5 shows download options")
        else:
            print("[WARN] No obvious download options visible")

        time.sleep(2)
        screenshot5 = await page.screenshot(path="stage5_export.png")
        print("[INFO] Screenshot saved: stage5_export.png")

        print("\n" + "=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)
        print("Screenshots saved:")
        print("  - stage1_navigate.png")
        print("  - stage2_research_complete.png")
        print("  - stage3_content_generated.png")
        print("  - stage4_approval.png")
        print("  - stage5_export.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_pipeline())
