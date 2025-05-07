from urllib.parse import urlparse
import pytest
import requests
from util import ssl_valid_days
from playwright.sync_api import Error, TimeoutError, sync_playwright


def test_webapp_exists(baseurl):
    """main website is up and running"""
    r = requests.get(baseurl)
    assert r.status_code == 200


def test_webapp_ssl_valid(hostname):
    """ssl is valid for at least 30 days"""
    assert ssl_valid_days(hostname) > 30


def test_webapp_login(baseurl, support_user):
    """support user can login"""
    (usr, pwd) = support_user
    success = False
    err = ""

    try:
        with sync_playwright() as p:
            browswer = p.chromium.launch(headless=True)
            page = browswer.new_page()

            page.goto(baseurl)
            page.fill("#email", usr)
            page.fill("#password", pwd)
            page.click("button[type=submit]")

            # assertions
            page.wait_for_selector("#nova", timeout=5000)

            url = urlparse(page.url)
            assert url.path == "/app/dashboards/main"

            browswer.close()

    except (TimeoutError, Error) as e:
        pytest.fail(f"Login failed or Playwright error: {type(e).__name__}: {e}")
