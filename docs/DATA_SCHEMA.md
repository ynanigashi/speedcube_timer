# データスキーマ仕様書

このドキュメントでは、Speedcube Timerで使用するマスターデータ（JSON）とリソースファイル（Pyxel）の仕様を定義します。

## 目次
- [patterns.json - パターンデータ](#patternsjson---パターンデータ)
- [algorithms.json - アルゴリズムデータ](#algorithmsjson---アルゴリズムデータ)
- [speedcube_timer.pyxres - Pyxelリソース](#speedcube_timerpyxres---pyxelリソース)
- [config.ini - 設定ファイル](#configini---設定ファイル)

---

## patterns.json - パターンデータ

### ファイルパス
`data/patterns.json`

### スキーマ構造

```json
{
  "patterns": [
    {
      "id": "string (必須)",
      "name": "string (必須)",
      "category": "OLL" | "PLL" (必須)",
      "setup_moves": "string (必須)",
      "description": "string (任意)",
      "difficulty": number (任意, 1-5)
    }
  ]
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 | 例 |
|-----------|---|-----|------|---|
| `id` | string | ✅ | パターンの一意識別子。`{CATEGORY}_{NUMBER}`形式を推奨 | `"OLL_01"`, `"PLL_A"` |
| `name` | string | ✅ | パターンの表示名 | `"OLL #1"`, `"T-Perm"` |
| `category` | string | ✅ | カテゴリ。`"OLL"`または`"PLL"`のみ | `"OLL"` |
| `setup_moves` | string | ✅ | パターンのセットアップ手順（キューブ記法） | `"R U R' U'"` |
| `description` | string | ❌ | パターンの説明文 | `"Pure dot (all edges flipped)"` |
| `difficulty` | number | ❌ | 難易度（1-5の整数） | `3` |

### カテゴリ列挙値

- `"OLL"`: Orientation of the Last Layer（57パターン）
- `"PLL"`: Permutation of the Last Layer（21パターン）

### データ例

```json
{
  "patterns": [
    {
      "id": "OLL_01",
      "name": "OLL #1",
      "category": "OLL",
      "setup_moves": "R U2 R2 F R F' U2 R' F R F'",
      "description": "Pure dot (all edges flipped)",
      "difficulty": 3
    },
    {
      "id": "PLL_A",
      "name": "A-Perm",
      "category": "PLL",
      "setup_moves": "R' F R' B2 R F' R' B2 R2",
      "description": "Adjacent corner swap",
      "difficulty": 2
    }
  ]
}
```

### 実装での使用方法

```python
from src.patterns import PatternDatabase, PatternCategory

db = PatternDatabase()

# カテゴリでフィルタ
oll_patterns = db.get_patterns_by_category(PatternCategory.OLL)

# IDで取得
pattern = db.get_pattern("OLL_01")
```

---

## algorithms.json - アルゴリズムデータ

### ファイルパス
`data/algorithms.json`

### スキーマ構造

```json
{
  "algorithms": [
    {
      "id": "string (必須)",
      "pattern_id": "string (必須)",
      "name": "string (必須)",
      "moves": "string (必須)",
      "finger_tricks": "string (任意)",
      "is_default": boolean (必須)",
      "notes": "string (任意)"
    }
  ]
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 | 例 |
|-----------|---|-----|------|---|
| `id` | string | ✅ | アルゴリズムの一意識別子。`{PATTERN_ID}_{NAME}`形式を推奨 | `"OLL_01_standard"` |
| `pattern_id` | string | ✅ | 対応するパターンID（`patterns.json`の`id`） | `"OLL_01"` |
| `name` | string | ✅ | アルゴリズムの表示名 | `"Standard"`, `"Alternative 1"` |
| `moves` | string | ✅ | アルゴリズムの手順（キューブ記法） | `"R U R' U' R' F R F'"` |
| `finger_tricks` | string | ❌ | フィンガートリックのヒント | `"RU with thumb"` |
| `is_default` | boolean | ✅ | デフォルトアルゴリズムか否か。各パターンに1つだけ`true`を設定 | `true` |
| `notes` | string | ❌ | メモや補足説明 | `"最も一般的"` |

### キューブ記法

標準的なキューブ記法を使用：

- **基本回転**: `R`, `L`, `U`, `D`, `F`, `B`（時計回り90度）
- **逆回転**: `R'`, `L'`, `U'`, `D'`, `F'`, `B'`（反時計回り90度）
- **2回転**: `R2`, `L2`, `U2`, `D2`, `F2`, `B2`（180度）
- **広い回転**: `r`, `l`, `u`, `d`, `f`, `b`（2層同時回転、小文字）
- **逆広回転**: `r'`, `l'`, `u'`, `d'`, `f'`, `b'`
- **回転**: `x`, `y`, `z`（キューブ全体の回転）

### データ例

```json
{
  "algorithms": [
    {
      "id": "OLL_01_standard",
      "pattern_id": "OLL_01",
      "name": "Standard",
      "moves": "R U2 R2 F R F' U2 R' F R F'",
      "finger_tricks": "",
      "is_default": true,
      "notes": "最も一般的"
    },
    {
      "id": "OLL_01_alternative_1",
      "pattern_id": "OLL_01",
      "name": "Alternative 1",
      "moves": "y R U' R2 D' r U' r' D R2 U R'",
      "finger_tricks": "",
      "is_default": false,
      "notes": "D回転使用"
    }
  ]
}
```

### 実装での使用方法

```python
# パターンのアルゴリズム一覧を取得
algorithms = db.get_algorithms_for_pattern("OLL_01")

# デフォルトアルゴリズムを取得
default_algo = db.get_default_algorithm("OLL_01")

# IDで取得
algo = db.get_algorithm("OLL_01_standard")
```

---

## speedcube_timer.pyxres - Pyxelリソース

### ファイルパス
`data/speedcube_timer.pyxres`

### 概要

Pyxelリソースファイルには以下が含まれます：

- **サウンドバンク**: 効果音定義
- **パレット**: カラーパレット（16色）
- **フォント**: 日本語対応フォント

### サウンド定義

アプリケーションで使用するサウンドは`src/constants.py`の`SoundConfig`クラスで定義されています。

#### サウンドチャンネル

| チャンネル | 用途 | 定数名 |
|-----------|------|--------|
| 0 | ビープ音・システム音 | `BEEP_CHANNEL` |
| 1 | 効果音 | `SOUND_CHANNEL` |

#### サウンドインデックス

| インデックス | 名前 | 用途 | 定数名 |
|------------|------|------|--------|
| 0 | カウントダウン音 | インスペクション残り3,2,1秒のビープ | `COUNTDOWN_SOUND` |
| 1 | スタート音 | タイマー開始時 | `START_SOUND` |
| 2 | フィニッシュ音 | タイマー停止時 | `FINISH_SOUND` |
| 3 | 変更音 | 状態遷移・選択変更時 | `CHANGE_SOUND` |
| 4 | ホールド音 | キー長押し中の継続音 | `HOLD_SOUND` |
| 5 | 同期音 | 手動同期開始時 | `SYNC_SOUND` |

#### 使用例

```python
import pyxel
from src.constants import SoundConfig as SC

# カウントダウン音を再生
pyxel.play(SC.BEEP_CHANNEL, SC.COUNTDOWN_SOUND)

# フィニッシュ音を再生
pyxel.play(SC.SOUND_CHANNEL, SC.FINISH_SOUND)
```

### パレット定義

Pyxelの16色パレットを使用。デフォルト配色：

| インデックス | 色 | 用途例 |
|------------|---|--------|
| 0 | 黒 | テキスト（明るい背景時） |
| 1 | 紺色 | デフォルト背景色 |
| 2 | 紫 | - |
| 3 | 緑 | - |
| 4 | 茶色 | - |
| 5 | 濃いグレー | - |
| 6 | 薄いグレー | - |
| 7 | 白 | テキスト（暗い背景時） |
| 8 | 赤 | 警告色（インスペクション4秒以下） |
| 9 | オレンジ | - |
| 10 | 黄色 | - |
| 11 | ライム | - |
| 12 | シアン | - |
| 13 | 青 | - |
| 14 | ラベンダー | - |
| 15 | ピンク | - |

### フォント

日本語対応のBDFフォントを使用：

| フォント名 | サイズ | 用途 | 定数 |
|-----------|-------|------|------|
| `umplus_j10r.bdf` | 10pt | 中サイズテキスト（スクランブル等） | `MIDDLE_FONT_FILE` |
| `umplus_j12r.bdf` | 12pt | 大サイズテキスト（タイマー表示等） | `LARGE_FONT_FILE` |

フォントパス: `.venv/Lib/site-packages/pyxel/examples/assets/`

---

## config.ini - 設定ファイル

### ファイルパス
`config.ini`（ルートディレクトリ）

テンプレート: `config.ini.example`

### 構造

```ini
[GoogleSpreadsheet]
spreadsheet_key = YOUR_SPREADSHEET_KEY
sheet_name = YOUR_SHEET_NAME
credentials_file = path/to/credentials.json

[Database]
db_path = data/speedcube.db
```

### セクション: `[GoogleSpreadsheet]`

Google Sheets APIとの連携設定（同期機能を使用する場合のみ必須）。

| キー | 必須 | 説明 | 例 |
|-----|-----|------|---|
| `spreadsheet_key` | ✅ | スプレッドシートのID。URLの`/d/{ここ}/edit`部分 | `1a2b3c4d5e6f7g8h9i0j` |
| `sheet_name` | ✅ | 使用するシート名（タブ名） | `Speedcube Records` |
| `credentials_file` | ✅ | Google API認証情報のJSONファイルパス（相対または絶対） | `credentials.json` |

#### Google API認証情報の取得手順

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成（または既存プロジェクトを選択）
3. 「APIとサービス」→「ライブラリ」で「Google Sheets API」を有効化
4. 「APIとサービス」→「認証情報」へ移動
5. 「認証情報を作成」→「サービスアカウント」を選択
6. サービスアカウントを作成し、JSONキーをダウンロード
7. ダウンロードしたJSONファイルを`credentials.json`としてプロジェクトルートに配置
8. スプレッドシートをサービスアカウントのメールアドレスと共有（編集権限）

### セクション: `[Database]`

SQLiteデータベースの設定。

| キー | 必須 | 説明 | デフォルト値 |
|-----|-----|------|-----------|
| `db_path` | ❌ | データベースファイルの保存パス（相対または絶対） | `data/speedcube.db` |

未設定の場合、`data/speedcube.db`が使用されます。

### 設定例

```ini
[GoogleSpreadsheet]
spreadsheet_key = 1a2b3c4d5e6f7g8h9i0jklmnopqrstuv
sheet_name = Speedcube Records
credentials_file = credentials.json

[Database]
db_path = data/speedcube.db
```

### 設定なしでの動作

- `config.ini`が存在しない場合、Google Sheets同期機能は無効化されます
- データベースは`data/speedcube.db`にデフォルト作成されます
- ローカルのみでの記録・統計機能は正常に動作します

---

## ランダムモード仕様

### 概要

パターン練習モードのRANDタブで利用できる、ランダムパターン選択機能の詳細仕様。

### カテゴリ選択肢

| カテゴリ | 説明 | 対象パターン数 |
|---------|------|--------------|
| `OLL` | OLLパターンのみ | 57パターン |
| `PLL` | PLLパターンのみ | 21パターン |
| `ALL` | OLL+PLL全パターン | 78パターン |

### 重複回避機能

直近5件の履歴を保持し、同じパターンが連続しないようにします。

#### パラメータ

- **履歴サイズ**: 5パターン（`recent_random_patterns`リストで管理）
- **除外対象**: 履歴に含まれるパターンID

#### フロー

```
1. ユーザーがカテゴリ（OLL/PLL/ALL）を選択
2. 選択カテゴリのパターン一覧を取得
3. 履歴（最大5件）に含まれるパターンを除外
4. 残りの候補からランダムに1つ選択
5. 選択したパターンを履歴に追加
6. 履歴が6件以上になったら最古の履歴を削除（5件に維持）
```

#### 実装コード例

```python
# src/patterns.py の get_random_pattern メソッド
def get_random_pattern(self, category: str = "ALL", 
                       exclude_ids: list = None) -> Pattern:
    """
    ランダムにパターンを取得（重複回避機能付き）
    
    Args:
        category: "OLL", "PLL", "ALL"のいずれか
        exclude_ids: 除外するパターンIDのリスト
        
    Returns:
        選択されたPatternオブジェクト
    """
    if category == "ALL":
        candidates = self.patterns
    else:
        cat_enum = PatternCategory[category]
        candidates = self.get_patterns_by_category(cat_enum)
    
    # 除外リストをフィルタ
    if exclude_ids:
        candidates = [p for p in candidates if p.id not in exclude_ids]
    
    # 候補が空の場合は履歴を無視
    if not candidates:
        if category == "ALL":
            candidates = self.patterns
        else:
            candidates = self.get_patterns_by_category(
                PatternCategory[category]
            )
    
    return random.choice(candidates)
```

#### 使用例

```python
# app.py でのランダムモード使用
random_pattern = self.pattern_db.get_random_pattern(
    category=self.random_category,  # "OLL", "PLL", "ALL"
    exclude_ids=self.recent_random_patterns  # 直近5件の履歴
)

# 履歴に追加
self.recent_random_patterns.append(random_pattern.id)
if len(self.recent_random_patterns) > 5:
    self.recent_random_patterns.pop(0)  # 最古を削除
```

### 連続実行モード

ランダムモードでは、パターン完了後にSPACE/ENTERキーで次のランダムパターンへ自動遷移します。

- **継続条件**: `random_mode = True`が設定されている
- **解除方法**: ESCキーでパターン一覧に戻る（`random_mode = False`に設定）

---

## UI仕様（画面レイアウト）

詳細は別ドキュメント [UI_SPECIFICATION.md](UI_SPECIFICATION.md) を参照してください。

- 画面サイズ: 397×240ピクセル
- レイアウト定数: `src/constants.py`の`DisplayConfig`クラスで定義
- 各状態ごとの描画仕様
- 配色・フォントサイズ・座標情報

---

## バージョン互換性

- **Python**: 3.10以上
- **Pyxel**: 2.3.18（固定）
- **gspread**: 6.2.0
- **google-auth**: 2.38.0

`requirements.txt`で固定バージョンを指定しているため、互換性問題を避けるため必ずこのバージョンを使用してください。

---

## 参考リンク

- [Pyxel公式ドキュメント](https://github.com/kitao/pyxel)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [キューブ記法（英語）](https://ruwix.com/the-rubiks-cube/notation/)
