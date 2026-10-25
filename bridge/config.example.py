# Vorlage fuer die Konfiguration der Flask-Bridge.
# Diese Datei nach config.py kopieren und die Werte eintragen.
# config.py steht in der .gitignore und wird nie hochgeladen.

HUE_BRIDGE_IP = "192.168.x.x"          # IP-Adresse der Hue Bridge im eigenen Netz
HUE_USER      = "DEIN-HUE-SCHLUESSEL"  # mit get_hue_key.py erzeugen
LIGHT_IDS     = [1, 2, 3]              # IDs der Lampen, die mitmachen sollen
