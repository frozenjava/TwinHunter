# TwinHunter
A proof of concept project to detect an stop Evil Twin Attacks.

# What It Does
Scans the wireless airspace and looks for wireless access points that may be imitating a legitmate one (this is called an evil twin attack).
If an Evil Twin is discovered then it will be instantly flooded with deauth frames preventing any clients from connecting to it.

# Known Issues
* No channel hopping
* Deauthing never stops even if the access point goes away
* Threads opened by the `Deauther` are not stopped properly
* Observers of the `Scanner` object are not stopped properly

# Goals
* Fix the known issues
* Allow white listing of multiple wifi access points
* Allow the use of multiple wifi interfaces to limit the amount of channel hopping a single interface needs to do
* Be able to detect and respond to other wifi events not just beacons

# Setup

This projects requires Python 3.5 or greater.

* Clone the repo:
```bash
git clone https://github.com/frozenjava/TwinHunter.git
```

* Install the requirements
```bash
cd TwinHunter
pip install -r requirements.txt
```

* Put your wireless interface into monitor mode
```bash
airmon-ng start wlan0
```

* Run the script
```bash
chmod +x twinhunter.py
./twinhunter.py --iface wlan0mon --essid home --bssid 00:11:22:33:44:55
```
