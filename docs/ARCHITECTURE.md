# AeroSoul – Systemarchitektur v0.1

Stand: 2026-11-05 · Grundlage: Entscheidungen in CONCEPTS.md (Headset H3, destilliertes Wasser, keine Zusätze)

## 1. Systemübersicht

```
┌──────────────── BASIS (Nachttisch) ────────────────┐            ┌──────── HEADSET ────────┐
│ USB-C 5 V ─► Schutz ─► 3,3-V-LDO ─► ESP32-C3        │            │                         │
│                 │                    │  │  │        │  Strang    │  Boom (biegbar)         │
│                 ├─► TMC2209 ─► Schrittmotor-Pumpe ──┼─ Wasser ──►│  └─ Sprühkopf           │
│                 │                    │  │           │  (PE 0,5)  │      ├─ Dosierkammer    │
│                 └─► Mesh-Treiber (MOSFET + L) ──────┼─ Piezo ───►│      ├─ Mesh-Scheibe    │
│                                      │              │  (TRRS)    │      └─ NTC-Atemsensor  │
│                      NTC-Messung ◄───┘──────────────┼─ NTC ◄─────│                         │
│ Tank 200 mL ─► Silikon-Pumpenschlauch               │            │  Kopfband (über Scheitel)│
└─────────────────────────────────────────────────────┘            └─────────────────────────┘
```

Das Headset enthält **keine Platine**. Nur Piezo-Scheibe und Thermistor hängen an vier Adern.
Die gesamte Elektronik sitzt in der Basis.

## 2. Funktionsprinzip

1. Der NTC im Boom misst den Luftstrom: Ausatemluft ist warm (~34 °C), Einatemluft kühl. Daraus ergeben sich Phase und Mundatmung.
2. Der Mesh-Treiber läuft nur während der Einatmung (~40 % der Zeit), bei ~108 kHz.
3. **Die Pumpe fördert nach Verbrauch, nicht kontinuierlich.** Die Firmware summiert die Sprühzeit der Scheibe und multipliziert sie mit der kalibrierten Zerstäubungsrate (µL/s). Genau diese Menge pumpt sie nach. Weil jeder Schritt ein festes Volumen bewegt (~0,05 mL/U), dosiert der Schrittmotor exakt.
4. Die Dosierkammer (~20 µL) wird bewusst knapp unter voll gehalten. Eine überfüllte Kammer tropft, eine leicht unterfüllte sprüht nur etwas weniger.
5. **Korrektur über den Mesh-Strom:** Eine trockene Scheibe hat eine andere Impedanz als eine benetzte. Bei Anzeichen von Trockenheit pumpt die Firmware zusätzlich nach. Bleibt die Scheibe trotz Nachpumpen trocken, meldet sie „Tank leer“ oder „Leitung unterbrochen“.
6. Wird einige Minuten keine Mundatmung erkannt, stoppt die Pumpe und zieht einige µL zurück, damit nichts nachsickert.
7. **Intensität stufenlos per Drehknopf:** Ein Potentiometer ohne Rastung an einem ADC-Eingang skaliert die Sprühmenge pro Atemzug kontinuierlich (z. B. 20–100 %). Die Pumpe folgt automatisch über Punkt 3. Ein Potentiometer statt Drehgeber, weil die absolute Stellung auch im Dunkeln fühlbar bleibt und nach Stromausfall erhalten ist.
8. Morgens dreht die Pumpe rückwärts und holt das Wasser aus der Leitung zurück in den Tank, danach ist die Leitung trocken.

## 3. Leistungsbudget

| Verbraucher | Leistung |
|---|---|
| Mesh-Treiber, aktiv | 1,5–3 W (bei 40 % Einschaltdauer: ~1 W Mittel) |
| Pumpe mit TMC2209 | ~0,5 W |
| ESP32-C3 (BLE meist aus) | 0,1–0,3 W |
| **Summe Mittel** | **~2 W**, Spitze ~4 W |

→ Ein USB-C-Netzteil mit 5 V / 2 A genügt. USB Power Delivery wird nicht benötigt.

## 4. Schnittstelle Basis ↔ Headset

| Ader | Funktion | Signal |
|---|---|---|
| 1 / 2 | Piezo + / − | ~108 kHz, bis ~60 Vss, verdrillt |
| 3 / 4 | NTC + / − | DC, < 3,3 V, verdrillt |
| – | Wasser | PE-Mikroschlauch ID 0,5 mm, parallel im Mantel |

Stecker: 3,5-mm-TRRS (4 Kontakte, billig, robust). Kurzschluss beim Einstecken wird über die Stromüberwachung erkannt; Treiber startet erst nach stabilem Kontakt.

## 5. Dimensionierung Mesh-Treiber

Resonanz zwischen Spule und Piezo-Kapazität bei 108 kHz: L = 1 / ((2πf)² · C)

Scheibengröße: Ziel 10–13 mm statt der üblichen 16 mm, für einen kleineren, leichteren Sprühkopf. Ob eine kleine Scheibe die nötige Rate von ~10 µL/s während der Einatmung schafft, wird im Labortest gemessen; die Sprührate skaliert grob mit der aktiven Mesh-Fläche.

| C der Scheibe | L |
|---|---|
| 1,5 nF | 1,45 mH |
| 2,5 nF | 0,87 mH |
| 3,5 nF | 0,62 mH |

C wird an der realen Scheibe gemessen. Der MOSFET braucht ≥ 100 V Sperrspannung, weil die Spannungsspitzen bei Resonanz den Wert von 5 V vielfach übersteigen. Die Firmware wobbelt die Frequenz (100–115 kHz) und regelt auf maximalen Strom, um Exemplarstreuung und Temperaturdrift auszugleichen.

## 6. Offene Punkte

1. Mesh-Scheibe mit grober Lochung (Ziel ~25 µm Tropfen): Lieferant offen, ggf. Sonderanfertigung
2. Ob das 108-kHz-Signal über 1,8 m Kabel EMV-konform bleibt: abgeschirmtes oder verdrilltes Paar, Messung nötig
3. TMC2209 läuft bei 5 V nahe seiner Mindestspannung (4,75 V). Spannungseinbruch am Kabel prüfen
4. Ob der Mesh-Strom neben „trocken“ und „benetzt“ auch „überfüllt“ erkennen lässt. Falls nicht, braucht die Dosierkammer einen eigenen Füllstandssensor, und damit doch Elektronik im Headset.
5. Kopfband: Rückenschläfer liegen auf dem Hinterkopf, deshalb Band über den Scheitel, nichts am Hinterkopf
