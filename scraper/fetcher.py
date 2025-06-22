from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def fetch_chapter_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path="chapter_screenshot.png", full_page=True)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return html, text.strip() 