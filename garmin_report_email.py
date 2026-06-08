import os
import json
import smtplib
import time
from datetime import datetime, timedelta
from email.message import EmailMessage

from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectTooManyRequestsError

from dotenv import load_dotenv

from HelperClass import HelperClass

load_dotenv()


def normalize_max_metrics_entry(entry):
    """Return Garmin max-metrics values from either top-level or nested payloads."""
    if isinstance(entry, list):
        for item in entry:
            normalized = normalize_max_metrics_entry(item)
            if isinstance(normalized, dict) and normalized:
                return normalized
        return {}

    if not isinstance(entry, dict):
        return {}

    for candidate_key in ("metrics", "dailyMetrics", "dailySummaryDTO", "maxMetrics"):
        candidate = entry.get(candidate_key)
        if isinstance(candidate, dict):
            return candidate
        if isinstance(candidate, list):
            normalized = normalize_max_metrics_entry(candidate)
            if isinstance(normalized, dict) and normalized:
                return normalized

    return entry


def extract_metric_value(entry, keys, default=0):
    """Return the first available metric value or a safe default for missing Garmin data."""
    normalized = normalize_max_metrics_entry(entry)

    for key in keys:
        value = normalized.get(key)
        if value is not None:
            return value

    return default


def authenticate_with_retry(client, tokenstore_path, max_attempts=3, base_delay_seconds=60):
    """Retry Garmin login when Garmin responds with 429 rate-limit errors."""
    for attempt in range(1, max_attempts + 1):
        try:
            client.login(tokenstore=tokenstore_path)
            return
        except (GarminConnectTooManyRequestsError, GarminConnectConnectionError) as exc:
            error_text = str(exc).lower()
            if "429" not in error_text and "rate limit" not in error_text:
                raise
            if attempt == max_attempts:
                raise
            wait_seconds = base_delay_seconds * attempt
            print(f"WARNING: Garmin login rate limited (attempt {attempt}/{max_attempts}). Waiting {wait_seconds}s before retry...")
            time.sleep(wait_seconds)


def main():
    # --- Garmin Login ---
    GC_EMAIL = os.environ['GC_EMAIL']
    GC_PASSWORD = os.environ['GC_PASSWORD']

    # --- Email Setup ---
    EMAIL_SENDER = os.environ['EMAIL_SENDER']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    EMAIL_RECEIVER = os.environ['EMAIL_RECEIVER']

    # --- Authenticate Garmin ---
    client = Garmin(GC_EMAIL, GC_PASSWORD)
    tokenstore_path = os.path.join(os.getcwd(), "garmin_tokens.json")
    os.makedirs(os.path.dirname(tokenstore_path) or ".", exist_ok=True)
    authenticate_with_retry(client, tokenstore_path)
    helper = HelperClass

    today = datetime.now().date()
    last_sunday = today - timedelta(days=today.weekday() + 1)

    last7DateList = helper.get_last_7_days()

    # --- Get Activities ---
    activities = client.get_activities_by_date(str(last_sunday), str(today))
    activity_details = []

    for act in activities:
        try:
            activity_id = act.get("activityId")
            detailed = client.get_activity_details(activity_id)
            splits = detailed.get("splits", [])
            act_detail = {
                "start_time": act.get("startTimeLocal"),
                "activity_type": act.get("activityType"),
                "duration_min": round(act.get("duration", 0) / 60, 2),
                "distance_km": round(act.get("distance", 0) / 1000, 2),
                "avg_hr": act.get("averageHR"),
                "max_hr": act.get("maxHR"),
                "cadence": act.get("averageRunningCadenceInStepsPerMinute"),
                "elevation_gain_m": act.get("elevationGain"),
                "training_effect": act.get("trainingEffect"),
                "aerobic_effect": act.get("aerobicTrainingEffect"),
                "anaerobic_effect": act.get("anaerobicTrainingEffect"),
                "calories": act.get("calories"),
                "power_avg": act.get("averagePower"),
                "temp_avg": act.get("avgTemperature"),
                "splits": splits,
            }
            activity_details.append(act_detail)
        except Exception as e:
            print(f"Fehler bei Aktivität {act.get('activityId')}: {e}")

    # --- Physiologische Daten ---
    # --- UserProfile Daten ---
    try:
        userProfile = client.get_user_profile()
        vo2Max = userProfile["userData"].get("vo2MaxRunning")
        lactateThresholdHeartRate = userProfile["userData"].get("lactateThresholdHeartRate")
        lactateThresholdSpeed = "3:46 min/km"
    except Exception as e:
        print("Fehler bei UserProfileDate", e)
        vo2Max = None
        lactateThresholdSpeed = None
        lactateThresholdHeartRate = None

    # --- HRV Werte ---
    try:
        hrv_status = client.get_hrv_data(str(today))
        hrv_status_weeklyAvg = hrv_status["hrvSummary"]["weeklyAvg"]
        hrv_status_status = hrv_status["hrvSummary"]["status"]
        hrv_status_lastNightAvg = hrv_status["hrvSummary"]["lastNightAvg"]
    except Exception as e:
        print("Fehler bei HRV Werten", e)
        hrv_status_weeklyAvg = None
        hrv_status_status = None
        hrv_status_lastNightAvg = None

    # --- Training Status Werte ---
    try:
        training_status = client.get_training_status(str(today))

        load_data = list(training_status["mostRecentTrainingLoadBalance"]["metricsTrainingLoadBalanceDTOMap"].values())[0]
        status_data = list(training_status["mostRecentTrainingStatus"]["latestTrainingStatusData"].values())[0]

        monthlyLoadAerobicLow = load_data["monthlyLoadAerobicLow"]
        monthlyLoadAerobicHigh = load_data["monthlyLoadAerobicHigh"]
        monthlyLoadAnaerobic = load_data["monthlyLoadAnaerobic"]
        trainingBalanceFeedbackPhrase = load_data["trainingBalanceFeedbackPhrase"]

        trainingStatus = status_data["trainingStatus"]
        trainingStatusFeedbackPhrase = status_data["trainingStatusFeedbackPhrase"]

        acute = status_data["acuteTrainingLoadDTO"]
        acwrPercent = acute["acwrPercent"]
        acwrStatus = acute["acwrStatus"]
        dailyTrainingLoadAcute = acute["dailyTrainingLoadAcute"]
        dailyTrainingLoadChronic = acute["dailyTrainingLoadChronic"]
    except Exception as e:
        print("Fehler beim Laden Training Satus Werte:", e)
        monthlyLoadAerobicLow = None
        monthlyLoadAerobicHigh = None
        monthlyLoadAnaerobic = None
        trainingBalanceFeedbackPhrase = None
        trainingStatus = None
        trainingStatusFeedbackPhrase = None
        acute = None
        acwrPercent = None
        acwrStatus = None
        dailyTrainingLoadAcute = None
        dailyTrainingLoadChronic = None

    # --- Schlaf Daten ---
    try:
        yesterday = today - timedelta(days=1)
        sleep_data = client.get_sleep_data(str(yesterday))
        last_night_sleep = sleep_data.get("dailySleepDTO", {})

        sleep_start_time = last_night_sleep.get("sleepStartTimestampGMT")
        sleep_end_time = last_night_sleep.get("sleepEndTimestampGMT")
        total_sleep_seconds = last_night_sleep.get("duration", 0)
        total_sleep_hours = round(total_sleep_seconds / 3600, 2)

        sleep_stages = last_night_sleep.get("sleepLevels", [])
        deep_sleep_seconds = sum([s.get("duration", 0) for s in sleep_stages if s.get("type") == 4])
        rem_sleep_seconds = sum([s.get("duration", 0) for s in sleep_stages if s.get("type") == 3])
        light_sleep_seconds = sum([s.get("duration", 0) for s in sleep_stages if s.get("type") == 2])
        awake_seconds = sum([s.get("duration", 0) for s in sleep_stages if s.get("type") == 1])

        deep_sleep_hours = round(deep_sleep_seconds / 3600, 2)
        rem_sleep_hours = round(rem_sleep_seconds / 3600, 2)
        light_sleep_hours = round(light_sleep_seconds / 3600, 2)
        awake_hours = round(awake_seconds / 3600, 2)

        sleep_quality = last_night_sleep.get("sleepQualityScore")
        sleep_efficiency_percent = last_night_sleep.get("sleepEfficiency")
        avg_resting_hr_sleep = last_night_sleep.get("averageRespirationValue")
        avg_spo2_sleep = last_night_sleep.get("avgSpO2Value")
    except Exception as e:
        print("Fehler bei Schlaf Daten:", e)
        total_sleep_hours = None
        deep_sleep_hours = None
        rem_sleep_hours = None
        light_sleep_hours = None
        awake_hours = None
        sleep_quality = None
        sleep_efficiency_percent = None
        avg_resting_hr_sleep = None
        avg_spo2_sleep = None

    # --- Assemble Report ---
    report = {
        "week": f"{last_sunday.isoformat()} - {today.isoformat()}",
        "userProfile": {
            "vo2max": vo2Max,
            "lactateThresholdHeartRate": lactateThresholdHeartRate,
            "lactateThresholdSpeed": lactateThresholdSpeed,
        },
        "activities": {
            "summary": {
                "totalActivities": len(activity_details),
                "totalDurationMinutes": round(sum([a.get("duration_min", 0) for a in activity_details]), 2),
                "totalDistanceKm": round(sum([a.get("distance_km", 0) for a in activity_details]), 2),
                "totalCalories": round(sum([a.get("calories", 0) for a in activity_details]), 2),
                "averageHeartRate": round(sum([a.get("avg_hr", 0) if a.get("avg_hr") else 0 for a in activity_details]) / max(len(activity_details), 1), 1) if activity_details else 0.0,
                "totalElevationGainM": round(sum([a.get("elevation_gain_m", 0) if a.get("elevation_gain_m") else 0 for a in activity_details]), 2),
            },
            "details": activity_details,
        },
        "sleep": {
            "lastNight": {
                "totalHours": total_sleep_hours,
                "deepSleepHours": deep_sleep_hours,
                "remSleepHours": rem_sleep_hours,
                "lightSleepHours": light_sleep_hours,
                "awakeHours": awake_hours,
                "qualityScore": sleep_quality,
                "efficiencyPercent": sleep_efficiency_percent,
                "avgRespirationRate": avg_resting_hr_sleep,
                "avgSpO2Percent": avg_spo2_sleep,
            }
        },
        "hrv": {
            "weeklyAverage": hrv_status_weeklyAvg,
            "status": hrv_status_status,
            "lastNightAverage": hrv_status_lastNightAvg,
        },
        "trainingLoad": {
            "monthly": {
                "aerobicLow": monthlyLoadAerobicLow,
                "aerobicHigh": monthlyLoadAerobicHigh,
                "anaerobic": monthlyLoadAnaerobic,
                "feedbackPhrase": trainingBalanceFeedbackPhrase,
            },
            "trainingStatus": {
                "status": trainingStatus,
                "feedbackPhrase": trainingStatusFeedbackPhrase,
            },
            "acuteTrainingLoad": {
                "acwrPercent": acwrPercent,
                "acwrStatus": acwrStatus,
                "dailyAcute": dailyTrainingLoadAcute,
                "dailyChronic": dailyTrainingLoadChronic,
            },
        },
    }

    print(report)

    # --- Generiere Report Zusammenfassung ---
    report_summary = helper.format_report_summary(report)
    print("\n" + "=" * 60)
    print("GARMIN WOCHENBERICHT ZUSAMMENFASSUNG")
    print("=" * 60)
    print(report_summary)
    print("=" * 60 + "\n")

    # --- Save JSON File Locally ---
    with open("garmin_report_full.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # --- Send Email ---
    msg = EmailMessage()
    msg['Subject'] = f"Garmin Wochenbericht - {last_sunday.isoformat()} bis {today.isoformat()}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    email_body = f"""
Hallo,

anbei ist dein detaillierter Garmin-Trainingsbericht für die Woche vom {last_sunday.isoformat()} bis {today.isoformat()}.

ZUSAMMENFASSUNG:
{report_summary}

Der vollständige JSON-Report mit allen Daten ist im Anhang für die Analyse durch Gemini AI verfügbar.

---
Dieser Bericht enthält:
✓ Alle Trainingsaktivitäten mit Details
✓ Schlafdaten (Dauer, Qualität, Schlafphasen)
✓ HRV & Herzratenvariabilität
✓ Trainingslast & Erholungsstatus
✓ 7-Tage-Metriken (Schritte, Kalorienverbrauch, Stress, etc.)
✓ Body Battery Analyse
✓ Physiologische Leistungsindikatoren

Viel Erfolg beim Training!
"""

    msg.set_content(email_body)
    msg.add_attachment(json.dumps(report, indent=2, ensure_ascii=False), filename="garmin_report_full.json")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Garmin Wochenbericht gesendet und gespeichert.")


if __name__ == "__main__":
    main()
