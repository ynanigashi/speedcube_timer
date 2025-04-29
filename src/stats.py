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