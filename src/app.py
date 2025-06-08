"""スピードキューブタイマーのメインアプリケーション"""
import pyxel
from .stats import SpeedcubeStats
from .scramble import generate_wca_cube_scramble
from .log_handler import SpeedcubeLogger
from .constants import DisplayConfig as DC, GameConfig as GC
from .constants import SoundConfig as SC
from .renderer import SpeedcubeRenderer
from .states import TimerState
from .state_handlers import StateHandlerManager


class SpeedcubeApp:
    def __init__(self):
        # ウィンドウサイズとタイトルの設定
        pyxel.init(
            DC.WINDOW_WIDTH,
            DC.WINDOW_HEIGHT,
            title="Speedcube Timer",
            fps=DC.FPS,
            quit_key=pyxel.KEY_END
        )
        # アセットの読み込み
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
        self.sync_end_frame = 0  # 同期終了フレームを保存する変数を追加
        
        # 月次統計キャッシュ（STATS状態初回時のみ計算）
        self.monthly_stats_cache = None  # (solve_count, avg_time) のタプル
        
        # 状態ハンドラマネージャーの初期化
        self.state_handler_manager = StateHandlerManager(self)
        
        # レンダラーの初期化（自身を渡す）
        self.renderer = SpeedcubeRenderer(self)

        # Pyxelの実行
        pyxel.run(self.update, self.draw)

    def update(self):
        """状態に応じた更新処理を実行"""        # ESCキーで終了
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            result = self.logger.sync_data()
            print(result[1])
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_C):
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            self.bg_color = (self.bg_color + 1) % 16
            self.text_color = 7 if self.bg_color < 6 else 0

        # 状態ハンドラマネージャーを使用して状態更新を委譲
        self.state_handler_manager.update()
            
    def draw(self):
        """描画処理を実行"""
        self.renderer.draw()

    def run(self):
        """アプリケーションを実行"""
        pass  # pyxel.runは__init__で既に呼ばれている