data = {'userId': 109761086, 'mostRecentVO2Max': {'userId': 109761086, 'generic': {'calendarDate': '2025-06-17', 'vo2MaxPreciseValue': 66.4, 'vo2MaxValue': 66.0, 'fitnessAge': None, 'fitnessAgeDescription': None, 'maxMetCategory': 0}, 'cycling': None, 'heatAltitudeAcclimation': {'calendarDate': '2025-06-20', 'altitudeAcclimationDate': '2025-06-20', 'previousAltitudeAcclimationDate': '2025-06-20', 'heatAcclimationDate': '2025-06-20', 'previousHeatAcclimationDate': '2025-06-19', 'altitudeAcclimation': 0, 'previousAltitudeAcclimation': 0, 'heatAcclimationPercentage': 50, 'previousHeatAcclimationPercentage': 52, 'heatTrend': 'DEACCLIMATIZING', 'altitudeTrend': None, 'currentAltitude': 28, 'previousAltitude': 0, 'acclimationPercentage': 0, 'previousAcclimationPercentage': 0, 'altitudeAcclimationLocalTimestamp': '2025-06-20T23:57:17.0'}}, 'mostRecentTrainingLoadBalance': {'userId': 109761086, 'metricsTrainingLoadBalanceDTOMap': {'3420895993': {'calendarDate': '2025-06-20', 'deviceId': 3420895993, 'monthlyLoadAerobicLow': 458.69794, 'monthlyLoadAerobicHigh': 594.48145, 'monthlyLoadAnaerobic': 694.22974, 'monthlyLoadAerobicLowTargetMin': 698, 'monthlyLoadAerobicLowTargetMax': 1535, 'monthlyLoadAerobicHighTargetMin': 837, 'monthlyLoadAerobicHighTargetMax': 1675, 'monthlyLoadAnaerobicTargetMin': 279, 'monthlyLoadAnaerobicTargetMax': 837, 'trainingBalanceFeedbackPhrase': 'AEROBIC_LOW_SHORTAGE', 'primaryTrainingDevice': True}}, 'recordedDevices': [{'deviceId': 3420895993, 'imageURL': 'https://res.garmin.com/en/products/010-02638-20/v/c1_01_md.png', 'deviceName': 'Forerunner 955 Solar', 'category': 0}]}, 'mostRecentTrainingStatus': {'userId': 109761086, 'latestTrainingStatusData': {'3420895993': {'calendarDate': '2025-06-20', 'sinceDate': '2025-06-20', 'weeklyTrainingLoad': None, 'trainingStatus': 7, 'timestamp': 1750453265000, 'deviceId': 3420895993, 'loadTunnelMin': None, 'loadTunnelMax': None, 'loadLevelTrend': None, 'sport': 'RUNNING', 'subSport': 'GENERIC', 'fitnessTrendSport': 'RUNNING', 'fitnessTrend': 2, 'trainingStatusFeedbackPhrase': 'PRODUCTIVE_8', 'trainingPaused': False, 'acuteTrainingLoadDTO': {'acwrPercent': 66, 'acwrStatus': 'HIGH', 'acwrStatusFeedback': 'FEEDBACK_4', 'dailyTrainingLoadAcute': 674, 'maxTrainingLoadChronic': 661.5, 'minTrainingLoadChronic': 352.8, 'dailyTrainingLoadChronic': 441, 'dailyAcuteChronicWorkloadRatio': 1.5}, 'primaryTrainingDevice': True}}, 'recordedDevices': [{'deviceId': 3420895993, 'imageURL': 'https://res.garmin.com/en/products/010-02638-20/v/c1_01_md.png', 'deviceName': 'Forerunner 955 Solar', 'category': 0}], 'showSelector': False, 'lastPrimarySyncDate': '2025-06-20'}, 'heatAltitudeAcclimationDTO': None}


# Angenommen dein Dictionary heißt data
load_data = list(data["mostRecentTrainingLoadBalance"]["metricsTrainingLoadBalanceDTOMap"].values())[0]
status_data = list(data["mostRecentTrainingStatus"]["latestTrainingStatusData"].values())[0]

# Gesuchte Werte
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

