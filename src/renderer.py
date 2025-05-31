"""スピードキューブタイマーの描画処理を管理するクラス"""
import pyxel
from .states import TimerState
from .constants import DisplayConfig as DC, GameConfig as GC, TextConstants as TC

class SpeedcubeRenderer:
    def __init__(self, app):
    # フォントの初期化
        self.middle_font = pyxel.Font(DC.MIDDLE_FONT_FILE)
        self.large_font = pyxel.Font(DC.LARGE_FONT_FILE)
        
        # アプリケーションの参照を保持
        self.app = app
        
    def draw(self):
        """状態に応じた描画処理"""
        # 背景を描画
        pyxel.cls(self.app.bg_color)
        
        # 状態に応じた描画処理
        match self.app.state:
            case TimerState.READY:
                self._draw_ready_state()
            case TimerState.COUNTDOWN:
                self._draw_countdown_state()
            case TimerState.RUNNING:
                self._draw_running_state()
            case TimerState.SYNCING:
                self._draw_syncing_state()
        
        # 共通UI要素の描画
        self._draw_common_elements()
    
    def _draw_ready_state(self):
        """READY状態の描画"""
        self._draw_scramble(self.app.scramble)
        self._draw_hold_text()
        self._draw_hold_status()
        self._draw_results(self.app.stats)

    def _draw_countdown_state(self):
        """COUNTDOWN状態の描画"""
        # インスペクションヘッダー
        inspection_x = (DC.WINDOW_WIDTH - len(TC.INSPECTION) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(inspection_x, DC.SCRAMBLE_Y, TC.INSPECTION, self.app.text_color, self.large_font)
          # カウントダウン表示
        countdown_time = GC.INSPECTION_TIME - (pyxel.frame_count - self.app.countdown_start) / DC.FPS
        color = DC.DEFAULT_WARNING_COLOR if countdown_time <= 4 else self.app.text_color
        time_x = (DC.WINDOW_WIDTH - len(f"{countdown_time:.1f}") * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(time_x, DC.TIMER_Y, f"{countdown_time:.1f}", color, self.large_font)
        
        # ホールド状態の描画
        self._draw_hold_status()

    def _draw_running_state(self):
        """RUNNING状態の描画"""
        # 停止方法表示
        press_space_x = (DC.WINDOW_WIDTH - len(TC.PRESS_SPACE) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(press_space_x, DC.SCRAMBLE_Y, TC.PRESS_SPACE, 
                   self.app.text_color, self.middle_font)
        
        # 経過時間表示
        time_x = (DC.WINDOW_WIDTH - len(f"{self.app.current_time:.2f}") * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(time_x, DC.TIMER_Y, f"{self.app.current_time:.2f}", 
                   self.app.text_color, self.large_font)

    def _draw_syncing_state(self):
        """同期中の描画処理"""
        # 同期状態のメッセージ
        if self.app.sync_result is None:
            status_text = "Data is syncing..."
            success = None
        else:
            success, message = self.app.sync_result
            status_text = message
            
        # ステータスメッセージの描画
        pyxel.text(
            DC.WINDOW_WIDTH // 2 - len(status_text) * 2,
            DC.WINDOW_HEIGHT // 2,
            status_text,
            self.app.text_color if success is None or success else self.app.warning_color
        )

    def _draw_common_elements(self):
        """共通UI要素の描画処理"""
        self._draw_quit_message()

    def _draw_scramble(self, scramble: str):
        """スクランブルの描画"""
        pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_Y, TC.SCRAMBLE, 
                  self.app.text_color, self.middle_font)
        pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y, scramble, 
                  self.app.text_color, self.middle_font)

    def _draw_hold_status(self):
        """ホールド状態の描画"""
        # スペースキーがホールドされている場合の処理
        if self.app.space_hold_start > 0:
            self._draw_progress_circle()

        if self.app.s_key_hold_start > 0:
            self._draw_s_key_arrow()
            

    def _draw_hold_text(self):
        # ホールド指示テキストの表示
        hold_x = (DC.WINDOW_WIDTH - len(TC.HOLD_INSTRUCTION) * DC.LARGE_FONT_WIDTH) // 2
        if self.app.space_hold_start > 0 or pyxel.frame_count % DC.BLINK_CYCLE < DC.BLINK_ON_TIME:
            pyxel.text(hold_x, DC.TIMER_Y, TC.HOLD_INSTRUCTION, 
                       self.app.text_color, self.large_font)

    def _draw_hold_time(self):
        """ホールド時間の描画"""
        hold_time = (pyxel.frame_count - self.app.space_hold_start) / DC.FPS
        hold_text = TC.HOLD_FORMAT.format(hold_time)
        hold_x = (DC.WINDOW_WIDTH - len(hold_text) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(hold_x, DC.RESULTS_Y, hold_text, 
                   self.app.text_color, self.middle_font)

    def _draw_results(self, stats):
        """記録表示の共通処理"""
        if not stats.session_results:
            return
        
        self._draw_recent_results(stats)
        self._draw_averages(stats)

    def _draw_recent_results(self, stats):
        """直近の記録表示"""
        pyxel.text(DC.MARGIN_X, DC.RESULTS_Y, TC.RECENT, 
                   self.app.text_color, self.middle_font)
        next_result_y = DC.RESULTS_Y + DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y
        
        # session_resultsの形式は(scramble, time_result, id)のリスト
        for solve_id, time_result, _, _ in stats.session_results[:5]:
            result_text = TC.SOLVE_FORMAT.format(solve_id, time_result)
            pyxel.text(DC.MARGIN_X, next_result_y, result_text, 
                       self.app.text_color, self.middle_font)
            next_result_y += DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y

    def _draw_averages(self, stats):
        """平均値の表示"""
        # statsクラスから直接統計情報を取得
        ao5 = stats.ao5
        ao12 = stats.ao12
        
        ao5_text = TC.AO5_FORMAT.format(ao5) if ao5 else TC.AO_EMPTY.format("AO5")
        ao12_text = TC.AO12_FORMAT.format(ao12) if ao12 else TC.AO_EMPTY.format("AO12")
        
        stats_x = DC.WINDOW_WIDTH // 2 + DC.MARGIN_X // 2
        pyxel.text(stats_x, DC.RESULTS_Y, TC.AVERAGE, 
                   self.app.text_color, self.middle_font)
        ao5_y = DC.RESULTS_Y + DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y
        ao12_y = ao5_y + DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y
        pyxel.text(stats_x, ao5_y, ao5_text, 
                   self.app.text_color, self.middle_font)
        pyxel.text(stats_x, ao12_y, ao12_text, 
                   self.app.text_color, self.middle_font)

    def _draw_quit_message(self):
        """終了メッセージの描画"""
        quit_x = DC.WINDOW_WIDTH - len(TC.QUIT) * DC.SMALL_FONT_WIDTH - DC.MARGIN_X
        quit_y = DC.WINDOW_HEIGHT - DC.SMALL_FONT_HEIGHT
        pyxel.text(quit_x, quit_y, TC.QUIT, self.app.text_color)

    def _draw_progress_circle(self):
        """ホールド進捗を示す円を描画"""
        if self.app.space_hold_start <= 0:
            return
            
        # 円の中心座標
        center_x = DC.WINDOW_WIDTH // 2
        center_y = DC.WINDOW_HEIGHT // 2
        
        # ホールド時間に基づいて円の半径を計算
        hold_time = (pyxel.frame_count - self.app.space_hold_start) / DC.FPS
        max_radius = min(DC.WINDOW_WIDTH, DC.WINDOW_HEIGHT) // 2
        radius = min(int(hold_time * 100), max_radius)
        
        # 円を描画
        pyxel.circ(center_x, center_y, radius, self.app.text_color)

    def _draw_s_key_arrow(self):
        """Sキーがホールドされている時に上昇矢印を描画"""
        if not hasattr(self.app, 's_key_hold_start') or self.app.s_key_hold_start <= 0:
            return
        
        # ホールド時間を計算
        hold_time = (pyxel.frame_count - self.app.s_key_hold_start) / DC.FPS
        
        # 矢印の基本パラメータ
        arrow_width = DC.WINDOW_WIDTH // 2  # 矢印の幅
        arrow_height = DC.WINDOW_HEIGHT // 1.2  # 矢印の高さ
        
        # ホールド時間に基づいて矢印の位置を計算
        travel_distance = DC.WINDOW_HEIGHT * hold_time
        
        # 矢印の現在のY座標を計算
        current_y = DC.WINDOW_HEIGHT - travel_distance
        
        # 矢印の中心X座標
        center_x = DC.WINDOW_WIDTH // 2
        
        # 矢印の描画
        # 矢印の本体（三角形）
        pyxel.tri(
            center_x, current_y,  # 頂点
            center_x - arrow_width // 2, current_y + arrow_height // 2,  # 左下
            center_x + arrow_width // 2, current_y + arrow_height // 2,  # 右下
            self.app.text_color
        )
        
        # 矢印の柄部分（長方形）
        rect_width = arrow_width // 4
        rect_height = arrow_height // 2
        pyxel.rect(
            center_x - rect_width // 2,
            current_y + arrow_height // 2,
            rect_width,
            rect_height,
            self.app.text_color
        )