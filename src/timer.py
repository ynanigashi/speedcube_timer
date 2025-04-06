import time
import keyboard

class SpeedcubeTimer:
    def __init__(self):
        self.results = []
        self.MAX_RESULTS = 12

    def start(self):
        input("エンターを押してタイマーをスタートします...")
        start_time = time.time()
        print("タイマーがスタートしました。スペースキーを押すとストップします。")
        
        while True:
            elapsed_time = time.time() - start_time
            print(f"\r経過時間: {elapsed_time:.2f} 秒", end="")
            if keyboard.is_pressed('space'):
                break
        
        return elapsed_time

    def add_result(self, scramble, time):
        self.results.append((scramble, time))
        if len(self.results) > self.MAX_RESULTS:
            self.results.pop(0)

    def get_recent_results(self):
        return self.results[::-1]