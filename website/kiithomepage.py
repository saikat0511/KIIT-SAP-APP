from playwright.sync_api import sync_playwright

def get_page():
    browser = sync_playwright().start().chromium.launch(headless=False) #headless=False
    context = browser.new_context()
    page = context.new_page()
    return page

def get_incognito_context():
    browser = sync_playwright().start().chromium.launch(headless=False) #headless=False
    context = browser.new_context()
    return context
