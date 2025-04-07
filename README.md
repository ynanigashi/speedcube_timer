# Speedcube Timer

WCAルールに準拠したスピードキューブタイマーアプリケーションです。Pyxelを使用したGUIインターフェース、インスペクションタイム、音声フィードバック機能を備えています。

## 機能

- WCAルールに準拠したインスペクションタイム（15秒）
- GUIベースのリアルタイム計測
- 音声フィードバック
  - インスペクション時のカウントダウン音
  - タイマー開始音
  - 計測終了音
- 最新5回の記録表示
- AO5（直近5回の平均）とAO12（直近12回の平均）の自動計算
- 試技回数のカウント
- Google Spreadsheetsへの自動記録保存
- カスタムフォントによる大きな数字表示

## インストールと実行

### 環境構築（初回のみ）

1. Python 3.10以上をインストール
2. リポジトリをクローンまたはダウンロード
3. 仮想環境の作成と有効化：
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

4. 必要なパッケージのインストール：
```bash
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

# アプリケーションの起動
python main_gui.py
```

または、同梱のバッチファイルを使用：
```bash
run.bat
```

## 使用方法

1. スペースキーを0.5秒長押し → インスペクション開始
2. インスペクション中（15秒）：
   - スペースキー長押しでタイマー開始
   - 15秒経過で自動開始
3. 計測中はタイムを大きく表示
4. スペースキーでタイマー停止
5. ESCキーで終了

## 画面レイアウト

- 上部：スクランブル表示
- 中央：タイマー表示（大きな数字）
- 左下：直近5回の記録
- 右下：AO5、AO12の表示

## ファイル構成

```
speedcube_timer/
├── src/
│   ├── gui/
│   │   ├── __init__.py
│   │   └── app.py       # GUIアプリケーション
│   ├── __init__.py
│   ├── timer.py         # タイマー機能
│   ├── speedcube_stats.py # 統計計算
│   ├── scramble.py      # スクランブル生成
│   └── log_handler.py   # ログ保存
├── main_gui.py         # エントリーポイント
├── requirements.txt    # 依存パッケージ
├── config.ini.example  # 設定ファイルテンプレート
└── README.md
```

## 開発環境

- Python 3.10以上
- 必要なライブラリ:
  - pyxel: GUIとタイマー制御
  - gspread: Google Spreadsheetsとの連携
  - google-auth: Google認証
  - google-auth-oauthlib: OAuth認証
