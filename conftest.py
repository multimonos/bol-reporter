import pytest
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from pydo import Client

from model import DropletConfig, ForgeConfig, OceanConfig, WebappConfig

"""load the env"""
load_dotenv()


def pytest_configure(config):
    config.option.maxprocesses = 1


"""
.env
"""
REQUIRED_ENV = [
    "APP_URL",
    "APP_USERNAME",
    "APP_PASSWORD",
    "FORGE_APIURL",
    "FORGE_APIKEY",
    "FORGE_SERVERID",
    "FORGE_SITEID",
    "OCEAN_APIKEY",
    "OCEAN_PRD_DROPLET_NAME",
    "OCEAN_STG_DROPLET_NAME",
]


def pytest_sessionstart(session: pytest.Session):
    missing = [var for var in REQUIRED_ENV if var not in os.environ]
    if missing:
        raise pytest.UsageError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


"""
Fixtures
"""


@pytest.fixture(scope="session")
def webapp_config() -> WebappConfig:
    """get webapp config"""
    return WebappConfig(
        url=os.environ.get("APP_URL", "") or "",
        hostname=urlparse(os.environ.get("APP_URL", "")).hostname or "",
        username=os.environ.get("APP_USERNAME", ""),
        password=os.environ.get("APP_PASSWORD", ""),
    )


@pytest.fixture(scope="session")
def forge_session() -> requests.Session:
    """get the laravel forge api baseurl and a requests session"""
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {os.environ.get('FORGE_APIKEY', '')}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    return session


@pytest.fixture(scope="session")
def forge_config() -> ForgeConfig:
    """get laravel forge config"""
    return ForgeConfig(
        apiurl=os.environ.get("FORGE_APIURL", ""),
        apikey=os.environ.get("FORGE_APIKEY", ""),
        server_id=int(os.environ.get("FORGE_SERVERID", 0)),
        site_id=int(os.environ.get("FORGE_SITEID", 0)),
    )


@pytest.fixture(scope="session")
def ocean_client() -> Client:
    """get the digital ocean client"""
    client = Client(token=os.environ.get("OCEAN_APIKEY", ""))
    return client


@pytest.fixture(scope="session")
def ocean_config() -> OceanConfig:
    """get digital ocean configs"""
    prd = DropletConfig(name=os.environ.get("OCEAN_PRD_DROPLET_NAME", ""))
    stg = DropletConfig(name=os.environ.get("OCEAN_STG_DROPLET_NAME", ""))

    return OceanConfig(apikey=os.environ.get("OCEAN_APIKEY", ""), prd=prd, stg=stg)


"""
Report output plugin adds docstrings where present.
"""
results: dict[str, str] = {}


def pytest_collection_modifyitems(items) -> None:
    """set custom docstring property when possible for each test"""
    for item in items:
        item.docstring = getattr(item.function, "__doc__", None)
        print("doc:", item.docstring)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """collect test results"""
    if report.when != "call":
        return

    results[report.nodeid] = report.outcome


def pytest_sessionfinish(session: pytest.Session) -> None:
    """write output to file"""
    # target
    Path("reports").mkdir(exist_ok=True)
    report_path = f"reports/{datetime.now().strftime('%Y-%m-%d')}.md"

    # write
    with open(report_path, "w") as f:
        f.write("\n#")
        f.write(f"\n# BOL Report – {datetime.now().strftime('%Y-%m-%d')}")
        f.write("\n#")
        f.write("\n")

        for item in session.items:
            docstring = getattr(item, "docstring", None)
            title = docstring if docstring else item.nodeid
            status = results.get(item.nodeid, "Unknown").upper()
            f.write(f"\n- {title} [{status}]")

        f.write("\n")
        f.write("\n# END")
        f.write("\n")
