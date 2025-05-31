"""タイマー状態ハンドラクラス群

各タイマー状態に対応する処理を管理するハンドラクラスを定義します。
これにより、状態管理ロジックがより整理され、保守性と拡張性が向上します。
"""
from abc import ABC, abstractmethod
import pyxel
from .states import TimerState
from .constants import DisplayConfig as DC, GameConfig as GC
from .constants import SoundConfig as SC
from .scramble import generate_wca_cube_scramble


class BaseStateHandler(ABC):
    """状態ハンドラの基底クラス"""
    
    def __init__(self, app):
        """
        Args:
            app: SpeedcubeAppインスタンス
        """
        self.app = app
    
    @abstractmethod
    def update(self):
        """状態の更新処理"""
        pass
    
    def _handle_key_hold(self, key, hold_start_attr, next_state,
                         change_sound, extra_action=None, reset_attr=None):
        """キーの長押し処理を汎用化したメソッド
        
        Args:
            key: チェックするキー (pyxel.KEY_*)
            hold_start_attr: 長押し開始時間を保持する属性名（廃止予定、reset_attrを使用）
            next_state: 長押し後に遷移する状態
            change_sound: 状態遷移時に再生するサウンド
            extra_action: 状態遷移前に実行する追加のアクション関数
            reset_attr: リセットする属性名
            
        Returns:
            bool: キー長押しによる状態遷移が発生した場合True
        """
        # 後方互換性のため、reset_attrが指定されていない場合はhold_start_attrを使用
        attr_name = reset_attr if reset_attr else hold_start_attr
        hold_start = getattr(self.app, attr_name)
        
        if pyxel.btn(key):
            if hold_start == 0:
                setattr(self.app, attr_name, pyxel.frame_count)
                # ホールド開始時にサウンド再生
                pyxel.play(SC.BEEP_CHANNEL, SC.HOLD_SOUND)
            elif ((pyxel.frame_count - hold_start) / DC.FPS >=
                  GC.BUTTON_HOLD_TIME):
                self.app.state = next_state
                # 状態遷移時にサウンド再生
                pyxel.play(SC.BEEP_CHANNEL, change_sound)
                setattr(self.app, attr_name, 0)
                
                # 追加のアクションがあれば実行
                if extra_action:
                    extra_action()
                    
                return True
        else:
            if hold_start > 0:
                pyxel.stop(SC.BEEP_CHANNEL)  # ホールド解除時にサウンド停止
            setattr(self.app, attr_name, 0)
        
        return False


class ReadyStateHandler(BaseStateHandler):
    """READY状態のハンドラ"""
    
    def update(self):
        """READY状態の更新処理"""
        # キー長押しの共通処理
        if self._handle_key_hold(
            pyxel.KEY_S,
            's_key_hold_start',
            TimerState.SYNCING,
            SC.SYNC_SOUND,
            reset_attr='s_key_hold_start'
        ):
            return
        
        if self._handle_key_hold(
            pyxel.KEY_SPACE,
            'space_hold_start',
            TimerState.COUNTDOWN,
            SC.CHANGE_SOUND,
            extra_action=self._set_countdown_start,
            reset_attr='space_hold_start'
        ):
            return
    
    def _set_countdown_start(self):
        """カウントダウン開始時間をセット"""
        self.app.countdown_start = pyxel.frame_count


class CountdownStateHandler(BaseStateHandler):
    """COUNTDOWN状態のハンドラ"""
    
    def update(self):
        """COUNTDOWN状態の更新処理"""
        current_time = (pyxel.frame_count - self.app.countdown_start) / DC.FPS
        
        self._play_countdown_beeps(current_time)

        # インスペクション開始から一定時間はホールドチェックを
        # スキップ
        if current_time <= GC.INSPECTION_GRACE_PERIOD:
            return
          # スペースキー長押しで計測開始
        if self._handle_key_hold(
            pyxel.KEY_SPACE,
            'space_hold_start',
            None,
            SC.CHANGE_SOUND,
            extra_action=self._start_timer,
            reset_attr='space_hold_start'
        ):
            return

        if current_time >= GC.INSPECTION_TIME:
            self._start_timer()
    
    def _play_countdown_beeps(self, current_time: float):
        """カウントダウン音を再生"""
        for beep_time in GC.COUNTDOWN_BEEP_TIMES:
            target_time = GC.INSPECTION_TIME - beep_time
            if self._should_play_beep(current_time, target_time):
                pyxel.play(SC.BEEP_CHANNEL, SC.COUNTDOWN_SOUND)
                break
    
    def _should_play_beep(self, current_time: float,
                          target_time: float) -> bool:
        """指定された時間の最初のフレームかどうかを判定"""
        frame_time = 1.0 / DC.FPS
        return target_time <= current_time <= target_time + frame_time
    
    def _start_timer(self):
        """タイマーを開始する共通処理"""
        self.app.state = TimerState.RUNNING
        self.app.start_time = pyxel.frame_count
        self.app.space_hold_start = 0
        pyxel.play(SC.BEEP_CHANNEL, SC.START_SOUND)


class RunningStateHandler(BaseStateHandler):
    """RUNNING状態のハンドラ"""
    
    def update(self):
        """RUNNING状態の更新処理"""
        self.app.current_time = (pyxel.frame_count - self.app.start_time) / DC.FPS
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._finish_solve()
    
    def _finish_solve(self):
        """ソルブ完了時の処理"""
        # BEEP_CHANNELはReadystateで使用されているため、SOUND_CHANNELを使用
        pyxel.play(SC.SOUND_CHANNEL, SC.FINISH_SOUND)
        self.app.finish_frame_count = pyxel.frame_count
        self.app.logger.save_result(self.app.current_time, self.app.scramble)
        self.app.stats.update_stats()
        self.app.scramble = generate_wca_cube_scramble()
        self.app.state = TimerState.READY


class SyncingStateHandler(BaseStateHandler):
    """SYNCING状態のハンドラ"""
    
    def update(self):
        """SYNCING状態の更新処理"""
        # 初回のみ同期処理を実行
        if self.app.sync_result is None:
            self.app.sync_result = self.app.logger.sync_data()
            # 同期結果表示開始時間を記録
            self.app.sync_end_frame = pyxel.frame_count
        # 結果表示から1秒経過したらREADY状態に戻る
        if (pyxel.frame_count - self.app.sync_end_frame) > DC.FPS * 1.5:
            self.app.sync_result = None
            self.app.state = TimerState.READY


class StateHandlerManager:
    """状態ハンドラを管理するマネージャークラス"""
    
    def __init__(self, app):
        """
        Args:
            app: SpeedcubeAppインスタンス
        """
        self.app = app
        self.handlers = {
            TimerState.READY: ReadyStateHandler(app),
            TimerState.COUNTDOWN: CountdownStateHandler(app),
            TimerState.RUNNING: RunningStateHandler(app),
            TimerState.SYNCING: SyncingStateHandler(app)
        }
    
    def update(self):
        """現在の状態に対応するハンドラの更新処理を実行"""
        handler = self.handlers.get(self.app.state)
        if handler:
            handler.update()
