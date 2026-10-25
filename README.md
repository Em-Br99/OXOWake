# OXOWake 🌅

Ein Lichtwecker, der morgens einen Sonnenaufgang simuliert: Vor der Weckzeit werden die Philips-Hue-Lampen im Schlafzimmer langsam heller, zur Weckzeit piepst die OXOCard, bis man sie per Joystick abstellt.

Schulprojekt an der HFTM (Modul Projektmanagement).

## So funktioniert es

```
OXOCard (NanoPy)  --GET-->  Flask-Bridge (Python)  --PUT-->  Hue Bridge  -->  Lampen
```

Die OXOCard kann nur einfache GET- und POST-Anfragen senden, die Hue-API braucht aber PUT-Anfragen. Deshalb läuft auf einem PC im selben Netz eine kleine Flask-Bridge, die als Übersetzer dient und den Sonnenaufgang steuert. Details: [docs/architektur.md](docs/architektur.md)

## Aufbau

| Ordner / Datei | Inhalt |
|---|---|
| `oxocard/oxowake.npy` | Hauptprogramm der OXOCard: Uhr, Sonnenaufgang-Animation, Weckton |
| `oxocard/host_finder.npy` | Prüft, auf welchem PC die Bridge gerade läuft |
| `oxocard/versuche/` | Einzelne Versuche: Uhr, Animation, Temperaturmessung mit NTC |
| `bridge/oxowake_bridge.py` | Flask-Bridge mit Endpunkten für Licht und Sonnenaufgang |
| `bridge/get_hue_key.py` | Erzeugt einmalig den API-Schlüssel der Hue Bridge |
| `bridge/config.example.py` | Vorlage für die eigene Konfiguration |

## Einrichten

**Voraussetzungen:** OXOCard Connect, Philips Hue Bridge mit Lampen, PC mit Python 3, alles im selben WLAN.

1. Abhängigkeiten installieren:
   ```
   cd bridge
   pip install -r requirements.txt
   ```
2. Hue-Schlüssel erzeugen: In `get_hue_key.py` die IP der Hue Bridge eintragen, den Knopf auf der Hue Bridge drücken und innert 30 Sekunden `python get_hue_key.py` starten.
3. `config.example.py` nach `config.py` kopieren und IP, Schlüssel und Lampen-IDs eintragen. `config.py` wird nicht hochgeladen (siehe `.gitignore`).
4. Bridge starten: `python oxowake_bridge.py` (läuft auf Port 5000).
5. In `oxocard/oxowake.npy` die IP des PCs eintragen, Weckzeit einstellen und das Programm auf die OXOCard laden.

## Endpunkte der Bridge

| Endpunkt | Wirkung |
|---|---|
| `/ping` | Lebenszeichen, berührt Hue nicht |
| `/light/on`, `/light/off` | Lampen voll ein / aus |
| `/sunrise/start` | Lampen schrittweise von dunkel auf hell dimmen |
| `/sunrise/stop` | Sonnenaufgang abbrechen, Lampen aus |

## Bekannte Grenzen

- Die Bridge hat keine Anmeldung. Jedes Gerät im selben WLAN kann die Lampen schalten. Für ein Heimnetz okay, für mehr nicht.
- Weckzeit und Vorlauf stehen fest im Code der OXOCard. Die Testwerte (z.B. 30 Sekunden Sonnenaufgang) müssen für den echten Einsatz angepasst werden.
- Die IP-Adresse des PCs ist fest eingetragen. Eine feste IP im Router (DHCP-Reservierung) macht das stabiler.

## Was ich dabei gelernt habe

- Wie Geräte im Heimnetz über HTTP miteinander sprechen und warum GET, POST und PUT nicht dasselbe sind
- Eine REST-API (Philips Hue) ansprechen und mit Flask einen eigenen kleinen Server bauen
- Warum ein Server mit `host="0.0.0.0"` laufen muss, damit andere Geräte ihn erreichen
- Zugangsdaten aus dem Code in eine eigene Konfigurationsdatei auslagern
