from datetime import datetime

class SpeedcubeStats:
    def __init__(self, logger=None):
        """
        スピードキューブの統計情報を計算・管理するクラス

        Args:
            logger: SpeedcubeLoggerのインスタンス
        """
        self.logger = logger
        
        # 統計情報を保持する変数
        self.session_results = []  # 現在のセッションの結果
        self.best_time = None      # ベストタイム
        self.worst_time = None     # ワーストタイム
        self.ao5 = None            # 直近5回の平均
        self.ao12 = None           # 直近12回の平均
        self.session_avg = None    # セッション平均
        
        # 初期データ読み込み
        if self.logger:
            self.update_stats()
    
    def update_stats(self):
        """
        ロガーからデータを読み込み、すべての統計情報を更新する
        """
        if not self.logger:
            return
            
        # セッションデータの取得（現在のセッションデータのみ）
        raw_results = self.logger.get_session_results()

        if not raw_results:
            self.session_results = []
            return
        
        # 古い順に並べ替えてインデックスを追加（1から始まる番号）
        # raw_resultsは新しい順（DESC）なので、逆順にして古い順にする
        indexed_results = []
        for index, result in enumerate(raw_results[::-1], 1):
            date_time, time_result, scramble, session_id = result
            # (scramble, time_result, result_id, solve_index)の形式で保存
            indexed_results.append((index, time_result, scramble, session_id))
        
        # 最新の結果が先頭に来るように再度並べ替え
        self.session_results = list(reversed(indexed_results))
        
        # 時間のリストを抽出
        times = [result[1] for result in self.session_results]
        
        # 基本統計の計算
        self.best_time = min(times) if times else None
        self.worst_time = max(times) if times else None
        self.session_avg = sum(times) / len(times) if times else None
        
        # 平均の計算
        self.ao5 = self.calculate_average(self.session_results, 5)
        self.ao12 = self.calculate_average(self.session_results, 12)
    
    
    def calculate_average(self, results, n):
        """
        直近n回の平均を計算する
        
        Args:
            results: 計算に使用する結果リスト
            n: 平均を取る結果の数
            
        Returns:
            平均値、または結果が不足している場合はNone
        """
        if len(results) < n:
            return None
        
        # 結果が十分にある場合、最新のn個を使用
        recent_results = results[:n]  # すでにDESC順で取得されているはず
        
        # タイムのみを抽出 (scramble, time_result, id) の形式
        recent_times = [result[1] for result in recent_results]
        
        return sum(recent_times) / len(recent_times)
    
    def calculate_average_of_n(self, n):
        """
        直近n回の平均を計算する（外部から呼び出し用）
        
        Args:
            n: 平均を取る結果の数
            
        Returns:
            平均値、または結果が不足している場合はNone
        """
        return self.calculate_average(self.session_results, n)
    
    def format_average(self, value):
        """
        平均値を表示用にフォーマットする
        
        Args:
            value: フォーマットする値
            
        Returns:
            フォーマットされた文字列
        """
        return f"{value:.2f}" if value is not None else "-"
    
    def get_stats_summary(self):
        """
        現在の統計情報のサマリーを取得する
        
        Returns:
            dict: 統計情報を含む辞書
        """
        return {
            "best_time": self.best_time,
            "worst_time": self.worst_time,
            "ao5": self.ao5,
            "ao12": self.ao12,
            "session_avg": self.session_avg,
            "solve_count": len(self.session_results)
        }
    
    def _get_monthly_results(self, year=None, month=None):
        """
        指定した月の結果データを取得する（内部用メソッド）
        
        Args:
            year: 年（デフォルトは現在の年）
            month: 月（デフォルトは現在の月）
              Returns:
            list: 指定した月の結果リスト、エラーの場合は空リスト
        """
        if not self.logger:
            return []
        
        # デフォルトは現在の年月
        if year is None or month is None:
            now = datetime.now()
            year = year or now.year
            month = month or now.month
        
        print(f"DEBUG: _get_monthly_results searching for year={year}, month={month}")        
        # ロガーから全ての結果を取得
        try:
            all_results = self.logger.get_results()
            print(f"DEBUG: Total results from logger: {len(all_results) if all_results else 0}")
            if not all_results:
                return []
            
            monthly_results = []
            for result in all_results:
                date_time_str, time_result, scramble, session_id = result
                
                # 日時文字列をdatetimeオブジェクトに変換
                try:
                    # 複数の日時形式に対応
                    try:
                        # ISO形式を試す
                        date_time = datetime.fromisoformat(date_time_str)
                    except ValueError:
                        # 日本語形式 (YYYY/MM/DD HH:MM:SS) を試す
                        date_time = datetime.strptime(date_time_str, "%Y/%m/%d %H:%M:%S")
                    
                    print(f"DEBUG: Processing result: {date_time_str}, parsed year={date_time.year}, month={date_time.month}")
                    # 指定した年月と一致するかチェック
                    if date_time.year == year and date_time.month == month:
                        print(f"DEBUG: Match found for {date_time_str}")
                        monthly_results.append(result)
                    else:
                        print(f"DEBUG: No match - looking for {year}/{month}, found {date_time.year}/{date_time.month}")
                except ValueError as e:
                    # 日時の形式が正しくない場合はスキップ
                    print(f"DEBUG: ValueError parsing date {date_time_str}: {e}")
                    continue
            
            print(f"DEBUG: Found {len(monthly_results)} results for {year}/{month}")
            return monthly_results
            
        except Exception:
            # エラーが発生した場合は空リストを返す
            return []

    def get_monthly_solve_count(self, year=None, month=None):
        """
        指定した月のソルブ回数を取得する
        
        Args:
            year: 年（デフォルトは現在の年）
            month: 月（デフォルトは現在の月）
              Returns:
            int: 指定した月のソルブ回数
        """
        monthly_results = self._get_monthly_results(year, month)
        return len(monthly_results)
    
    def get_current_month_solve_count(self):
        """
        現在の月のソルブ回数を取得する
        
        Returns:
            int: 現在の月のソルブ回数
        """
        return self.get_monthly_solve_count()
    
    def get_monthly_average_time(self, year=None, month=None):
        """
        指定した月の平均ソルブ時間を取得する
        
        Args:
            year: 年（デフォルトは現在の年）
            month: 月（デフォルトは現在の月）
            
        Returns:
            float: 指定した月の平均ソルブ時間、データがない場合はNone
        """
        print(f"DEBUG: get_monthly_average_time called with year={year}, month={month}")
        monthly_results = self._get_monthly_results(year, month)
        print(f"DEBUG: monthly_results length: {len(monthly_results)}")
        
        if not monthly_results:
            print("DEBUG: No monthly results found, returning None")
            return None
        
        # タイムのみを抽出
        monthly_times = [result[1] for result in monthly_results]
        print(f"DEBUG: monthly_times: {monthly_times}")
        
        # 平均を計算
        average = sum(monthly_times) / len(monthly_times)
        print(f"DEBUG: calculated average: {average}")
        return average
    
    def get_current_month_average_time(self):
        """
        現在の月の平均ソルブ時間を取得する
        
        Returns:
            float: 現在の月の平均ソルブ時間、データがない場合はNone
        """
        return self.get_monthly_average_time()
    
    # ========================================
    # パターン習得モード用の統計メソッド（Phase 1）
    # ========================================
    
    def get_pattern_times(self, pattern_id, limit=None):
        """
        特定パターンの全タイムを取得
        
        Args:
            pattern_id: パターンID
            limit: 取得する最大件数（Noneの場合は全件）
            
        Returns:
            list: タイムのリスト（新しい順）
        """
        if not self.logger:
            return []
        
        try:
            cursor = self.logger.cursor
            if limit:
                cursor.execute(
                    "SELECT solve_time FROM pattern_solves WHERE pattern_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (pattern_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT solve_time FROM pattern_solves WHERE pattern_id = ? ORDER BY timestamp DESC",
                    (pattern_id,)
                )
            
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            print(f"DEBUG: get_pattern_times error: {e}")
            return []
    
    def get_pattern_best(self, pattern_id):
        """
        特定パターンのベストタイムを取得
        
        Args:
            pattern_id: パターンID
            
        Returns:
            float: ベストタイム、データがない場合はNone
        """
        if not self.logger:
            return None
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT MIN(solve_time) FROM pattern_solves WHERE pattern_id = ?",
                (pattern_id,)
            )
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None
        except Exception as e:
            print(f"DEBUG: get_pattern_best error: {e}")
            return None
    
    def get_pattern_count(self, pattern_id):
        """
        特定パターンの試技回数を取得
        
        Args:
            pattern_id: パターンID
            
        Returns:
            int: 試技回数
        """
        if not self.logger:
            return 0
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT COUNT(*) FROM pattern_solves WHERE pattern_id = ?",
                (pattern_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"DEBUG: get_pattern_count error: {e}")
            return 0
    
    # ========================================
    # アルゴリズム別統計メソッド
    # ========================================
    
    def get_algorithm_times(self, algorithm_id, limit=None):
        """
        特定アルゴリズムの全タイムを取得
        
        Args:
            algorithm_id: アルゴリズムID
            limit: 取得する最大件数
            
        Returns:
            list: タイムのリスト（新しい順）
        """
        if not self.logger:
            return []
        
        try:
            cursor = self.logger.cursor
            if limit:
                cursor.execute(
                    "SELECT solve_time FROM pattern_solves WHERE algorithm_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (algorithm_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT solve_time FROM pattern_solves WHERE algorithm_id = ? ORDER BY timestamp DESC",
                    (algorithm_id,)
                )
            
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            print(f"DEBUG: get_algorithm_times error: {e}")
            return []
    
    def get_algorithm_best(self, algorithm_id):
        """
        特定アルゴリズムのベストタイムを取得
        
        Args:
            algorithm_id: アルゴリズムID
            
        Returns:
            float: ベストタイム、データがない場合はNone
        """
        if not self.logger:
            return None
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT MIN(solve_time) FROM pattern_solves WHERE algorithm_id = ?",
                (algorithm_id,)
            )
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None
        except Exception as e:
            print(f"DEBUG: get_algorithm_best error: {e}")
            return None
    
    def get_algorithm_count(self, algorithm_id):
        """
        特定アルゴリズムの試技回数を取得
        
        Args:
            algorithm_id: アルゴリズムID
            
        Returns:
            int: 試技回数
        """
        if not self.logger:
            return 0
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT COUNT(*) FROM pattern_solves WHERE algorithm_id = ?",
                (algorithm_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"DEBUG: get_algorithm_count error: {e}")
            return 0
    
    # ========================================
    # ユーザー設定管理メソッド（Phase 2）
    # ========================================
    
    def get_user_selected_algorithm(self, pattern_id):
        """
        ユーザーが選択したアルゴリズムIDを取得
        
        Args:
            pattern_id: パターンID
            
        Returns:
            str: アルゴリズムID、設定がない場合はNone
        """
        if not self.logger:
            return None
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT selected_algorithm_id FROM user_pattern_preferences WHERE pattern_id = ?",
                (pattern_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"DEBUG: get_user_selected_algorithm error: {e}")
            return None
    
    def set_user_selected_algorithm(self, pattern_id, algorithm_id):
        """
        ユーザーのアルゴリズム選択を保存
        
        Args:
            pattern_id: パターンID
            algorithm_id: アルゴリズムID
            
        Returns:
            bool: 成功した場合True
        """
        if not self.logger:
            return False
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_pattern_preferences 
                (pattern_id, selected_algorithm_id, last_updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                """,
                (pattern_id, algorithm_id)
            )
            self.logger.conn.commit()
            return True
        except Exception as e:
            print(f"DEBUG: set_user_selected_algorithm error: {e}")
            return False
    
    def get_algorithm_rating(self, algorithm_id):
        """
        アルゴリズムの評価を取得
        
        Args:
            algorithm_id: アルゴリズムID
            
        Returns:
            tuple: (rating, notes) 評価がない場合は (None, None)
        """
        if not self.logger:
            return (None, None)
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                "SELECT rating, notes FROM user_algorithm_ratings WHERE algorithm_id = ?",
                (algorithm_id,)
            )
            result = cursor.fetchone()
            return (result[0], result[1]) if result else (None, None)
        except Exception as e:
            print(f"DEBUG: get_algorithm_rating error: {e}")
            return (None, None)
    
    def set_algorithm_rating(self, algorithm_id, rating, notes=""):
        """
        アルゴリズムの評価を保存
        
        Args:
            algorithm_id: アルゴリズムID
            rating: 評価（1-5）
            notes: メモ（オプション）
            
        Returns:
            bool: 成功した場合True
        """
        if not self.logger:
            return False
        
        # 評価値の範囲チェック
        if rating < 1 or rating > 5:
            print(f"DEBUG: Invalid rating value: {rating}")
            return False
        
        try:
            cursor = self.logger.cursor
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_algorithm_ratings 
                (algorithm_id, rating, notes, last_updated)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (algorithm_id, rating, notes)
            )
            self.logger.conn.commit()
            return True
        except Exception as e:
            print(f"DEBUG: set_algorithm_rating error: {e}")
            return False