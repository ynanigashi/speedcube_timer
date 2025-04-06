class SpeedcubeStats:
    @staticmethod
    def calculate_average(times, n):
        if len(times) < n:
            return None
        recent_times = [time for _, time in times[-n:]]
        return sum(recent_times) / len(recent_times)

    def format_average(self, value):
        return f"{value:.2f}" if value is not None else "-"