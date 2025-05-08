from dataclasses import dataclass


@dataclass
class WebappConfig:
    url: str
    hostname: str
    username: str
    password: str
