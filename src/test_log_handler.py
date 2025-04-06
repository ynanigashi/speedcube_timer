import unittest
from unittest.mock import patch, MagicMock
from log_handler import save_to_spreadsheet
import configparser

class TestLogHandler(unittest.TestCase):
    @patch('gspread.service_account')
    def test_save_to_spreadsheet(self, mock_service_account):
        # モックのセットアップ
        mock_gc = MagicMock()
        mock_service_account.return_value = mock_gc

        mock_spreadsheet = MagicMock()
        mock_gc.open_by_key.return_value = mock_spreadsheet

        mock_sheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_sheet

        # テストデータ
        scramble = "R U R' U R U2 R'"
        time_result = 12.34

        # config.iniから設定を読み込む
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        spreadsheet_key = config['GoogleSpreadsheet']['spreadsheet_key']
        sheet_name = config['GoogleSpreadsheet']['sheet_name']
        credentials_file = config['GoogleSpreadsheet']['credentials_file']

        # 実行
        save_to_spreadsheet(scramble, time_result)

        # アサーション
        mock_service_account.assert_called_once_with(filename=credentials_file)
        mock_gc.open_by_key.assert_called_once_with(spreadsheet_key)
        mock_spreadsheet.worksheet.assert_called_once_with(sheet_name)
        mock_sheet.append_row.assert_called_once_with([unittest.mock.ANY, "12.34", scramble])

if __name__ == '__main__':
    unittest.main()