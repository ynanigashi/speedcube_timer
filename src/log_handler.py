import gspread
import configparser
import datetime
from gspread.exceptions import APIError

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
            # config.iniから設定を読み込む
            config = configparser.ConfigParser()
            config.read('config.ini', encoding='utf-8')

            spreadsheet_key = config['GoogleSpreadsheet']['spreadsheet_key']
            sheet_name = config['GoogleSpreadsheet']['sheet_name']
            credentials_file = config['GoogleSpreadsheet']['credentials_file']

            # Google Spreadsheetに接続
            self.gc = gspread.service_account(filename=credentials_file)
            self.spreadsheet = self.gc.open_by_key(spreadsheet_key)
            self.sheet = self.spreadsheet.worksheet(sheet_name)
        except (configparser.Error, KeyError) as e:
            raise SpeedcubeLoggerError(f"設定ファイルの読み込みに失敗しました: {str(e)}")
        except Exception as e:
            raise SpeedcubeLoggerError(f"初期化中にエラーが発生しました: {str(e)}")

    def save_result(self, time_result: float) -> None:
        """
        スピードキューブの結果をスプレッドシートに保存する

        Args:
            time_result (float): 計測タイム（秒）

        Raises:
            SpeedcubeLoggerError: データの保存に失敗した場合
        """
        # 現在の日時を取得し、フォーマットする
        now = datetime.datetime.now()
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
        
        # データを追加
        try:
            self.sheet.append_row(
                [datetime_str, f"{time_result:.2f}"],
                value_input_option='USER_ENTERED'
            )
        except APIError as e:
            raise SpeedcubeLoggerError(f"Google SpreadsheetへのAPI呼び出しに失敗しました: {str(e)}")
        except Exception as e:
            raise SpeedcubeLoggerError(f"データの保存に失敗しました: {str(e)}")

if __name__ == '__main__':
    # テスト用の実行
    time_result = 12.34
    logger = SpeedcubeLogger()
    logger.save_result(time_result)