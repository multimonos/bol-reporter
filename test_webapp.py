import requests


def test_app_exists(app_baseurl):
    """Check the main website is up and running"""
    r = requests.get(app_baseurl)
    assert r.status_code == 200
