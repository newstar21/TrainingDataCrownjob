import os
import json
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from garminconnect import Garmin

from dotenv import load_dotenv
load_dotenv()


# --- Garmin Login ---
GC_EMAIL = os.environ['GC_EMAIL']
GC_PASSWORD = os.environ['GC_PASSWORD']

# --- Email Setup ---
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_RECEIVER = os.environ['EMAIL_RECEIVER']

# --- Authenticate Garmin ---
client = Garmin(GC_EMAIL, GC_PASSWORD)
client.login()

today = datetime.now().date()
last_sunday = today - timedelta(days=today.weekday() + 1)

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
            "duration_min": round(act.get("duration", 0)/60, 2),
            "distance_km": round(act.get("distance", 0)/1000, 2),
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
            "splits": splits
        }
        activity_details.append(act_detail)
    except Exception as e:
        print(f"Fehler bei Aktivität {act.get('activityId')}: {e}")

# --- Physiologische Daten ---
try:
    stats = client.get_stats_and_body(last_sunday.isoformat())
    training_status = client.get_training_status(str(last_sunday))  # ✅ FIX
    hrv_status = client.get_hrv_data(str(today))
    sleep_data = client.get_sleep_data(last_sunday.isoformat())
    body_battery = client.get_body_battery()
    readiness = client.get_training_readiness()
    stress_data = client.get_stress_details(last_sunday.isoformat())

    fitness_age = stats.get("fitnessAge")
    vo2max = stats.get("vo2Max")
    lactate_threshold = stats.get("lactateThreshold")
    weight = stats.get("weight")
    body_fat = stats.get("bodyFat")
    resting_hr = stats.get("restingHeartRate")

    training_load = training_status.get("trainingLoad")
    recovery_time = client.get_recovery_time()
    training_status_summary = training_status.get("trainingStatus")

    hrv_avg_value = hrv_status['hrvSummary']['weeklyAvg']
    hrv_state = hrv_status['hrvSummary']['status']

    sleep_score = sleep_data.get("sleepScore")
    sleep_phases = sleep_data.get("sleepLevelsMap")
    stress_level = sleep_data.get("avgStressLevel")

    bb_avg = body_battery.get("average")
    bb_min = body_battery.get("min")
    bb_max = body_battery.get("max")

    readiness_score = readiness.get("trainingReadinessScore")
    readiness_status = readiness.get("trainingReadinessStatus")

    stress_hours = stress_data.get("stressLevelValues")

except Exception as e:
    print("Fehler beim Laden physiologischer Daten:", e)

    fitness_age = vo2max = lactate_threshold = weight = body_fat = resting_hr = None
    training_load = recovery_time = training_status_summary = None
    hrv_avg_value = hrv_state = None
    sleep_score = stress_level = sleep_phases = None
    bb_avg = bb_min = bb_max = None
    readiness_score = readiness_status = None
    stress_hours = None

# --- Assemble Report ---
report = {
    "week": f"{last_sunday.isoformat()} - {today.isoformat()}",
    "fitness": {
        "fitness_age": fitness_age,
        "vo2max": vo2max,
        "lactate_threshold": lactate_threshold,
        "weight_kg": weight,
        "body_fat_percent": body_fat,
        "resting_hr": resting_hr
    },
    "training_status": {
        "status": training_status_summary,
        "training_load": training_load,
        "recovery_time_h": recovery_time
    },
    "hrv": {
        "hrv_average_value": hrv_avg_value,
        "status": hrv_state
    },
    "sleep": {
        "score": sleep_score,
        "phases": sleep_phases,
        "avg_stress": stress_level
    },
    "body_battery": {
        "avg": bb_avg,
        "min": bb_min,
        "max": bb_max
    },
    "training_readiness": {
        "score": readiness_score,
        "status": readiness_status
    },
    "stress_over_day": stress_hours,
    "activities": activity_details
}

# --- Save JSON File Locally ---
with open("garmin_report_full.json", "w") as f:
    json.dump(report, f, indent=2)

# --- Send Email ---
msg = EmailMessage()
msg['Subject'] = f"Garmin Maximalbericht – {last_sunday.isoformat()}"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_RECEIVER
msg.set_content(f"Dein vollständiger Garmin-Wochenbericht ist im Anhang.")
msg.add_attachment(json.dumps(report, indent=2), filename="garmin_report_full.json")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("✅ Garmin Maximalbericht gesendet und gespeichert.")