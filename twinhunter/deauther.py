from threading import Thread
import typing

import scapy.all as scapy
from twinhunter.accesspoint import AccessPoint


class Deauther(object):
    def __init__(self, interface: str, trusted_ap: AccessPoint):
        self._interface = interface
        self._trusted_ap = trusted_ap
        self._deauth_threads: typing.List[Thread] = list()

    def check_threat(self, ap: AccessPoint):
        """
        Compare ESSIDs and BSSIDs of access point `ap` with access point `_trusted_ap`.
        If the ESSIDS match and the BSSIDS do not match then assume its an evil twin and start sending deauth packets.
        """
        if ap.essid == self._trusted_ap.essid and ap.bssid.lower() != self._trusted_ap.bssid.lower():
            print("FOUND EVIL TWIN!!! BSSID: {0!s} | ESSID: {1!s}".format(ap.bssid, ap.essid))
            thread = Thread(target=self.deuath, args=(ap,))
            self._deauth_threads.append(thread)
            thread.start()

    def deuath(self, ap: AccessPoint):
        """
        Sends deauth packets to a given access point.
        """
        pkt = (
            scapy.RadioTap()
            / scapy.Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=ap.bssid, addr3=ap.bssid)
            / scapy.Dot11Deauth(reason=7)
        )
        while True:
            scapy.sendp(pkt, iface=self._interface)
