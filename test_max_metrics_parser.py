import os
import unittest

os.environ.setdefault("GC_EMAIL", "test@example.com")
os.environ.setdefault("GC_PASSWORD", "test")
os.environ.setdefault("EMAIL_SENDER", "test@example.com")
os.environ.setdefault("EMAIL_PASSWORD", "test")
os.environ.setdefault("EMAIL_RECEIVER", "test@example.com")

from garmin_report_email import normalize_max_metrics_entry


SAMPLE = [
    {
        "metrics": {
            "totalSteps": 1234,
            "totalDistanceMeters": 5000,
            "totalKilocalories": 300,
            "activeKilocalories": 200,
            "bmrKilocalories": 100,
            "minHeartRate": 60,
            "maxHeartRate": 170,
            "restingHeartRate": 50,
            "averageStressLevel": 20,
            "stressPercentage": 10,
            "bodyBatteryHighestValue": 90,
            "bodyBatteryLowestValue": 30,
        }
    }
]


class NormalizeMaxMetricsTest(unittest.TestCase):
    def test_supports_nested_metrics(self):
        entry = normalize_max_metrics_entry(SAMPLE[0])

        self.assertEqual(entry["totalSteps"], 1234)
        self.assertEqual(entry["totalDistanceMeters"], 5000)
        self.assertEqual(entry["bodyBatteryHighestValue"], 90)

    def test_falls_back_to_pass_through(self):
        entry = normalize_max_metrics_entry({"totalSteps": 7})

        self.assertEqual(entry["totalSteps"], 7)


if __name__ == "__main__":
    unittest.main()
