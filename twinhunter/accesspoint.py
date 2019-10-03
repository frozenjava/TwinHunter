from dataclasses import dataclass


@dataclass
class AccessPoint:
    bssid: str
    essid: str
