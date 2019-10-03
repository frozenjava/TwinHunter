from typing import List
import scapy.all as scapy
from twinhunter.accesspoint import AccessPoint


class Scanner(object):
    def __init__(self, interface: str):
        self._interface: str = interface
        self._ap_list: List[AccessPoint] = list()
        self._discovery_callbacks: list = list()

    def _packet_handler(self, pkt):
        """
        Handle packets picked up by scapy and determine if they are actual 802.11 beacons.
        If they are, check if its a new Access Point we haven't seen and add it to the list of known APs.
        Also, when a new AP is discovered any observers will be called and passed the new AccessPoint object.
        """
        if pkt.haslayer(scapy.Dot11Elt) and pkt.type == 0 and pkt.subtype == 8:
            ap = AccessPoint(bssid=pkt.addr2, essid=pkt.info.decode("utf-8"))
            if ap not in self._ap_list:
                self._ap_list.append(ap)

                # Call all observers
                for callback in self._discovery_callbacks:
                    callback(ap)

    def subscribe(self, callback):
        """
        Subscribe to the access point discovery events.
        Callbacks must take 1 argument of type AccessPoint
        """
        self._discovery_callbacks.append(callback)

    def scan(self):
        """
        Start scanning for wireless networks.
        """
        scapy.sniff(iface=self._interface, prn=self._packet_handler, store=0)
