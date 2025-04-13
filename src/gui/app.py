"""スピードキューブタイマーのメインアプリケーション"""
import pyxel
from ..timer import SpeedcubeTimer
from ..speedcube_stats import SpeedcubeStats
from ..scramble import generate_wca_cube_scramble
from ..log_handler import SpeedcubeLogger
from .constants import DisplayConfig as DC, GameConfig as GC
from .constants import SoundConfig as SC
from .renderer import SpeedcubeRenderer
from .states import TimerState

class SpeedcubeApp:
    def __init__(self):
        # ウィンドウサイズとタイトルの設定
        pyxel.init(DC.WINDOW_WIDTH, DC.WINDOW_HEIGHT, 
                  title="Speedcube Timer", fps=DC.FPS)
        
        # load assets
        pyxel.load('speedcube_timer.pyxres')
        
        # コンポーネントの初期化
        self.timer = SpeedcubeTimer()
        self.stats = SpeedcubeStats()
        self.logger = SpeedcubeLogger()
        
        # 状態の初期化
        self.bg_color = DC.DEFAULT_BACKGROUND_COLOR
        self.text_color = DC.DEFAULT_TEXT_COLOR
        self.warning_color = DC.DEFAULT_WARNING_COLOR
        self.state = TimerState.READY
        self.space_hold_start = 0
        self.countdown_start = 0
        self.start_time = 0
        self.current_time = 0.0
        self.scramble = generate_wca_cube_scramble()
        
        # レンダラーの初期化（自身を渡す）
        self.renderer = SpeedcubeRenderer(self)

        # Pyxelの実行
        pyxel.run(self.update, self.draw)

    def update(self):
        """状態に応じた更新処理を実行"""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            
        if pyxel.btnp(pyxel.KEY_C):
            self.bg_color = (self.bg_color + 1) % 16
            self.text_color = 7 if self.bg_color < 6 else 0
        
        match self.state:
            case TimerState.READY:
                self._update_ready_state()
            case TimerState.COUNTDOWN:
                self._update_countdown_state()
            case TimerState.RUNNING:
                self._update_running_state()

    def draw(self):
        """描画処理を実行"""
        self.renderer.draw(self.state)

    def _update_ready_state(self):
        """READY状態の更新処理"""
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.space_hold_start == 0:
                self.space_hold_start = pyxel.frame_count
            elif (pyxel.frame_count - self.space_hold_start) / DC.FPS >= GC.SPACE_HOLD_TIME:
                self.state = TimerState.COUNTDOWN
                self.countdown_start = pyxel.frame_count
                pyxel.play(SC.BEEP_CHANNEL, SC.COIN_SOUND)
                self.space_hold_start = 0
        else:
            self.space_hold_start = 0

    def _update_countdown_state(self):
        """COUNTDOWN状態の更新処理"""
        current_time = (pyxel.frame_count - self.countdown_start) / DC.FPS
        
        self._play_countdown_beeps(current_time)
        
        if self._check_space_hold():
            self._start_timer()
            return

        if current_time >= GC.INSPECTION_TIME:
            self._start_timer()

    def _update_running_state(self):
        """RUNNING状態の更新処理"""
        self.current_time = (pyxel.frame_count - self.start_time) / DC.FPS
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._finish_solve()

    def _play_countdown_beeps(self, current_time: float):
        """カウントダウン音を再生"""
        for beep_time in GC.COUNTDOWN_BEEP_TIMES:
            target_time = GC.INSPECTION_TIME - beep_time
            if self._should_play_beep(current_time, target_time):
                pyxel.play(SC.BEEP_CHANNEL, SC.COUNTDOWN_SOUND)
                break

    def _check_space_hold(self) -> bool:
        """スペースキーの長押しを確認"""
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.space_hold_start == 0:
                self.space_hold_start = pyxel.frame_count
            elif (pyxel.frame_count - self.space_hold_start) / DC.FPS >= GC.SPACE_HOLD_TIME:
                return True
        else:
            self.space_hold_start = 0
        return False

    def _should_play_beep(self, current_time: float, target_time: float) -> bool:
        """指定された時間の最初のフレームかどうかを判定"""
        frame_time = 1.0 / DC.FPS
        return target_time <= current_time <= target_time + frame_time

    def _start_timer(self):
        """タイマーを開始する共通処理"""
        self.state = TimerState.RUNNING
        self.start_time = pyxel.frame_count
        self.space_hold_start = 0
        pyxel.play(SC.BEEP_CHANNEL, SC.START_SOUND)

    def _finish_solve(self):
        """ソルブ完了時の処理"""
        self.timer.add_result(self.scramble, self.current_time)
        self.logger.save_result(self.current_time)
        pyxel.play(SC.BEEP_CHANNEL, SC.FINISH_SOUND)
        self.scramble = generate_wca_cube_scramble()
        self.state = TimerState.READY