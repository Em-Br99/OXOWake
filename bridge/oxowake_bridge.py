# OXOWake - Flask-Bridge (mit Sonnenaufgang)
# Dolmetscher zwischen OXOCard und Philips Hue + Dimm-Logik.
#
# Vorbereitung:  pip install -r requirements.txt
# Start:         python oxowake_bridge.py

from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# --- Konfiguration -------------------------------------------------
# Adresse, Hue-Schluessel und Lampen stehen in config.py (wird nicht hochgeladen).
# Vorlage: config.example.py nach config.py kopieren und ausfuellen.
try:
    from config import HUE_BRIDGE_IP, HUE_USER, LIGHT_IDS
except ImportError:
    raise SystemExit("config.py fehlt: config.example.py kopieren und ausfuellen.")

# Dauer des Sonnenaufgangs in Sekunden.
# Zum TESTEN kurz lassen (30 s). Fuer echt auf 1800 (= 30 Min) setzen.
SUNRISE_DURATION_S = 30
SUNRISE_STEPS      = 15
# -------------------------------------------------------------------

_stop_flag = False   # interner Schalter, um den Sonnenaufgang abzubrechen


def set_light(light_id, body):
    """Ein PUT an eine Hue-Lampe - genau das, was NanoPy nicht kann."""
    url = f"http://{HUE_BRIDGE_IP}/api/{HUE_USER}/lights/{light_id}/state"
    return requests.put(url, json=body, timeout=3)


def sunrise_run():
    """Dimmt die Lampen langsam von dunkel auf hell (laeuft im Hintergrund)."""
    global _stop_flag
    for i in range(SUNRISE_STEPS + 1):
        if _stop_flag:
            return
        bri = max(1, int(254 * i / SUNRISE_STEPS))   # Hue-Helligkeit 1..254
        for lid in LIGHT_IDS:
            try:
                set_light(lid, {"on": True, "bri": bri})
            except Exception:
                pass
        time.sleep(SUNRISE_DURATION_S / SUNRISE_STEPS)


@app.route("/ping")
def ping():
    return jsonify(status="ok"), 200


@app.route("/light/on", methods=["GET", "POST"])
def light_on():
    try:
        for lid in LIGHT_IDS:
            set_light(lid, {"on": True, "bri": 254})
        return jsonify(status="on"), 200
    except Exception as e:
        return jsonify(status="error", detail=str(e)), 502


@app.route("/light/off", methods=["GET", "POST"])
def light_off():
    try:
        for lid in LIGHT_IDS:
            set_light(lid, {"on": False})
        return jsonify(status="off"), 200
    except Exception as e:
        return jsonify(status="error", detail=str(e)), 502


@app.route("/sunrise/start", methods=["GET", "POST"])
def sunrise_start():
    global _stop_flag
    _stop_flag = False
    threading.Thread(target=sunrise_run).start()
    return jsonify(status="sunrise gestartet"), 200


@app.route("/sunrise/stop", methods=["GET", "POST"])
def sunrise_stop():
    global _stop_flag
    _stop_flag = True
    for lid in LIGHT_IDS:
        try:
            set_light(lid, {"on": False})
        except Exception:
            pass
    return jsonify(status="gestoppt"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)