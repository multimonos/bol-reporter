import pytest
from collections.abc import Generator
from datetime import datetime
from pathlib import Path


results = {}


def pytest_configure(config):
    config.option.maxprocesses = 1


def pytest_collection_modifyitems(items):
    """set custom docstring property when possible for each test"""
    for item in items:
        item.docstring = getattr(item.function, "__doc__", None)
        print("doc:", item.docstring)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """collect test results"""
    if report.when != "call":
        return

    results[report.nodeid] = report.outcome


def pytest_sessionfinish(session):
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
