# UI仕様書

このドキュメントでは、Speedcube TimerのUI（ユーザーインターフェース）の詳細仕様を定義します。

## 目次
- [画面サイズとレイアウト](#画面サイズとレイアウト)
- [配色設定](#配色設定)
- [フォント設定](#フォント設定)
- [状態別画面仕様](#状態別画面仕様)
- [アニメーション・エフェクト](#アニメーションエフェクト)

---

## 画面サイズとレイアウト

### ウィンドウサイズ

```python
WINDOW_WIDTH = 397  # ピクセル
WINDOW_HEIGHT = 240  # ピクセル
FPS = 30  # フレームレート
```

計算式: `MIDDLE_FONT_WIDTH(5) * 59 + FONT_SPACING_X(1) * 58 + MARGIN_X(20) * 2 = 397`

### マージン・スペーシング

| 定数 | 値 | 説明 |
|-----|---|------|
| `MARGIN_X` | 20px | 左右のマージン |
| `MARGIN_Y` | 10px | 上下のマージン |
| `FONT_SPACING_X` | 1px | 文字間の横スペース |
| `FONT_SPACING_Y` | 5px | 行間の縦スペース |

### Y座標レイアウト

| 要素 | Y座標 | 計算式 |
|-----|-------|--------|
| スクランブルラベル | 10px | `MARGIN_Y` |
| スクランブルテキスト | 25px | `SCRAMBLE_Y + MIDDLE_FONT_HEIGHT + FONT_SPACING_Y` |
| タイマー表示 | 70px | `SCRAMBLE_TEXT_Y + MIDDLE_FONT_HEIGHT + MARGIN_Y * 3` |
| 結果表示開始 | 112px | `TIMER_Y + LARGE_FONT_HEIGHT + MARGIN_Y * 3` |

---

## 配色設定

### デフォルト配色

```python
DEFAULT_BACKGROUND_COLOR = 1   # 紺色
DEFAULT_TEXT_COLOR = 7         # 白色
DEFAULT_WARNING_COLOR = 8      # 赤色
DEFAULT_BLINK_COLOR = 7        # 白色（点滅用）
```

### 背景色切り替え

Cキーで背景色を変更可能（0-15のパレット番号を循環）。

```python
# 背景色に応じてテキスト色を自動調整
if bg_color < 6:
    text_color = 7  # 白（暗い背景）
else:
    text_color = 0  # 黒（明るい背景）
```

### 状態別配色

| 状態 | 背景色 | テキスト色 | 特殊色 |
|-----|-------|----------|--------|
| READY | 紺(1) | 白(7) | - |
| COUNTDOWN | 紺(1) | 白(7) | 警告:赤(8) |
| RUNNING | 紺(1) | 白(7) | - |
| STATS | 紺(1) | 白(7) | - |
| SYNCING | 紺(1) | 白(7) | - |
| PATTERN_* | 紺(1) | 白(7) | 選択:反転 |

### 警告色の使用

インスペクション残り4秒以下で赤色(8)に変更：

```python
if remaining_time <= 4:
    color = WARNING_COLOR  # 赤(8)
else:
    color = TEXT_COLOR  # 白(7)
```

---

## フォント設定

### フォントサイズ

| サイズ | 幅 | 高さ | 用途 | 定数 |
|-------|---|-----|------|------|
| 小 | 4px | 8px | 小テキスト（未使用） | `SMALL_FONT_*` |
| 中 | 5px | 10px | スクランブル、ラベル、リスト | `MIDDLE_FONT_*` |
| 大 | 6px | 12px | タイマー表示 | `LARGE_FONT_*` |

### 使用フォント

- **中サイズ**: `umplus_j10r.bdf`（10ポイント日本語対応）
- **大サイズ**: `umplus_j12r.bdf`（12ポイント日本語対応）

### テキスト描画メソッド

```python
# Pyxel標準（小サイズ）
pyxel.text(x, y, text, color)

# BDFフォント（中・大サイズ）
pyxel.text(x, y, text, color, font=MIDDLE_FONT_FILE)
pyxel.text(x, y, text, color, font=LARGE_FONT_FILE)
```

---

## 状態別画面仕様

### READY - メイン画面

```
┌─────────────────────────────────────┐
│ SCRAMBLE                   (10, 10) │
│ R U R' U' R' F R F'       (10, 25) │
│                                     │
│         12.34            (中央, 70) │
│                                     │
│ RECENT                    (10, 112) │
│ #01:  12.34              (10, 127) │
│ #02:  13.56              (10, 142) │
│ #03:  11.23              (10, 157) │
│ #04:  14.78              (10, 172) │
│ #05:  12.90              (10, 187) │
│                                     │
│ AO5 : 12.96    AO12: 13.12 (10,202)│
│ PRESS [Q] TO QUIT         (10, 217) │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 色 |
|-----|-------|-------|---------|---|
| "SCRAMBLE" | 10 | 10 | 中 | テキスト色 |
| スクランブル文字列 | 10 | 25 | 中 | テキスト色 |
| タイム | 中央揃え | 70 | 大 | テキスト色 |
| "RECENT" | 10 | 112 | 中 | テキスト色 |
| 記録リスト（5件） | 10 | 127+ | 中 | テキスト色 |
| AO5/AO12 | 10 | 202 | 中 | テキスト色 |
| "PRESS [Q] TO QUIT" | 10 | 217 | 中 | テキスト色 |

### COUNTDOWN - インスペクション

```
┌─────────────────────────────────────┐
│ SCRAMBLE                            │
│ R U R' U' R' F R F'                │
│                                     │
│ INSPECTION TIME                     │
│         12                          │
│                                     │
│ HOLD [SPACE] TO START               │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 色 | 備考 |
|-----|-------|-------|---------|---|------|
| "INSPECTION TIME" | 中央 | 70 | 中 | テキスト色 | |
| 残り時間 | 中央 | 95 | 大 | 条件付き | ≤4秒:赤、>4秒:白 |
| "HOLD [SPACE]..." | 中央 | 130 | 中 | テキスト色 | |

#### 残り時間の色分け

```python
if remaining_time <= 4:
    color = 8  # 赤色で警告
else:
    color = 7  # 白色
```

### RUNNING - タイマー実行中

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│         12.34                       │
│                                     │
│ PRESS [SPACE] TO STOP               │
│                                     │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 色 |
|-----|-------|-------|---------|---|
| 経過時間 | 中央 | 70 | 大 | テキスト色 |
| "PRESS [SPACE] TO STOP" | 中央 | 130 | 中 | テキスト色 |

### STATS - 統計画面

```
┌─────────────────────────────────────┐
│ SESSION STATS                       │
│                                     │
│ Best   : 10.23                      │
│ Worst  : 15.67                      │
│ Average: 12.45                      │
│ AO5    : 12.34                      │
│ AO12   : 12.89                      │
│ Count  : 23 solves                  │
│                                     │
│ MONTHLY STATS (2025/11)             │
│ Solves : 150                        │
│ Average: 13.21                      │
│                                     │
│ [←] BACK TO READY                   │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 色 |
|-----|-------|-------|---------|---|
| "SESSION STATS" | 10 | 10 | 中 | テキスト色 |
| 各統計項目 | 20 | 30+ | 中 | テキスト色 |
| "MONTHLY STATS" | 10 | 130 | 中 | テキスト色 |
| 月次統計 | 20 | 150+ | 中 | テキスト色 |
| "[←] BACK" | 10 | 217 | 中 | テキスト色 |

### SYNCING - 同期中・結果表示

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│       SYNCING...                    │
│                                     │
│   downloaded: 0, Uploaded: 5        │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 色 |
|-----|-------|-------|---------|---|
| "SYNCING..." | 中央 | 70 | 大 | テキスト色 |
| 同期結果 | 中央 | 100 | 中 | テキスト色 |

約1.5秒後にREADYに自動遷移。

### PATTERN_LIST_SELECT - パターン選択

```
┌─────────────────────────────────────┐
│ [RAND] [PLL] [OLL]       ← タブ    │
│                                     │
│ ▶ OLL #1  (3 algorithms)           │
│   OLL #2  (2 algorithms)           │
│   OLL #3  (1 algorithm)            │
│   ...                               │
│                                     │
│ Page 1/12                           │
│ [A]lgorithm [ESC]Back               │
└─────────────────────────────────────┘
```

#### タブ表示

- 選択中のタブは反転表示（背景:テキスト色、文字:背景色）
- 未選択タブは通常表示（背景:背景色、文字:テキスト色）

#### リスト表示

- 選択中の項目は先頭に`▶`マーカー表示
- 1ページ5件表示
- スクロールオフセットで表示範囲を調整

#### 座標

| 要素 | X座標 | Y座標 | フォント | 備考 |
|-----|-------|-------|---------|------|
| タブ（各） | 10, 90, 170 | 10 | 中 | 等間隔配置 |
| リスト項目 | 20 | 40+ | 中 | 15px間隔 |
| ページ番号 | 10 | 200 | 中 | |
| 操作ガイド | 10 | 217 | 中 | |

### PATTERN_ALGORITHM_SELECT - アルゴリズム選択

```
┌─────────────────────────────────────┐
│ OLL #1 - Select Algorithm           │
│                                     │
│ ▶ Standard                          │
│   R U2 R2 F R F' U2 R' F R F'      │
│   (Default)                         │
│                                     │
│   Alternative 1                     │
│   y R U' R2 D' r U' r' D R2 U R'   │
│                                     │
│ [ESC]Back                           │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント | 備考 |
|-----|-------|-------|---------|------|
| パターン名 | 10 | 10 | 中 | |
| アルゴリズム名 | 20 | 40+ | 中 | 選択中は`▶`付き |
| 手順 | 30 | 55+ | 中 | 折り返し表示 |
| デフォルト表記 | 30 | - | 中 | "(Default)" |

### PATTERN_READY - パターン準備

```
┌─────────────────────────────────────┐
│ OLL #1 - Standard                   │
│                                     │
│ R U2 R2 F R F' U2 R' F R F'        │
│                                     │
│ Best: 2.34  Count: 15               │
│                                     │
│ HOLD [SPACE] TO START               │
│ [A]lgorithm [ESC]Back               │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント |
|-----|-------|-------|---------|
| パターン+アルゴリズム名 | 10 | 10 | 中 |
| アルゴリズム手順 | 10 | 40 | 中 |
| 統計情報 | 10 | 70 | 中 |
| "HOLD [SPACE]..." | 中央 | 130 | 中 |
| 操作ガイド | 10 | 217 | 中 |

### PATTERN_FINISH - パターン結果

```
┌─────────────────────────────────────┐
│ OLL #1 - Standard                   │
│                                     │
│ Time: 2.45                          │
│ Best: 2.34                          │
│                                     │
│ Rating: ★★★☆☆ (3)                  │
│ [1-5] Set Rating                    │
│                                     │
│ [R]etry [SPACE]Next [ESC]Back       │
└─────────────────────────────────────┘
```

#### 表示要素

| 要素 | X座標 | Y座標 | フォント |
|-----|-------|-------|---------|
| パターン+アルゴリズム名 | 10 | 10 | 中 |
| 記録タイム | 10 | 50 | 大 |
| ベストタイム | 10 | 80 | 中 |
| 評価表示 | 10 | 110 | 中 |
| 操作ガイド | 10 | 217 | 中 |

---

## アニメーション・エフェクト

### 点滅表示

カウントダウン中やホールド中のテキストで使用。

```python
BLINK_CYCLE = 30  # 1サイクル30フレーム（1秒）
BLINK_ON_TIME = 20  # 1サイクル中20フレーム表示

# 点滅判定
if (pyxel.frame_count % BLINK_CYCLE) < BLINK_ON_TIME:
    pyxel.text(x, y, text, color)  # 表示
else:
    # 非表示
    pass
```

### ホールド進捗表示

```python
hold_progress = (pyxel.frame_count - hold_start) / FPS
hold_text = f"HOLD: {hold_progress:.1f}"
```

### スクロールアニメーション

パターン選択リストで使用。

```python
# 選択位置に応じてスクロールオフセットを調整
if selected_index >= scroll_offset + visible_items:
    scroll_offset = selected_index - visible_items + 1
elif selected_index < scroll_offset:
    scroll_offset = selected_index
```

---

## 中央揃え計算

```python
def center_x(text: str, font_width: int) -> int:
    """テキストを水平中央揃えにするX座標を計算"""
    text_width = len(text) * font_width
    return (WINDOW_WIDTH - text_width) // 2

# 使用例
x = center_x("12.34", LARGE_FONT_WIDTH)  # 大フォント用
pyxel.text(x, y, "12.34", color, font=LARGE_FONT_FILE)
```

---

## レスポンシブ対応

現在は固定サイズ（397×240）のみ対応。

将来的な拡張:
- ウィンドウサイズ変更への対応
- 高解像度ディスプレイ対応
- モバイル表示対応

---

## アクセシビリティ

### 配色コントラスト

- 背景色と文字色は十分なコントラストを確保
- 警告色（赤）は明確に識別可能

### キーボード操作

- すべての操作をキーボードのみで完結
- マウス操作は不要

### 視認性

- 大きなフォントサイズでタイマー表示
- 重要な情報は画面中央に配置

---

## 実装参考コード

### 描画の基本構造

```python
def draw(self):
    """状態に応じた描画"""
    pyxel.cls(self.bg_color)  # 背景クリア
    
    if self.state == TimerState.READY:
        self._draw_ready()
    elif self.state == TimerState.COUNTDOWN:
        self._draw_countdown()
    # ... 他の状態
```

### テキスト描画ヘルパー

```python
def draw_text_centered(text: str, y: int, color: int, 
                       font_size: str = "large"):
    """中央揃えでテキストを描画"""
    if font_size == "large":
        font = LARGE_FONT_FILE
        width = LARGE_FONT_WIDTH
    else:
        font = MIDDLE_FONT_FILE
        width = MIDDLE_FONT_WIDTH
    
    x = center_x(text, width)
    pyxel.text(x, y, text, color, font=font)
```

---

## 関連ドキュメント

- [ARCHITECTURE.md](ARCHITECTURE.md) - システム設計
- [DATA_SCHEMA.md](DATA_SCHEMA.md) - データ仕様
- [constants.py](../src/constants.py) - 定数定義（実装）
- [renderer.py](../src/renderer.py) - 描画実装
