from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from .kiithomepage import get_incognito_context
import json
from pathlib import Path


def block_aggressively(route):
	if (route.request.resource_type in {'image', 'font', 'media', 'other'}):
		route.abort()
	else:
		route.continue_()

def is_valid_user(userid: str, password: str) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch() #headless=False
        context = browser.new_context()
        page = context.new_page()
        page.route("**/*", block_aggressively)
        page.goto('https://kiitportal.kiituniversity.net/irj/portal')
        page.fill('#logonuidfield', userid)
        page.fill('#logonpassfield', password)
        page.click('input[type = submit]')
        page.wait_for_load_state('networkidle')
        if page.locator('#navNodeAnchor_1_1').is_visible():
            return True
        else:
            return False

def login(context, userid, password):
    page = context.new_page()
    page.route("**/*", block_aggressively)
    # page.on("request", lambda request: print(">>", request.method, request.url, request.resource_type))
    # page.on("response", lambda response: print("<<", response.status, response.url))
    # page.on("request", lambda request: print(">>", request.resource_type))
    try:
        page.goto('https://kiitportal.kiituniversity.net/irj/portal')
        page.fill('#logonuidfield', userid)
        page.fill('#logonpassfield', password)
        page.click('input[type = submit]')
        page.click('#navNodeAnchor_1_1')
    except PlaywrightTimeoutError:
        return -1
    return page






# generate cookies from saved password
def generate_cookies(userid, password, context=None):
    if context is None:
        context = get_incognito_context()
    page = context.new_page()
    # login
    page.goto('https://kiitportal.kiituniversity.net/irj/portal')
    page.fill('#logonuidfield', userid)
    page.fill('#logonpassfield', password)
    page.click('input[type = submit]')
    try:
        page.click('#navNodeAnchor_1_1', timeout=5000)
        # page.wait_for_load_state('networkidle')
    except PlaywrightTimeoutError:
        return -1
    else:
        cookie_path = Path(f'./{userid}.json')
        passwd_path = Path(f'./{userid}.txt')
        with open(cookie_path, "w") as f:
            f.write(json.dumps(context.cookies()))  # save new cookies
        if passwd_path.is_file() == False:
            with open(passwd_path, "w") as f:
                f.write(password)  # save password if not saved

        return page

# try to login using existing cookies, or regenerate cookies if failed
# return context with cookies loaded
def try_login(context, userid):
    try:  # check if login succeeded
        with open(f'{userid}.json', 'r') as f:
            context.add_cookies(json.loads(f.read()))
        page = context.new_page()
        page.goto('https://kiitportal.kiituniversity.net/irj/portal')
        page.click('#navNodeAnchor_1_1', timeout=2500)
    # if not succeeded regenerate cookies
    except (FileNotFoundError, PlaywrightTimeoutError) as e:
        with open(f'{userid}.txt', "r") as f:
            password = f.read()
        return generate_cookies(userid, password, context)
    else:
        return page
