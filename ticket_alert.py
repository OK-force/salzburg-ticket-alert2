from playwright.sync_api import sync_playwright
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.salzburgerfestspiele.at/en/p/vienna-philhamonic-muti-2026"

def send_telegram(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, timeout=60000)

    page.wait_for_timeout(5000)

    html = page.content()

    browser.close()

    if "BUY" in html:
        send_telegram(
    "🎟️ Vienna Philharmonic · Muti 취소표 떴다!!!\n\n"
    "https://www.salzburgerfestspiele.at/en/p/vienna-philhamonic-muti-2026"
)
        print("FOUND BUY")
    else:
        print("Still sold out")
