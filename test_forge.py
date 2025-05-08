import pytest


@pytest.fixture(scope="module")
def server(forge_config, forge_session):
    url = f"{forge_config.apiurl}/servers/{forge_config.server_id}"
    res = forge_session.get(url)
    res.raise_for_status()
    return res.json()["server"]


@pytest.fixture(scope="module")
def site(forge_config, forge_session):
    url = f"{forge_config.apiurl}/servers/{forge_config.server_id}/sites/{forge_config.site_id}"
    res = forge_session.get(url)
    res.raise_for_status()
    return res.json()["site"]


@pytest.fixture(scope="module")
def monitors(forge_config, forge_session):
    url = f"{forge_config.apiurl}/servers/{forge_config.server_id}/monitors"
    res = forge_session.get(url)
    res.raise_for_status()
    return res.json()["monitors"]


@pytest.fixture(scope="module")
def backups(forge_config, forge_session):
    url = f"{forge_config.apiurl}/servers/{forge_config.server_id}/backup-configs"
    res = forge_session.get(url)
    res.raise_for_status()
    return res.json()["backups"]


def test_forge_server_exists(server):
    """forge : server : exists"""
    assert isinstance(server, dict)


def test_forge_server_name(server):
    """forge : server : name=colouredaggregates-prd"""
    v = server["name"]
    assert isinstance(v, str)
    assert v == "colouredaggregates-prd"


def test_forge_server_type(server):
    """forge : server : type=app"""
    v = server["type"]
    assert isinstance(v, str)
    assert v == "app"


def test_forge_server_php_version(server):
    """forge : server : php version=7.4"""
    v = server["php_version"]
    assert isinstance(v, str)
    assert v == "php74"


def test_forge_server_mysql_version(server):
    """forge : server : mysql version=8"""
    v = server["database_type"]
    assert isinstance(v, str)
    assert v == "mysql8"


def test_forge_server_ready(server):
    """forge : server : is_ready"""
    v = server["is_ready"]
    assert isinstance(v, bool)
    assert v == True


def test_forge_site_exists(site):
    """forge : site : exists"""
    assert isinstance(site, dict)


def test_forge_site_name(site):
    """forge : site : name=app.colouredaggregates.com"""
    v = site["name"]
    assert isinstance(v, str)
    assert v == "app.colouredaggregates.com"


def test_forge_site_status(site):
    """forge : site : status=installed"""
    v = site["status"]
    assert isinstance(v, str)
    assert v == "installed"


def test_forge_site_project_type(site):
    """forge : site : project_type=php"""
    v = site["project_type"]
    assert isinstance(v, str)
    assert v == "php"


def test_forge_site_php_version(site):
    """forge : site : php_version=php74"""
    v = site["php_version"]
    assert isinstance(v, str)
    assert v == "php74"


def test_forge_site_failure_notify(site):
    """forge : site : notify=craig@iglooit.com"""
    v = site["failure_deployment_emails"]
    assert isinstance(v, str)
    assert v == '["craig@iglooit.com"]'


def test_forge_monitor_states(monitors):
    """forge : monitors : status=OK"""
    assert len(monitors) == 2
    for monitor in monitors:
        assert monitor["state"] == "OK"


def test_forge_monitor_types(monitors):
    """forge : monitors : type=disk"""
    assert len(monitors) == 2
    for monitor in monitors:
        assert monitor["type"] == "disk"


def test_forge_monitor_statuses(monitors):
    """forge : monitors : status=installed"""
    assert len(monitors) == 2
    for monitor in monitors:
        assert monitor["status"] == "installed"


def test_forge_backup(backups):
    """forge : backup configs : count=3"""
    assert len(backups) == 3


def test_forge_backup_installed(backups):
    """forge : backup configs : installed=true"""
    assert len(backups) == 3
    for backup in backups:
        assert backup["status"] == "installed"


def test_forge_backup_provider(backups):
    """forge : backup configs : provider=spaces"""
    assert len(backups) == 3
    for backup in backups:
        assert backup["provider"] == "spaces"


def test_forge_backup_databases(backups):
    """forge : backup configs : database=forge,colouredaggregates_prd"""
    assert len(backups) == 3
    for backup in backups:
        assert len(backup["databases"]) == 2
        names = [x["name"] for x in backup["databases"]]
        assert "forge" in names
        assert "colouredaggregates_prd" in names


def test_forge_backup_schedules(backups):
    """forge : backup configs : schedules=hourly,daily,weekly"""
    assert len(backups) == 3
    schedules = [x["schedule"] for x in backups]
    assert "daily" in schedules
    assert "hourly" in schedules
    assert "weekly" in schedules


def test_forge_backup_successes(backups):
    """forge : backup successes : all ok"""
    assert len(backups) == 3
    for backup in backups:
        statuses = list(set([x["status"] for x in backup["backups"]]))
        assert len(statuses) == 1
        assert "success" in statuses
