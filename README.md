# Speedcube Timer

WCAルールに準拠したスピードキューブタイマーアプリケーションです。Pyxelを使用したGUIインターフェースで、インスペクションタイム、音声フィードバック機能を備えています。

## 機能

- WCAルールに準拠したタイマー機能
  - インスペクションタイム（15秒）
  - スペースキー長押しでスタート
  - スペースキーでストップ
- 音声フィードバック
  - インスペクション開始音
  - カウントダウンビープ（残り3,2,1秒）
  - タイマー開始・終了音
- スクランブル生成と表示
- 記録管理
  - 最新5回の記録表示
  - AO5（直近5回の平均）計算
  - AO12（直近12回の平均）計算
  - 試技回数のカウント
- Google Spreadsheetsへの記録保存

## 必要要件

- Python 3.10以上
- Pyxel 1.9.0以上
- gspread（Googleスプレッドシート連携用）

## インストール手順

1. リポジトリのクローン


2. 仮想環境の作成と有効化
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. 必要パッケージのインストール
```bash
pip install -r requirements.txt
```

4. Google Sheets APIの設定（オプション）
   - Google Cloud ConsoleでプロジェクトとAPI認証情報を作成
   - 認証情報JSONファイルを`credentials.json`として保存
   - `config.ini.example`を`config.ini`にコピーし、必要な情報を入力

## 使用方法

1. タイマーの起動
```bash
python main.py
```

2. 基本操作
   - スペースキーを0.5秒長押し → インスペクション開始
   - インスペクション中のスペースキー長押し → タイマー開始
   - タイマー停止はスペースキー
   - ESCキーで終了

## プロジェクト構成

```
speedcube_timer/
├── src/
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py          # メインアプリケーション
│   │   ├── constants.py    # 設定定数
│   │   ├── renderer.py     # 描画処理
│   │   └── states.py       # 状態管理
│   ├── __init__.py
│   ├── timer.py           # タイマー機能
│   ├── speedcube_stats.py # 統計計算
│   ├── scramble.py        # スクランブル生成
│   └── log_handler.py     # ログ保存
├── main.py               # エントリーポイント
├── requirements.txt      # 依存パッケージ
├── config.ini.example    # 設定ファイルテンプレート
└── README.md
```

## 開発環境

- Windows 11
- Python 3.10
- VS Code
- Pyxel 2.3.18
- gspread 6.2.0

