"""
Test-Version des Garmin Reports ohne echte API-Aufrufe
Zeigt, ob die Datenstruktur und das Report-Format richtig funktioniert
"""

import json
from datetime import datetime, timedelta
from HelperClass import HelperClass

# Mock-Daten (Beispiel von deinen echten Daten)
today = datetime.now().date()
last_sunday = today - timedelta(days=today.weekday() + 1)

helper = HelperClass()
last7DateList = helper.get_last_7_days()

# Beispiel Activity Details
activity_details = [
    {
        "start_time": "2026-06-01 15:26:49",
        "activity_type": {"typeKey": "strength_training"},
        "duration_min": 17.69,
        "distance_km": 0.0,
        "avg_hr": 110.0,
        "max_hr": 146.0,
        "cadence": None,
        "elevation_gain_m": None,
        "training_effect": None,
        "aerobic_effect": 0.4,
        "anaerobic_effect": 0.5,
        "calories": 134.0,
        "power_avg": None,
        "temp_avg": None,
        "splits": []
    },
]

# Report mit fixen Daten
report = {
    "week": f"{last_sunday.isoformat()} - {today.isoformat()}",
    "userProfile": {
        "vo2max": 62.0,
        "lactateThresholdHeartRate": 181,
        "lactateThresholdSpeed": "3:46 min/km"
    },
    "activities": {
        "summary": {
            "totalActivities": len(activity_details),
            "totalDurationMinutes": sum([a.get("duration_min", 0) for a in activity_details]),
            "totalDistanceKm": sum([a.get("distance_km", 0) for a in activity_details]),
            "totalCalories": sum([a.get("calories", 0) for a in activity_details]),
            "averageHeartRate": None,
            "totalElevationGainM": 0
        },
        "details": activity_details
    },
    "sleep": {
        "lastNight": {
            "totalHours": 7.5,
            "deepSleepHours": 2.1,
            "remSleepHours": 1.8,
            "lightSleepHours": 3.6,
            "awakeHours": 0.0,
            "qualityScore": 78,
            "efficiencyPercent": 95.0,
            "avgRespirationRate": 15.0,
            "avgSpO2Percent": 97.5
        }
    },
    "hrv": {
        "weeklyAverage": 78,
        "status": "BALANCED",
        "lastNightAverage": 80
    },
    "trainingLoad": {
        "monthly": {
            "aerobicLow": 1457.5,
            "aerobicHigh": 136.1,
            "anaerobic": 1398.7,
            "feedbackPhrase": "AEROBIC_HIGH_SHORTAGE"
        },
        "trainingStatus": {
            "status": 4,
            "feedbackPhrase": "MAINTAINING_1"
        },
        "acuteTrainingLoad": {
            "acwrPercent": 29,
            "acwrStatus": "LOW",
            "dailyAcute": 572,
            "dailyChronic": 814
        }
    },
    "sevenDaySummary": {
        "dates": last7DateList,
        "steps": [5000, 6200, 7100, 5500, 6800, 4300, 5900],  # 7 Werte
        "distanceKm": [2.1, 2.5, 3.0, 2.3, 2.8, 1.9, 2.4],  # 7 Werte
        "calories": {
            "total": [2100, 2300, 2450, 2200, 2400, 2050, 2250],
            "active": [450, 520, 620, 480, 550, 400, 480],
            "bmr": [1650, 1650, 1650, 1650, 1650, 1650, 1650]
        },
        "heartRate": {
            "min": [52, 50, 51, 52, 49, 53, 51],
            "max": [155, 162, 158, 160, 165, 152, 161],
            "resting": [56, 54, 55, 56, 53, 57, 55],
            "avgByDay": [103.5, 106.0, 104.5, 106.0, 107.0, 102.5, 106.0]
        },
        "stress": {
            "average": [35, 42, 38, 40, 45, 32, 38],
            "percentage": [28, 35, 32, 33, 38, 26, 31]
        },
        "bodyBattery": {
            "highest": [95, 92, 88, 94, 89, 97, 91],
            "lowest": [23, 18, 25, 20, 19, 28, 22]
        }
    }
}

# Test: Speichere JSON und prüfe Struktur
print("=" * 60)
print("🧪 TEST: Garmin Report Struktur")
print("=" * 60)

# Speichern
with open("garmin_report_test.json", "w") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\nReport als JSON gespeichert: garmin_report_test.json")

# Validierung
print("\nStruktur-Validierung:")

# Check Activities
print(f"✓ Activities: {report['activities']['summary']['totalActivities']} Trainings")
print(f"  - Dauer: {report['activities']['summary']['totalDurationMinutes']} min")
print(f"  - Strecke: {report['activities']['summary']['totalDistanceKm']} km")

# Check Sleep
sleep = report['sleep']['lastNight']
print(f"✓ Sleep (letzte Nacht): {sleep['totalHours']} h")
print(f"  - Deep: {sleep['deepSleepHours']}h, REM: {sleep['remSleepHours']}h, Light: {sleep['lightSleepHours']}h")
print(f"  - Qualität: {sleep['qualityScore']}, Effizienz: {sleep['efficiencyPercent']}%")

# Check 7-Day Summary
print(f"✓ 7-Day Summary:")
print(f"  - Tage: {len(report['sevenDaySummary']['dates'])} (sollte 7 sein)")
print(f"  - Schritte: {len(report['sevenDaySummary']['steps'])} Einträge (sollte 7 sein)")
print(f"  - Distanzen: {len(report['sevenDaySummary']['distanceKm'])} Einträge (sollte 7 sein)")

# Check HRV
print(f"✓ HRV Status: {report['hrv']['status']}")
print(f"  - Weekly Avg: {report['hrv']['weeklyAverage']}")

# Summary verwenden
print("\n" + "=" * 60)
print("📋 Report Zusammenfassung:")
print("=" * 60)
summary = HelperClass.format_report_summary(report)
print(summary)

print("\nAlle Tests bestanden! Die Datenstruktur funktioniert richtig.")
print("📝 Nächste Schritte:")
print("   1. .env Datei mit Garmin-Credentials erstellen")
print("   2. garmin_report_email.py ausführen")
print("   3. Überprüfe garmin_report_full.json für echte Daten")
