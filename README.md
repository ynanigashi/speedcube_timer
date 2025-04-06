# Speedcube timer

WCAルールに準拠したスピードキューブ練習用タイマーアプリケーション

## 機能

- WCAルールに準拠したスクランブル生成
- タイム計測
- AO5、AO12の自動計算
- Google Spreadsheetへの記録保存

## ファイル構成

```
speedcube_timer/
├── src/
│   ├── __init__.py
│   ├── timer.py          # タイマー機能の実装
│   ├── speedcube_stats.py # 統計計算機能の実装
│   ├── display.py        # 表示機能の実装
│   ├── scramble.py       # スクランブル生成機能
│   └── log_handler.py    # ログ保存機能
├── main.py               # アプリケーションのエントリーポイント
├── requirements.txt      # 必要なパッケージのリスト
├── config.ini.example    # 設定ファイルのテンプレート
└── README.md            # プロジェクトのドキュメント
```

## セットアップ

1. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

2. Google Sheets APIの認証情報を設定:
- credentials.jsonをプロジェクトルートに配置

3. 設定ファイルの作成:
```bash
cp config.ini.example config.ini
```

4. config.iniを開き、必要な情報を入力:
   - YOUR_SPREADSHEET_ID_HERE: Google SheetsのスプレッドシートID
   - YOUR_SHEET_NAME_HERE: 記録を保存するシート名
- PASS_TO_YOUR_CREDENTIALS_FILE: スプレッドシートに書き込み許可されたサービスアカウントの認証ファイル

## 使い方

```bash
python main.py
```

エンターキーを押すとタイマーがスタートし、スペースキーを押すとストップします。
タイム計測後、自動的にGoogle Spreadsheetに記録が保存されます。

## 開発環境

- Python 3.x
- 必要なライブラリ:
  - keyboard: タイマー制御
  - gspread: Google Spreadsheetsとの連携
  - google-auth: Google認証
  - google-auth-oauthlib: OAuth認証

