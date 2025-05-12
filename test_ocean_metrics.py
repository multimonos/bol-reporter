from _pytest import scope
from pydo import Client
import pytest
from datetime import datetime, timedelta, timezone
from model import DropletInfo, OceanConfig, TimestampWindow

from typing import Any


def get_metric_values(metric_response: Any) -> list:
    try:
        result = metric_response.get("data", {}).get("result", [])
        if result and len(result) > 0:
            return result[0].get("values", [])
        return []
    except (AttributeError, IndexError, TypeError):
        return []


@pytest.fixture(scope="module")
def window() -> TimestampWindow:
    """use the same timestamp window for all queries"""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=7)
    start_ts = int(start.timestamp())
    end_ts = int(now.timestamp())
    ts = TimestampWindow(start=start_ts, end=end_ts)
    return ts


@pytest.fixture(scope="module")
def droplet_info(ocean_client: Client) -> list[DropletInfo]:
    """collect a subset of the droplet info required for the metrics"""
    res = ocean_client.droplets.list()
    droplets = res.get("droplets", [])

    info = []
    for droplet in droplets:
        di = DropletInfo(
            id=droplet.get("id", 0),
            name=droplet.get("name", ""),
            disk_size=droplet.get("disk", 0) * 1024**3,
        )
        info.append(di)
    return info


def test_ocean_metric_filesystem_free(
    ocean_client: Client, droplet_info: list[DropletInfo], window: TimestampWindow
):
    """disk free is greater than 20%"""
    for droplet in droplet_info:
        res = ocean_client.monitoring.get_droplet_filesystem_free_metrics(
            host_id=str(droplet.id), start=str(window.start), end=str(window.end)
        )

        values = get_metric_values(res)

        sizes = [int(x[1]) for x in values]
        avg = sum(sizes) / len(sizes) if len(sizes) > 0 else 0
        df = avg / droplet.disk_size

        assert df > 0.2
