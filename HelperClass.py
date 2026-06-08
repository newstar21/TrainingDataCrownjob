from pyarrow import null
from datetime import datetime, timedelta

class HelperClass(object):
    @staticmethod
    def get_last_7_days():
        today = datetime.now().date()
        return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    
    @staticmethod
    def calculate_training_load_category(load_value):
        """Kategorisiert das Trainingsload Level"""
        if load_value is None:
            return "Unknown"
        if load_value < 2:
            return "Sehr niedrig"
        elif load_value < 4:
            return "Niedrig"
        elif load_value < 7:
            return "Moderat"
        elif load_value < 10:
            return "Hoch"
        else:
            return "Sehr hoch"
    
    @staticmethod
    def calculate_recovery_status(hrv_value, resting_hr, stress_level):
        """Berechnet den Gesamterholungsstatus"""
        scores = []
        
        if hrv_value:
            scores.append(1 if hrv_value > 50 else 0.5 if hrv_value > 30 else 0)
        
        if resting_hr:
            scores.append(1 if resting_hr < 60 else 0.7 if resting_hr < 70 else 0.4)
        
        if stress_level is not None:
            scores.append(1 if stress_level < 25 else 0.7 if stress_level < 50 else 0.4)
        
        if scores:
            return round(sum(scores) / len(scores) * 100, 1)
        return None
    
    @staticmethod
    def format_report_summary(report):
        """Erstellt eine lesbare Zusammenfassung des Reports für Gemini"""
        summary = []
        
        # Woche
        summary.append(f"Trainingswoche: {report.get('week', 'N/A')}\n")
        
        # Aktivitäten
        if "activities" in report:
            acts = report["activities"]
            summary.append(f"Trainingsaktivitaeten: {acts['summary']['totalActivities']} Trainingseinheiten")
            summary.append(f"   - Gesamtdauer: {acts['summary']['totalDurationMinutes']} Minuten")
            summary.append(f"   - Gesamtstrecke: {acts['summary']['totalDistanceKm']} km")
            summary.append(f"   - Kalorien verbrannt: {acts['summary']['totalCalories']} kcal\n")
        
        # Schlaf
        if "sleep" in report and report["sleep"]["lastNight"]["totalHours"]:
            sleep = report["sleep"]["lastNight"]
            summary.append(f"Schlaf (letzte Nacht): {sleep['totalHours']} Stunden")
            summary.append(f"   - Tiefschlaf: {sleep['deepSleepHours']} h")
            summary.append(f"   - REM-Schlaf: {sleep['remSleepHours']} h")
            summary.append(f"   - Qualitätsscore: {sleep['qualityScore']}\n")
        
        # HRV Status
        if "hrv" in report:
            hrv = report["hrv"]
            summary.append(f"HRV Status: {hrv['status']}")
            summary.append(f"   - Wochenschaftlich durchschnitt: {hrv['weeklyAverage']}")
            summary.append(f"   - Letzte Nacht durchschnitt: {hrv['lastNightAverage']}\n")
        
        # Training Status
        if "trainingLoad" in report:
            tl = report["trainingLoad"]["trainingStatus"]
            summary.append(f"Trainingsstatus: {tl['status']}")
            summary.append(f"   Feedback: {tl['feedbackPhrase']}\n")
        
        return "\n".join(summary)

