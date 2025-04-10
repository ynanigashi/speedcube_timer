import time
import keyboard

class SpeedcubeTimer:
    def __init__(self):
        self.results = []
        self.MAX_RESULTS = 12
        self.solve_count = 1  # 1からカウント開始

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
        """新しい結果を追加し、解いた回数をカウントアップ"""
        self.results.append((scramble, time, self.solve_count))
        # 最大結果数を超えた場合、古い結果を削除
        if len(self.results) > self.MAX_RESULTS:
            self.results.pop(0)
        
        # 解いた回数をインクリメント
        self.solve_count += 1

    def get_recent_results(self):
        return self.results[::-1]

    def get_solve_count(self):
        """合計解いた回数を返す"""
        return self.solve_count