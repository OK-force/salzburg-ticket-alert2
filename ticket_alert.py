from playwright.sync_api import sync_playwright
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.salzburgerfestspiele.at/en/p/vienna-philhamonic-muti-2026#tickets"

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

    # 16 August 영역만 찾기
    if '<div class="en-format-number">16</div>' in html:
        target = html.split('<div class="en-format-number">16</div>')[1][:1500]

        # 16일 블록 안에 Sold Out이 없으면 알림
        if "Sold Out" not in target and "SOLD OUT" not in target:
            send_telegram(
                "🎟️ Vienna Philharmonic · Muti (16 Aug) 취소표 떴다!!!\n\n"
                "https://www.salzburgerfestspiele.at/en/p/vienna-philhamonic-muti-2026#tickets"
            )
            print("FOUND 16 AUG TICKET")
        else:
            print("16 Aug still sold out")
    else:
        print("16 Aug section not found")
