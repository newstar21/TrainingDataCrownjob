from pyarrow import null
from datetime import datetime, timedelta

class HelperClass(object):
    @staticmethod
    def get_last_7_days():
        today = datetime.now().date()
        return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
