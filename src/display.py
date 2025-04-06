import os

class SpeedcubeDisplay:
    def clear(self):
        os.system('cls')

    def show_scramble(self, scramble):
        print("WCAルールに近い3x3x3ルービックキューブのスクランブル:")
        print(scramble)

    def show_results(self, results):
        if not results:
            return
        
        print("\n過去のリザルト:")
        for i, (_, time_result) in enumerate(results, 1):
            print(f"{i:02d}: {time_result:.2f} 秒")

    def show_statistics(self, ao5, ao12):
        print("\n統計:")
        print(f"AO5: {ao5} 秒 / AO12: {ao12} 秒")