# 🤖 Gemini AI Prompt Templates

Nutze diese Prompts mit Gemini API, um personalisierte Trainingspläne & Tipps zu bekommen:

---

## 1️⃣ **Wöchentliche Bewertung & Training Plan**

```
Ich habe einen detaillierten Garmin-Trainingsbericht für die letzte Woche.
Hier sind meine Daten:

[KOPIERE HIER DEN GARMIN JSON REPORT]

Bitte analysiere folgende Punkte:
1. Wie ist mein Trainingsstatus insgesamt? (Berücksichtige Training Load, ACWR, HRV)
2. Habe ich genug trainiert oder sollte ich mehr/weniger machen?
3. Wie waren meine Schlafqualität & deren Auswirkung auf die Erholung?
4. Basierend auf meinen Metriken: Welche Art von Training (Ausdauer, Kraft, Intervall) sollte ich nächste Woche machen?
5. Gib mir einen konkreten 7-Tage Trainingsplan für nächste Woche
```

---

## 2️⃣ **Schlaf-Optimierung**

```
Hier ist mein Garmin Schlafreport der letzten Woche:

Schlaf-Daten:
- Durchschnittliche Schlafdauer: [total_sleep_hours]
- Tiefschlaf: [deep_sleep_hours] Stunden
- REM-Schlaf: [rem_sleep_hours] Stunden
- Schlafqualität Score: [sleep_quality]
- Durchschnittliche Schlafeffizienz: [sleep_efficiency_percent]%

Trainings-Daten:
- Wöchentliche Trainingsintensität: [training_status]
- Trainingslast (akut): [daily_training_load_acute]

Gib mir konkrete Tipps zur Schlafverbesserung, um:
- Mehr Tiefschlaf zu bekommen
- Bessere Schlafeffizienz zu erreichen
- Schlaf und Training zu optimieren
```

---

## 3️⃣ **Performance Analytics**

```
Meine physiologischen Daten:
- VO2 Max: [vo2Max]
- Laktatschwelle HR: [lactateThresholdHeartRate]
- HRV Wochenschaftlich durchschnitt: [hrv_status_weeklyAvg]
- Ruhepuls (7-Tage durchschnitt): [resting_heartRate]

Training der letzten Woche:
- Gesamt Trainingsminuten: [total_duration_minutes]
- Durchschnittlicher Puls während Training: [average_heart_rate]
- Gesamte Trainingseffekt: [training_effect]
- Aerobe Trainingseffekt: [aerobic_effect]
- Anaerobe Trainingseffekt: [anaerobic_effect]

Analysiere:
1. Wo stehen meine aerobe und anaerobe Fitness?
2. Welche energetische Systeme sollte ich schwerpunktmäßig trainieren?
3. Sollte ich meine Trainingsintensität anpassen?
```

---

## 4️⃣ **Stress & Erholung**

```
Meine Stress & Recovery Metriken (7-Tage):

Body Battery:
- Höchster Wert: [highest_bodyBattery]
- Niedrigster Wert: [lowest_bodyBattery]

Stress:
- Durchschnittlicher Stress Level: [average_stress]
- Stress Prozentanteil: [percentage_stress]

HRV Status: [hrv_status_status]
Trainingslast ACWR: [acwrPercent]% - [acwrStatus]

Fragen:
1. Bin ich übertrainiert oder untertrainiert?
2. Was kann ich konkret tun für bessere Erholung?
3. Sollte ich aktive Erholung (leichte Aktivität) oder kompletten Rest machen?
```

---

## 5️⃣ **Aktivitäts-Analyse**

```
Meine Trainingsaktivitäten letzte Woche:

[KOPIERE HIER DEN "activities" SECTION AUS DEM JSON]

Analysiere:
1. Wie effektiv war mein Training insgesamt?
2. Welche Aktivitätstypen waren am effektivsten für meine Ziele?
3. Sollte ich die Häufigkeit, Dauer oder Intensität anpassen?
4. Gib mir spezifische Empfehlungen für nächste Woche
```

---

## 🎯 **Ganzheitlicher Fitness Report**

```
Hier ist mein kompletter Garmin-Report. Erstelle mir einen umfassenden Fitnessbericht:

[KOPIERE HIER DEN KOMPLETTEN JSON REPORT]

Bitte erstelle folgendes:

## 1. Fitness-Status Zusammenfassung
- Gesamtbewertung meines Trainingszustands
- Stärken und Schwächen

## 2. Wochenbewertung
- Was war gut? Was könnte besser sein?

## 3. Schlaf & Recovery
- Wie ist meine Erholung?
- Schlafqualität vs. Trainingsintensität Korrelation

## 4. Trainingsprogramm für nächste Woche
- Mo-So konkrete Workouts mit:
  - Aktivitätstyp
  - Empfohlene Dauer
  - Empfohlene Intensität
  - Ziele (Ausdauer/Kraft/Recovery/etc.)

## 5. Top 5 Verbesserungspunkte
- Konkrete, umsetzbare Tipps

## 6. Motivierende Zusammenfassung
```

---

## 📋 **Wie man den JSON Report mit Gemini teilt:**

1. **Öffne den generierten JSON** (`garmin_report_full.json`)
2. **Kopiere den gesamten Inhalt**
3. **Füge es in deine Gemini Anfrage ein**
4. **Nutze einen der obigen Templates**
5. **Lasse dich von Gemini analysieren & beraten**

---

## 💡 **Tipps für beste Ergebnisse:**

✅ Sei konsistent - führe diesen Report jede Woche durch
✅ Gib Gemini auch deine Ziele (z.B. "ich möchte schneller werden" oder "Gewicht abnehmen")
✅ Teile Gemini auch externe Faktoren (Stress bei der Arbeit, Krankheit, etc.)
✅ Nutze Gemini's Ratschläge und track die Verbesserungen in den folgenden Reports
✅ Passe deinen Trainingsplan kontinuierlich an basierend auf Gemini's Empfehlungen

---

**Viel Erfolg beim KI-gestützten Training! 🏋️‍♂️🧠**
