# 🚀 Garmin Report Email - Verbesserungen

## 📊 Was wurde aktualisiert?

### 1. **Schlafdaten (NEU)** 😴
- **Gesamtschlafdauer** (in Stunden)
- **Schlafphasen:**
  - Tiefschlaf (Deep Sleep)
  - REM-Schlaf (für Gehirnaktivität & Erholung)
  - Leichtschlaf (Light Sleep)
  - Wachphasen
- **Schlafqualität Score** (0-100)
- **Schlafeffizienz %** (Wie viel % der Zeit wirklich schlief)
- **Durchschnittliche Atemfrequenz** während des Schlafs
- **SpO2 Wert** (Sauerstoffsättigung) während des Schlafs

### 2. **Erweiterte 7-Tage-Metriken** 📈
Die vorher kommentierten Daten sind nun **aktiviert und verbessert**:
- Tägliche Schritte
- Gehstrecke in km
- Kalorienverbrennung (gesamt, aktiv, BMR)
- Herzfrequenz (Min, Max, Ruhepuls, durchschnittlich pro Tag)
- Stressmetriken (durchschnittlicher Stress, Stress %)
- Body Battery (höchster & niedrigster Wert pro Tag)

### 3. **Bessere Report-Struktur** 🗂️
Der JSON-Report ist nun hierarchisch organisiert für bessere AI-Analyse:
```
{
  "week": "...",
  "userProfile": { vo2max, Laktatschwelle, ... },
  "activities": {
    "summary": { Gesamtzahlen },
    "details": [ aktivitätsdetails ]
  },
  "sleep": { Schlafdaten },
  "hrv": { Herzratenvariabilität },
  "trainingLoad": { Trainingslast & Status },
  "sevenDaySummary": { Wochen-Metriken }
}
```

### 4. **HelperClass erweitert** 🛠️
Neue Utility-Funktionen hinzugefügt:
- `format_report_summary()` - Lesbare Zusammenfassung für Email
- `calculate_training_load_category()` - Kategorisiert Trainingsbelastung
- `calculate_recovery_status()` - Berechnet Gesamterholungsstatus basierend auf HRV, Ruhepuls & Stress

### 5. **Bessere Email** 📧
- Formatierter Report mit Zusammenfassung
- Klare Übersicht der Trainings- & Schlafmetriken
- Hinweis auf JSON-Anhang für Gemini-Analyse
- Motivierende Nachrichten

## 💡 Wie nutzt du das mit Gemini?

Der JSON-Report bietet Gemini folgende Informationen:

### **Trainingspläne**
- Künftige Trainings basierend auf aktuellem Training Load Status
- Empfohlene Trainingsintensität (Gemini sieht ACWR %, acuteTrainingLoad)
- Periodisierung basierend auf aerobem vs. anaerobem Load

### **Schlaf & Recovery**
- Schlafqualität direkt beeinflussen durch vorherige Trainingstage
- REM vs. Deep Sleep Verteilung
- Empfehlungen zur Schlafdauer basierend auf Trainingsload

### **Physiologische Adaptationen**
- VO2Max Entwicklung
- Laktatschwelle als Performance Indicator
- HRV als Erholungsindikator

### **Stress Management**
- Ruhepuls Trends
- Durchschnittlicher Stress vs. Trainingsload Korrelation
- Body Battery als mentale Erholung

## 📝 Beispiel-Prompt für Gemini:

```
"Analysiere meinen Garmin-Trainingsbericht und gib mir:
1. Eine Bewertung meines Trainings-Recovery-Status (basierend auf HRV, Ruhepuls, Stress)
2. Empfehlungen für nächste Woche (intensives Training vs. Erholung)
3. Tipps zur Schlafoptimierung basierend auf meinen Schlafphasen
4. Welche körperliche Adaption ich machen sollte (VO2Max, Ausdauer, Kraft)
5. Motivierende Zusammenfassung meiner Leistung"
```

## 🔧 Installation & Ausführung

```bash
# Dependencies installieren
pip install -r requirements.txt

# Skript ausführen
python garmin_report_email.py
```

Die Daten werden:
1. ✅ Lokal als `garmin_report_full.json` gespeichert
2. ✅ Per Email mit Zusammenfassung versendet
3. ✅ Im Terminal schön formatiert angezeigt

---

**Viel Erfolg beim Training! 💪🏃‍♂️**
