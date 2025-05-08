from urllib.parse import urlparse
import pytest
import requests
from model import WebappConfig
from util import ssl_valid_days
from playwright.sync_api import Error, TimeoutError, sync_playwright


def test_webapp_exists(webapp_config: WebappConfig) -> None:
    """webapp : main website is up and running"""
    r = requests.get(webapp_config.url)
    assert r.status_code == 200


def test_webapp_ssl_valid(webapp_config: WebappConfig) -> None:
    """webapp : ssl is valid for at least 30 days"""
    assert ssl_valid_days(webapp_config.hostname) > 30


def test_webapp_login(webapp_config: WebappConfig) -> None:
    """webapp : support user can login"""

    try:
        with sync_playwright() as p:
            browswer = p.chromium.launch(headless=True)
            page = browswer.new_page()

            page.goto(webapp_config.url)
            page.fill("#email", webapp_config.username)
            page.fill("#password", webapp_config.password)
            page.click("button[type=submit]")

            # assertions
            page.wait_for_selector("#nova", timeout=5000)

            url = urlparse(page.url)
            assert url.path == "/app/dashboards/main"

            browswer.close()

    except (TimeoutError, Error) as e:
        pytest.fail(f"Login failed or Playwright error: {type(e).__name__}: {e}")
