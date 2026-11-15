import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACTS_DIR = r"C:\Users\jayes\.gemini\antigravity-ide\brain\cfea5f02-0d60-4809-aa74-4676d78612b9"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        base_url = "http://127.0.0.1:8085"
        
        # Take a screenshot of the home page
        print("Capturing Home Page...")
        await page.goto(f"{base_url}/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "home_page.png"), full_page=True)
        
        # Take a screenshot of the login page
        print("Capturing Login Page...")
        await page.goto(f"{base_url}/auth/login/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "login_page.png"), full_page=True)
        
        # Login as buyer to access other pages
        print("Logging in as buyer...")
        await page.fill("input[name='username']", "buyer")
        await page.fill("input[name='password']", "admin")
        await page.click("button[type='submit']")
        await page.wait_for_load_state('networkidle')
        
        # Take a screenshot of the catalog page
        print("Capturing Catalog Page...")
        await page.goto(f"{base_url}/catalog/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "catalog_page.png"), full_page=True)
        
        # Take a screenshot of the buyer dashboard
        print("Capturing Buyer Dashboard...")
        await page.goto(f"{base_url}/portal/buyer/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "buyer_dashboard.png"), full_page=True)

        # AI tools
        print("Capturing AI Tools...")
        await page.goto(f"{base_url}/ai/tools/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "ai_tools.png"), full_page=True)
        
        # Chatbot
        print("Capturing Chatbot...")
        await page.goto(f"{base_url}/ai/chatbot/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "chatbot.png"), full_page=True)
        
        # Logout
        print("Logging out...")
        await page.goto(f"{base_url}/auth/logout/")
        
        # Login as vendor
        print("Logging in as vendor...")
        await page.goto(f"{base_url}/auth/login/")
        await page.fill("input[name='username']", "vendor")
        await page.fill("input[name='password']", "admin")
        await page.click("button[type='submit']")
        await page.wait_for_load_state('networkidle')
        
        # Take a screenshot of the vendor dashboard
        print("Capturing Vendor Dashboard...")
        await page.goto(f"{base_url}/portal/vendor/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "vendor_dashboard.png"), full_page=True)
        
        # Logout
        await page.goto(f"{base_url}/auth/logout/")

        # Login as admin
        print("Logging in as admin...")
        await page.goto(f"{base_url}/auth/login/")
        await page.fill("input[name='username']", "admin")
        await page.fill("input[name='password']", "admin")
        await page.click("button[type='submit']")
        await page.wait_for_load_state('networkidle')

        # Take a screenshot of the admin dashboard
        print("Capturing Admin Dashboard...")
        await page.goto(f"{base_url}/portal/admin/")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "admin_dashboard.png"), full_page=True)

        await browser.close()
        print("Done!")

asyncio.run(main())
