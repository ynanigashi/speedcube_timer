# Speedcube Timer

WCAルールに準拠したスピードキューブタイマーアプリケーションです。Pyxelを使用したGUIインターフェースで、インスペクションタイム、音声フィードバック機能を備えています。

## 機能

### 基本タイマー機能
- WCAルールに準拠したタイマー機能
  - インスペクションタイム（15秒）
  - スペースキー長押しでスタート
  - スペースキーでストップ
- 音声フィードバック
  - インスペクション開始音
  - カウントダウンビープ（残り3,2,1秒）
  - タイマー開始・終了音
- スクランブル生成と表示
- ローカルデータベース（SQLite）による記録保存
  - セッション単位での記録管理
  - READY状態でのSキー長押しまたは終了時のGoogle Spreadsheets同期
- 記録管理
  - 最新5回の記録表示
  - AO5（直近5回の平均）計算
  - AO12（直近12回の平均）計算
  - 試技回数のカウント

### パターン習得モード
タイム向上のためのパターン別練習機能

**実装済み機能（Phase 1-3完了）**:
- ✅ 78パターン対応（OLL: 57種、PLL: 21種）
- ✅ 複数アルゴリズム選択・評価機能
- ✅ 手動パターン選択モード（カテゴリタブ、ページ送り、循環ナビゲーション）
- ✅ ランダム練習モード（OLL/PLL/ALL、重複回避、連続練習）
- ✅ パターン別・アルゴリズム別統計

**今後の予定（Phase 4-6）**:
- 🔄 プリセット連続実行モード（全OLL・全PLL等を一気に練習）
- 🔄 カスタムセット作成・管理（苦手パターンをまとめて練習）
- 🔄 パターン統計画面の拡張（詳細統計・グラフ表示）

詳細な実装計画は [開発ロードマップ](docs/roadmap.md) を参照してください。 

## 必要要件

- Python 3.10以上
- Pyxel 2.3.18（`requirements.txt`で固定指定）
- gspread 6.2.0（Googleスプレッドシート連携用）
- **SQLite3（標準ライブラリ）**

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
  - `config.ini.example`を`config.ini`にコピーし、`[GoogleSpreadsheet]`（`spreadsheet_key`, `sheet_name`, `credentials_file`）と`[Database]`（`db_path`）を設定

## 使用方法

### 初回セットアップ

1. タイマーの起動（初回起動時にデータベースが自動作成されます）
```bash
python main.py
```

初回起動時、以下のSQLiteデータベースとテーブルが自動的に作成されます：
- `data/speedcube.db`（データベースファイル。`config.ini`の`db_path`で変更可能）
- テーブル: `results`, `pattern_solves`, `user_pattern_preferences`, `user_algorithm_ratings`

### テストの実行

```bash
# 全テストを実行
python -m pytest tests/

# 特定のテストファイルを実行
python -m pytest tests/test_algorithms.py

# 詳細な出力で実行
python -m pytest tests/ -v
```

### 基本操作

2. 基本操作
   - **メイン画面（READY）**
     - スペースキーを1秒長押し → インスペクション開始
     - Pキー → パターン練習モードへ
     - 右矢印キー → 統計画面（STATS）へ遷移
     - Sキー長押し（約1秒） → 手動同期（SYNCING状態で結果表示）
     - Cキー → 背景色と文字色の切り替え
     - Qキー → 終了（終了時に自動で同期処理を実行）
   
   - **インスペクション中（COUNTDOWN）**
     - スペースキー長押し → タイマー開始
     - ESCキー → スクランブル再生成（メイン画面に戻る）
   
   - **タイマー実行中（RUNNING）**
     - スペースキー → タイマー停止
     - ESCキー → タイマーキャンセル（メイン画面に戻る）
   
   - **パターン練習モード**
     - **パターン選択画面（PATTERN_LIST_SELECT）**
       - TABキー → カテゴリ切り替え（RAND ⇔ PLL ⇔ OLL）
       - 上下キー → パターン選択（循環）
       - 左右キー → ページ送り（5件単位、循環）
       - Enterキー → パターン決定
       - Aキー → アルゴリズム選択画面へ
       - ESCキー → メイン画面に戻る
     
     - **アルゴリズム選択画面（PATTERN_ALGORITHM_SELECT）**
       - 上下キー → アルゴリズム選択
       - Enterキー → アルゴリズム決定
       - ESCキー → パターン選択画面に戻る
     
     - **パターン準備画面（PATTERN_READY）**
       - スペースキー長押し → タイマー開始
       - Aキー → アルゴリズム変更
       - ESCキー → パターン選択画面に戻る
     
     - **パターン結果画面（PATTERN_FINISH）**
       - 1-5キー → 評価設定（1-5）
       - Rキー → 同じパターンを再実行
       - スペース/Enterキー → ランダムモード時は次のランダムパターンを表示／個別選択時はパターン一覧に戻る
       - ESCキー → パターン一覧に戻る（ランダムモードでは終了して通常モードに復帰）
       - （評価は画面遷移時に自動保存）

## プロジェクト構成

```
speedcube_timer/
├── src/
│   ├── app.py                 # メインアプリケーション
│   ├── constants.py           # 設定定数
│   ├── renderer.py            # 描画処理
│   ├── states.py              # 状態管理
│   ├── state_handlers.py      # 状態別入力ハンドラ
│   ├── stats.py               # 統計計算
│   ├── scramble.py            # スクランブル生成
│   ├── patterns.py            # パターン・アルゴリズムデータ
│   └── log_handler.py         # データ保存・同期処理
├── data/
│   ├── speedcube_timer.pyxres # Pyxelデータ
│   ├── patterns.json          # パターンマスターデータ（78パターン）
│   └── algorithms.json        # アルゴリズムマスターデータ
├── docs/
│   ├── flow_diagrams.md       # フロー図（Mermaid形式）
│   └── roadmap.md             # 開発ロードマップ
├── tests/
│   ├── test_algorithms.py     # アルゴリズムテスト
│   ├── test_json_load.py      # JSONロードテスト
│   ├── test_phase1.py         # Phase 1テスト
│   └── test_phase2.py         # Phase 2テスト
├── main.py                    # エントリーポイント
├── requirements.txt           # 依存パッケージ
├── config.ini.example         # 設定ファイルテンプレート
├── CHANGELOG.md               # 変更履歴
└── README.md                  # このファイル
```

## 開発環境

- Windows 11
- Python 3.10
- VS Code
- Pyxel 2.3.18
- gspread 6.2.0
- SQLite3（標準ライブラリ）

## 開発計画

プロジェクトは段階的に機能を追加しています。

### 完了済み
- ✅ **Phase 1-3**: 基本タイマー機能、パターン練習モード（手動選択・ランダム）
- ✅ 78パターン対応、複数アルゴリズム選択、評価機能

### 今後の予定
- 🔄 **Phase 4**: プリセット連続実行モード（全OLL・全PLLを一気に練習）
- 🔄 **Phase 5**: カスタムセット機能（苦手パターンをまとめて練習）
- 🔄 **Phase 6**: パターン統計画面の拡張（詳細統計・グラフ表示）

詳細な実装計画・タスクリストは **[開発ロードマップ](docs/roadmap.md)** を参照してください。

## ドキュメント

### ユーザー向け
- 📝 [README.md](README.md) - プロジェクト概要と使い方（このファイル）
- 📝 [CHANGELOG.md](CHANGELOG.md) - 変更履歴

### 開発者向け
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - コントリビューションガイド（開発環境セットアップ、テスト、コーディング規約）
- 🏗️ [アーキテクチャドキュメント](docs/ARCHITECTURE.md) - システム設計、モジュール構成、データベース設計
- 🔧 [開発者ガイド](docs/DEVELOPMENT.md) - 実践的な開発方法、デバッグ、トラブルシューティング
- � [データスキーマ仕様](docs/DATA_SCHEMA.md) - JSON/Pyxelリソース/config.ini仕様、ランダムモード詳細
- 🎨 [UI仕様書](docs/UI_SPECIFICATION.md) - 画面レイアウト、配色、座標、アニメーション
- �🗺️ [開発ロードマップ](docs/roadmap.md) - 詳細な実装計画とタスクリスト
- 📊 [フロー図](docs/flow_diagrams.md) - 画面遷移とデータフロー（Mermaid形式）

---

## 変更履歴

プロジェクトの変更履歴については、[CHANGELOG.md](CHANGELOG.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。