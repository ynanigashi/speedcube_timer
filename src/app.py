"""スピードキューブタイマーのメインアプリケーション"""
import pyxel
from .stats import SpeedcubeStats
from .scramble import generate_wca_cube_scramble
from .log_handler import SpeedcubeLogger
from .constants import DisplayConfig as DC, GameConfig as GC
from .constants import SoundConfig as SC
from .renderer import SpeedcubeRenderer
from .states import TimerState

class SpeedcubeApp:
    def __init__(self):
        # ウィンドウサイズとタイトルの設定
        pyxel.init(DC.WINDOW_WIDTH, DC.WINDOW_HEIGHT, 
                  title="Speedcube Timer", fps=DC.FPS,
                  quit_key=pyxel.KEY_END)
        
        # load assets
        pyxel.load('../data/speedcube_timer.pyxres')
        
        # コンポーネントの初期化
        self.logger = SpeedcubeLogger()
        self.stats = SpeedcubeStats(self.logger)  # ロガーを渡す
        
        # 状態の初期化
        self.bg_color = DC.DEFAULT_BACKGROUND_COLOR
        self.text_color = DC.DEFAULT_TEXT_COLOR
        self.warning_color = DC.DEFAULT_WARNING_COLOR
        self.state = TimerState.READY
        self.space_hold_start = 0
        self.s_key_hold_start = 0  # Sキー長押し開始時間を追加
        self.countdown_start = 0
        self.start_time = 0
        self.current_time = 0.0
        self.scramble = generate_wca_cube_scramble()
        self.finish_frame_count = 0  # 完了時刻を保存する変数を追加
        self.sync_result = None  # 同期結果を保存する変数を追加

        # レンダラーの初期化（自身を渡す）
        self.renderer = SpeedcubeRenderer(self)

        # Pyxelの実行
        pyxel.run(self.update, self.draw)

    def update(self):
        """状態に応じた更新処理を実行"""
        # ESCキーで終了        
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            result = self.logger.sync_data()
            print(result[1])
            pyxel.quit()
            
        if pyxel.btnp(pyxel.KEY_C):
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            self.bg_color = (self.bg_color + 1) % 16
            self.text_color = 7 if self.bg_color < 6 else 0
        
        match self.state:
            case TimerState.READY:
                self._update_ready_state()
            case TimerState.COUNTDOWN:
                self._update_countdown_state()
            case TimerState.RUNNING:
                self._update_running_state()
            case TimerState.SYNCING:
                self._update_syncing_state()
            
    def draw(self):
        """描画処理を実行"""
        self.renderer.draw(self.state)

    def _update_ready_state(self):
        """READY状態の更新処理"""
        # キー長押しの共通処理
        if self._handle_key_hold(pyxel.KEY_S, self.s_key_hold_start, 
                                TimerState.SYNCING, reset_attr='s_key_hold_start'):
            return
        
        if self._handle_key_hold(pyxel.KEY_SPACE, self.space_hold_start, 
                                TimerState.COUNTDOWN, extra_action=self._set_countdown_start,
                                reset_attr='space_hold_start'):
            return

    def _update_countdown_state(self):
        """COUNTDOWN状態の更新処理"""
        current_time = (pyxel.frame_count - self.countdown_start) / DC.FPS
        
        self._play_countdown_beeps(current_time)
        
        # インスペクション開始から一定時間はホールドチェックをスキップ
        if current_time <= GC.INSPECTION_GRACE_PERIOD:
            return
        
        # スペースキー長押しで計測開始
        if self._handle_key_hold(pyxel.KEY_SPACE, self.space_hold_start, 
                               None, extra_action=self._start_timer,
                               reset_attr='space_hold_start'):
            return

        if current_time >= GC.INSPECTION_TIME:
            self._start_timer()

    def _update_running_state(self):
        """RUNNING状態の更新処理"""
        self.current_time = (pyxel.frame_count - self.start_time) / DC.FPS
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._finish_solve()

    def _update_syncing_state(self):
        """SYNCING状態の更新処理"""
        # 初回のみ同期処理を実行
        if self.sync_result is None:
            self.sync_result = self.logger.sync_data()
            self.sync_end_frame = pyxel.frame_count  # 同期結果表示開始時間を記録
        
        # 結果表示から1秒経過したらREADY状態に戻る
        if (pyxel.frame_count - self.sync_end_frame) > DC.FPS*1.5:
            self.sync_result = None
            self.state = TimerState.READY
        
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
        #BEEP_CHANNELはReadystateで使用されているので、SOUND_CHANNELを使用
        pyxel.play(SC.SOUND_CHANNEL, SC.FINISH_SOUND)
        self.finish_frame_count = pyxel.frame_count
        self.logger.save_result(self.current_time, self.scramble)
        self.stats.update_stats()
        self.scramble = generate_wca_cube_scramble()
        self.state = TimerState.READY

    def _handle_key_hold(self, key, hold_start_attr, next_state, extra_action=None, reset_attr=None):
        """キーの長押し処理を汎用化したメソッド
        
        Args:
            key: チェックするキー (pyxel.KEY_*)
            hold_start_attr: 長押し開始時間を保持する属性名
            next_state: 長押し後に遷移する状態
            extra_action: 状態遷移前に実行する追加のアクション関数
            reset_attr: リセットする属性名
            
        Returns:
            bool: キー長押しによる状態遷移が発生した場合True
        """
        hold_start = getattr(self, reset_attr)
        
        if pyxel.btn(key):
            if hold_start == 0:
                setattr(self, reset_attr, pyxel.frame_count)
                pyxel.play(SC.BEEP_CHANNEL, SC.HOLD_SOUND)  # ホールド開始時にサウンド再生
            elif (pyxel.frame_count - hold_start) / DC.FPS >= GC.BUTTON_HOLD_TIME:
                self.state = next_state
                pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
                setattr(self, reset_attr, 0)
                
                # 追加のアクションがあれば実行
                if extra_action:
                    extra_action()
                    
                return True
        else:
            if hold_start > 0:
                pyxel.stop(SC.BEEP_CHANNEL)  # ホールド解除時にサウンド停止
            setattr(self, reset_attr, 0)
        
        return False

    def _set_countdown_start(self):
        """カウントダウン開始時間をセット"""
        self.countdown_start = pyxel.frame_count