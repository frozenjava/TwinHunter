#!/usr/bin/env python3

import argparse

from twinhunter.scanner import Scanner
from twinhunter.deauther import Deauther
from twinhunter.accesspoint import AccessPoint


def logger(ap):
    print("Discorvered Accesspoint => BSSID: {0!s} | ESSID: {1!s}".format(ap.bssid, ap.essid))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and stop Evil Twin attacks.")
    parser.add_argument("--iface", help="The monitor interface to watch on (ex: wlan0mon).", required=True)
    parser.add_argument("--essid", help="The SSID of the access point to protect.", required=True)
    parser.add_argument("--bssid", help="The BSSID of the legitimate access point to protect.", required=True)
    args = parser.parse_args()

    # The legitimate access point to trust
    trusted_ap = AccessPoint(bssid=args.bssid, essid=args.essid)

    # Create the deauth service
    deauther = Deauther(args.iface, trusted_ap)

    # Create the network scanner
    scanr = Scanner(args.iface)

    # Subscribe the logger to AP discovery events
    scanr.subscribe(logger)

    # Subscribe the deauther to AP discovery events
    scanr.subscribe(deauther.check_threat)

    # Start scanning for networks
    scanr.scan()
