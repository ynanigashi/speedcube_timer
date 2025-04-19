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
        # 現在の日時を取得し、フォーマットする
        now = datetime.datetime.now()
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
        
        # SQLiteデータベースにデータを追加（scrambleとsessionも保存）
        try:
            self.cursor.execute(
                "INSERT INTO results (datetime, time_result, scramble, session) VALUES (?, ?, ?, ?)",
                (datetime_str, time_result, scramble, self.session_id)
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

    def sync_data(self) -> tuple:
        """
        SQLiteデータベースとGoogle Spreadsheetの間でデータを双方向に同期する
        
        Returns:
            tuple: 成功した場合は (True, メッセージ)、失敗した場合は (False, エラーメッセージ)
        """
        try:
            # --- Google Spreadsheetからのインポート処理 ---
            # シートからすべてのデータを取得
            all_records = self.sheet.get_all_values()
            
            # ヘッダー行が存在する場合はスキップ
            sheet_rows = all_records[1:] if len(all_records) > 0 else []
            
            # インポート用のデータを処理
            imported_count = 0
            sheet_records = set()  # エクスポート時に重複確認用
            
            for row in sheet_rows:
                if len(row) >= 2:  # 少なくとも日時と記録がある行のみ処理
                    datetime_str = row[0]
                    try:
                        # 記録の文字列をfloat型に変換
                        time_result = float(row[1].replace(',', '.'))
                        
                        # スプレッドシートの記録をセットに追加（後のエクスポート処理用）
                        sheet_records.add((datetime_str, time_result))
                        
                        # 重複チェック
                        self.cursor.execute(
                            "SELECT COUNT(*) FROM results WHERE datetime = ? AND time_result = ?", 
                            (datetime_str, time_result)
                        )
                        exists = self.cursor.fetchone()[0] > 0
                        
                        if not exists:
                            # SQLiteに保存 (セッションIDはNullに設定)
                            self.cursor.execute(
                                "INSERT INTO results (datetime, time_result, scramble, session) VALUES (?, ?, ?, ?)",
                                (datetime_str, time_result, None, None)
                            )
                            imported_count += 1
                    except ValueError:
                        # 数値として解析できない場合はスキップ
                        continue
            
            # --- SQLiteからのエクスポート処理 ---
            # SQLiteからすべてのデータを取得
            self.cursor.execute("SELECT datetime, time_result FROM results ORDER BY datetime")
            db_records = self.cursor.fetchall()
            
            # エクスポートするレコードを特定
            to_export = []
            for datetime_str, time_result in db_records:
                # スプレッドシートに存在しないデータのみエクスポート
                if (datetime_str, time_result) not in sheet_records:
                    to_export.append((datetime_str, time_result))
            
            # Google Spreadsheetにデータを追加
            exported_count = 0
            
            # バッチ処理のサイズ（API呼び出し回数を減らすため）
            batch_size = 100
            
            for i in range(0, len(to_export), batch_size):
                batch = to_export[i:i+batch_size]
                rows_to_add = []
                
                for datetime_str, time_result in batch:
                    rows_to_add.append([datetime_str, f"{time_result:.2f}"])
                
                if rows_to_add:
                    # バッチでスプレッドシートに追加
                    self.sheet.append_rows(
                        rows_to_add,
                        value_input_option='USER_ENTERED'
                    )
                    exported_count += len(rows_to_add)
            
            # 変更をコミット
            self.conn.commit()
            
            # 成功メッセージを返す
            message = f"同期が完了しました。インポート: {imported_count}件, エクスポート: {exported_count}件"
            return (True, message)
        
        except SpeedcubeLoggerError as e:
            return (False, f"同期中にエラーが発生しました: {e.message}")
        except Exception as e:
            print(f"同期処理でエラーが発生しました: {str(e)}")  # ログ出力
            return (False, f"予期しないエラーが発生しました: {str(e)}")

    def __del__(self):
        """デストラクタ：データベース接続を閉じる"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == '__main__':
    logger = SpeedcubeLogger()
    result = logger.sync_data()
    print(result[1])
