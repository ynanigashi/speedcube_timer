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
  - プログラム終了時のGoogle Spreadsheetsへの記録同期
- 記録管理
  - 最新5回の記録表示
  - AO5（直近5回の平均）計算
  - AO12（直近12回の平均）計算
  - 試技回数のカウント

### パターン習得モード
タイム向上のためのパターン別練習機能

**実装完了（Phase 1 & 1.5 & 2）**:
- ✅ パターンデータ構造（78パターン：OLL 57種、PLL 21種）
- ✅ 複数アルゴリズム対応（JSONマスターデータ管理）
- ✅ データベーススキーマ（`pattern_solves`、`user_pattern_preferences`、`user_algorithm_ratings`）
- ✅ パターン別・アルゴリズム別統計メソッド
- ✅ **手動パターン選択モード**
  - ✅ カテゴリタブ（OLL/PLL）によるパターン一覧表示
  - ✅ TABキーでカテゴリ切り替え
  - ✅ 左右キーでページ送り（5件単位）
  - ✅ 上下キーで選択、リスト末尾から先頭への循環
  - ✅ アルゴリズム選択機能（複数アルゴリズムがある場合）
  - ✅ ユーザー選択の保存・復元
  - ✅ パターン練習→タイム記録の一連のフロー
- ✅ **アルゴリズム評価機能**
  - ✅ 速度・使いやすさの星評価（1-5）
  - ✅ お気に入り機能
  - ✅ ユーザーメモ・練習回数記録

**実装予定（Phase 3以降）**:
- 🔄 ランダム単発実行モード
- 🔄 プリセット連続実行モード（全OLL、全PLL等）
- 🔄 カスタムセット作成・管理
- 🔄 パターン統計画面の拡張 

## 必要要件

- Python 3.10以上
- Pyxel 1.9.0以上
- gspread（Googleスプレッドシート連携用）
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
   - `config.ini.example`を`config.ini`にコピーし、必要な情報を入力

## 使用方法

1. タイマーの起動
```bash
python main.py
```

2. 基本操作
   - **メイン画面（READY）**
     - スペースキーを0.5秒長押し → インスペクション開始
     - Pキー → パターン練習モードへ
     - Sキー → 統計画面へ
     - Qキー → 終了（**終了時にGoogle Sheetsへの同期を実行**）
   
   - **インスペクション中（COUNTDOWN）**
     - スペースキー長押し → タイマー開始
     - ESCキー → スクランブル再生成（メイン画面に戻る）
   
   - **タイマー実行中（RUNNING）**
     - スペースキー → タイマー停止
     - ESCキー → タイマーキャンセル（メイン画面に戻る）
   
   - **パターン練習モード**
     - **パターン選択画面（PATTERN_LIST_SELECT）**
       - TABキー → カテゴリ切り替え（OLL ⇔ PLL）
       - 上下キー → パターン選択（循環）
       - 左右キー → ページ送り（5件単位、循環）
       - Enterキー → パターン決定
       - Aキー → アルゴリズム選択画面へ
       - ESCキー → メイン画面に戻る
     
     - **アルゴリズム選択画面（PATTERN_ALGORITHM_SELECT）**
       - 上下キー → アルゴリズム選択
       - Enterキー → アルゴリズム決定
       - Dキー → デフォルトアルゴリズムを選択
       - ESCキー → パターン選択画面に戻る
     
     - **パターン準備画面（PATTERN_READY）**
       - スペースキー長押し → タイマー開始
       - Aキー → アルゴリズム変更
       - ESCキー → パターン選択画面に戻る
     
     - **パターン結果画面（PATTERN_FINISH）**
       - 1-5キー → 評価設定（1-5）
       - Rキー → 同じパターンを再実行
       - スペース/Enter/ESCキー → パターン選択画面に戻る
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
├── main.py                    # エントリーポイント
├── requirements.txt           # 依存パッケージ
├── config.ini.example         # 設定ファイルテンプレート
└── README.md
```

## 開発環境

- Windows 11
- Python 3.10
- VS Code
- Pyxel 2.3.18
- gspread 6.2.0
- SQLite3（標準ライブラリ）

## TODO

### パターン習得モード（新機能）
タイム向上のためのパターン別練習モード

#### 実装進捗サマリー

| 項目 | 状態 | 詳細 |
|-----|------|-----|
| パターンデータ | ✅ 完了 | 78パターン（OLL: 57, PLL: 21）（JSON管理） |
| アルゴリズムデータ | ✅ 完了 | 複数アルゴリズム対応（JSON管理） |
| データベース | ✅ 完了 | `pattern_solves`, `user_pattern_preferences`, `user_algorithm_ratings` |
| 統計メソッド | ✅ 完了 | パターン・アルゴリズム別基本統計、ユーザー設定管理 |
| UI実装（Phase 2） | ✅ 完了 | パターン選択・アルゴリズム選択・評価画面 |
| 状態ハンドラ（Phase 2） | ✅ 完了 | パターンモード用ハンドラ群、循環・ページ送り機能 |
| カテゴリタブ（Phase 2） | ✅ 完了 | TABキーでOLL/PLL切り替え |
| ページ送り（Phase 2） | ✅ 完了 | 左右キーで5件単位ページ送り、循環機能 |
| RANDタブ（Phase 3） | ✅ 完了 | RAND/PLL/OLLタブ、OLL/PLL/ALLランダム選択、重複回避 |
| 連続ランダム（Phase 3） | ✅ 完了 | 完了後SPACE連打で連続練習、ESCで終了 |
| 連続実行モード | 🔄 未着手 | プリセット・カスタムセット |
| パターン統計画面 | 🔄 未着手 | 詳細統計・グラフ表示 |

#### 実装計画（フェーズ分け）

パターン習得モードを段階的に実装するため、以下の6フェーズに分けて開発を進めます。各フェーズは独立してテスト・デプロイ可能な単位としています。

**Phase 1: 基盤構築** ✅ **完了** - データ構造とDB準備  
**Phase 1.5: 複数アルゴリズム対応** ✅ **完了** - アルゴリズム選択・評価機能の設計  
**Phase 2: 手動選択モード** ✅ **完了** - パターン練習が可能（アルゴリズム選択・評価含む）  
**Phase 3: ランダムモード** ✅ **完了** - ランダム練習が可能  
**Phase 4: プリセット連続実行** 🔄 目標：カテゴリ全体練習が可能  
**Phase 5: カスタムセット機能** 🔄 目標：オリジナルセット作成が可能  
**Phase 6: 統計・最適化** 🔄 目標：全機能統合・洗練

---

#### 機能概要
パターン別にタイムを計測・記録し、苦手パターンの克服を支援するモード。各パターンのタイムをトラッキングして上達度を可視化します。

##### 練習モードの種類

**1. ランダム単発実行モード**
- カテゴリ（OLL/PLL/F2L/Cross）からランダムに1パターンを抽出
- 1パターンのみ集中して練習
- 使用例：「今日のOLL」として毎日異なるパターンを練習

**2. 手動パターン選択モード**
- パターン一覧から任意の1パターンを選択
- 選択したパターンのみを繰り返し練習
- 使用例：「OLL #23」など特定のパターンを集中練習

**3. プリセット複数連続実行モード**
- 事前定義されたカテゴリ全体を順番に実行
- 各パターンで個別にスタート・ストップ操作
- タイムは各パターンごとに記録
- プリセット例：
  - **全OLL練習（57パターン）**: OLL #1 → #2 → ... → #57
  - **全PLL練習（21パターン）**: PLL Aa → Ab → ... → Y
  - **全F2L練習（41パターン）**: F2L #1 → #2 → ... → #41
  - **Cross練習（8パターン）**: 白Cross → 黄Cross → ...
- 途中でESCキーにより中断可能
- 進捗状況の表示（例：「OLL 15/57」）

**4. カスタム連続実行モード**
- ユーザーが任意のパターンセットを作成
- 苦手パターンだけを集めた練習セット
- よく使うパターンの組み合わせ
- 作成例：
  - 「苦手なOLLセット」：OLL #7, #23, #45
  - 「頻出PLLセット」：PLL Ua, Ub, Z, H
  - 「今週の目標」：任意の複数パターン
- セット保存・読み込み機能
- セット編集機能（追加・削除・並び替え）

##### 共通機能
- パターン表示：パターン名 + スクランブル/セットアップムーブ
- タイマー操作：通常モードと同様（スペースキー長押し）
- 記録保存：各パターンのタイムを個別に保存
- 統計表示：パターンごとの試技回数、ベスト、平均、AO5
- スキップ機能：現在のパターンをスキップして次へ
- リトライ機能：同じパターンを再実行

---

#### フェーズ別実装計画（詳細）

##### **Phase 1: 基盤構築** 📋 ✅ **完了**
**目標**: パターンデータ構造とデータベース基盤の準備  
**成果物**: パターン定義、DB拡張、基本クラス

**実装項目**:
- [x] パターンデータ構造の設計
  - [x] `Pattern`クラスの実装（`patterns.py`）
  - [x] パターンマスターデータの定義（最初は5-10パターンで検証）
  - [x] カテゴリ定数の定義
- [x] データベーススキーマの拡張
  - [x] `pattern_solves`テーブルの作成（`algorithm_id`カラム含む）
  - [x] インデックスの作成（3つ）
  - [x] 既存DBとの互換性確認
- [x] 基本的な統計メソッドの実装
  - [x] `get_pattern_times(pattern_id)`
  - [x] `get_pattern_best(pattern_id)`
  - [x] `get_pattern_count(pattern_id)`
- [x] 状態定義の追加
  - [x] `TimerState`に`PATTERN_READY`を追加（最小限）

**テスト**:
- [x] パターンデータの読み込みテスト
- [x] DBテーブル作成の確認
- [x] 統計メソッドの単体テスト

**成果**:
- 10パターン実装（OLL: 5, PLL: 3, F2L: 2）
- `pattern_solves`テーブルと3つのインデックス作成完了
- 基本統計メソッド3つ実装完了
- テストスクリプト作成・全テスト合格

---

##### **Phase 1.5: 複数アルゴリズム対応** 🔧 ✅ **完了**
**目標**: 1パターンに複数のアルゴリズムを関連付け、ユーザーが選択・評価できる機能  
**成果物**: アルゴリズム管理機能、JSON読み込み、ユーザー設定DB

**背景**: ユーザーが「PLL_Uaのアルゴリズムが自分のと違う」と指摘したことから、1パターンに複数のアルゴリズムを持たせる設計に変更。

**実装項目**:
- [x] アルゴリズムデータ構造の設計
  - [x] `Algorithm`クラスの実装（`patterns.py`）
  - [x] `pattern_id`による紐付け
  - [x] `is_default`フラグでデフォルトアルゴリズム管理
  - [x] `speed_rating`, `ergonomics_rating`フィールド
- [x] JSONファイルによるマスターデータ管理
  - [x] `data/patterns.json`の作成（10パターン）
  - [x] `data/algorithms.json`の作成（9アルゴリズム）
  - [x] JSON読み込み機能の実装
  - [x] フォールバック機能（JSON読み込み失敗時）
- [x] アルゴリズム管理メソッドの実装
  - [x] `get_algorithm(algorithm_id)`
  - [x] `get_algorithms_for_pattern(pattern_id)`
  - [x] `get_default_algorithm(pattern_id)`
  - [x] `has_multiple_algorithms(pattern_id)`
  - [x] `get_all_algorithms()`
- [x] データベーススキーマの拡張
  - [x] `pattern_solves`テーブルに`algorithm_id`カラム追加
  - [x] アルゴリズム別統計メソッド実装
    - [x] `get_algorithm_times(algorithm_id, limit)`
    - [x] `get_algorithm_best(algorithm_id)`
    - [x] `get_algorithm_count(algorithm_id)`
- [x] ユーザー設定用テーブルの設計
  - [x] `user_pattern_preferences`テーブル設計（選択したアルゴリズム）
  - [x] `user_algorithm_ratings`テーブル設計（評価・お気に入り）

**テスト**:
- [x] 複数アルゴリズム機能のテスト（`test_algorithms.py`）
- [x] JSON読み込み機能のテスト（`test_json_load.py`）
- [x] アルゴリズム管理メソッドの動作確認
- [x] Phase 1テストとの互換性確認

**成果**:
- 9アルゴリズム実装（PLL_Ua: 3種類, PLL_Aa: 2種類, PLL_H: 2種類, OLL_21: 2種類）
- JSONファイルによるマスターデータ管理実現
- アルゴリズム別統計メソッド3つ実装完了
- 全テスト合格（`test_phase1.py`, `test_algorithms.py`, `test_json_load.py`）

**データ設計**:
```
【マスターデータ（JSON）】
patterns.json       → パターン定義（不変）
algorithms.json     → アルゴリズム定義（不変）

【ユーザーデータ（SQLite）】
pattern_solves              → 練習記録（algorithm_id含む）
user_pattern_preferences    → ユーザーが選択したアルゴリズム
user_algorithm_ratings      → アルゴリズムの評価・お気に入り
```

---

##### **Phase 2: 手動パターン選択モード** ✅ **完了**
**目標**: パターンを選択して練習できる機能（アルゴリズム選択含む）  
**成果物**: パターン選択→アルゴリズム選択→練習→記録→評価の一連の流れ

**実装項目**:
- [x] データベース拡張
  - [x] `user_pattern_preferences`テーブル作成（選択アルゴリズム保存）
  - [x] `user_algorithm_ratings`テーブル作成（評価・お気に入り）
  - [x] ユーザー設定管理メソッド（4メソッド）

- [x] 状態管理の拡張（`states.py`）
  - [x] `PATTERN_LIST_SELECT`状態 - パターン一覧画面
  - [x] `PATTERN_ALGORITHM_SELECT`状態 - アルゴリズム選択画面
  - [x] `PATTERN_READY`状態 - パターン準備画面
  - [x] `PATTERN_FINISH`状態 - 結果表示・評価入力

- [x] UI実装（`renderer.py`）
  - [x] パターン一覧画面（カテゴリタブ、統計プレビュー）
  - [x] アルゴリズム選択画面（複数アルゴリズム表示）
  - [x] パターン準備画面（アルゴリズム情報表示）
  - [x] パターン結果画面（評価入力UI）

- [x] 状態ハンドラ実装（`state_handlers.py`）
  - [x] `PatternListSelectHandler` - パターン選択、カテゴリ切り替え、ページ送り
  - [x] `PatternAlgorithmSelectHandler` - アルゴリズム選択
  - [x] `PatternReadyHandler` - パターン準備
  - [x] `PatternFinishHandler` - 結果表示・評価入力

- [x] ナビゲーション機能
  - [x] TABキーでカテゴリ切り替え（OLL ⇔ PLL）
  - [x] 左右キーでページ送り（5件単位）
  - [x] 上下キーで選択（末尾→先頭の循環）
  - [x] ESCキーで画面間移動・キャンセル

- [x] データ記録（`log_handler.py`）
  - [x] パターン解法記録の保存（`algorithm_id`含む）
  - [x] ユーザー設定の保存（選択アルゴリズム、評価）

**テスト**:
- [x] UI表示テスト
- [x] 操作フローテスト（選択→実行→記録→評価）
- [x] データ保存テスト
- [x] カテゴリタブ・ページ送り・循環機能テスト

**成果**:
- 78パターン（OLL: 57, PLL: 21）を効率的にナビゲート
- アルゴリズム選択・評価機能の完全実装
- ユーザー設定の永続化
- スムーズな画面遷移とキーボード操作

---

#### フロー図

画面遷移とデータフローの詳細は、以下のドキュメントを参照してください：

📊 **[フロー図（Mermaid形式）](docs/flow_diagrams.md)**

このドキュメントには以下の情報が含まれています：
- 通常タイマーモードのフロー
- パターン練習モード（手動選択・ランダム）のフロー
- 全状態遷移図
- データフロー詳細
- 将来の実装計画（Phase 4-6）

---

#### 状態遷移一覧

**Phase 2（手動選択モード）:**

| 現在の状態 | 操作 | 次の状態 | 処理 |
|-----------|------|---------|------|
| READY | P キー | PATTERN_LIST_SELECT | パターン一覧表示 |
| PATTERN_LIST_SELECT | ENTER (OLL/PLLタブ) | PATTERN_READY | 前回選択/デフォルトアルゴリズムで開始 |
| PATTERN_LIST_SELECT | A キー | PATTERN_ALGORITHM_SELECT | アルゴリズム変更画面へ |
| PATTERN_LIST_SELECT | ESC | READY | メインメニューに戻る |
| PATTERN_ALGORITHM_SELECT | ENTER | PATTERN_READY | 選択を保存、準備画面へ |
| PATTERN_ALGORITHM_SELECT | ESC | PATTERN_LIST_SELECT | 一覧に戻る |
| PATTERN_READY | SPACE 長押し | PATTERN_INSPECTION | インスペクション開始 |
| PATTERN_READY | A キー | PATTERN_ALGORITHM_SELECT | アルゴリズム変更 |
| PATTERN_READY | ESC | PATTERN_LIST_SELECT | 一覧に戻る |
| PATTERN_INSPECTION | SPACE 長押し | PATTERN_RUNNING | タイマー開始 |
| PATTERN_RUNNING | SPACE | PATTERN_FINISH | タイマー停止、記録保存 |
| PATTERN_FINISH | R キー | PATTERN_READY | 同じパターンを再実行（評価自動保存） |
| PATTERN_FINISH | SPACE/ENTER/ESC | PATTERN_LIST_SELECT | パターン一覧に戻る（評価自動保存） |

**Phase 3（ランダムモード）追加:**

| 現在の状態 | 操作 | 次の状態 | 処理 |
|-----------|------|---------|------|
| PATTERN_LIST_SELECT | TAB (RANDタブへ) | (同じ状態) | RANDタブに切り替え |
| PATTERN_LIST_SELECT | ENTER (RANDタブ) | PATTERN_READY | カテゴリからランダム抽出、ランダムモード開始 |
| PATTERN_FINISH (ランダムモード) | SPACE/ENTER | PATTERN_READY | 次のランダムパターンへ（評価自動保存） |
| PATTERN_FINISH (ランダムモード) | R キー | PATTERN_READY | 同じパターンを再実行（評価自動保存） |
| PATTERN_FINISH (ランダムモード) | ESC | PATTERN_LIST_SELECT | RANDタブに戻る（評価自動保存、ランダムモード終了） |

---

**実装項目**:

**1. データベース拡張**
- [x] ユーザー設定テーブルの作成（SQLite）
  - [x] `user_pattern_preferences`テーブル作成
    ```sql
    CREATE TABLE user_pattern_preferences (
        pattern_id TEXT PRIMARY KEY,
        selected_algorithm_id TEXT,
        priority INTEGER DEFAULT 0,
        notes TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ```
  - [x] `user_algorithm_ratings`テーブル作成
    ```sql
    CREATE TABLE user_algorithm_ratings (
        algorithm_id TEXT PRIMARY KEY,
        speed_rating INTEGER,        -- 1-5
        ergonomics_rating INTEGER,   -- 1-5
        is_favorite BOOLEAN DEFAULT 0,
        user_notes TEXT,
        practice_count INTEGER DEFAULT 0,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ```
- [x] ユーザー設定管理メソッドの実装（`stats.py`）
  - [x] `get_user_selected_algorithm(pattern_id)` - 選択したアルゴリズム取得
  - [x] `set_user_selected_algorithm(pattern_id, algorithm_id)` - アルゴリズム選択を保存
  - [x] `get_algorithm_rating(algorithm_id)` - 評価取得
  - [x] `set_algorithm_rating(algorithm_id, rating)` - 評価保存（簡易版）

**2. 状態管理の拡張（`states.py`）**
- [x] 状態定義の追加
  - [ ] `PATTERN_MODE_SELECT`状態（Phase 2では未使用、Phase 3以降で実装）
  - [x] `PATTERN_LIST_SELECT`状態 - パターン一覧画面
  - [x] `PATTERN_ALGORITHM_SELECT`状態 - アルゴリズム選択画面（複数ある場合）
  - [x] `PATTERN_READY`状態 - パターン準備画面（アルゴリズム情報表示）
  - [x] `PATTERN_INSPECTION`状態 - インスペクション（既存流用）
  - [x] `PATTERN_RUNNING`状態 - タイマー実行中（既存流用）
  - [x] `PATTERN_FINISH`状態 - 結果表示・評価入力

**3. UI実装（`renderer.py`）**
- [x] **パターン一覧画面の実装** (`_draw_pattern_list_select()`)
  - [x] パターン一覧表示（カテゴリタブで切り替え）
    ```
    ========== PATTERN SELECT ==========
    [OLL Patterns]
    1. OLL #1     ×0  ---
                  (Default)
    2. OLL #2     ×5  3.2s
                  (Standard) ← カーソル
    3. OLL #3     ×0  ---
                  (Default)
    ...
    
    [PLL Patterns]
    6. PLL Aa     ×10  2.5s
                  (Standard)
    7. PLL Ua     ×15  1.8s
                  (Alternative)
    ...
    ```
  - [x] カーソル表示（選択中のパターンをハイライト）
  - [x] パターン統計プレビュー（練習回数、ベストタイム）
  - [x] **現在選択されているアルゴリズム名を表示**
    - [x] `user_pattern_preferences`から取得
    - [x] 未設定の場合は「Default」と表示
  - [x] カテゴリタブ表示（TABキーで切り替え）
  - [x] ページ送り機能（左右キー、5件単位）
  - [x] 循環機能（末尾→先頭）
  - [x] 操作ガイド表示
    ```
    ↑↓: Select   TAB: Category   ←→: Page
    ENTER: Start   A: Change Algorithm   ESC: Back
    ```

- [x] **アルゴリズム選択画面の実装** (`_draw_algorithm_select()`)
  - [x] アルゴリズム一覧表示
    ```
    ====== ALGORITHM SELECT: PLL Ua ======
    
    1. ★ Standard (Default)
       R U' R U R U R U' R' U' R2
       ×10  1.8s
       [Rating: ★★★★☆]
    
    2.   Alternative
       M2 U M U2 M' U M2
       ×3  2.1s
       [Rating: ★★★☆☆]
    
    3.   RUD
       R U R' U R' U' R2 U' R' U R' U R
       ×0  ---
       [Not rated]
    ```
  - [x] 選択中のアルゴリズムをハイライト
  - [x] デフォルトアルゴリズムに★マーク
  - [x] ユーザー評価の星表示
  - [x] 各アルゴリズムの統計（練習回数、ベストタイム）
  - [x] 操作ガイド表示
    ```
    ↑↓: Select   ENTER: Choose   ESC: Back
    ```

- [x] **パターン準備画面の実装** (`_draw_pattern_ready()`)
  - [x] パターン情報表示
    ```
    ========================================
              PLL Ua - 3 edges clockwise
    ========================================
    
    Algorithm: Standard
    R U' R U R U R U' R' U' R2
    
    Setup: R U' R U R U R U' R' U' R2
    
    [Stats]
    ×15  Best: 1.8s  Avg: 2.3s  AO5: 2.1s
    ```
  - [x] 選択したアルゴリズムのムーブ表示
  - [x] セットアップムーブ表示
  - [x] パターン統計表示
  - [x] 操作ガイド
    ```
    SPACE (Hold): Start   A: Change Algorithm   ESC: Back
    ```

- [x] **パターン結果画面の実装** (`_draw_pattern_finish()`)
  - [x] タイム表示（大きく）
  - [x] 記録更新の表示（ベスト更新時）
  - [x] 使用したアルゴリズム名の表示
  - [x] **アルゴリズム評価UI**
    ```
    ========================================
              Time: 2.15s
         🎉 NEW BEST! (Previous: 2.3s)
    ========================================
    
    Algorithm: Standard
    R U' R U R U R U' R' U' R2
    
    [Rate This Algorithm]
    Rating: ★★★★☆ (4/5)  [1-5 keys to rate]
    
    [Stats]
    ×16 (+1)  Best: 2.15s (NEW!)  Avg: 2.28s
    
    SPACE/ENTER: Continue   R: Retry   ESC: Back
    (Rating auto-saved on exit)
    ```
  - [x] 1-5キーで評価入力
  - [x] 評価の自動保存（画面遷移時）
  - [x] 統計情報の更新表示
  - [x] 操作ガイド

**4. 状態ハンドラ実装（`state_handlers.py`）**
- [x] **`PatternListSelectHandler`** - パターン選択ハンドラ
  - [x] 上下キーでカーソル移動（循環）
  - [x] 左右キーでページ送り（5件単位、循環）
  - [x] TABキーでカテゴリ切り替え
  - [x] Enterキーでパターン決定
    - [x] 前回選択したアルゴリズムまたはデフォルトアルゴリズムを使用
    - [x] `PATTERN_READY`へ直接遷移
  - [x] Aキーでアルゴリズム変更
    - [x] `PATTERN_ALGORITHM_SELECT`へ遷移
    - [x] 選択中のパターンを状態変数に保持
  - [x] 選択中のパターンの現在のアルゴリズムを表示
    - [x] `user_pattern_preferences`から取得
    - [x] 未設定の場合はデフォルトアルゴリズムを表示
  - [x] ESCキーで`READY`状態に戻る

- [x] **`PatternAlgorithmSelectHandler`** - アルゴリズム選択ハンドラ
  - [x] 上下キーでカーソル移動
  - [x] Enterキーでアルゴリズム決定
  - [x] 選択したアルゴリズムを`user_pattern_preferences`に保存
  - [x] `PATTERN_READY`状態へ遷移
  - [x] ESCキーで`PATTERN_LIST_SELECT`に戻る

- [x] **`PatternReadyHandler`** - パターン準備ハンドラ
  - [x] パターン情報と選択アルゴリズムを表示
  - [x] スペースキー長押し検知 → インスペクション開始
  - [x] Aキーで`PATTERN_ALGORITHM_SELECT`に戻る（アルゴリズム変更）
  - [x] ESCキーで`PATTERN_LIST_SELECT`に戻る

- [x] **`PatternInspectionHandler`** - インスペクションハンドラ（既存流用）
  - [x] 既存の`CountdownHandler`を流用
  - [x] タイマー開始

- [x] **`PatternRunningHandler`** - タイマー実行ハンドラ（既存流用）
  - [x] 既存の`RunningHandler`を流用
  - [x] スペースキーでタイマー停止
  - [x] `PATTERN_FINISH`へ遷移

- [x] **`PatternFinishHandler`** - 結果表示・評価入力ハンドラ
  - [x] タイム記録処理（`algorithm_id`を含む）
  - [x] 記録更新判定（ベスト更新チェック）
  - [x] 評価入力UI制御
    - [x] 1-5キーで評価設定（1-5）
    - [x] 評価の自動保存（画面遷移時）
  - [x] 次の動作
    - [x] Rキー → 同じパターンを`PATTERN_READY`で再実行（評価自動保存）
    - [x] スペース/Enter/ESCキー → `PATTERN_LIST_SELECT`に戻る（評価自動保存）

**5. データ記録（`log_handler.py`）**
- [x] パターン解法記録の保存
  - [x] `pattern_solves`テーブルへの挿入
  - [x] `algorithm_id`を含むレコード保存
  - [x] セッションIDの関連付け
  - [x] タイムスタンプの記録
- [x] ユーザー設定の保存
  - [x] `user_pattern_preferences`への選択アルゴリズム保存
  - [x] `user_algorithm_ratings`への評価保存

**6. メインメニューからの遷移（`app.py`）**
- [x] READY画面にパターンモード起動ボタン追加
  - [x] 「P」キーでパターンモードへ遷移
  - [x] `PATTERN_LIST_SELECT`状態に移行
- [x] 操作ガイドの更新（Qキーで終了）

**テスト**:
- [x] **UI表示テスト**
  - [x] パターン一覧画面の表示確認
  - [x] アルゴリズム選択画面の表示確認
  - [x] パターン準備画面の表示確認
  - [x] パターン結果画面の表示確認
  - [x] 評価UIの動作確認
- [x] **操作フローテスト**
  - [x] パターン選択→アルゴリズム選択→実行→記録の一連の流れ
  - [x] カテゴリタブ・ページ送り・循環機能
  - [x] アルゴリズム変更（Aキー）の動作
  - [x] リトライ（Rキー）の動作
- [x] **データ保存テスト**
  - [x] ユーザー選択の保存・読み込み
  - [x] アルゴリズム評価の保存
  - [x] DBへの保存確認（`algorithm_id`含む）
- [x] **統計テスト**
  - [x] パターン別統計の取得確認
  - [x] アルゴリズム別統計の取得確認

**完成機能**: 
- 78パターン（OLL: 57, PLL: 21）の練習が可能
- カテゴリタブ・ページ送り・循環による効率的なナビゲーション
- 複数アルゴリズムの選択と評価
- 選択したアルゴリズムの自動復元
- パターン・アルゴリズムごとのタイム履歴記録
- 評価の自動保存
- 同じパターンの即時再実行機能

---

##### **Phase 3: ランダムモード** 🎲
**目標**: カテゴリからランダムにパターンを抽出して連続練習  
**成果物**: RANDタブによるランダム練習機能

**設計コンセプト**:
- パターン選択画面のカテゴリタブに「RAND」を追加
- 既存のOLL/PLLタブと同じ感覚で使える統一UI
- 連続ランダム練習機能（SPACE で次のランダムパターン）

---

#### フロー図

```
READY (P キー)
  ↓
PATTERN_LIST_SELECT (パターン選択画面)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [OLL:57]  [PLL:21]  [RAND]  ← TABキーで切り替え
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  【OLL/PLLタブ】選択時:
    → 既存の手動選択機能（Phase 2）
    
  【RANDタブ】選択時:
    ========== RANDOM PRACTICE ==========
    
    Select random pattern from:
    
    1. OLL     57 patterns  ×5/57   Avg: 3.2s
    2. PLL     21 patterns  ×3/21   Avg: 2.5s
    3. ALL     78 patterns  ×8/78   Avg: 3.0s
    
    ↑↓: Select   ENTER: Start Random
    
    ↓ ENTER (カテゴリ選択)
    
  ランダム抽出（重複回避）
    ↓
  PATTERN_READY (ランダムモード)
    ↓
  (練習・タイマー)
    ↓
  PATTERN_FINISH (ランダムモード)
    ├→ SPACE/ENTER: 同じカテゴリから次のランダム → PATTERN_READY
    ├→ R: 同じパターンを再実行 → PATTERN_READY
    └→ ESC: パターン選択に戻る → PATTERN_LIST_SELECT (RANDタブ)
```

---

**実装項目**:

**1. データ構造の拡張（`patterns.py`）**
- [x] ランダム選択メソッドの実装
  - [x] `get_random_pattern(category, exclude_recent)` - カテゴリからランダム抽出
    - [x] OLL/PLL/ALL（全パターン）から選択
    - [x] 重複回避機能（最近選ばれた5パターンを除外）
  - [ ] `get_category_stats(category)` - カテゴリ統計取得（※統計はstats.pyで取得可能）
    - [x] パターン総数
    - [x] 練習済み数
    - [x] 平均タイム

**2. 状態管理の拡張（`app.py`）**
- [x] ランダムモード用の状態変数追加
  - [x] `random_mode: bool` - ランダムモードかどうか
  - [x] `random_category: str` - ランダム選択元のカテゴリ（"OLL"/"PLL"/"ALL"）
  - [x] `recent_random_patterns: List[str]` - 最近選ばれたパターンID（重複回避用、最大5件）

**3. UI実装（`renderer.py`）**
- [x] **パターン選択画面の拡張** (`_draw_pattern_list_select()`)
  - [x] RANDタブの追加表示（順序: RAND/PLL/OLL）
    ```
    [RAND]  [PLL:21]  [OLL:57]
    ```
  - [x] RANDタブ選択時の画面切り替え
    - [x] カテゴリ選択リスト表示（OLL/PLL/ALL）
    - [x] 各カテゴリの統計情報表示
      - [x] パターン総数
      - [x] 練習済み数 (×X/Y)
      - [x] 平均タイム
    - [x] 重複回避の説明テキスト
  - [x] 操作ガイドの更新
    ```
    RANDタブ時: ↑↓: Select   ENTER: Start Random   ESC: Back
    ```

- [x] **パターン準備画面の拡張** (`_draw_pattern_ready()`)
  - [x] ランダムモード時の表示（既存のパターンモード表示を利用）

- [x] **パターン完了画面の拡張** (`_draw_pattern_finish()`)
  - [x] ランダムモード時の操作ガイド更新（既存の表示で対応）

**4. 状態ハンドラの拡張（`state_handlers.py`）**
- [x] **`PatternListSelectHandler`の拡張** - RANDタブ対応
  - [x] RANDタブの追加（TABキーで切り替え可能に）
  - [x] RANDタブ選択時の動作（`_handle_rand_tab()`）
    - [x] 上下キーでカテゴリ選択（OLL/PLL/ALL）
    - [x] ENTERキーで選択確定
      - [x] `random_mode = True` に設定
      - [x] `random_category` にカテゴリを保存
      - [x] ランダムにパターンを抽出
      - [x] 選択されたパターンを `recent_random_patterns` に追加
      - [x] PATTERN_READYへ遷移

- [x] **`PatternFinishHandler`の拡張** - ランダムモード対応
  - [x] ランダムモード判定
  - [x] SPACE/ENTERキー押下時の動作分岐
    ```python
    if self.app.random_mode:
        # 次のランダムパターンを選択
        self._continue_random_mode()
        self.app.state = TimerState.PATTERN_READY
    else:
        # パターン一覧に戻る（既存動作）
        self.app.state = TimerState.PATTERN_LIST_SELECT
    ```
  - [x] `_continue_random_mode()` メソッド実装
    - [x] 同じカテゴリからランダム抽出
    - [x] 重複回避（最近の5パターンを除外）
    - [x] デフォルトアルゴリズムを設定

**5. 重複回避ロジック**
- [x] 履歴管理
  - [x] 最大5パターンまで記憶
  - [x] ランダムモード終了時にクリア
- [x] 除外処理
  - [x] 除外後の候補が0の場合は履歴なしで再試行

**テスト**:
- [x] **UI表示テスト**
  - [x] RANDタブの表示確認（RAND/PLL/OLLの順）
  - [x] カテゴリ選択リストの表示確認
  - [x] 統計情報の表示確認
- [x] **ランダム選択テスト**
  - [x] OLLからのランダム選択
  - [x] PLLからのランダム選択
  - [x] ALLからのランダム選択
  - [x] 重複回避機能の動作確認
- [x] **連続練習テスト**
  - [x] SPACE で次のランダムパターンへ
  - [x] 連続で異なるパターンが選ばれること
  - [x] ESCでRANDタブに戻ること
- [x] **状態復元テスト**
  - [x] ランダムモード終了後、通常モードが正常動作
  - [x] パターン一覧からREADYに戻った時の状態クリア

**成果物**: 
- RANDタブによる統一されたUI
- OLL/PLL/ALLからのランダム選択
- 連続ランダム練習機能
- 重複回避機能（最近5パターンを除外）
- 既存の手動選択機能との共存

**デモ**: 
- RANDタブでOLLを選択 → 57種類からランダムに抽出
- SPACE連打で次々と異なるOLLパターンを練習
- 同じパターンが連続で出現しない（最大5パターン除外）

---

##### **Phase 4: プリセット複数連続実行モード** 📚
**目標**: カテゴリ全体を順番に練習できる連続実行機能  
**成果物**: 全57種OLLなどを連続で練習可能

**実装項目**:

**1. パターンセット管理（`patterns.py`）**
- [ ] `PatternSet`クラスの実装
  ```python
  @dataclass
  class PatternSet:
      id: str                    # セットID
      name: str                  # セット名
      pattern_ids: List[str]     # パターンIDのリスト
      mode: str                  # "preset" or "custom"
      description: str = ""      # 説明
  ```
- [ ] プリセットセット定義（コード内定義）
  - [ ] 全OLLセット（57パターン）
  - [ ] 全PLLセット（21パターン）
  - [ ] 全F2Lセット（41パターン）
  - [ ] 全Crossセット（8パターン）
- [ ] セット管理メソッド
  - [ ] `get_preset_sets()` - プリセットセット一覧取得
  - [ ] `get_set_by_id(set_id)` - セット取得

**2. 状態管理の拡張（`states.py`）**
- [ ] 連続実行用の状態変数
  - [ ] 現在のセットID
  - [ ] 現在のパターンインデックス
  - [ ] セットの進捗（完了数/総数）
  - [ ] スキップしたパターンのリスト

**3. UI実装（`renderer.py`）**
- [ ] **プリセットセット選択画面** (`_draw_preset_set_select()`)
  - [ ] セット選択UI
    ```
    ========== PRESET SETS ==========
    
    1. All OLL (57 patterns)   ×5/57
    2. All PLL (21 patterns)   ×3/21
    3. All F2L (41 patterns)   ×0/41
    4. All Cross (8 patterns)  ×0/8
    
    ↑↓: Select   ENTER: Start   ESC: Back
    ```
  - [ ] 進捗状況の表示（完了数/総数）
  - [ ] セットの説明表示

- [ ] **パターン準備画面の拡張** (`_draw_pattern_ready()`)
  - [ ] 進捗表示の追加
    ```
    ========================================
         [Set: All OLL] Progress: 15/57
    ========================================
              OLL #15 - Diagonal
    ========================================
    
    Algorithm: Standard
    ...
    
    NEXT: OLL #16 - Knight Move
    ```
  - [ ] プログレスバー表示
  - [ ] 次のパターン名表示
  - [ ] 操作ガイド更新
    ```
    SPACE (Hold): Start   S: Skip   ESC: Abort Set
    ```

- [ ] **パターン結果画面の拡張** (`_draw_pattern_finish()`)
  - [ ] 進捗表示
    ```
    ========================================
         [Set: All OLL] Progress: 16/57 ✓
    ========================================
              Time: 2.15s
    ========================================
    ...
    
    NEXT: OLL #17 - Lightning Bolt
    
    SPACE: Next Pattern   S: Skip Next   ESC: Abort Set
    ```
  - [ ] 自動的に次のパターンへ遷移オプション

- [ ] **セット完了画面** (`_draw_set_complete()`)
  - [ ] 完了サマリー表示
    ```
    ========================================
          🎉 SET COMPLETE! 🎉
            All OLL (57 patterns)
    ========================================
    
    Total Time: 2:15:30
    Average: 2.37s
    Best: 1.52s (OLL #21)
    Worst: 4.12s (OLL #7)
    
    Skipped: 2 patterns (OLL #3, OLL #45)
    
    SPACE: Back to Menu   R: Retry Set
    ```

**4. 状態ハンドラの拡張**
- [ ] **`PatternReadyHandler`の拡張**
  - [ ] Sキーでスキップ処理
    - [ ] スキップしたパターンをリストに追加
    - [ ] 次のパターンへ遷移
  - [ ] 進捗管理

- [ ] **`PatternFinishHandler`の拡張**
  - [ ] 自動的に次のパターンへ遷移
  - [ ] 最後のパターン完了時にセット完了画面へ
  - [ ] ESCキーでセット中断確認ダイアログ

- [ ] **`PatternSetCompleteHandler`** - セット完了ハンドラ
  - [ ] セット統計の計算
  - [ ] サマリー表示
  - [ ] 次の動作
    - [ ] スペースキー → `PATTERN_MODE_SELECT`に戻る
    - [ ] Rキー → セットを最初から再実行

**5. スキップ・中断機能**
- [ ] スキップしたパターンの記録
- [ ] 中断時の確認ダイアログ
  ```
  ========================================
         Abort this set?
     Progress will be lost.
  ========================================
  
  Y: Yes, abort   N: No, continue
  ```

**テスト**:
- [ ] 連続実行の完全なフロー
- [ ] スキップ機能
- [ ] 中断・再開
- [ ] 全パターン完了時の処理

**デモ**: 全21種PLLを連続で練習完走

---

##### **Phase 5: カスタムセット機能** 🎨
**目標**: ユーザーが独自の練習セットを作成・管理  
**成果物**: カスタムセット作成・編集・実行

**実装項目**:

**1. データベース拡張（`log_handler.py`）**
- [ ] `pattern_custom_sets`テーブル作成
- [ ] カスタムセット管理メソッド
  - [ ] `save_custom_set(set_id, set_name, pattern_ids)` - 保存
  - [ ] `load_custom_set(set_id)` - 読み込み
  - [ ] `get_all_custom_sets()` - 一覧取得
  - [ ] `delete_custom_set(set_id)` - 削除
  - [ ] `update_custom_set(set_id, set_name, pattern_ids)` - 更新

**2. 状態管理の追加（`states.py`）**
- [ ] `PATTERN_CUSTOM_SET_LIST`状態 - カスタムセット一覧
- [ ] `PATTERN_CUSTOM_SET_EDIT`状態 - カスタムセット編集
- [ ] `PATTERN_CUSTOM_SET_ADD_PATTERN`状態 - パターン追加

**3. UI実装（`renderer.py`）**
- [ ] **カスタムセット一覧画面** (`_draw_custom_set_list()`)
  - [ ] セット一覧表示
    ```
    ========== CUSTOM SETS ==========
    
    1. My Weak OLL (10 patterns)
       Last practiced: 2025/11/05
       Avg: 3.5s
    
    2. Fast PLL Practice (5 patterns)
       Last practiced: 2025/11/06
       Avg: 2.1s
    
    3. Daily F2L (15 patterns)
       Last practiced: Never
       Avg: ---
    
    N: New Set   E: Edit   D: Delete   ESC: Back
    ```
  - [ ] セット統計の表示（パターン数、最終練習日、平均）
  - [ ] 操作ガイド

- [ ] **カスタムセット編集画面** (`_draw_custom_set_edit()`)
  - [ ] セット名編集
  - [ ] パターンリスト表示
    ```
    ========== EDIT SET: My Weak OLL ==========
    
    Set Name: [My Weak OLL___________]
    
    Patterns (10):
    1. OLL #7    ×8  4.2s  [Remove: X]
    2. OLL #23   ×12 3.8s  [Remove: X]
    3. OLL #45   ×5  3.5s  [Remove: X]
    ...
    
    A: Add Pattern   ↑↓: Reorder   S: Save   ESC: Cancel
    ```
  - [ ] パターン追加ボタン
  - [ ] パターン削除ボタン
  - [ ] パターン並び替え（上下移動）

- [ ] **パターン追加画面** (`_draw_custom_set_add_pattern()`)
  - [ ] 全パターン一覧（カテゴリ別）
  - [ ] 既に追加済みパターンをグレーアウト
  - [ ] 苦手パターン識別（赤マーク）
    ```
    ========== ADD PATTERN ==========
    
    [OLL]
    □ OLL #1   ×10  2.5s
    ☑ OLL #2   [Already in set]
    □ OLL #3   ×0   ---
    □ OLL #7   🔴 ×8  4.2s WEAK!
    ...
    
    [Filter]
    A: All   W: Weak Only   U: Unpracticed
    
    SPACE: Toggle   ENTER: Done   ESC: Cancel
    ```
  - [ ] フィルタ機能（全て / 苦手のみ / 未練習のみ）
  - [ ] チェックボックスで複数選択

- [ ] **セット削除確認ダイアログ** (`_draw_delete_confirmation()`)
  ```
  ========================================
       Delete "My Weak OLL"?
      This cannot be undone.
  ========================================
  
  Y: Yes, delete   N: Cancel
  ```

**4. 状態ハンドラ実装（`state_handlers.py`）**
- [ ] **`PatternCustomSetListHandler`** - セット一覧ハンドラ
  - [ ] 上下キーでセット選択
  - [ ] Enterキーでセット実行（Phase 4の連続実行を利用）
  - [ ] Nキーで新規セット作成
  - [ ] Eキーでセット編集
  - [ ] Dキーでセット削除（確認ダイアログ）
  - [ ] ESCキーで`PATTERN_MODE_SELECT`に戻る

- [ ] **`PatternCustomSetEditHandler`** - セット編集ハンドラ
  - [ ] セット名編集（テキスト入力）
  - [ ] 上下キーでパターン選択
  - [ ] Xキーでパターン削除
  - [ ] 上下キーでパターン並び替え
  - [ ] Aキーでパターン追加画面へ
  - [ ] Sキーで保存
  - [ ] ESCキーでキャンセル（変更破棄確認）

- [ ] **`PatternCustomSetAddPatternHandler`** - パターン追加ハンドラ
  - [ ] 上下キーでパターン選択
  - [ ] スペースキーでチェックボックストグル
  - [ ] Enterキーで追加完了
  - [ ] A/W/Uキーでフィルタ切り替え
  - [ ] ESCキーでキャンセル

**5. 苦手パターン識別機能（`stats.py`）**
- [ ] `get_weak_patterns(category=None, threshold=1.2)` 実装
  - [ ] カテゴリ平均タイムを計算
  - [ ] 平均 > カテゴリ平均 × threshold のパターンを抽出
  - [ ] 未練習パターンは除外
- [ ] 「苦手パターンから作成」機能
  - [ ] ワンクリックで苦手パターンセットを作成

**テスト**:
- [ ] カスタムセット作成
- [ ] セット保存・読み込み
- [ ] セット編集
- [ ] セット削除
- [ ] カスタムセットでの連続実行

**デモ**: 「苦手なOLL 10選」セットを作成して練習

---

##### **Phase 6: 統計表示と最適化** 📊
**目標**: パターン統計の可視化と全体的な品質向上  
**成果物**: 完全な統計表示、パフォーマンス最適化

**実装項目**:
- [ ] Stats画面の拡張
  - [ ] タブ切り替え実装（Monthly / Pattern）
  - [ ] パターン統計サマリー表示
  - [ ] カテゴリ別統計
  - [ ] パターン詳細リスト
- [ ] ソート・フィルタ機能
  - [ ] 各種ソート（ベスト、平均、試技回数等）
  - [ ] フィルタ（練習済み、未練習、苦手等）
- [ ] 統計メソッドの完全実装
  - [ ] `get_pattern_average()`
  - [ ] `get_pattern_ao5()`
  - [ ] `get_pattern_ao12()`
  - [ ] `get_all_patterns_summary()`
  - [ ] `get_category_patterns_summary()`
- [ ] パフォーマンス最適化
  - [ ] 統計キャッシュ機構
  - [ ] DBクエリの最適化
  - [ ] インデックスの追加
- [ ] Google Sheets連携
  - [ ] パターン記録の同期
  - [ ] 専用シート作成
- [ ] UI/UX洗練
  - [ ] アニメーション追加
  - [ ] サウンドエフェクト
  - [ ] エラーハンドリング改善
- [ ] 全パターンデータの追加
  - [ ] 全57種OLL
  - [ ] 全21種PLL
  - [ ] 全41種F2L
  - [ ] 全8種Cross

**テスト**:
- [ ] 全機能の統合テスト
- [ ] パフォーマンステスト
- [ ] 大量データでの動作確認
- [ ] Google Sheets同期テスト
- [ ] エッジケースのテスト

**デモ**: 完全なパターン統計とグラフ表示

---

#### フェーズ間の依存関係

```
Phase 1 (基盤構築) ✅ 完了
    ↓
Phase 1.5 (複数アルゴリズム対応) ✅ 完了
    ↓
Phase 2 (手動選択 + アルゴリズム選択) ← 最小機能完成（ここで動作確認）
    ↓
Phase 3 (ランダム) ← Phase 2 の成果を利用
    ↓
Phase 4 (連続実行) ← Phase 2, 3 の成果を利用
    ↓
Phase 5 (カスタム) ← Phase 4 の連続実行機能を利用
    ↓
Phase 6 (統計・最適化) ← 全フェーズの成果を統合
```

#### 各フェーズ完了時の状態

| フェーズ | 動作する機能 | 使用可能なモード | 状態 |
|---------|------------|----------------|------|
| Phase 1 | なし（基盤のみ） | - | ✅ 完了 |
| Phase 1.5 | なし（データ構造拡張のみ） | - | ✅ 完了 |
| Phase 2 | パターン選択→アルゴリズム選択→練習→記録→評価 | 手動選択のみ | ✅ 完了 |
| Phase 3 | RANDタブからランダム練習、連続ランダム機能 | 手動選択、ランダム | ✅ 完了 |
| Phase 4 | プリセット連続実行 | 手動、ランダム、プリセット連続 | 🔄 未着手 |
| Phase 5 | カスタムセット | 全モード | 🔄 未着手 |
| Phase 6 | 完全な統計表示 | 全モード + 詳細統計 | 🔄 未着手 |

---

#### 実装すべき項目（全体リスト）

##### 1. 状態管理（states.py）
- [x] `TimerState`に以下の状態を追加（Phase 2で実装済み）
  - [x] `PATTERN_LIST_SELECT` - パターン個別選択画面
  - [x] `PATTERN_ALGORITHM_SELECT` - アルゴリズム選択画面
  - [x] `PATTERN_READY` - パターン表示・準備状態
  - [x] `PATTERN_FINISH` - パターン完了・結果表示
  - [ ] `PATTERN_MODE_SELECT` - 練習モード選択画面（Phase 4以降）
  - [ ] `PATTERN_CUSTOM_SET_EDIT` - カスタムセット編集画面（Phase 5）
- [x] パターン練習用の状態変数管理（Phase 2-3で実装済み）
  - [x] 現在のパターン (`current_pattern`)
  - [x] 現在のアルゴリズム (`current_algorithm`)
  - [x] ランダムモード (`random_mode`, `random_category`)
  - [x] 重複回避履歴 (`recent_random_patterns`)
  - [ ] 実行中のパターンセット（Phase 4）
  - [ ] 現在のパターンインデックス（Phase 4）
  - [ ] セットの進捗状況（Phase 4）

##### 2. パターンデータ管理
- [x] パターン定義ファイルの作成（`patterns.py`）（Phase 1で実装済み）
  - [x] パターンクラスの実装
    ```python
    @dataclass
    class Pattern:
        id: str              # パターンID（例："OLL_01", "PLL_Aa"）
        name: str            # パターン名（例："OLL #1", "PLL Aa"）
        category: PatternCategory  # カテゴリEnum（OLL, PLL, F2L, Cross）
        setup_moves: str     # セットアップムーブ
        description: str     # パターンの説明
        difficulty: int      # 難易度（1-5）
    ```
  - [x] パターンマスターリストの実装（Phase 2で完了）
    - [x] 全OLLパターン（57種類）
    - [x] 全PLLパターン（21種類）
    - [x] 合計78パターンをJSON管理 (`data/patterns.json`)
- [x] アルゴリズム定義（Phase 1.5で実装済み）
  - [x] アルゴリズムクラスの実装
    ```python
    @dataclass
    class Algorithm:
        id: str                    # アルゴリズムID
        pattern_id: str            # 紐付けるパターンID
        name: str                  # アルゴリズム名
        moves: str                 # ムーブ（回転記号）
        finger_tricks: str = ""    # フィンガートリック説明
        speed_rating: int = 0      # スピード評価（1-5）
        ergonomics_rating: int = 0 # 使いやすさ評価（1-5）
        is_default: bool = False   # デフォルトアルゴリズム
        notes: str = ""            # 備考
    ```
  - [x] アルゴリズムマスターリストの実装（Phase 2で完了）
    - [x] 78パターンに対する複数アルゴリズム対応
    - [x] JSON管理 (`data/algorithms.json`)
    - [x] デフォルトアルゴリズム設定
    - [x] ユーザー選択アルゴリズムの保存・復元
- [ ] パターンセット管理クラス（`pattern_sets.py`）
  - [ ] `PatternSet`クラス
    ```python
    class PatternSet:
        id: str              # セットID
        name: str            # セット名
        patterns: List[str]  # パターンIDのリスト
        mode: str            # "preset" or "custom"
        created_at: datetime
        updated_at: datetime
    ```
  - [ ] プリセットセット定義
    - [ ] 全OLLセット（57パターン）
    - [ ] 全PLLセット（21パターン）
    - [ ] 全F2Lセット（41パターン）
    - [ ] 全Crossセット（8パターン）
  - [ ] カスタムセット管理
    - [ ] セット作成・保存
    - [ ] セット読み込み
    - [ ] セット編集（追加・削除・並び替え）
    - [ ] セット削除
- [x] パターン選択ロジック（Phase 2-3で実装済み）
  - [x] ランダム選択（OLL/PLL/ALL カテゴリ指定、重複回避）
  - [x] 手動選択（パターンリストから、ページ送り対応）
  - [ ] セット順次実行（Phase 4）

##### 3. データベース拡張（stats.py, log_handler.py）
- [x] パターン練習用テーブルの追加
  ```sql
  -- パターン解法記録テーブル（Phase 1で実装済み）
  CREATE TABLE pattern_solves (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      pattern_id TEXT NOT NULL,           -- パターンID（例："OLL_01"）
      pattern_name TEXT NOT NULL,         -- パターン名（例："OLL #1"）
      pattern_category TEXT NOT NULL,     -- カテゴリ（"OLL", "PLL"等）
      solve_time REAL NOT NULL,           -- 解法時間（秒）
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      session_id TEXT,                    -- セッションID
      practice_mode TEXT,                 -- 練習モード（"random", "manual", "preset", "custom"）
      set_id TEXT,                        -- カスタムセットID（該当する場合）
      algorithm_id TEXT,                  -- 使用したアルゴリズムID（Phase 1.5で追加）
      FOREIGN KEY (session_id) REFERENCES sessions(session_id)
  );
  
  -- ユーザーのパターン設定テーブル（Phase 2で実装予定）
  CREATE TABLE user_pattern_preferences (
      pattern_id TEXT PRIMARY KEY,
      selected_algorithm_id TEXT,         -- ユーザーが選択したアルゴリズム
      priority INTEGER DEFAULT 0,         -- 練習優先度
      notes TEXT,                         -- ユーザーメモ
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  
  -- ユーザーのアルゴリズム評価テーブル（Phase 2で実装予定）
  CREATE TABLE user_algorithm_ratings (
      algorithm_id TEXT PRIMARY KEY,
      speed_rating INTEGER,               -- スピード評価 (1-5)
      ergonomics_rating INTEGER,          -- 使いやすさ評価 (1-5)
      is_favorite BOOLEAN DEFAULT 0,      -- お気に入り
      user_notes TEXT,                    -- ユーザーメモ
      practice_count INTEGER DEFAULT 0,   -- 練習回数
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  
  -- カスタムセット保存テーブル（Phase 5で実装予定）
  CREATE TABLE pattern_custom_sets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      set_id TEXT UNIQUE NOT NULL,        -- セットID
      set_name TEXT NOT NULL,             -- セット名
      pattern_ids TEXT NOT NULL,          -- パターンIDのJSON配列
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  
  -- インデックス作成（Phase 1で実装済み）
  CREATE INDEX idx_pattern_solves_pattern_id ON pattern_solves(pattern_id);
  CREATE INDEX idx_pattern_solves_category ON pattern_solves(pattern_category);
  CREATE INDEX idx_pattern_solves_timestamp ON pattern_solves(timestamp);
  ```
- [x] パターン別統計取得メソッドの実装（Phase 1-2で実装済み）
  - [x] `get_pattern_times(pattern_id, limit=None)` - 特定パターンの全タイム取得
  - [x] `get_pattern_best(pattern_id)` - パターンのベストタイム
  - [x] `get_pattern_count(pattern_id)` - パターンの試技回数
  - [x] `save_pattern_solve()` - パターン解法の記録
  - [ ] `get_pattern_average(pattern_id)` - パターンの平均タイム（Phase 6）
  - [ ] `get_pattern_ao5(pattern_id)` - パターンのAO5（Phase 6）
  - [ ] `get_pattern_ao12(pattern_id)` - パターンのAO12（Phase 6）
- [x] アルゴリズム別統計取得メソッドの実装（Phase 2で実装済み）
  - [x] `get_algorithm_times(algorithm_id, limit=None)` - アルゴリズムの全タイム取得
  - [x] `get_algorithm_best(algorithm_id)` - アルゴリズムのベストタイム
  - [x] `get_algorithm_count(algorithm_id)` - アルゴリズムの試技回数
- [x] ユーザー設定管理メソッドの実装（Phase 2で実装済み）
  - [x] `get_user_selected_algorithm(pattern_id)` - ユーザーが選択したアルゴリズム取得
  - [x] `set_user_selected_algorithm(pattern_id, algorithm_id)` - アルゴリズム選択を保存
  - [x] `get_algorithm_rating(algorithm_id)` - アルゴリズム評価取得
  - [x] `set_algorithm_rating(algorithm_id, rating)` - 評価保存（1-5）
- [ ] カスタムセット管理メソッド
  - [ ] `save_custom_set(set_id, set_name, pattern_ids)` - セット保存
  - [ ] `load_custom_set(set_id)` - セット読み込み
  - [ ] `get_all_custom_sets()` - 全カスタムセット取得
  - [ ] `delete_custom_set(set_id)` - セット削除
  - [ ] `update_custom_set(set_id, set_name, pattern_ids)` - セット更新

##### 4. UI/UX実装（renderer.py）
- [x] **パターン選択画面**の描画（Phase 2-3で実装済み）
  - [x] カテゴリタブ（RAND/PLL/OLL）
  - [x] RANDタブ：カテゴリ選択UI（OLL/PLL/ALL）
  - [x] PLL/OLLタブ：パターン一覧表示
    - [x] 試技回数とベストタイム表示
    - [x] 選択中のアルゴリズム表示
    - [x] カーソル/選択ハイライト
    - [x] ページ送り（左右キー、5件単位）
    - [x] 循環ナビゲーション

- [x] **アルゴリズム選択画面**の描画（Phase 2で実装済み）
  - [x] パターン名表示
  - [x] アルゴリズム一覧（複数ある場合）
  - [x] 各アルゴリズムの詳細（ムーブ、評価）
  - [x] 選択カーソル表示

- [ ] **モード選択画面**の描画（Phase 4以降）
  - [ ] プリセット連続実行
  - [ ] カスタム連続実行

- [ ] **カスタムセット編集画面**の描画
  - [ ] 保存済みセット一覧
  - [ ] 新規セット作成ボタン
  - [ ] セット詳細表示
    - [ ] セット名
    - [ ] 含まれるパターン数
    - [ ] 編集・削除ボタン
  - [ ] パターン追加UI
    - [ ] カテゴリ選択
    - [ ] パターン選択
    - [ ] 追加ボタン
  - [ ] パターンリスト表示（並び替え可能）

- [x] **パターン準備画面**の描画（Phase 2で実装済み）
  - [x] パターン名表示
  - [x] アルゴリズム情報表示（名前、ムーブ）
  - [x] 統計情報表示（試技回数、ベストタイム）
  - [x] 操作ガイド表示（SPACE長押しでスタート）

- [x] **パターン実行画面**の描画（Phase 2で実装済み）
  - [x] パターン名表示（上部）
  - [x] アルゴリズム情報表示
  - [x] タイマー表示（中央）

- [x] **パターン完了画面**の描画（Phase 2-3で実装済み）
  - [x] パターン名とタイム表示
  - [x] 評価入力（1-5キー）
  - [x] 操作ガイド（SPACE: 次へ、R: リトライ、ESC: 戻る）
  - [x] ランダムモード対応（連続練習）

##### 5. 状態ハンドラ（state_handlers.py）
- [x] **PatternListSelectHandler** - パターン選択ハンドラ（Phase 2-3で実装済み）
  - [x] カテゴリタブ切り替え（TABキー）
  - [x] RANDタブ処理（カテゴリ選択、ランダム抽出）
  - [x] パターン一覧表示制御（PLL/OLLタブ）
  - [x] カーソル移動（上下キー、循環）
  - [x] ページ送り（左右キー、5件単位）
  - [x] パターン決定（ENTERキー）
  - [x] アルゴリズム選択画面遷移（Aキー）
  - [x] READY状態に戻る（ESCキー、状態クリア）

- [x] **PatternAlgorithmSelectHandler** - アルゴリズム選択ハンドラ（Phase 2で実装済み）
  - [x] アルゴリズム一覧表示
  - [x] カーソル移動（上下キー）
  - [x] アルゴリズム決定（ENTERキー、ユーザー選択保存）
  - [x] パターン一覧に戻る（ESCキー）

- [x] **PatternReadyHandler** - パターン準備ハンドラ（Phase 2で実装済み）
  - [x] スペースキー長押し検知→タイマー開始
  - [x] パターン一覧に戻る（ESCキー）

- [x] **PatternFinishHandler** - パターン完了ハンドラ（Phase 2-3で実装済み）
  - [x] 評価入力（1-5キー）
  - [x] リトライ処理（Rキー）
  - [x] 次の動作処理
    - [x] SPACE/ENTER: 通常モードは一覧へ、ランダムモードは次のパターンへ
    - [x] ESC: ランダムモード解除して一覧へ
  - [x] 評価の自動保存

- [ ] **プリセット連続実行ハンドラ**（Phase 4）
  - [ ] セット進捗管理
  - [ ] 次のパターンへ自動遷移
  - [ ] セット完了処理

- [ ] **カスタムセット編集ハンドラ**（Phase 5）
  - [ ] セット作成・編集・削除
  - [ ] パターン追加・削除・並び替え
  - [ ] カテゴリ/パターン選択画面
    - [ ] 上下左右キー：カーソル移動
    - [ ] Enter/スペース：決定
    - [ ] ESC：前の画面に戻る
  - [ ] パターン準備・実行画面
    - [ ] スペースキー：インスペクション/開始/停止
    - [ ] Sキー：スキップ
    - [ ] ESC：パターンモード終了
  - [ ] パターン結果画面
    - [ ] スペースキー：次のパターン
    - [ ] Rキー：リトライ
    - [ ] ESC：パターンモード終了
  - [ ] カスタムセット編集画面
    - [ ] 上下キー：項目移動
    - [ ] Enter：決定
    - [ ] Delete：削除
    - [ ] Nキー：新規作成
    - [ ] ESC：前の画面に戻る

##### 6. Stats画面の拡張（renderer.py）
- [ ] **パターン統計画面への切り替え**
  - [ ] STATS画面でタブ切り替え機能
    - [ ] 「Monthly Stats」タブ（既存）
    - [ ] 「Pattern Stats」タブ（新規）
  - [ ] タブキーまたは数字キーで切り替え

- [ ] **パターン統計サマリー表示**
  - [ ] 全体統計
    - [ ] 総パターン数（例：「127 patterns」）
    - [ ] 練習済みパターン数（例：「45/127」）
    - [ ] 総試技回数
    - [ ] 最も練習したパターン
  - [ ] カテゴリ別統計
    - [ ] OLL：練習済み/総数、平均タイム
    - [ ] PLL：練習済み/総数、平均タイム
    - [ ] F2L：練習済み/総数、平均タイム
    - [ ] Cross：練習済み/総数、平均タイム

- [ ] **パターン詳細リスト表示**
  - [ ] カテゴリ選択（OLL/PLL/F2L/Cross/全て）
  - [ ] パターンテーブル表示
    ```
    Pattern    | Count | Best  | Avg   | AO5   | Last Practiced
    OLL #1     | ×15   | 2.34s | 3.12s | 2.98s | 2025/11/05
    OLL #2     | ×0    | ---   | ---   | ---   | ---
    ```
  - [ ] 未練習パターンのハイライト（グレーアウト）
  - [ ] 苦手パターンの識別
    - [ ] 平均タイムがカテゴリ平均より遅い
    - [ ] 赤色または警告マーク表示
  - [ ] 得意パターンの表示
    - [ ] 平均タイムがカテゴリ平均より速い
    - [ ] 緑色または優秀マーク表示

- [ ] **ソート機能**
  - [ ] ソートキー選択
    - [ ] パターン名順（デフォルト）
    - [ ] 試技回数順（多い→少ない）
    - [ ] ベストタイム順（速い→遅い）
    - [ ] 平均タイム順（速い→遅い）
    - [ ] 最終練習日順（新しい→古い）
  - [ ] 昇順/降順切り替え

- [ ] **フィルタ機能**
  - [ ] カテゴリフィルタ（OLL/PLL/F2L/Cross）
  - [ ] 状態フィルタ
    - [ ] 全て
    - [ ] 練習済みのみ
    - [ ] 未練習のみ
    - [ ] 苦手パターンのみ（平均 > カテゴリ平均）
    - [ ] 得意パターンのみ（平均 < カテゴリ平均）
    - [ ] 最近練習したパターン（7日以内）

- [ ] **パターン詳細表示（選択時）**
  - [ ] パターン情報
    - [ ] パターン名
    - [ ] カテゴリ
    - [ ] 難易度
    - [ ] セットアップムーブ
  - [ ] 統計情報
    - [ ] 試技回数
    - [ ] ベストタイム
    - [ ] 平均タイム
    - [ ] AO5 / AO12
    - [ ] 最終練習日
  - [ ] タイム履歴（直近10回）
    - [ ] タイムのリスト表示
    - [ ] グラフ表示（オプション）
  - [ ] アクション
    - [ ] 「このパターンを練習」ボタン
    - [ ] 「カスタムセットに追加」ボタン

- [ ] **スクロール・ページネーション**
  - [ ] 上下キーでスクロール
  - [ ] PageUp/PageDownで高速スクロール
  - [ ] 表示範囲インジケータ（例：「1-20 / 57」）

##### 7. Google Sheets連携拡張（log_handler.py）
- [ ] パターン練習用シートの追加
- [ ] パターン別記録の同期処理
- [ ] 統計データの同期

##### 8. 設定・カスタマイズ
- [ ] パターン表示設定
  - [ ] スクランブル表示の有無
  - [ ] セットアップムーブの表示
- [ ] 自動次パターン機能の設定
- [ ] パターン順序の設定（順番/ランダム/カスタム）

##### 9. テスト項目
- [ ] **パターンデータテスト**
  - [ ] パターン定義の正確性（OLL 57種、PLL 21種など）
  - [ ] セットアップムーブの検証
  - [ ] パターンIDの一意性確認

- [ ] **モード選択テスト**
  - [ ] ランダム単発実行モード
    - [ ] ランダム選択の動作確認
    - [ ] カテゴリ別ランダム選択
  - [ ] 手動パターン選択モード
    - [ ] パターン選択UIの動作
    - [ ] 選択したパターンの正確な実行
  - [ ] プリセット連続実行モード
    - [ ] 全パターンの順次実行
    - [ ] スキップ機能
    - [ ] 進捗管理
  - [ ] カスタム連続実行モード
    - [ ] カスタムセットの作成
    - [ ] セットの保存・読み込み
    - [ ] セットの編集・削除

- [ ] **タイマー機能テスト**
  - [ ] インスペクションタイムの正確性
  - [ ] タイマー計測の正確性
  - [ ] パターン別記録の保存

- [ ] **データベーステスト**
  - [ ] パターン記録の保存
  - [ ] カスタムセットの保存・読み込み
  - [ ] 統計情報の取得
  - [ ] データの整合性確認

- [ ] **統計計算テスト**
  - [ ] パターン別ベストタイム計算
  - [ ] パターン別平均タイム計算
  - [ ] パターン別AO5/AO12計算
  - [ ] カテゴリ別統計計算
  - [ ] 苦手パターン識別の正確性

- [ ] **UI/UXテスト**
  - [ ] 各画面の表示確認
  - [ ] 画面遷移の確認
  - [ ] キーバインドの動作確認
  - [ ] エラーハンドリング

- [ ] **パフォーマンステスト**
  - [ ] 大量パターンでの動作確認
  - [ ] 統計計算の速度
  - [ ] データベースクエリの最適化

- [ ] **Google Sheets同期テスト**
  - [ ] パターン記録の同期
  - [ ] カスタムセットの同期（オプション）
  - [ ] エラー時の挙動

##### 10. ドキュメント
- [ ] **ユーザーガイド**
  - [ ] パターン習得モードの概要
  - [ ] 各練習モードの使い方
    - [ ] ランダム単発実行モードの使用方法
    - [ ] 手動パターン選択モードの使用方法
    - [ ] プリセット連続実行モードの使用方法
    - [ ] カスタム連続実行モードの使用方法
  - [ ] カスタムセットの作成方法
  - [ ] パターン統計の見方
  - [ ] 効果的な練習方法のTips

- [ ] **開発者ドキュメント**
  - [ ] パターン定義フォーマット
  - [ ] データベーススキーマ
  - [ ] 新しいパターンの追加方法
  - [ ] カスタムカテゴリの追加方法
  - [ ] APIリファレンス

- [ ] **設計ドキュメント**
  - [ ] アーキテクチャ図
  - [ ] 状態遷移図
  - [ ] データフロー図
  - [ ] UI/UXワイヤーフレーム

---

### タイマー機能の拡充
既存のタイマー機能に対する改善・拡張項目

- [ ] 終了確認画面の作成
- [ ] 手動アップロード処理の作成
- [ ] タイマー表示の改善
  - [ ] デジタル時計風の大きな表示
  - [ ] 都度描画 vs BMP読み込みのパフォーマンス検証
  - [ ] 描画であれば、三角形+長方形+三角形で1パーツ構成
- [ ] サウンドの改善
  - [ ] より明確なフィードバック音
  - [ ] 音量調整機能
  - [ ] 音声パターンのカスタマイズ
- [ ] ローカルDBからのレコード削除機能
  - [ ] 個別レコード削除
  - [ ] 一括削除
  - [ ] 削除確認ダイアログ
- [ ] 画面読み込み処理の実装
  - [ ] ローディングアニメーション
  - [ ] 非同期読み込み
- [ ] 設定ファイル機能
  - [ ] 色設定の読み込み（コンフィグファイル）
  - [ ] 自動設定保存機能
  - [ ] 設定のインポート/エクスポート
- [ ] Stats画面の実装改善
  - [ ] より詳細な統計表示
  - [ ] グラフ表示機能
- [ ] 画面遷移の実装改善
  - [ ] スムーズなトランジション効果
  - [ ] 画面遷移アニメーション
- [ ] 設定画面の実装
  - [ ] 各種オプション設定
  - [ ] キーバインドカスタマイズ
  - [ ] テーマ選択
- [ ] サイレントモードの実装
  - [ ] 音声OFF機能
  - [ ] ビジュアルフィードバックのみのモード
- [ ] メイン画面の表示改善
  - [ ] 描画メソッドを使った改善
  - [ ] レイアウトの最適化
  - [ ] 情報の可読性向上
- [ ] **セッション管理機能の拡張**
  - [ ] セッション選択UI
  - [ ] セッション名前付け機能
  - [ ] セッション統計の比較
- [ ] **統計情報の視覚化**
  - [ ] グラフ表示（折れ線グラフ、棒グラフ）
  - [ ] タイムの推移表示
  - [ ] 記録の分布表示