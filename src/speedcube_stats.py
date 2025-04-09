class SpeedcubeStats:
    def calculate_average(self, results, n):
        if len(results) < n:
            return None
        
        # タプルの2番目の要素（time）のみを使用
        recent_times = [result[1] for result in results[-n:]]
        return sum(recent_times) / len(recent_times)

    def format_average(self, value):
        return f"{value:.2f}" if value is not None else "-"