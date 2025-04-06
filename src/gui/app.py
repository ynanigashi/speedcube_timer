import pyxel
from enum import Enum, auto
from ..timer import SpeedcubeTimer
from ..speedcube_stats import SpeedcubeStats
from ..scramble import generate_wca_cube_scramble
from ..log_handler import SpeedcubeLogger

class TimerState(Enum):
    READY = auto()
    COUNTDOWN = auto()
    RUNNING = auto()

class SpeedcubeApp:
    def __init__(self):
        self.fps = 60  # FPSを変数として定義
        # ウィンドウサイズを240x180に拡大（1.5倍）
        pyxel.init(240, 180, title="Speedcube Timer", fps=self.fps)
        
        # サウンドの初期化
        # ピッ音 (低音)
        pyxel.sounds[0].set("a3", "p", "3", "n", 5)
        # ポーン音 (高音)
        pyxel.sounds[1].set("a4", "p", "5", "n", 10)
        # コイン音 (コイーン)
        pyxel.sounds[2].set("c3e3g3c4", "s", "7", "n", 10)
        
        # コンポーネントの初期化
        self.timer = SpeedcubeTimer()
        self.stats = SpeedcubeStats()
        self.logger = SpeedcubeLogger()
        
        # 画面状態の初期化
        self.scramble = generate_wca_cube_scramble()
        self.current_time = 0.0
        self.timer_running = False
        self.start_time = 0
        self.space_hold_start = 0
        self.countdown_start = 0
        self.state = TimerState.READY  # ready, countdown, running
        self.INSPECTION_TIME = 15.0  # WCAルールの15秒
        self.SPACE_HOLD_TIME = 0.5   # スペースキー長押しの必要時間
        self.COUNTDOWN_BEEP_TIMES = [4, 3, 2, 1, 0]  # ピッ音を鳴らすタイミング（残り秒数）

        # Pyxelの実行
        pyxel.run(self.update, self.draw)

    def _start_timer(self):
        """タイマーを開始する共通処理"""
        self.state = TimerState.RUNNING
        self.timer_running = True
        self.start_time = pyxel.frame_count
        pyxel.play(0, 1)  # タイマー開始時にポーン音を再生

    def _should_play_beep(self, current_time: float, target_time: float) -> bool:
        """指定された時間の最初のフレームかどうかを判定"""
        frame_time = 1.0 / self.fps
        return target_time <= current_time <= target_time + frame_time

    def update(self):
        # ESCで終了
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # 状態に応じた処理
        match self.state:
            case TimerState.READY:
                if pyxel.btn(pyxel.KEY_SPACE):  # スペースキーが押されている間
                    if self.space_hold_start == 0:
                        self.space_hold_start = pyxel.frame_count
                    elif (pyxel.frame_count - self.space_hold_start) / self.fps >= self.SPACE_HOLD_TIME:
                        # 長押しでインスペクションタイム開始
                        self.state = TimerState.COUNTDOWN
                        self.countdown_start = pyxel.frame_count
                        self.space_hold_start = 0  # space_hold_startを初期化
                else:
                    self.space_hold_start = 0

            case TimerState.COUNTDOWN:
                current_time = (pyxel.frame_count - self.countdown_start) / self.fps
                
                # カウントダウン音の再生
                for beep_time in self.COUNTDOWN_BEEP_TIMES:
                    target_time = self.INSPECTION_TIME - beep_time
                    if self._should_play_beep(current_time, target_time):
                        pyxel.play(0, 0)
                        break
                
                # カウントダウン中のスペースキー長押し確認
                if pyxel.btn(pyxel.KEY_SPACE):
                    if self.space_hold_start == 0:
                        self.space_hold_start = pyxel.frame_count
                    elif (pyxel.frame_count - self.space_hold_start) / self.fps >= self.SPACE_HOLD_TIME:
                        # スペースキーが長押しされたらタイマー開始
                        self._start_timer()
                else:
                    self.space_hold_start = 0

                # もしくは15秒経過でタイマー開始
                if current_time >= self.INSPECTION_TIME:
                    self._start_timer()

            case TimerState.RUNNING:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.timer_running = False
                    self.timer.add_result(self.scramble, self.current_time)
                    self.logger.save_result(self.current_time)
                    pyxel.play(0, 2)  # コイン音を再生
                    self.scramble = generate_wca_cube_scramble()
                    self.state = TimerState.READY

        # タイマー更新（タイマー動作中は実行）
        if self.timer_running:
            self.current_time = (pyxel.frame_count - self.start_time) / self.fps

    def draw(self):
        pyxel.cls(0)

        match self.state:
            case TimerState.READY:
                # スクランブル表示
                pyxel.text(10, 10, "Scramble:", 7)
                pyxel.text(10, 25, self.scramble, 7)
                
                # タイマー状態表示
                if self.space_hold_start > 0:
                    hold_time = (pyxel.frame_count - self.space_hold_start) / self.fps
                    pyxel.text(10, 60, f"Hold: {hold_time:.1f}", 7)
                else:
                    pyxel.text(10, 60, "Hold SPACE", 7)

                # 記録表示
                self._draw_results()

            case TimerState.COUNTDOWN:
                # "INSPECTION TIME"を画面上部に表示
                pyxel.text(85, 10, "INSPECTION TIME", 7)
                
                # カウントダウンのみを大きく表示
                countdown_time = self.INSPECTION_TIME - (pyxel.frame_count - self.countdown_start) / self.fps
                color = 8 if countdown_time <= 4 else 7
                pyxel.text(100, 80, f"{countdown_time:.1f}", color)

                # 長押し状態表示（小さく）
                if self.space_hold_start > 0:
                    hold_time = (pyxel.frame_count - self.space_hold_start) / self.fps
                    pyxel.text(10, 150, f"Hold: {hold_time:.1f}", 7)

            case TimerState.RUNNING:
                # タイム表示のみを大きく中央に
                pyxel.text(90, 80, f"{self.current_time:.2f}", 7)

    def _draw_results(self):
        """記録表示の共通処理"""
        if not self.timer.results:
            return

        y = 100
        pyxel.text(10, y, "Recent:", 7)
        for i, (_, time) in enumerate(self.timer.get_recent_results()[:5]):
            pyxel.text(10, y + 15 + (i * 10), f"{time:.2f}", 7)

        # 平均の表示
        ao5 = self.stats.calculate_average(self.timer.results, 5)
        ao12 = self.stats.calculate_average(self.timer.results, 12)
        
        ao5_text = f"AO5: {ao5:.2f}" if ao5 else "AO5: -"
        ao12_text = f"AO12: {ao12:.2f}" if ao12 else "AO12: -"
        
        pyxel.text(120, 100, ao5_text, 7)
        pyxel.text(120, 115, ao12_text, 7)

    def run(self):
        # メインループはpyxel.runで実行されるため、
        # このメソッドは互換性のために残しています
        pass