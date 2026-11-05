# AeroSoul – Konzeptstudie (Phase 0)

Stand: 2026-11-05 · Erstellt ohne Kenntnis bestehender Prototypen oder CADs.

## Problemstellung (vom Owner)

- Nutzer: Mundatmung in der Nacht nach Nasen-OP, bei chronischer Nasenverstopfung, Mundtrockenheit
- Harte Grenze: **nichts berührt das Gesicht**; ein peripheres Gerät am Nachttisch ist erlaubt
- Positionierung: Wellness/Komfort, keine Heilversprechen
- Angenommene Defaults (bitte bestätigen): 8 h Laufzeit, ≤ 30 dB(A) in 1 m, Netzbetrieb am Bett zulässig

## Physikalische Ausgangslage

| Größe | Wert |
|---|---|
| Wasserdampf in Raumluft, 22 °C / 40 % rF | 7,7 g/m³ |
| Wasserdampf in Lungenluft, 37 °C gesättigt | 43,8 g/m³ |
| Defizit, das Mund und Rachen pro m³ Luft decken müssen | ~36 g/m³ |
| Atemluft pro Nacht (≈ 7 L/min, 8 h) | ~3,4 m³ |
| Wasser, das der Mundraum pro Nacht abgibt | ~120 g |

**Kernerkenntnis:** Das Defizit ist so groß, weil Raumluft kalt ist. Nur die relative Feuchte anzuheben bringt wenig.
Der Hebel ist **warme und zugleich feuchte Einatemluft**.

## Konzepte

### A – Raumbefeuchter (Referenz)
Schlafzimmer (30 m³) von 40 % auf 60 % rF bringen.
- Deckt nur **~11 %** des Defizits ab und verbraucht ~0,6 L Wasser pro Nacht
- Ist bereits Massenware, also keine Differenzierung
- **Bewertung: schwach.** Dient nur als Vergleichsbasis.

### B – Gerichteter Warmluftstrahl vom Nachttisch, atemsynchron
Eine Düse am Bett erkennt Kopfposition und Einatmung (ToF/Radar) und bläst nur beim Einatmen warme, feuchte Luft (31 °C, 90 % rF, 2 L/s) Richtung Mund.
- ~0,5 L Wasser pro Nacht, ~50 W im Mittel
- Unbekannt ist, wie viel des Strahls tatsächlich eingeatmet wird. Wahrscheinlich nur 10–30 %, weil der Rest sich mit Raumluft vermischt.
- Kopfdrehungen im Schlaf machen eine Nachführung nötig, die laut und störanfällig ist
- **Bewertung: mittel.** Technisch reizvoll, aber die Wirksamkeit ist das Hauptrisiko.

### C – Halboffener Kopf-Baldachin („Mikroklima-Zone")
Eine Haube oder ein Dach über dem Kopfende des Kissens, das das Gesicht nicht berührt und zum Körper hin offen ist. Ein Basisgerät am Nachttisch speist warme, feuchte Luft (28 °C, 85 % rF) mit geringer Strömung ein.
- Mindest-Spülstrom gegen CO₂-Anreicherung (< 0,5 %): **~0,7 L/s**
- Einatemluft hat ~23 g/m³ und deckt damit **~43 %** des Defizits, also etwa das Vierfache von A
- ~0,3 L Wasser pro Nacht, **~30 W** Leistung bei Netzbetrieb
- Pflichtfunktionen: NDIR-CO₂-Sensor mit Abschaltung bzw. Vollspülung, fail-safe Lüfter, Verdampfung durch Kochen statt Ultraschall (keine Keim-Aerosole, Legionellen-Schutz)
- Risiken: Akzeptanz (Enge, Optik), Kondensat an der Haubeninnenseite, Bettwäsche
- **Bewertung: stärkstes Konzept physikalisch.** Nächster Schritt ist ein Kondensat- und Strömungsmodell.

### D – Am Körper getragen (Hals/Brust), ohne Gesichtskontakt
Dieselbe Funktion wie B, aber mit Akku am Körper.
- 8 h × ~50 W ≈ **400 Wh**, das sind ~1,6 kg Akku plus Wassertank
- **Bewertung: physikalisch nicht machbar.** Ohne Abdichtung am Mund lässt sich die Feuchte der Ausatemluft nicht zurückgewinnen (Wärme-/Feuchtetauscher). Dadurch fehlt jede Effizienz, die ein Akkubetrieb bräuchte.

## Vergleich

| | Deckung Defizit | Wasser/Nacht | Leistung | Hauptrisiko |
|---|---|---|---|---|
| A Raum | ~11 % | ~0,6 L | 20–30 W | Wirkung zu gering |
| B Strahl | unklar (10–30 % Einfang) | ~0,5 L | ~50 W | Wirksamkeit, Nachführung |
| **C Baldachin** | **~43 %** | **~0,3 L** | **~30 W** | Akzeptanz, Kondensat |
| D Wearable | – | – | ~400 Wh Akku | nicht machbar |

## Owner-Entscheidung (2026-11-05): Headset mit Boom-Mundstück

Die Konzepte A–D sind verworfen. Weiterentwickelt wird ein Headset, bei dem das Mundstück wie ein Boom-Mikrofon
wenige Zentimeter vor dem Mund sitzt, ohne Gesichtskontakt. Durch die Nähe zum Mund steigt der Einfang stark,
deshalb sinkt der Energiebedarf um eine Größenordnung gegenüber B und D.

### H1 – Warmfeuchte Luft, über Schlauch vom Nachttisch versorgt
Basisgerät mit Tank, Heizung und Netzteil am Nachttisch. Ein dünner beheizter Schlauch führt zum Headset, das nur Boom, Düse und Sensor trägt.
- Zuluft 30 °C / 90 % rF, atemsynchron → deckt ~54 % des Defizits ab
- 70–110 g Wasser pro Nacht und **7–12 W** bei 80–50 % Einfang, Netzbetrieb
- Headset bleibt leicht (Ziel < 80 g), weil Akku und Tank entfallen
- Risiken: Schlauch verheddert sich, Kondensat im Schlauch (deshalb beheizt), Geräusch des Gebläses

### H2 – Kaltnebel, kabellos
Piezo-Mesh-Zerstäuber im Boom, der Wasser als feinen Nebel auf die Mundschleimhaut bringt. Tank und Akku sitzen am Headset.
- 120–130 g Wasser pro Nacht (Ablagerungsgrad 30–50 % angenommen), **2–5 W** → **~40 Wh Akku (~160 g)** zusätzlich zum Tank
- Hygiene: Ein Zerstäuber bringt Keime direkt in die Atemwege. Nur mit versiegelten sterilen Kartuschen vertretbar, was zugleich ein Verbrauchsmaterial-Geschäftsmodell ergibt.
- Inhaliertes Wasser-Aerosol rückt das Produkt regulatorisch Richtung Vernebler und gefährdet damit die Wellness-Einstufung
- Kalte Nachtluft kühlt zusätzlich, nasses Kissen ist möglich

### H2 – Lösung des Depositionsproblems
Die Tropfengröße bestimmt, wo der Nebel landet:
- < 1 µm: wird wieder ausgeatmet
- 1–5 µm: gelangt in die Lunge. Das ist der Bereich, den medizinische Mesh-Vernebler bewusst erzeugen, und den wir **vermeiden** müssen.
- **15–40 µm: prallt beim Einatmen auf Zunge, Gaumen und Rachen.** Das ist das Zielfenster.

Ein Boom im Abstand von 2–4 cm macht das Zielfenster nutzbar:
- Flugzeit ~30 ms bei ~1 m/s. Ein 30-µm-Tropfen braucht bei 40 % rF ~1 s zum Verdunsten (d²-Gesetz), sinkt mit ~2,7 cm/s und kommt deshalb praktisch unverändert an.
- Abgabe nur in der Einatemphase und nur bei offenem Mund. Der Einatemstrom trägt die Tropfen in den Mundraum.
- Daraus ergeben sich die Anforderungen an den Zerstäuber: grober Mesh (Lochgröße für ~25 µm MMAD), Massenanteil < 10 µm unter 5 %
- Validierung: Tropfenspektrum per Laserbeugung, Deposition in einem gedruckten Mund-Rachen-Modell (z. B. Alberta Idealized Throat), CFD mit Partikeltracking (OpenFOAM, CPU)

### H3 – Hybrid: Flüssigwasser über Kapillare, Zerstäubung am Boom
Owner-Hinweis: Vom Nachttisch zum Kopf sind realistisch ≥ 1,5 m.
- Nebel durch 1,5 m Schlauch: Ein 25-µm-Tropfen sinkt in ~1,5 s Transitzeit ~4 cm, im Schlauch von ~4 mm Durchmesser schlägt sich also fast alles nieder. **Das geht nicht.**
- Warmfeuchte Luft (H1) durch 1,5 m: Sie kondensiert ohne Schlauchheizung. Das geht nur mit Zusatzaufwand.
- **Flüssiges Wasser durch 1,5 m: unproblematisch.** Benötigt werden nur ~15 g/h ≈ 4 µL/s, eine Kapillare mit ~0,5 mm Innendurchmesser hat ~0,3 mL Totvolumen.
- Aufbau: Am Nachttisch sitzen sterile Kartusche, Mikropumpe, Netzteil und Elektronik. Kapillare und Kabel laufen als ein Strang zum Headset. Am Kopf bleiben nur Grob-Mesh-Zerstäuber, Atemsensor und Boom, das Ziel ist < 50 g.
- Hygiene: Kapillare als Einwegteil zusammen mit der Kartusche, Leerspülen nach Gebrauch, kein stehendes Wasser im Strang

### Für beide gilt
- **Seitenschläfer:** Ein Boom auf der Kissenseite wird gegen das Gesicht gedrückt und verletzt dann die Kein-Kontakt-Regel. Mechanik muss wegklappen oder beidseitig umsteckbar sein. Dieser Punkt ist der wahrscheinlichste K.-o.-Punkt.
- Die Atemerkennung (Thermistor oder Drucksensor im Boom) steuert die Abgabe nur beim Einatmen

## Empfehlung

Gesetzt ist ein Headset mit Boom (Owner-Entscheidung). Empfohlen wird **H3**: Flüssigwasser über eine Kapillare, Zerstäubung im Zielfenster von 15–40 µm direkt am Boom. Damit ist das Kopfgewicht am geringsten, es braucht weder Akku noch Tank am Kopf, und kein Aerosol muss transportiert werden. H2 (voll kabellos) bleibt die Option für später.
Die Zahlen beruhen auf Ruhe-Atemwerten und Idealmischung. Validieren lassen sie sich nur mit
einer Messung von Temperatur und Feuchte am Mund und einem CO₂-Logger unter einer Attrappe.
