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
        # ESCキーでスクランブルを再生成
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            from .scramble import generate_wca_cube_scramble
            self.app.scramble = generate_wca_cube_scramble()
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # 右矢印キーでSTATS状態に遷移
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.app.state = TimerState.STATS
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            # STATS状態に遷移する際にキャッシュをクリア（新しい統計を計算するため）
            self.app.monthly_stats_cache = None
            return
        
        # Pキーでパターン練習モードに遷移
        if pyxel.btnp(pyxel.KEY_P):
            self.app.state = TimerState.PATTERN_LIST_SELECT
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            # パターンモードの初期化
            self.app.selected_pattern_index = 0
            self.app.pattern_list_scroll_offset = 0
            self.app.selected_category_tab = 0  # カテゴリタブをリセット
            self.app.current_pattern = None
            self.app.current_algorithm = None
            return
        
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
        
        # ESCキーでインスペクションを中断してREADYに戻る（スクランブル再生成）
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            from .scramble import generate_wca_cube_scramble
            self.app.scramble = generate_wca_cube_scramble()
            self.app.state = TimerState.READY
            self.app.space_hold_start = 0
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            pyxel.stop(SC.BEEP_CHANNEL)  # ホールド音を停止
            return
        
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
        
        # ESCキーで計測を中断
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self._cancel_solve()
            return
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._finish_solve()
    
    def _cancel_solve(self):
        """計測を中断する処理"""
        # パターンモードかどうかを判定
        is_pattern_mode = hasattr(self.app, 'current_pattern') and self.app.current_pattern is not None
        
        if is_pattern_mode:
            # パターンモードの場合はPATTERN_READYに戻る
            self.app.state = TimerState.PATTERN_READY
        else:
            # 通常モードの場合はREADYに戻る（スクランブル再生成）
            from .scramble import generate_wca_cube_scramble
            self.app.scramble = generate_wca_cube_scramble()
            self.app.state = TimerState.READY
        
        pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
    
    def _finish_solve(self):
        """ソルブ完了時の処理"""
        # BEEP_CHANNELはReadystateで使用されているため、SOUND_CHANNELを使用
        pyxel.play(SC.SOUND_CHANNEL, SC.FINISH_SOUND)
        self.app.finish_frame_count = pyxel.frame_count
        
        # パターンモードかどうかを判定
        is_pattern_mode = hasattr(self.app, 'current_pattern') and self.app.current_pattern is not None
        
        if is_pattern_mode:
            # パターンモードの場合
            self.app.pattern_result_time = self.app.current_time
            
            # データベースに記録を保存
            try:
                cursor = self.app.logger.cursor
                cursor.execute(
                    """
                    INSERT INTO pattern_solves 
                    (pattern_id, pattern_name, pattern_category, solve_time, 
                     session_id, practice_mode, algorithm_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.app.current_pattern.id,
                        self.app.current_pattern.name,
                        self.app.current_pattern.category.value,
                        self.app.current_time,
                        self.app.logger.session_id,
                        'manual',  # Phase 2では手動選択モードのみ
                        self.app.current_algorithm.id if self.app.current_algorithm else None
                    )
                )
                self.app.logger.conn.commit()
            except Exception as e:
                print(f"DEBUG: パターン記録の保存に失敗: {e}")
            
            self.app.pending_rating = 0
            self.app.state = TimerState.PATTERN_FINISH
        else:
            # 通常モードの場合
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
        # 結果表示から1秒経過したらREADY状態に戻る        if (pyxel.frame_count - self.app.sync_end_frame) > DC.FPS * 1.5:
            self.app.sync_result = None
            self.app.state = TimerState.READY


class StatsStateHandler(BaseStateHandler):
    """STATS状態のハンドラ"""
    
    def update(self):
        """STATS状態の更新処理"""
        # 初回のみ月次統計を計算
        if self.app.monthly_stats_cache is None:
            monthly_solve_count = self.app.stats.get_current_month_solve_count()
            monthly_avg_time = self.app.stats.get_current_month_average_time()
            self.app.monthly_stats_cache = (monthly_solve_count, monthly_avg_time)
            print(f"DEBUG: 月次統計を計算しました - Solves: {monthly_solve_count}, Average: {monthly_avg_time}")
        
        # 左矢印キーでREADY状態に戻る
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.app.state = TimerState.READY
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            # STATS状態から出る時にキャッシュをクリア
            self.app.monthly_stats_cache = None
            return


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
            TimerState.SYNCING: SyncingStateHandler(app),
            TimerState.STATS: StatsStateHandler(app),
            TimerState.PATTERN_LIST_SELECT: PatternListSelectHandler(app),
            TimerState.PATTERN_ALGORITHM_SELECT: PatternAlgorithmSelectHandler(app),
            TimerState.PATTERN_READY: PatternReadyHandler(app),
            TimerState.PATTERN_FINISH: PatternFinishHandler(app)
        }
    
    def update(self):
        """現在の状態に対応するハンドラの更新処理を実行"""
        handler = self.handlers.get(self.app.state)
        if handler:
            handler.update()


# ========================================
# パターン習得モード用ハンドラー（Phase 2）
# ========================================

class PatternListSelectHandler(BaseStateHandler):
    """パターン一覧選択画面のハンドラ"""
    
    def update(self):
        """パターン一覧選択画面の更新処理"""
        # ESCキーでREADY状態に戻る
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            # パターンモードを完全にクリア
            self.app.current_pattern = None
            self.app.current_algorithm = None
            self.app.random_mode = False
            self.app.state = TimerState.READY
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # TABキーでカテゴリを切り替え（RAND/PLL/OLLの3つ）
        if pyxel.btnp(pyxel.KEY_TAB):
            self.app.selected_category_tab = (self.app.selected_category_tab + 1) % 3  # 0:RAND, 1:PLL, 2:OLL
            self.app.selected_pattern_index = 0
            self.app.pattern_list_scroll_offset = 0
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # RANDタブ選択時の処理
        if self.app.selected_category_tab == 0:  # RANDタブ
            self._handle_rand_tab()
            return
        
        # 通常のパターン選択（PLL/OLL）
        # selected_category_tab: 0=RAND, 1=PLL, 2=OLL
        categories = self.app.pattern_db.get_available_categories()  # [OLL, PLL]
        # PLLは1番目(index=1)、OLLは0番目(index=0)なので逆順にマッピング
        category_index = 2 - self.app.selected_category_tab  # 1->1(PLL), 2->0(OLL)
        selected_category = categories[category_index]
        patterns = self.app.pattern_db.get_patterns_by_category(selected_category)
        
        # 表示可能なアイテム数を計算（ページサイズ用）
        from .constants import DisplayConfig as DC
        tab_height = DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y
        start_y = DC.SCRAMBLE_Y + DC.LARGE_FONT_HEIGHT + DC.FONT_SPACING_Y + tab_height
        max_y = DC.WINDOW_HEIGHT - DC.SMALL_FONT_HEIGHT - DC.MARGIN_Y * 2
        available_height = max_y - start_y
        item_height = DC.MIDDLE_FONT_HEIGHT * 2 + DC.FONT_SPACING_Y * 2
        page_size = available_height // item_height
        
        # 上下キーで選択を移動（循環）
        if pyxel.btnp(pyxel.KEY_UP):
            self.app.selected_pattern_index -= 1
            if self.app.selected_pattern_index < 0:
                # 先頭から末尾へ循環
                self.app.selected_pattern_index = len(patterns) - 1
            self._update_scroll(patterns)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.app.selected_pattern_index += 1
            if self.app.selected_pattern_index >= len(patterns):
                # 末尾から先頭へ循環
                self.app.selected_pattern_index = 0
            self._update_scroll(patterns)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        # 左右キーでページ移動（循環）
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.app.selected_pattern_index -= page_size
            if self.app.selected_pattern_index < 0:
                # 先頭より前に行く場合は末尾へ循環
                self.app.selected_pattern_index = len(patterns) - 1
            self._update_scroll(patterns)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.app.selected_pattern_index += page_size
            if self.app.selected_pattern_index >= len(patterns):
                # 末尾を超える場合は先頭へ循環
                self.app.selected_pattern_index = 0
            self._update_scroll(patterns)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        # ENTERキーで現在のアルゴリズムを使って練習開始
        if pyxel.btnp(pyxel.KEY_RETURN):
            selected_pattern = patterns[self.app.selected_pattern_index]
            self.app.current_pattern = selected_pattern
            
            # 保存されているアルゴリズム選択を取得
            selected_algo_id = self.app.stats.get_user_selected_algorithm(selected_pattern.id)
            if selected_algo_id:
                algorithms = self.app.pattern_db.get_algorithms_for_pattern(selected_pattern.id)
                self.app.current_algorithm = next((a for a in algorithms if a.id == selected_algo_id), None)
            else:
                # デフォルトアルゴリズムを使用
                self.app.current_algorithm = self.app.pattern_db.get_default_algorithm(selected_pattern.id)
            
            self.app.state = TimerState.PATTERN_READY
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # Aキーでアルゴリズム選択画面へ
        if pyxel.btnp(pyxel.KEY_A):
            selected_pattern = patterns[self.app.selected_pattern_index]
            self.app.current_pattern = selected_pattern
            self.app.available_algorithms = self.app.pattern_db.get_algorithms_for_pattern(selected_pattern.id)
            self.app.selected_algorithm_index = 0
            self.app.state = TimerState.PATTERN_ALGORITHM_SELECT
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
    
    def _handle_rand_tab(self):
        """RANDタブ選択時の処理"""
        from .patterns import PatternCategory
        
        # 上下キーでランダムカテゴリを選択（OLL/PLL/ALL）
        if pyxel.btnp(pyxel.KEY_UP):
            categories = ["OLL", "PLL", "ALL"]
            current_idx = categories.index(self.app.random_category)
            self.app.random_category = categories[(current_idx - 1) % 3]
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        if pyxel.btnp(pyxel.KEY_DOWN):
            categories = ["OLL", "PLL", "ALL"]
            current_idx = categories.index(self.app.random_category)
            self.app.random_category = categories[(current_idx + 1) % 3]
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        # ENTERキーでランダムモード開始
        if pyxel.btnp(pyxel.KEY_RETURN):
            # ランダムパターンを取得
            random_pattern = self.app.pattern_db.get_random_pattern(
                category=self.app.random_category,
                exclude_ids=self.app.recent_random_patterns
            )
            
            if random_pattern:
                self.app.random_mode = True
                self.app.current_pattern = random_pattern
                
                # 履歴に追加（最大5件）
                self.app.recent_random_patterns.append(random_pattern.id)
                if len(self.app.recent_random_patterns) > 5:
                    self.app.recent_random_patterns.pop(0)
                
                # デフォルトアルゴリズムを使用
                self.app.current_algorithm = self.app.pattern_db.get_default_algorithm(random_pattern.id)
                
                self.app.state = TimerState.PATTERN_READY
                pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
    
    def _update_scroll(self, patterns):
        """選択位置に応じてスクロールオフセットを更新"""
        # 表示可能なアイテム数を計算
        from .constants import DisplayConfig as DC
        
        # カテゴリタブ分のオフセットを考慮
        tab_height = DC.MIDDLE_FONT_HEIGHT + DC.MARGIN_Y
        start_y = DC.SCRAMBLE_Y + DC.LARGE_FONT_HEIGHT + DC.FONT_SPACING_Y + tab_height
        max_y = DC.WINDOW_HEIGHT - DC.SMALL_FONT_HEIGHT - DC.MARGIN_Y * 2
        available_height = max_y - start_y
        item_height = DC.MIDDLE_FONT_HEIGHT * 2 + DC.FONT_SPACING_Y * 2
        max_visible_items = available_height // item_height
        
        selected = self.app.selected_pattern_index
        scroll = self.app.pattern_list_scroll_offset
        
        # 選択が表示範囲より下にある場合、スクロールダウン
        if selected >= scroll + max_visible_items:
            self.app.pattern_list_scroll_offset = selected - max_visible_items + 1
        # 選択が表示範囲より上にある場合、スクロールアップ
        elif selected < scroll:
            self.app.pattern_list_scroll_offset = selected


class PatternAlgorithmSelectHandler(BaseStateHandler):
    """アルゴリズム選択画面のハンドラ"""
    
    def update(self):
        """アルゴリズム選択画面の更新処理"""
        # ESCキーでパターン一覧に戻る
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.app.state = TimerState.PATTERN_LIST_SELECT
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # 上下キーで選択を移動
        if pyxel.btnp(pyxel.KEY_UP):
            self.app.selected_algorithm_index = max(0, self.app.selected_algorithm_index - 1)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        if pyxel.btnp(pyxel.KEY_DOWN):
            max_index = len(self.app.available_algorithms) - 1
            self.app.selected_algorithm_index = min(max_index, self.app.selected_algorithm_index + 1)
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
        
        # ENTERキーで選択したアルゴリズムを保存して練習開始
        if pyxel.btnp(pyxel.KEY_RETURN):
            selected_algo = self.app.available_algorithms[self.app.selected_algorithm_index]
            self.app.current_algorithm = selected_algo
            
            # 選択を保存
            self.app.stats.set_user_selected_algorithm(self.app.current_pattern.id, selected_algo.id)
            
            self.app.state = TimerState.PATTERN_READY
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return


class PatternReadyHandler(BaseStateHandler):
    """パターン練習準備画面のハンドラ"""
    
    def update(self):
        """パターン練習準備画面の更新処理"""
        # ESCキーでパターン一覧に戻る
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.app.state = TimerState.PATTERN_LIST_SELECT
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # スペースキー長押しで計測開始
        if self._handle_key_hold(
            pyxel.KEY_SPACE,
            'space_hold_start',
            TimerState.RUNNING,
            SC.START_SOUND,
            extra_action=self._start_pattern_timer,
            reset_attr='space_hold_start'
        ):
            return
    
    def _start_pattern_timer(self):
        """パターン練習タイマー開始"""
        self.app.start_time = pyxel.frame_count
        self.app.space_hold_start = 0


class PatternFinishHandler(BaseStateHandler):
    """パターン完了・評価画面のハンドラ"""
    
    def update(self):
        """パターン完了・評価画面の更新処理"""
        # 1-5キーで評価を設定
        for i in range(1, 6):
            if pyxel.btnp(getattr(pyxel, f'KEY_{i}')):
                self.app.pending_rating = i
                pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
                return
        
        # Rキーで同じパターンを再実行
        if pyxel.btnp(pyxel.KEY_R):
            # 評価を保存
            self._save_rating_if_exists()
            # 同じパターンでPATTERN_READYに戻る
            self.app.state = TimerState.PATTERN_READY
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # SPACE/ENTERキーの処理
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            # 評価を保存
            self._save_rating_if_exists()
            
            # ランダムモードの場合は次のランダムパターンへ
            if self.app.random_mode:
                self._continue_random_mode()
            else:
                # 通常モードはパターン一覧に戻る
                self.app.pending_rating = 0
                self.app.state = TimerState.PATTERN_LIST_SELECT
            
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
        
        # ESCキーでパターン一覧に戻る（ランダムモード解除）
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            # 評価を保存
            self._save_rating_if_exists()
            # ランダムモードを解除してパターン一覧に戻る
            self.app.random_mode = False
            self.app.pending_rating = 0
            self.app.state = TimerState.PATTERN_LIST_SELECT
            pyxel.play(SC.BEEP_CHANNEL, SC.CHANGE_SOUND)
            return
    
    def _continue_random_mode(self):
        """ランダムモードを継続して次のパターンへ"""
        # 次のランダムパターンを取得
        random_pattern = self.app.pattern_db.get_random_pattern(
            category=self.app.random_category,
            exclude_ids=self.app.recent_random_patterns
        )
        
        if random_pattern:
            self.app.current_pattern = random_pattern
            
            # 履歴に追加（最大5件）
            self.app.recent_random_patterns.append(random_pattern.id)
            if len(self.app.recent_random_patterns) > 5:
                self.app.recent_random_patterns.pop(0)
            
            # デフォルトアルゴリズムを使用
            self.app.current_algorithm = self.app.pattern_db.get_default_algorithm(random_pattern.id)
            
            self.app.pending_rating = 0
            self.app.state = TimerState.PATTERN_READY
    
    def _save_rating_if_exists(self):
        """評価が設定されていれば保存"""
        if hasattr(self.app, 'pending_rating') and self.app.pending_rating > 0:
            self.app.stats.set_algorithm_rating(
                self.app.current_algorithm.id,
                self.app.pending_rating
            )

