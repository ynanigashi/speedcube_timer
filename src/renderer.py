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
            case TimerState.STATS:
                self._draw_stats_state()
            case TimerState.PATTERN_LIST_SELECT:
                self._draw_pattern_list_select()
            case TimerState.PATTERN_ALGORITHM_SELECT:
                self._draw_algorithm_select()
            case TimerState.PATTERN_READY:
                self._draw_pattern_ready()
            case TimerState.PATTERN_FINISH:
                self._draw_pattern_finish()
        
        # 共通UI要素の描画
        self._draw_common_elements()
    
    def _draw_ready_state(self):
        """READY状態の描画"""
        self._draw_scramble(self.app.scramble)
        self._draw_hold_text()
        self._draw_hold_status()
        self._draw_results(self.app.stats)
        self._draw_ready_instructions()

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
        # パターンモードかどうかを判定
        is_pattern_mode = hasattr(self.app, 'current_pattern') and self.app.current_pattern is not None
        
        if is_pattern_mode:
            # パターンモード：パターン情報を表示
            pattern_text = f"{self.app.current_pattern.name}"
            pattern_x = DC.MARGIN_X
            pyxel.text(pattern_x, DC.SCRAMBLE_Y, pattern_text, 
                      self.app.text_color, self.middle_font)
            
            # アルゴリズム情報を表示
            if hasattr(self.app, 'current_algorithm') and self.app.current_algorithm:
                algo_text = f"{self.app.current_algorithm.name}: {self.app.current_algorithm.moves}"
                pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y, algo_text, 
                          self.app.text_color, self.middle_font)
        else:
            # 通常モード：停止方法表示
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
            status_text,            self.app.text_color if success is None or success else self.app.warning_color
        )

    def _draw_stats_state(self):
        """STATS状態の描画"""
        # ヘッダー
        header_text = "MONTHLY STATISTICS"
        header_x = (DC.WINDOW_WIDTH - len(header_text) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(header_x, DC.SCRAMBLE_Y, header_text, self.app.text_color, self.large_font)
        
        # キャッシュされた月次統計情報を使用
        if self.app.monthly_stats_cache is not None:
            monthly_solve_count, monthly_avg_time = self.app.monthly_stats_cache
        else:
            # キャッシュがない場合のフォールバック（通常は発生しない）
            monthly_solve_count = 0
            monthly_avg_time = None
        
        # 表示する統計情報
        y_pos = DC.SCRAMBLE_TEXT_Y + DC.MARGIN_Y * 2
        
        # 月次ソルブ数
        solve_count_text = f"This Month Solves: {monthly_solve_count}"
        pyxel.text(DC.MARGIN_X, y_pos, solve_count_text, self.app.text_color, self.middle_font)
        y_pos += DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y * 2
        
        # 月次平均時間
        if monthly_avg_time is not None:
            avg_time_text = f"This Month Average: {monthly_avg_time:.2f}s"
        else:
            avg_time_text = "This Month Average: -"
        pyxel.text(DC.MARGIN_X, y_pos, avg_time_text, self.app.text_color, self.middle_font)
        y_pos += DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y * 3
        
        # 現在のセッション統計
        session_stats = self.app.stats.get_stats_summary()
        session_text = f"Session Solves: {session_stats['solve_count']}"
        pyxel.text(DC.MARGIN_X, y_pos, session_text, self.app.text_color, self.middle_font)
        y_pos += DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y
        
        if session_stats['best_time'] is not None:
            best_text = f"Session Best: {session_stats['best_time']:.2f}s"
        else:
            best_text = "Session Best: -"
        pyxel.text(DC.MARGIN_X, y_pos, best_text, self.app.text_color, self.middle_font)
        y_pos += DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y
        
        if session_stats['session_avg'] is not None:
            session_avg_text = f"Session Average: {session_stats['session_avg']:.2f}s"
        else:
            session_avg_text = "Session Average: -"
        pyxel.text(DC.MARGIN_X, y_pos, session_avg_text, self.app.text_color, self.middle_font)
          # 操作説明
        self._draw_instruction_text("PRESS [<-] TO BACK")

    def _draw_ready_instructions(self):
        """READY状態での操作説明を描画"""
        self._draw_instruction_text("PRESS [->] FOR STATS, [P] FOR PATTERN, [ESC] FOR NEW SCRAMBLE, [Q] TO QUIT")

    def _draw_instruction_text(self, text: str):
        """指示テキストを画面下部に描画する共通メソッド
        
        Args:
            text: 表示するテキスト
        """
        # 画面下部中央に配置
        instruction_x = DC.MARGIN_X
        instruction_y = DC.WINDOW_HEIGHT - DC.SMALL_FONT_HEIGHT
        pyxel.text(instruction_x, instruction_y, text, self.app.text_color)

    def _draw_common_elements(self):
        """共通UI要素の描画処理"""
        pass  # 共通要素が必要になったらここに追加

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
    
    # ========================================
    # パターン習得モード用描画メソッド（Phase 2）
    # ========================================
    
    def _draw_pattern_list_select(self):
        """パターン一覧選択画面の描画"""
        # ヘッダー
        header_text = "PATTERN PRACTICE"
        header_x = (DC.WINDOW_WIDTH - len(header_text) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(header_x, DC.SCRAMBLE_Y, header_text, self.app.text_color, self.large_font)
        
        # カテゴリタブの表示（RAND/PLL/OLL）
        tab_y = DC.SCRAMBLE_Y + DC.LARGE_FONT_HEIGHT + DC.FONT_SPACING_Y
        tab_x = DC.MARGIN_X
        
        categories = self.app.pattern_db.get_available_categories()  # [OLL, PLL]
        
        # RANDタブ（最初）
        rand_color = DC.DEFAULT_WARNING_COLOR if self.app.selected_category_tab == 0 else self.app.text_color
        rand_tab_text = "[RAND]"
        pyxel.text(tab_x, tab_y, rand_tab_text, rand_color, self.middle_font)
        tab_x += len(rand_tab_text) * DC.MIDDLE_FONT_WIDTH + DC.MARGIN_X
        
        # PLLタブ（2番目）
        pll_color = DC.DEFAULT_WARNING_COLOR if self.app.selected_category_tab == 1 else self.app.text_color
        pll_count = self.app.pattern_db.get_category_count(categories[1])  # PLL
        pll_tab_text = f"[{categories[1].value}:{pll_count}]"
        pyxel.text(tab_x, tab_y, pll_tab_text, pll_color, self.middle_font)
        tab_x += len(pll_tab_text) * DC.MIDDLE_FONT_WIDTH + DC.MARGIN_X
        
        # OLLタブ（3番目）
        oll_color = DC.DEFAULT_WARNING_COLOR if self.app.selected_category_tab == 2 else self.app.text_color
        oll_count = self.app.pattern_db.get_category_count(categories[0])  # OLL
        oll_tab_text = f"[{categories[0].value}:{oll_count}]"
        pyxel.text(tab_x, tab_y, oll_tab_text, oll_color, self.middle_font)
        
        # RANDタブ選択時は専用UIを表示
        if self.app.selected_category_tab == 0:
            self._draw_rand_tab_content(tab_y)
            return
        
        # パターンデータベースから選択されたカテゴリのパターンを取得
        if not hasattr(self.app, 'pattern_db'):
            return
        
        # selected_category_tab: 0=RAND, 1=PLL, 2=OLL
        category_index = 2 - self.app.selected_category_tab  # 1->1(PLL), 2->0(OLL)
        selected_category = categories[category_index]
        patterns = self.app.pattern_db.get_patterns_by_category(selected_category)
        selected_index = getattr(self.app, 'selected_pattern_index', 0)
        scroll_offset = getattr(self.app, 'pattern_list_scroll_offset', 0)
        
        # 表示領域の計算
        start_y = tab_y + DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y
        max_y = DC.WINDOW_HEIGHT - DC.SMALL_FONT_HEIGHT - DC.MARGIN_Y * 2
        available_height = max_y - start_y
        
        # 1パターンあたりの高さ（パターン名 + アルゴリズム名 + スペース）
        item_height = DC.MIDDLE_FONT_HEIGHT * 2 + DC.FONT_SPACING_Y * 2
        max_visible_items = available_height // item_height
        
        # 表示範囲を計算
        start_index = scroll_offset
        end_index = min(start_index + max_visible_items, len(patterns))
        
        # パターン一覧を描画
        y_pos = start_y
        for i in range(start_index, end_index):
            pattern = patterns[i]
            
            # 選択中のパターンをハイライト
            color = DC.DEFAULT_WARNING_COLOR if i == selected_index else self.app.text_color
            
            # 統計情報を取得
            count = self.app.stats.get_pattern_count(pattern.id)
            best = self.app.stats.get_pattern_best(pattern.id)
            best_text = f"{best:.2f}s" if best is not None else "---"
            
            # パターン名と統計を1行で表示
            pattern_text = f"{i + 1}. {pattern.name}  ×{count}  {best_text}"
            pyxel.text(DC.MARGIN_X, y_pos, pattern_text, color, self.middle_font)
            
            # 現在選択されているアルゴリズムを表示
            selected_algo_id = self.app.stats.get_user_selected_algorithm(pattern.id)
            if selected_algo_id:
                algorithms = self.app.pattern_db.get_algorithms_for_pattern(pattern.id)
                selected_algo = next((a for a in algorithms if a.id == selected_algo_id), None)
                if selected_algo:
                    algo_text = f"  ({selected_algo.name})"
                else:
                    algo_text = "  (Default)"
            else:
                # デフォルトアルゴリズムを表示
                default_algo = self.app.pattern_db.get_default_algorithm(pattern.id)
                algo_text = f"  ({default_algo.name if default_algo else 'None'})"
            
            pyxel.text(DC.MARGIN_X + 10, y_pos + DC.MIDDLE_FONT_HEIGHT + 2, 
                      algo_text, color, None)
            
            y_pos += item_height
        
        # スクロールインジケータ（必要な場合）
        if len(patterns) > max_visible_items:
            indicator_text = f"({start_index + 1}-{end_index}/{len(patterns)})"
            indicator_x = DC.WINDOW_WIDTH - len(indicator_text) * DC.SMALL_FONT_WIDTH - DC.MARGIN_X
            indicator_y = start_y - DC.SMALL_FONT_HEIGHT - 2
            pyxel.text(indicator_x, indicator_y, indicator_text, self.app.text_color)
        
        # 操作説明
        self._draw_instruction_text("PRESS [TAB] TO SWITCH CATEGORY, [ENTER] TO START, [A] TO CHANGE, [ESC] TO BACK")
    
    def _draw_rand_tab_content(self, tab_y):
        """RANDタブのコンテンツを描画"""
        start_y = tab_y + DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y * 2
        
        # タイトル
        title_text = "RANDOM PRACTICE MODE"
        title_x = (DC.WINDOW_WIDTH - len(title_text) * DC.MIDDLE_FONT_WIDTH) // 2
        pyxel.text(title_x, start_y, title_text, self.app.text_color, self.middle_font)
        
        # カテゴリ選択
        category_y = start_y + DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y * 3
        
        categories = ["OLL", "PLL", "ALL"]
        for i, cat in enumerate(categories):
            color = DC.DEFAULT_WARNING_COLOR if cat == self.app.random_category else self.app.text_color
            
            # カテゴリごとの件数を表示
            if cat == "OLL":
                from .patterns import PatternCategory
                count = self.app.pattern_db.get_category_count(PatternCategory.OLL)
            elif cat == "PLL":
                from .patterns import PatternCategory
                count = self.app.pattern_db.get_category_count(PatternCategory.PLL)
            else:  # ALL
                count = self.app.pattern_db.get_pattern_count()
            
            cat_text = f"{cat} ({count} patterns)"
            cat_x = (DC.WINDOW_WIDTH - len(cat_text) * DC.MIDDLE_FONT_WIDTH) // 2
            y = category_y + i * (DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y)
            
            # 選択中のカテゴリにマーカーを表示
            if cat == self.app.random_category:
                marker_x = cat_x - DC.MIDDLE_FONT_WIDTH * 2
                pyxel.text(marker_x, y, ">", color, self.middle_font)
            
            pyxel.text(cat_x, y, cat_text, color, self.middle_font)
        
        # 説明テキスト
        info_y = category_y + len(categories) * (DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y) + DC.MARGIN_Y * 2
        info_text = "Select category and press ENTER to start"
        info_x = (DC.WINDOW_WIDTH - len(info_text) * 5) // 2  # 小さいフォント想定
        pyxel.text(info_x, info_y, info_text, self.app.text_color)
        
        # 重複回避の説明
        note_y = info_y + DC.SMALL_FONT_HEIGHT + DC.MARGIN_Y
        note_text = "* Last 5 patterns will be avoided"
        note_x = (DC.WINDOW_WIDTH - len(note_text) * 5) // 2
        pyxel.text(note_x, note_y, note_text, self.app.text_color)
        
        # 操作説明
        self._draw_instruction_text("PRESS [UP/DOWN] TO SELECT, [ENTER] TO START, [TAB] TO SWITCH TAB, [ESC] TO BACK")
    
    def _draw_algorithm_select(self):
        """アルゴリズム選択画面の描画"""
        # ヘッダー
        header_text = "SELECT ALGORITHM"
        header_x = (DC.WINDOW_WIDTH - len(header_text) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(header_x, DC.SCRAMBLE_Y, header_text, self.app.text_color, self.large_font)
        
        # 現在のパターン名
        if hasattr(self.app, 'current_pattern') and self.app.current_pattern:
            pattern_text = f"Pattern: {self.app.current_pattern.name}"
            pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y, pattern_text, 
                      self.app.text_color, self.middle_font)
        
        # アルゴリズム一覧
        y_pos = DC.SCRAMBLE_TEXT_Y + DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y * 2
        
        if hasattr(self.app, 'available_algorithms'):
            algorithms = self.app.available_algorithms
            selected_index = getattr(self.app, 'selected_algorithm_index', 0)
            
            for i, algo in enumerate(algorithms):
                # 選択中のアルゴリズムをハイライト
                color = DC.DEFAULT_WARNING_COLOR if i == selected_index else self.app.text_color
                
                # アルゴリズム名
                algo_text = f"{i + 1}. {algo.name}"
                pyxel.text(DC.MARGIN_X, y_pos, algo_text, color, self.middle_font)
                
                # 手順（長い場合は省略）
                moves_text = algo.moves if len(algo.moves) < 40 else algo.moves[:37] + "..."
                pyxel.text(DC.MARGIN_X + 10, y_pos + DC.MIDDLE_FONT_HEIGHT + 2, 
                          moves_text, color, None)
                
                # 評価があれば表示
                rating, notes = self.app.stats.get_algorithm_rating(algo.id)
                if rating:
                    rating_text = f"  Rating: {'★' * rating}"
                    pyxel.text(DC.MARGIN_X + 10, y_pos + DC.MIDDLE_FONT_HEIGHT * 2 + 4, 
                              rating_text, color, None)
                    y_pos += DC.MIDDLE_FONT_HEIGHT * 3 + DC.FONT_SPACING_Y
                else:
                    y_pos += DC.MIDDLE_FONT_HEIGHT * 2 + DC.FONT_SPACING_Y * 2
        
        # 操作説明
        self._draw_instruction_text("PRESS [ENTER] TO SELECT, [ESC] TO BACK")
    
    def _draw_pattern_ready(self):
        """パターン練習準備画面の描画"""
        # パターン情報
        if hasattr(self.app, 'current_pattern') and self.app.current_pattern:
            # パターン名
            pattern_text = f"Pattern: {self.app.current_pattern.name}"
            pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_Y, pattern_text, 
                      self.app.text_color, self.large_font)
            
            # アルゴリズム情報
            if hasattr(self.app, 'current_algorithm') and self.app.current_algorithm:
                algo_text = f"Algorithm: {self.app.current_algorithm.name}"
                pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y, 
                          algo_text, self.app.text_color, self.middle_font)
                
                moves_text = f"{self.app.current_algorithm.moves}"
                pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y + DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y, 
                          moves_text, self.app.text_color, self.middle_font)
        
        # ホールド指示
        self._draw_hold_text()
        self._draw_hold_status()
        
        # 操作説明
        self._draw_instruction_text("PRESS [SPACE] TO START, [ESC] TO BACK")
        self._draw_hold_status()
        
        # 操作説明
        self._draw_instruction_text("PRESS [SPACE] TO START, [ESC] TO BACK")
    
    def _draw_pattern_finish(self):
        """パターン完了・評価画面の描画"""
        # 結果表示
        header_text = "PRACTICE COMPLETE!"
        header_x = (DC.WINDOW_WIDTH - len(header_text) * DC.LARGE_FONT_WIDTH) // 2
        pyxel.text(header_x, DC.SCRAMBLE_Y, header_text, self.app.text_color, self.large_font)
        
        # パターン情報
        if hasattr(self.app, 'current_pattern') and self.app.current_pattern:
            pattern_text = f"Pattern: {self.app.current_pattern.name}"
            pyxel.text(DC.MARGIN_X, DC.SCRAMBLE_TEXT_Y, pattern_text, 
                      self.app.text_color, self.middle_font)
        
        # タイム表示
        if hasattr(self.app, 'pattern_result_time'):
            time_text = f"Time: {self.app.pattern_result_time:.2f}s"
            time_x = (DC.WINDOW_WIDTH - len(time_text) * DC.LARGE_FONT_WIDTH) // 2
            pyxel.text(time_x, DC.TIMER_Y, time_text, self.app.text_color, self.large_font)
        
        # ベストタイム表示
        if hasattr(self.app, 'current_pattern'):
            best_time = self.app.stats.get_pattern_best(self.app.current_pattern.id)
            if best_time:
                best_text = f"Best: {best_time:.2f}s"
            else:
                best_text = "Best: -"
            pyxel.text(DC.MARGIN_X, DC.RESULTS_Y, best_text, 
                      self.app.text_color, self.middle_font)
        
        # 評価入力UI
        y_pos = DC.RESULTS_Y + DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y * 2
        rating_text = "Rate this algorithm (1-5):"
        pyxel.text(DC.MARGIN_X, y_pos, rating_text, self.app.text_color, self.middle_font)
        
        # 評価の星表示
        if hasattr(self.app, 'pending_rating'):
            stars = '★' * self.app.pending_rating + '☆' * (5 - self.app.pending_rating)
            pyxel.text(DC.MARGIN_X, y_pos + DC.MIDDLE_FONT_HEIGHT + DC.FONT_SPACING_Y, 
                      stars, DC.DEFAULT_WARNING_COLOR, self.large_font)
        
        # 操作説明
        self._draw_instruction_text("SPACE/ENTER: Continue  R: Retry  ESC: Back (Auto-saved)")