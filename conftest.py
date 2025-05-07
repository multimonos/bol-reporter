import pytest
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

"""load the env"""
load_dotenv()


def pytest_configure(config):
    config.option.maxprocesses = 1


"""
.env
"""
REQUIRED_ENV = ["APP_BASEURL", "APP_SUPPORT_USERNAME", "APP_SUPPORT_PASSWORD"]


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
def baseurl() -> str:
    return os.environ.get("APP_BASEURL", "")


@pytest.fixture(scope="session")
def hostname() -> str:
    h = urlparse(os.environ.get("APP_BASEURL", "")).hostname
    return h if h else ""


@pytest.fixture(scope="session")
def support_user() -> tuple[str, str]:
    return (
        os.environ.get("APP_SUPPORT_USERNAME", ""),
        os.environ.get("APP_SUPPORT_PASSWORD", ""),
    )


"""
Report output plugin
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
        f.write(f"\n# BOL Report – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
