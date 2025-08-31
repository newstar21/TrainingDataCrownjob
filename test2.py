import json

from pyarrow import null


sevenDayMaxMetricList = '''[{
  "userProfileId": 109761086,
  "totalKilocalories": 3145.0,
  "activeKilocalories": 930.0,
  "bmrKilocalories": 2215.0,
  "wellnessKilocalories": 3145.0,
  "burnedKilocalories": null,
  "consumedKilocalories": null,
  "remainingKilocalories": null,
  "totalSteps": 17998,
  "netCalorieGoal": null,
  "totalDistanceMeters": 16995,
  "wellnessDistanceMeters": 16995,
  "wellnessActiveKilocalories": 930.0,
  "netRemainingKilocalories": 930.0,
  "userDailySummaryId": 109761086,
  "calendarDate": "2025-06-10",
  "rule": {
    "typeId": 4,
    "typeKey": "groups"
  },
  "uuid": "b2aca7e03d5d46bbbcd94459494b48cb",
  "dailyStepGoal": 10000,
  "wellnessStartTimeGmt": "2025-06-09T22:00:00.0",
  "wellnessStartTimeLocal": "2025-06-10T00:00:00.0",
  "wellnessEndTimeGmt": "2025-06-10T22:00:00.0",
  "wellnessEndTimeLocal": "2025-06-11T00:00:00.0",
  "durationInMilliseconds": 86400000,
  "wellnessDescription": null,
  "highlyActiveSeconds": 1597,
  "activeSeconds": 8999,
  "sedentarySeconds": 46584,
  "sleepingSeconds": 29220,
  "includesWellnessData": true,
  "includesActivityData": true,
  "includesCalorieConsumedData": false,
  "privacyProtected": false,
  "moderateIntensityMinutes": 6,
  "vigorousIntensityMinutes": 25,
  "floorsAscendedInMeters": 88.392,
  "floorsDescendedInMeters": 85.689,
  "floorsAscended": 29.0,
  "floorsDescended": 28.11319,
  "intensityMinutesGoal": 150,
  "userFloorsAscendedGoal": 10,
  "minHeartRate": 42,
  "maxHeartRate": 174,
  "restingHeartRate": 45,
  "lastSevenDaysAvgRestingHeartRate": 47,
  "source": "GARMIN",
  "averageStressLevel": 26,
  "maxStressLevel": 96,
  "stressDuration": 19740,
  "restStressDuration": 36900,
  "activityStressDuration": 16680,
  "uncategorizedStressDuration": 10620,
  "totalStressDuration": 83940,
  "lowStressDuration": 8700,
  "mediumStressDuration": 6300,
  "highStressDuration": 4740,
  "stressPercentage": 23.52,
  "restStressPercentage": 43.96,
  "activityStressPercentage": 19.87,
  "uncategorizedStressPercentage": 12.65,
  "lowStressPercentage": 10.36,
  "mediumStressPercentage": 7.51,
  "highStressPercentage": 5.65,
  "stressQualifier": "BALANCED",
  "measurableAwakeDuration": 45600,
  "measurableAsleepDuration": 27720,
  "lastSyncTimestampGMT": null,
  "minAvgHeartRate": 42,
  "maxAvgHeartRate": 171,
  "bodyBatteryChargedValue": 66,
  "bodyBatteryDrainedValue": 76,
  "bodyBatteryHighestValue": 100,
  "bodyBatteryLowestValue": 24,
  "bodyBatteryMostRecentValue": 24,
  "bodyBatteryDuringSleep": 58,
  "bodyBatteryAtWakeTime": 100,
  "bodyBatteryVersion": 3.0,
  "abnormalHeartRateAlertsCount": null,
  "averageSpo2": null,
  "lowestSpo2": null,
  "latestSpo2": null,
  "latestSpo2ReadingTimeGmt": null,
  "latestSpo2ReadingTimeLocal": null,
  "averageMonitoringEnvironmentAltitude": 445.0,
  "restingCaloriesFromActivity": 34.0,
  "bodyBatteryDynamicFeedbackEvent": {
    "eventTimestampGmt": "2025-06-10T21:13:54",
    "bodyBatteryLevel": "MODERATE",
    "feedbackShortType": "SLEEP_PREPARATION_STRESSFUL_AND_ACTIVE_AND_INTENSIVE_EXERCISE",
    "feedbackLongType": "SLEEP_PREPARATION_STRESSFUL_AND_ACTIVE_AND_INTENSIVE_EXERCISE"
  },
  "endOfDayBodyBatteryDynamicFeedbackEvent": {
    "eventTimestampGmt": "2025-06-10T21:30:14",
    "bodyBatteryLevel": "MODERATE",
    "feedbackShortType": "SLEEP_TIME_PASSED_STRESSFUL_AND_ACTIVE_AND_INTENSIVE_EXERCISE",
    "feedbackLongType": "SLEEP_TIME_PASSED_STRESSFUL_AND_ACTIVE_AND_INTENSIVE_EXERCISE"
  },
  "bodyBatteryActivityEventList": [
    {
      "eventType": "SLEEP",
      "eventStartTimeGmt": "2025-06-09T22:28:14",
      "timezoneOffset": 7200000,
      "durationInMilliseconds": 29220000,
      "bodyBatteryImpact": 58,
      "feedbackType": "NONE",
      "shortFeedback": "NONE",
      "deviceId": 3420895993,
      "activityName": null,
      "activityType": null,
      "activityId": null,
      "eventUpdateTimeGmt": "2025-06-10T07:27:08"
    },
    {
      "eventType": "ACTIVITY",
      "eventStartTimeGmt": "2025-06-10T14:01:22",
      "timezoneOffset": 7200000,
      "durationInMilliseconds": 1320000,
      "bodyBatteryImpact": -5,
      "feedbackType": "EXERCISE_TRAINING_EFFECT_3",
      "shortFeedback": "IMPROVING_TEMPO",
      "deviceId": 3420895993,
      "activityName": "Perugia - Montag – Intervallläufe (Anae",
      "activityType": "running",
      "activityId": 19390064517,
      "eventUpdateTimeGmt": "2025-06-10T14:24:06"
    }
  ],
  "avgWakingRespirationValue": 14.0,
  "highestRespirationValue": 21.0,
  "lowestRespirationValue": 7.0,
  "latestRespirationValue": 14.0,
  "latestRespirationTimeGMT": "2025-06-10T22:00:00.0",
  "respirationAlgorithmVersion": 200
}]'''

sevenDaysSteps = []
totalWalkingDistance = []
total_calories = []
active_calories = []
bmr_calories = []
min_heartRate = []
max_heartRate = []
resting_heartRate = []
average_stress = []
percentage_stress = []
highest_bodyBattery = []
lowest_bodyBattery = []

sevenDayMaxMetricList = json.loads(sevenDayMaxMetricList)
for dic in sevenDayMaxMetricList:
    try:

        sevenDaysSteps.append(dic.get("totalSteps"))
        totalWalkingDistance.append(round(dic.get("totalDistanceMeters", 0) / 1000, 2))
        total_calories.append(dic.get("totalKilocalories"))
        active_calories.append(dic.get("activeKilocalories"))
        bmr_calories.append(dic.get("bmrKilocalories"))
        min_heartRate.append(dic.get("minHeartRate"))
        max_heartRate.append(dic.get("maxHeartRate"))
        resting_heartRate.append(dic.get("restingHeartRate"))
        percentage_stress.append(dic.get("stressPercentage"))
        highest_bodyBattery.append(dic.get("bodyBatteryHighestValue"))
        lowest_bodyBattery.append(dic.get("bodyBatteryLowestValue"))

    except Exception as e:
        print(f"Fehler bei Max Metrics: {e}")
        sevenDaysSteps.append(None)
        totalWalkingDistance.append(None)
        total_calories.append(None)
        active_calories.append(None)
        bmr_calories.append(None)
        min_heartRate.append(None)
        max_heartRate.append(None)
        resting_heartRate.append(None)
        percentage_stress.append(None)
        highest_bodyBattery.append(None)
        lowest_bodyBattery.append(None)

print(sevenDaysSteps, totalWalkingDistance, total_calories, active_calories, lowest_bodyBattery)
