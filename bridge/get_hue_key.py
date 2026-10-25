# Erzeugt einen API-Schluessel (username) fuer die Philips Hue Bridge.
# Ablauf: zuerst den runden Knopf auf der Hue Bridge druecken,
# dann innert 30 Sekunden dieses Skript starten.
# Den ausgegebenen "username" in config.py bei HUE_USER eintragen.
import requests

HUE_BRIDGE_IP = "192.168.x.x"   # IP-Adresse der Hue Bridge eintragen

r = requests.post(f"http://{HUE_BRIDGE_IP}/api", json={"devicetype": "oxowake#pc"})
print(r.json())
