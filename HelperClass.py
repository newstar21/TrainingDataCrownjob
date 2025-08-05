from pyarrow import null


class HelperClass(object):
    @staticmethod
    def convert_speed_to_pace(speed):
        try:
            """ speed in m/s -> pace in min/km """
            speed *= 10  # Garmin-Korrektur
            pace_seconds = 1000 / speed
            minutes = int(pace_seconds // 60)
            seconds = round(pace_seconds % 60)
            return f"{minutes}:{seconds:02d} min/km"
        except:
            return null()
