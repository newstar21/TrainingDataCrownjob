import unittest
from unittest.mock import Mock, patch

from garmin_report_email import authenticate_with_retry
from garminconnect import GarminConnectTooManyRequestsError


class AuthenticateWithRetryTest(unittest.TestCase):
    def test_retries_after_rate_limit_and_then_succeeds(self):
        client = Mock()
        client.login.side_effect = [
            GarminConnectTooManyRequestsError("429"),
            None,
        ]

        with patch("garmin_report_email.time.sleep", return_value=None) as sleep_mock:
            authenticate_with_retry(client, "garmin_tokens.json", max_attempts=3, base_delay_seconds=1)

        self.assertEqual(client.login.call_count, 2)
        sleep_mock.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
