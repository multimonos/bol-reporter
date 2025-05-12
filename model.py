from dataclasses import dataclass


@dataclass
class DropletInfo:
    id: int
    name: str
    disk_size: int


@dataclass
class TimestampWindow:
    start: int
    end: int


@dataclass
class WebappConfig:
    url: str
    hostname: str
    username: str
    password: str


@dataclass
class ForgeConfig:
    apiurl: str
    apikey: str
    server_id: int
    site_id: int


@dataclass
class DropletConfig:
    name: str


@dataclass
class OceanConfig:
    apikey: str
    prd: DropletConfig
    stg: DropletConfig
