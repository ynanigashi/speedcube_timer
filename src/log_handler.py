import gspread
import configparser
import datetime
import os
import sqlite3

class SpeedcubeLoggerError(Exception):
    """スピードキューブタイマーのログ処理に関する例外クラス
    
    Attributes:
        message -- エラーの説明メッセージ
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class SpeedcubeLogger:
    def __init__(self):
        try:
            # セッションIDを生成 (起動時のタイムスタンプ)
            self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # プロジェクトのルートディレクトリのパスを取得
            self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(self.root_dir, 'config.ini')

            # config.iniから設定を読み込む
            config = configparser.ConfigParser()
            config.read(config_path, encoding='utf-8')

            spreadsheet_key = config['GoogleSpreadsheet']['spreadsheet_key']
            sheet_name = config['GoogleSpreadsheet']['sheet_name']
            credentials_file = config['GoogleSpreadsheet']['credentials_file']

            # SQLiteデータベースのパスを設定
            # config.iniから読み込むか、デフォルト値を使用
            self.db_path = config.get('Database', 'db_path', 
                                    fallback=os.path.join(self.root_dir, 'data', 'speedcube.db'))
            
            # データベースディレクトリの存在確認と作成
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # データベース接続とテーブル作成
            self._init_database()

            # Google Spreadsheetに接続
            self.gc = gspread.service_account(filename=credentials_file)
            self.spreadsheet = self.gc.open_by_key(spreadsheet_key)
            self.sheet = self.spreadsheet.worksheet(sheet_name)
            
        except (configparser.Error, KeyError) as e:
            raise SpeedcubeLoggerError(f"設定ファイルの読み込みに失敗しました: {str(e)}")
        except Exception as e:
            raise SpeedcubeLoggerError(f"初期化中にエラーが発生しました: {str(e)}")

    def _init_database(self):
        """SQLiteデータベースの初期化とテーブル作成"""
        try:
            # データベース接続
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # resultsテーブルの作成（存在しない場合）
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    time_result REAL NOT NULL,
                    scramble TEXT,
                    session TEXT
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            raise SpeedcubeLoggerError(f"データベースの初期化に失敗しました: {str(e)}")

    def save_result(self, time_result: float, scramble: str = None) -> None:
        """
        スピードキューブの結果をローカルデータベースに保存する
        
        Args:
            time_result (float): 計測タイム（秒）
            scramble (str, optional): キューブのスクランブル（初期状態）
            
        Raises:
            SpeedcubeLoggerError: データの保存に失敗した場合
        """
        # 現在の日時を取得し、フォーマットする（ゼロ埋めされた形式で）
        now = datetime.datetime.now()
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")  # 24時間形式でゼロ埋め
        
        # time_resultを小数点以下2桁に丸める
        rounded_time = round(time_result, 2)
        
        # SQLiteデータベースにデータを追加（scrambleとsessionも保存）
        try:
            self.cursor.execute(
                "INSERT INTO results (datetime, time_result, scramble, session) VALUES (?, ?, ?, ?)",
                (datetime_str, rounded_time, scramble, self.session_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise SpeedcubeLoggerError(f"ローカルデータベースへのデータ保存に失敗しました: {str(e)}")

    def get_results(self, limit: int = None) -> list:
        """
        ローカルデータベースから結果を取得する

        Args:
            limit (int, optional): 取得する結果の最大数。指定がない場合はすべての結果を取得。

        Returns:
            list: 結果リスト（各要素は (datetime, time_result, scramble, session) のタプル）

        Raises:
            SpeedcubeLoggerError: データの取得に失敗した場合
        """
        try:
            if limit:
                self.cursor.execute("SELECT datetime, time_result, scramble, session FROM results ORDER BY id DESC LIMIT ?", (limit,))
            else:
                self.cursor.execute("SELECT datetime, time_result, scramble, session FROM results ORDER BY id DESC")
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise SpeedcubeLoggerError(f"データベースからの結果取得に失敗しました: {str(e)}")


    def get_session_results(self, limit: int = None) -> list:
        """
        現在のセッションの結果を取得する

        Args:
            limit (int, optional): 取得する結果の最大数。指定がない場合はすべての結果を取得。

        Returns:
            list: 結果リスト（各要素は (scramble, time_result, id) のタプル）

        Raises:
            SpeedcubeLoggerError: データの取得に失敗した場合
        """
        try:
            if limit:
                self.cursor.execute(
                    "SELECT datetime, time_result, scramble, session FROM results WHERE session = ? ORDER BY id DESC LIMIT ?",
                    (self.session_id, limit)
                )
            else:
                self.cursor.execute(
                    "SELECT datetime, time_result, scramble, session FROM results WHERE session = ? ORDER BY id DESC",
                    (self.session_id,)
                )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise SpeedcubeLoggerError(f"セッションの結果取得に失敗しました: {str(e)}")

    def _convert_to_comparable_records(self, data_list: list) -> set:
        """
        データソースを比較可能なセットに変換する
        
        Args:
            data_list (list): 変換するデータのリスト
            
        Returns:
            set: (datetime_str, time_result) のタプルのセット
        """
        result_set = set()
        
        for item in data_list:
            try:
                # データが最低2つの要素を持つことを確認
                if len(item) >= 2:
                    # 日時文字列を標準化
                    datetime_str = self._standardize_datetime_format(item[0])
                    
                    # 数値を浮動小数点に変換（文字列の場合はカンマをピリオドに置換）
                    # スプシはカンマ区切りの数値を返すため、置換処理を行う
                    if isinstance(item[1], str):
                        time_value = item[1].replace(',', '.')
                    else:
                        time_value = item[1]
                    
                    # 浮動小数点に変換して丸める
                    time_result = round(float(time_value), 2)
                    
                    # 結果をセットに追加
                    result_set.add((datetime_str, time_result))
            except (ValueError, TypeError, IndexError):
                # 変換できない項目はスキップ
                continue
                
        return result_set

    def sync_data(self) -> tuple:
        """
        SQLiteデータベースとGoogle Spreadsheetの間でデータを双方向に同期する
        
        Returns:
            tuple: 成功した場合は (True, メッセージ)、失敗した場合は (False, エラーメッセージ)
        """
        try:
            # スプレッドシートとデータベースのデータを比較可能なセットに変換
            
            # --- Google Spreadsheetからデータを取得 ---
            all_records = self.sheet.get_all_values()
            # ヘッダー行はスキップ
            sheet_rows = all_records[1:] if len(all_records) > 0 else []
            sheet_records = self._convert_to_comparable_records(sheet_rows)
            
            # --- SQLiteからデータを取得 ---
            all_db_results = self.get_results()
            db_records = self._convert_to_comparable_records(all_db_results)
            
            # --- インポート処理 (Spreadsheet -> SQLite) ---
            to_import = sheet_records - db_records
            imported_count = 0
            
            if to_import:
                # 一括インサート用のリスト
                import_data = [(datetime_str, time_result, None, None) 
                              for datetime_str, time_result in to_import]
                
                # 一括でインポート
                self.cursor.executemany(
                    "INSERT INTO results (datetime, time_result, scramble, session) VALUES (?, ?, ?, ?)",
                    import_data
                )
                imported_count = len(import_data)
                
                # インポート処理が完了したらコミット
                self.conn.commit()
            
            # --- エクスポート処理 (SQLite -> Spreadsheet) ---
            to_export = db_records - sheet_records
            exported_count = 0
            
            # エクスポート用のリストを作成
            export_rows = [[datetime_str, f"{time_result:.2f}"] 
                          for datetime_str, time_result in to_export]
            
            # バッチ処理のサイズ
            batch_size = 100
            
            for i in range(0, len(export_rows), batch_size):
                batch = export_rows[i:i+batch_size]
                if batch:
                    self.sheet.append_rows(
                        batch,
                        value_input_option='USER_ENTERED'
                    )
                    exported_count += len(batch)

            
            # 成功メッセージを返す
            message = f"downloaded: {imported_count}, Uploaded: {exported_count}"
            return (True, message)
            
        except SpeedcubeLoggerError as e:
            return (False, f"同期中にエラーが発生しました: {e.message}")
        except Exception as e:
            print(f"同期処理でエラーが発生しました: {str(e)}")  # ログ出力
            return (False, f"予期しないエラーが発生しました: {str(e)}")
    
    
    def _standardize_datetime_format(self, datetime_str: str) -> str:
        """
        日時の文字列を標準フォーマット（YYYY/MM/DD HH:MM:SS）に変換する
        時・分・秒が1桁の場合は0埋めして2桁にする
        
        Args:
            datetime_str (str): 変換する日時の文字列
            
        Returns:
            str: 標準化された日時の文字列
        """
        try:
            # 日付と時間の部分に分割
            date_part, time_part = datetime_str.split(' ', 1)
            
            # 時間部分を時、分、秒に分割
            time_components = time_part.split(':')
            
            # 時間の各要素を2桁にゼロ埋め
            padded_time = []
            for component in time_components:
                # コンポーネントが数値であることを確認
                if component.strip().isdigit():
                    # 数値に変換してゼロ埋め
                    padded_time.append(f"{int(component):02d}")
                else:
                    # 数値でない場合はそのまま
                    padded_time.append(component)
            
            # 標準化された日時文字列を構築
            standardized_datetime = f"{date_part} {':'.join(padded_time)}"
            
            # 秒がない場合（HH:MM形式）は秒を追加
            if len(padded_time) == 2:
                standardized_datetime += ":00"
                
            return standardized_datetime
            
        except Exception:
            # パースに失敗した場合は元の文字列を返す
            return datetime_str


    def __del__(self):
        """デストラクタ：データベース接続を閉じる"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == '__main__':
    logger = SpeedcubeLogger()
    result = logger.sync_data()
    print(result[1])
