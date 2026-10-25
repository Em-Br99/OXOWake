# Architektur und Netzwerk

## Komponenten

| Komponente | Aufgabe | Adresse |
|---|---|---|
| OXOCard Connect | Mikrocontroller, programmiert in NanoPy. Zeigt Uhr und Sonnenaufgang, gibt den Weckton aus. | im WLAN |
| Flask-Bridge | Python-Server auf einem PC im selben Netz. Übersetzt die Anfragen der OXOCard in Hue-API-Aufrufe. | `192.168.x.x:5000` |
| Philips Hue Bridge | Steuert die Lampen | `192.168.x.x` |
| Hue-Lampen | Sonnenaufgang-Simulation | Light-IDs 1, 2, 3 |
| NTC-Sensor (10 kΩ) | Raumtemperatur (Versuch, analog an der OXOCard) | |

## Request-Fluss

```
[ OXOCard Connect ]  NanoPy, WLAN
        |
        |  HTTP GET  /sunrise/start, /sunrise/stop
        v
[ Flask-Bridge ]     Python / Flask, Port 5000
        |
        |  HTTP PUT  /api/<schluessel>/lights/<id>/state
        v
[ Hue Bridge ]
        |
        v
[ Lampen 1 bis 3 ]   werden schrittweise heller
```

## Warum eine Bridge dazwischen?

Die OXOCard kann nur einfache GET- und POST-Anfragen senden. Die Hue-API verlangt zum Schalten der Lampen aber PUT-Anfragen mit JSON. Die Flask-Bridge nimmt deshalb einfache Anfragen der OXOCard entgegen und macht daraus die richtigen Hue-Aufrufe. Ausserdem liegen der Hue-Schlüssel und die Dimm-Logik so nur auf dem PC und nicht auf der Karte.

## Ablauf am Morgen

1. Die OXOCard zeigt im Normalbetrieb eine analoge Uhr mit Weckzeit-Zeiger.
2. Eine eingestellte Zeit vor dem Wecken ruft sie `/sunrise/start` auf. Die Bridge dimmt die Lampen schrittweise von dunkel auf hell, und die Karte zeigt eine Sonnenaufgang-Animation.
3. Zur Weckzeit piepst der Piezo, bis der Joystick gedrückt wird.
4. Danach ruft die Karte `/sunrise/stop` auf und die Lampen gehen aus.
