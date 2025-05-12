from pydo import Client
import pytest
from pprint import pprint
from datetime import datetime, timedelta, timezone
from model import OceanConfig


@pytest.fixture(scope="module")
def projects(ocean_client: Client) -> dict:
    res = ocean_client.projects.list()
    return res.get("projects", [])


@pytest.fixture(scope="module")
def droplets(ocean_client: Client) -> dict:
    res = ocean_client.droplets.list()
    return res.get("droplets", [])


def test_ocean_project_exists(projects: dict):
    """digital-ocean : project : exists"""
    assert len(projects) == 1
    v = projects[0].get("name", "")
    assert v.lower() == "igloo dev"


def test_ocean_droplet_count(droplets: dict):
    """digital-ocean : droplets : 2"""
    assert len(droplets) == 2


def test_ocean_droplet_names(droplets: dict, ocean_config: OceanConfig):
    """digital-ocean : droplets : found staging, production"""
    assert len(droplets) == 2
    names = [x.get("name", "") for x in droplets]
    assert ocean_config.stg.name in names
    assert ocean_config.prd.name in names


def test_ocean_droplet_status(droplets: dict):
    """digital-ocean : droplets : all envs : status=active"""
    assert len(droplets) == 2
    l = list(set([x.get("status", "") for x in droplets]))
    assert len(l) == 1
    assert "active" in l


def test_ocean_droplet_memory(droplets: dict):
    """digital-ocean : droplets : all envs : memory=1024"""
    assert len(droplets) == 2
    l = list(set([x.get("memory", "") for x in droplets]))
    assert len(l) == 1
    assert 1024 in l


def test_ocean_droplet_cpus(droplets: dict):
    """digital-ocean : droplets : all envs : cpus=1"""
    assert len(droplets) == 2
    l = list(set([x.get("vcpus", "") for x in droplets]))
    assert len(l) == 1
    assert 1 in l


def test_ocean_droplet_disk(droplets: dict):
    """digital-ocean : droplets : all envs : disk=25"""
    assert len(droplets) == 2
    l = list(set([x.get("disk", "") for x in droplets]))
    assert len(l) == 1
    assert 25 in l
