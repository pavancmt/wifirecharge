import os
import asyncio
from playwright.async_api import async_playwright

async def run():
    target_number = os.getenv("TARGET_NUMBER")
    user = os.getenv("PORTAL_USER")
    password = os.getenv("PORTAL_PASS")

    if not target_number:
        print("Error: No target number provided.")
        return

    async with async_playwright() as p:
        # headless=True means it runs invisibly on GitHub's servers
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("1. Logging into J-Networks...")
            await page.goto("https://admin.jnetworksbroadband.com")
            await page.fill('input[name="username"]', user)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')
            
            # Wait for the dashboard to load completely
            await page.wait_for_timeout(3000) 
            
            print(f"2. Searching for customer: {target_number}...")
            # Clicks the phone number/name from the Total list
            await page.get_by_text(target_number).click()
            await page.wait_for_timeout(2000)
            
            print("3. Opening 'Renew User' tab...")
            await page.get_by_text("Renew User").click()
            await page.wait_for_timeout(1000)
            
            print("4. Selecting Package and Subpackage...")
            # NOTE: If these are standard dropdowns, this works. 
            # You may need to change '1 month' to the exact text shown in the dropdown.
            # If they are just clickable boxes, change this to: await page.get_by_text("1 month").click()
            await page.locator('select[name="package"]').select_option(index=1) # Selects the first package
            await page.locator('select[name="subpackage"]').select_option(label="1 month")
            
            print("5. Clicking Renew...")
            await page.get_by_text("Renew", exact=True).click()
            await page.wait_for_timeout(1000)
            
            print("6. Confirming Renewal...")
            await page.get_by_text("Confirm Renew").click()
            
            print(f"✅ SUCCESS: Recharge completed for {target_number}")
            
        except Exception as e:
            print(f"❌ ERROR during recharge: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
