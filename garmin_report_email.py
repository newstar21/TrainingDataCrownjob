import os
import json
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from garminconnect import Garmin

from dotenv import load_dotenv

from HelperClass import HelperClass

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
helper = HelperClass

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
    hrv_status_weeklyAvg = hrv_status["hrvSummary"].get("weeklyAvg")
    hrv_status_status = hrv_status["hrvSummary"].get("status")
    hrv_status_lastNightAvg = hrv_status["hrvSummary"].get("lastNightAvg")
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


# --- Assemble Report ---
report = {
    "week": f"{last_sunday.isoformat()} - {today.isoformat()}",
    "fitness": {
        "vo2max": vo2Max,
        "lactateThresholdHeartRate": lactateThresholdHeartRate
    },
    "activities": activity_details,
    "hrv": {
        "hrv_status_weeklyAvg": hrv_status_weeklyAvg,
        "status": hrv_status_status,
        "lastNightAvg": hrv_status_lastNightAvg
    },
    "monthlyLoad": {
        "aerobicLow": monthlyLoadAerobicLow,
        "aerobicHigh": monthlyLoadAerobicHigh,
        "anaerobic": monthlyLoadAnaerobic,
        "trainingBalanceFeedbackPhrase": trainingBalanceFeedbackPhrase
    },
    "trainingStatus": {
        "status": trainingStatus,
        "feedbackPhrase": trainingStatusFeedbackPhrase,
        "acuteTrainingLoad": {
            "acwrPercent": acwrPercent,
            "acwrStatus": acwrStatus,
            "dailyAcute": dailyTrainingLoadAcute,
            "dailyChronic": dailyTrainingLoadChronic
        }
    }
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