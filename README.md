# Speedcube Timer

スピードキューブの記録を計測し、自動的にGoogle Spreadsheetに保存するタイマーアプリケーションです。WCAルールに準拠したインスペクションタイムとGUI表示を備えています。

## 機能

- WCAルールに準拠したインスペクションタイム（15秒）
- GUIベースのリアルタイム計測
- 最新5回の記録表示
- AO5（直近5回の平均）とAO12（直近12回の平均）の自動計算
- Google Spreadsheetsへの自動記録保存
- 音声フィードバック（インスペクション時のカウントダウン音）

## インストールと実行

### 環境構築（初回のみ）

1. Python 3.10以上をインストール
2. リポジトリをクローンまたはダウンロード
3. 仮想環境の作成と有効化：

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
.\.venv\Scripts\activate

# 必要なパッケージのインストール
python -m pip install -r requirements.txt
```

### Google Cloud Platformの設定

1. Google Cloud Platformでプロジェクトを作成
2. Google Sheets APIを有効化
3. サービスアカウントを作成し認証情報をダウンロード
4. `credentials.json`をプロジェクトルートに配置

### 設定ファイルの準備

1. 設定ファイルのテンプレートをコピー：
```bash
copy config.ini.example config.ini
```

2. `config.ini`を編集：
   - スプレッドシートID
   - シート名
   - 認証ファイルのパス

### アプリケーションの実行

```bash
# 仮想環境が有効でない場合は有効化
.\.venv\Scripts\activate

# GUIバージョンの起動
python main_gui.py
```

または、同梱のバッチファイルを使用：
```bash
run.bat
```

## 使用方法

1. スペースキー0.5秒長押し → インスペクション開始
2. インスペクション中（15秒）：
   - スペースキー長押しでタイマー開始
   - または15秒経過で自動開始
3. スペースキーでタイマー停止
4. ESCキーで終了

## ファイル構成

```
speedcube_timer/
├── src/
│   ├── gui/
│   │   ├── __init__.py
│   │   └── app.py       # GUIアプリケーションの実装
│   ├── __init__.py
│   ├── timer.py         # タイマー機能
│   ├── speedcube_stats.py # 統計計算
│   ├── scramble.py      # スクランブル生成
│   └── log_handler.py   # ログ保存
├── main_gui.py          # GUIバージョンのエントリーポイント
├── requirements.txt     # 依存パッケージ
├── config.ini.example   # 設定ファイルテンプレート
├── run.bat             # 実行用バッチファイル
└── README.md
```

## 開発環境

- Python 3.10以上
- 必要なライブラリ:
  - pyxel: GUIとタイマー制御
  - gspread: Google Spreadsheetsとの連携
  - google-auth: Google認証
  - google-auth-oauthlib: OAuth認証
