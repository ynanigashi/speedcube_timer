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
    # ウィンドウサイズとレイアウトの定数
    SMALL_FONT_WIDTH = 4   # フォントの幅
    SMALL_FONT_HEIGHT = 8  # フォントの高さ
    MIDDLE_FONT_WIDTH = 5   # フォントの幅
    MIDDLE_FONT_HEIGHT = 10 # フォントの高さ
    LARGE_FONT_WIDTH = 6   # フォントの幅
    LARGE_FONT_HEIGHT = 12 # フォントの高さ
    FONT_SPACING = 5       # フォント間のスペース
    MARGIN_X = 20          # 左右マージン
    MARGIN_Y = 10          # 上下マージン

    # 画面幅の計算
    # スクランブル最大40文字 × (フォント幅5 + 文字間隔5) + 左右マージン20×2
    WINDOW_WIDTH = 40 * (MIDDLE_FONT_WIDTH + FONT_SPACING) + MARGIN_X * 2
    WINDOW_HEIGHT = 240
    
    FPS = 60  # FPSをクラス定数として定義
    
    # WCAルールに関する定数
    INSPECTION_TIME = 15.0  # WCAルールの15秒
    SPACE_HOLD_TIME = 0.5  # スペースキー長押しの必要時間
    COUNTDOWN_BEEP_TIMES = [3, 2, 1, 0]  # ピッ音を鳴らすタイミング（残り秒数）
    
    # 縦方向の位置（上マージンを考慮して調整）
    SCRAMBLE_Y = MARGIN_Y
    SCRAMBLE_TEXT_Y = SCRAMBLE_Y + MIDDLE_FONT_HEIGHT + FONT_SPACING
    TIMER_Y = SCRAMBLE_TEXT_Y + MIDDLE_FONT_HEIGHT + MARGIN_Y * 2
    RESULTS_Y = TIMER_Y + LARGE_FONT_HEIGHT + MARGIN_Y * 2
    
    def __init__(self):
        # ウィンドウサイズとタイトルの設定
        pyxel.init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 
                  title="Speedcube Timer", fps=self.FPS)
        
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

        # フォントの初期化
        self.middle_font = pyxel.Font(r"../../.venv/Lib/site-packages/pyxel/examples/assets/umplus_j10r.bdf")
        self.large_font = pyxel.Font(r"../../.venv/Lib/site-packages/pyxel/examples/assets/umplus_j12r.bdf")

        # Pyxelの実行
        pyxel.run(self.update, self.draw)

    def _start_timer(self):
        """タイマーを開始する共通処理"""
        self.state = TimerState.RUNNING
        self.timer_running = True
        self.start_time = pyxel.frame_count
        self.space_hold_start = 0  # スペースキー長押しの状態をリセット
        pyxel.play(0, 1)  # タイマー開始時にポーン音を再生

    def _should_play_beep(self, current_time: float, target_time: float) -> bool:
        """指定された時間の最初のフレームかどうかを判定"""
        frame_time = 1.0 / self.FPS
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
                    elif (pyxel.frame_count - self.space_hold_start) / self.FPS >= self.SPACE_HOLD_TIME:
                        # 長押しでインスペクションタイム開始
                        self.state = TimerState.COUNTDOWN
                        self.countdown_start = pyxel.frame_count
                        self.space_hold_start = 0  # space_hold_startを初期化
                else:
                    self.space_hold_start = 0

            case TimerState.COUNTDOWN:
                current_time = (pyxel.frame_count - self.countdown_start) / self.FPS
                
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
                    elif (pyxel.frame_count - self.space_hold_start) / self.FPS >= self.SPACE_HOLD_TIME:
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
            self.current_time = (pyxel.frame_count - self.start_time) / self.FPS

    def draw(self):
        pyxel.cls(1)

        match self.state:
            case TimerState.READY:
                # スクランブル表示（画面上部中央）
                pyxel.text(self.MARGIN_X, self.SCRAMBLE_Y, "Scramble:", 7, self.middle_font)
                pyxel.text(self.MARGIN_X, self.SCRAMBLE_TEXT_Y, self.scramble, 7, self.middle_font)
                
                # タイマー状態表示（画面中央）
                if self.space_hold_start > 0:
                    hold_time = (pyxel.frame_count - self.space_hold_start) / self.FPS
                    hold_x = (self.WINDOW_WIDTH - len(f"Hold: {hold_time:.1f}") * 
                             self.LARGE_FONT_WIDTH) // 2
                    pyxel.text(hold_x, self.TIMER_Y, f"Hold: {hold_time:.1f}", 
                             7, self.large_font)
                else:
                    hold_x = (self.WINDOW_WIDTH - len("Hold SPACE") * self.LARGE_FONT_WIDTH) // 2
                    pyxel.text(hold_x, self.TIMER_Y, "Hold SPACE", 7, self.large_font)

                # 記録表示（画面下部）
                self._draw_results()

            case TimerState.COUNTDOWN:
                # INSPECTIONを画面上部中央に表示
                inspection_x = (self.WINDOW_WIDTH - len("INSPECTION TIME") * 
                              self.LARGE_FONT_WIDTH) // 2
                pyxel.text(inspection_x, self.SCRAMBLE_Y, "INSPECTION TIME", 
                          7, self.large_font)
                
                # カウントダウンを画面中央に表示
                countdown_time = self.INSPECTION_TIME - (pyxel.frame_count - 
                               self.countdown_start) / self.FPS
                color = 8 if countdown_time <= 4 else 7
                time_x = (self.WINDOW_WIDTH - len(f"{countdown_time:.1f}") * 
                         self.LARGE_FONT_WIDTH) // 2
                pyxel.text(time_x, self.TIMER_Y, f"{countdown_time:.1f}", 
                          color, self.large_font)

                # 長押し状態表示（画面下部）
                if self.space_hold_start > 0:
                    hold_time = (pyxel.frame_count - self.space_hold_start) / self.FPS
                    pyxel.text(20, 200, f"Hold: {hold_time:.1f}", 7, self.middle_font)

            case TimerState.RUNNING:
                # タイム表示を画面中央に
                time_x = (self.WINDOW_WIDTH - len(f"{self.current_time:.2f}") * 
                         self.LARGE_FONT_WIDTH) // 2
                pyxel.text(time_x, self.TIMER_Y, f"{self.current_time:.2f}", 
                          7, self.large_font)

    def _draw_results(self):
        """記録表示の共通処理"""
        if not self.timer.results:
            return

        # 直近の記録（左下）
        pyxel.text(self.MARGIN_X, self.RESULTS_Y, "Recent", 7, self.middle_font)
        next_result_y = self.RESULTS_Y + self.MIDDLE_FONT_HEIGHT + self.FONT_SPACING
        
        for i, (_, time, solve_count) in enumerate(self.timer.get_recent_results()[:5]):
            pyxel.text(self.MARGIN_X, next_result_y, f"{solve_count}: {time:.2f}", 7,self.middle_font)
            next_result_y += self.MIDDLE_FONT_HEIGHT + self.FONT_SPACING
        
        # 平均の表示（右下）
        ao5 = self.stats.calculate_average(self.timer.results, 5)
        ao12 = self.stats.calculate_average(self.timer.results, 12)
        
        ao5_text = f"AO5: {ao5:.2f}" if ao5 else "AO5: -"
        ao12_text = f"AO12: {ao12:.2f}" if ao12 else "AO12: -"
        
        stats_x = self.WINDOW_WIDTH // 2 + self.MARGIN_X // 2
        pyxel.text(stats_x, self.RESULTS_Y, "Avarage of n", 7, self.middle_font)
        ao5_y = self.RESULTS_Y + self.MIDDLE_FONT_HEIGHT + self.FONT_SPACING
        ao12_y = ao5_y + self.MIDDLE_FONT_HEIGHT + self.FONT_SPACING
        pyxel.text(stats_x, ao5_y, ao5_text, 7, self.middle_font)
        pyxel.text(stats_x, ao12_y, ao12_text, 7, self.middle_font)

    def run(self):
        # メインループはpyxel.runで実行されるため、
        # このメソッドは互換性のために残しています
        pass