from dataclasses import dataclass


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
class OceanConfig:
    apiurl: str
    apikey: str
