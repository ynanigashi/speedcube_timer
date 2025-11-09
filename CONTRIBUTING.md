# Contributing to Speedcube Timer

Speedcube Timerへのコントリビューションに興味を持っていただきありがとうございます！このドキュメントでは、プロジェクトへの参加方法を説明します。

## 目次
- [開発環境のセットアップ](#開発環境のセットアップ)
- [テストの実行](#テストの実行)
- [コーディング規約](#コーディング規約)
- [プルリクエストの手順](#プルリクエストの手順)
- [コミットメッセージ規約](#コミットメッセージ規約)

---

## 開発環境のセットアップ

### 前提条件
- Python 3.10以上
- Git
- Visual Studio Code（推奨）

### セットアップ手順

1. **リポジトリのクローン**
```bash
git clone https://github.com/ynanigashi/speedcube_timer.git
cd speedcube_timer
```

2. **仮想環境の作成と有効化**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **依存パッケージのインストール**
```bash
pip install -r requirements.txt
```

4. **設定ファイルの準備**
```bash
# config.ini.exampleをコピーしてconfig.iniを作成
copy config.ini.example config.ini  # Windows
cp config.ini.example config.ini    # macOS/Linux
```

5. **Google Sheets API設定（オプション）**
   - Google Cloud Consoleでプロジェクトを作成
   - Google Sheets APIを有効化
   - 認証情報を作成してJSONファイルを`credentials.json`として保存
    - `config.ini`の`[GoogleSpreadsheet]`セクション（`spreadsheet_key`, `sheet_name`, `credentials_file`）と`[Database]`セクション（`db_path`）を設定

6. **データベースの初期化**
   
    アプリケーションを初回起動すると、自動的にSQLiteデータベース（`data/speedcube.db`）が作成されます。保存先は`config.ini`の`[Database]`セクションで変更可能です。
    ```bash
    python main.py
    ```
   
    初回起動で以下のテーブルが自動作成されます：
    - `results` - 通常タイマーの記録
    - `pattern_solves` - パターン練習記録
    - `user_pattern_preferences` - パターンごとのデフォルトアルゴリズム
    - `user_algorithm_ratings` - アルゴリズム評価

7. **動作確認**
   - アプリケーションが正常に起動すること
   - スペースキー長押しでタイマーが起動すること
   - Pキーでパターン練習モードに入れること

---

## テストの実行

### テストの構成

プロジェクトには以下のテストファイルがあります：

```
tests/
├── test_phase1.py         # Phase 1（基盤構築）のテスト
├── test_algorithms.py     # 複数アルゴリズム機能のテスト
├── test_json_load.py      # JSONデータ読み込みのテスト
└── test_phase2.py         # Phase 2（手動選択モード）のテスト
```

### テストの実行方法

```bash
# 全テストを実行
python -m pytest tests/

# 特定のテストファイルを実行
python -m pytest tests/test_algorithms.py

# 詳細な出力で実行
python -m pytest tests/ -v

# カバレッジ付きで実行（要pytest-cov）
python -m pytest tests/ --cov=src
```

### 個別テストの実行

```bash
# Phase 1のテスト
python tests/test_phase1.py

# アルゴリズムのテスト
python tests/test_algorithms.py
```

### 新機能追加時のテスト要件

- 新しい機能を追加する場合、対応するテストも追加してください
- テストファイル名は `test_*.py` の形式で作成
- 重要な機能には単体テストを必ず追加
- プルリクエスト前に全テストが通過することを確認

---

## コーディング規約

### Python スタイルガイド

基本的に [PEP 8](https://pep8-ja.readthedocs.io/ja/latest/) に準拠します。

#### インデント
- スペース4つを使用
- タブは使用しない

#### 命名規則
- **クラス名**: PascalCase（例: `TimerState`, `PatternHandler`）
- **関数名**: snake_case（例: `get_pattern_times`, `save_solve`）
- **変数名**: snake_case（例: `current_pattern`, `solve_time`）
- **定数**: UPPER_CASE（例: `SCREEN_WIDTH`, `MAX_PATTERNS`）
- **プライベートメソッド**: 先頭にアンダースコア（例: `_internal_method`）

#### インポート順序
1. 標準ライブラリ
2. サードパーティライブラリ
3. プロジェクト内モジュール

```python
# 標準ライブラリ
import os
from datetime import datetime

# サードパーティ
import pyxel
import gspread

# プロジェクト内
from src.constants import SCREEN_WIDTH
from src.states import TimerState
```

#### コメント
- 複雑なロジックには日本語でコメントを追加
- 関数・クラスにはdocstringを記載（日本語可）

```python
def calculate_ao5(times: list[float]) -> float:
    """AO5（Average of 5）を計算する。
    
    最良と最悪のタイムを除いた3つの平均を返す。
    
    Args:
        times: タイムのリスト（5つ必要）
    
    Returns:
        float: AO5の値
    """
    if len(times) < 5:
        return 0.0
    sorted_times = sorted(times)
    return sum(sorted_times[1:4]) / 3
```

### ファイル構成規約

#### 新しいモジュールの追加
- `src/`ディレクトリ内に配置
- 単一責任の原則に従う
- 適切な命名（例: `stats.py`は統計関連、`renderer.py`は描画関連）

#### データファイルの配置
- マスターデータ: `data/`ディレクトリ
- ドキュメント: `docs/`ディレクトリ
- テスト: `tests/`ディレクトリ

---

## プルリクエストの手順

### 1. Issueの確認・作成

- 既存のIssueを確認し、重複がないか確認
- なければ新しいIssueを作成して、実装内容を説明

### 2. ブランチの作成

```bash
# featureブランチを作成
git checkout -b feature/your-feature-name

# bugfixブランチを作成
git checkout -b fix/bug-description
```

ブランチ命名規則：
- 機能追加: `feature/機能名`
- バグ修正: `fix/バグの説明`
- ドキュメント: `docs/ドキュメント名`
- リファクタリング: `refactor/対象`

### 3. 開発とコミット

- こまめにコミットする
- コミットメッセージは[規約](#コミットメッセージ規約)に従う
- テストを追加・更新する

### 4. テストの実行

```bash
# 全テストが通過することを確認
python -m pytest tests/

# コードスタイルのチェック（オプション）
flake8 src/
```

### 5. プッシュとプルリクエスト作成

```bash
git push origin feature/your-feature-name
```

GitHubでプルリクエストを作成：
- タイトルは簡潔に
- 説明には変更内容と動機を記載
- 関連するIssue番号を記載（例: `Closes #123`）
- スクリーンショットやGIFがあると良い

### 6. レビュー対応

- レビューコメントに対応
- 修正後は再度プッシュ
- 承認されたらマージ

---

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/ja/) に準拠します。

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type（必須）

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正や機能追加ではないコード変更
- `test`: テストの追加や修正
- `chore`: ビルドプロセスやツールの変更

### 例

```bash
# 良い例
feat: RANDタブによるランダムパターン選択機能を追加

OLL/PLL/ALLからランダムにパターンを選択できる機能を実装。
重複回避機能（最近5パターンを除外）も含む。

Closes #45

# シンプルな例
fix: パターン選択後の状態クリア処理を修正

# ドキュメント
docs: CONTRIBUTING.mdを追加
```

---

## 質問・相談

- Issueで質問を投稿してください
- バグ報告は可能な限り再現手順を記載してください
- 機能提案は背景と期待される効果を説明してください

---

## 参考リンク

- [開発ロードマップ](docs/roadmap.md) - 今後の実装計画
- [アーキテクチャドキュメント](docs/ARCHITECTURE.md) - システム設計
- [データスキーマ仕様](docs/DATA_SCHEMA.md) - JSON/リソース/設定ファイル仕様
- [UI仕様書](docs/UI_SPECIFICATION.md) - 画面レイアウトと配色
- [フロー図](docs/flow_diagrams.md) - 画面遷移
- [変更履歴](CHANGELOG.md) - リリース履歴

貢献していただきありがとうございます！
