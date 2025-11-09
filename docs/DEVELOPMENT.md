# 開発者ガイド

このドキュメントでは、Speedcube Timerの開発を行う上での実践的な情報を提供します。

## 目次
- [開発環境の詳細設定](#開発環境の詳細設定)
- [デバッグ方法](#デバッグ方法)
- [トラブルシューティング](#トラブルシューティング)
- [よくある開発タスク](#よくある開発タスク)
- [パフォーマンス最適化](#パフォーマンス最適化)

---

## 開発環境の詳細設定

### Visual Studio Code設定

#### 推奨拡張機能

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "ms-toolsai.jupyter",
    "visualstudioexptteam.vscodeintellicode"
  ]
}
```

#### .vscode/settings.json

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true
  }
}
```

#### .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Current Test File",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "${file}",
        "-v"
      ],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

### 仮想環境の管理

#### venvの再構築

```powershell
# 既存の仮想環境を削除
Remove-Item -Recurse -Force .venv

# 新規作成
python -m venv .venv

# 有効化
.\.venv\Scripts\Activate.ps1

# 依存関係の再インストール
pip install -r requirements.txt
```

#### 依存関係の更新

```powershell
# 現在のパッケージリストを確認
pip list

# 特定パッケージのアップグレード
pip install --upgrade pyxel

# 全パッケージのアップグレード（注意して実行）
pip list --outdated
pip install --upgrade <package_name>

# requirements.txtを更新
pip freeze > requirements.txt
```

---

## デバッグ方法

### Pyxelアプリケーションのデバッグ

#### ログ出力の活用

```python
import logging

# log_handler.pyでの設定
logger = logging.getLogger(__name__)

# 各モジュールでの使用
logger.debug(f"Current state: {self.state}")
logger.info(f"Timer started at {timestamp}")
logger.warning(f"No algorithm found for pattern {pattern_id}")
logger.error(f"Database error: {e}")
```

#### ログレベルの変更

`config.ini`でログレベルを調整：

```ini
[Logging]
level = DEBUG  # DEBUG, INFO, WARNING, ERROR
file = logs/speedcube_timer.log
```

#### プリントデバッグ

```python
# app.pyのupdate()内
def update(self):
    print(f"State: {self.state}, Frame: {pyxel.frame_count}")
    
    # 状態遷移のトレース
    old_state = self.state
    # ... 処理 ...
    if old_state != self.state:
        print(f"State transition: {old_state} -> {self.state}")
```

### データベースのデバッグ

#### SQLiteブラウザでの確認

[DB Browser for SQLite](https://sqlitebrowser.org/) をインストール：

```powershell
# chocolateyを使用
choco install db-browser-for-sqlite

# または直接ダウンロード
# https://sqlitebrowser.org/dl/
```

データベースファイルを開く：
```
data/speedcube.db
```

#### SQL直接実行

```python
# デバッグ用のSQLを実行
import sqlite3

conn = sqlite3.connect('data/speedcube.db')
cursor = conn.cursor()

# テーブルの内容確認
cursor.execute("SELECT * FROM pattern_solves ORDER BY timestamp DESC LIMIT 10")
print(cursor.fetchall())

# 統計確認
cursor.execute("""
    SELECT pattern_id, COUNT(*), AVG(solve_time), MIN(solve_time)
    FROM pattern_solves
    GROUP BY pattern_id
""")
print(cursor.fetchall())

conn.close()
```

### パフォーマンスプロファイリング

#### cProfileを使用

```python
import cProfile
import pstats

# app.pyの最後に追加
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    app = SpeedcubeApp()
    pyxel.run(app.update, app.draw)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # 上位20個を表示
```

---

## トラブルシューティング

### よくある問題と解決方法

#### 1. Pyxelが起動しない

**症状**: `ImportError: No module named 'pyxel'`

**解決方法**:
```powershell
# 仮想環境が有効化されているか確認
.\.venv\Scripts\Activate.ps1

# pyxelを再インストール
pip uninstall pyxel
pip install pyxel==2.3.18
```

#### 2. データベースエラー

**症状**: `sqlite3.OperationalError: no such table`

**解決方法**:
```powershell
# データベースファイルを削除して再作成
Remove-Item data\speedcube.db

# アプリケーションを起動（自動で再作成される）
python main.py
```

#### 3. Google Sheets同期が失敗する

**症状**: `gspread.exceptions.APIError`

**確認事項**:
1. `credentials.json`が正しく配置されているか
2. Google Sheets APIが有効になっているか
3. インターネット接続があるか

**解決方法**:
```powershell
# credentials.jsonの確認
Test-Path credentials.json

# config.iniの設定確認
Get-Content config.ini

# ログを確認
Get-Content logs/speedcube_timer.log | Select-String "sheets"
```

#### 4. 文字化け

**症状**: 日本語が正しく表示されない

**解決方法**:
- Pyxelのバージョンを確認（2.3.18以上）
- フォントリソースの確認
- ソースコードのエンコーディング確認（UTF-8 BOM無し）

#### 5. 音が鳴らない

**症状**: インスペクション音やアラートが鳴らない

**解決方法**:
```python
# pyxresファイルの確認
import os
print(os.path.exists("data/speedcube_timer.pyxres"))

# Pyxelリソースの再読み込み
pyxel.load("data/speedcube_timer.pyxres")
```

### ログの確認

```powershell
# 最新のログを確認
Get-Content logs/speedcube_timer.log -Tail 50

# エラーのみフィルタ
Get-Content logs/speedcube_timer.log | Select-String "ERROR"

# 特定の文字列を検索
Get-Content logs/speedcube_timer.log | Select-String "pattern"
```

---

## よくある開発タスク

### 新しいパターンの追加

1. **data/patterns.jsonに追加**

```json
{
  "id": "OLL_58",
  "category": "OLL",
  "name": "OLL 58",
  "description": "...",
  "image_path": "assets/oll_58.png",
  "algorithm_ids": ["OLL_58_A", "OLL_58_B"]
}
```

2. **data/algorithms.jsonに追加**

```json
{
  "id": "OLL_58_A",
  "pattern_id": "OLL_58",
  "notation": "R U R' U' R' F R F'",
  "name": "Sexy Move",
  "description": "基本的なアルゴリズム"
}
```

3. **テストを追加**

```python
# tests/test_patterns.py
def test_new_pattern():
    patterns = load_patterns()
    pattern = get_pattern("OLL_58")
    assert pattern is not None
    assert pattern.name == "OLL 58"
```

### 新しい画面（状態）の追加

1. **states.pyに状態を追加**

```python
class TimerState(Enum):
    # 既存の状態...
    NEW_STATE = "new_state"
```

2. **state_handlers.pyにハンドラーを追加**

```python
class NewStateHandler:
    def handle_input(self, app):
        if pyxel.btnp(pyxel.KEY_SPACE):
            return TimerState.READY
        return None
```

3. **renderer.pyに描画関数を追加**

```python
def draw_new_state(self):
    pyxel.cls(0)
    pyxel.text(50, 50, "New State", 7)
```

4. **app.pyに統合**

```python
def update(self):
    # ...
    elif self.state == TimerState.NEW_STATE:
        handler = NewStateHandler()
        new_state = handler.handle_input(self)
        if new_state:
            self.state = new_state

def draw(self):
    # ...
    elif self.state == TimerState.NEW_STATE:
        self.renderer.draw_new_state()
```

### 統計項目の追加

1. **データベースにカラム追加**

```python
# stats.py の _create_tables() 内
cursor.execute('''
    CREATE TABLE IF NOT EXISTS solves (
        -- 既存のカラム...
        new_column TEXT
    )
''')
```

2. **保存処理を更新**

```python
# log_handler.py の save_solve() 内
cursor.execute('''
    INSERT INTO solves 
    (session_id, solve_time, scramble, timestamp, new_column)
    VALUES (?, ?, ?, ?, ?)
''', (session_id, solve_time, scramble, timestamp, new_value))
```

3. **取得処理を追加**

```python
# stats.py に新しいメソッド
def get_new_statistic(self):
    cursor = self.conn.cursor()
    cursor.execute("SELECT new_column FROM solves")
    return cursor.fetchall()
```

### テストの追加

```python
# tests/test_new_feature.py
import pytest
from src.module import function_to_test

def test_function_basic():
    """基本的なテスト"""
    result = function_to_test(input_value)
    assert result == expected_value

def test_function_edge_case():
    """エッジケースのテスト"""
    result = function_to_test(edge_case_input)
    assert result == edge_case_expected

def test_function_error():
    """エラーケースのテスト"""
    with pytest.raises(ValueError):
        function_to_test(invalid_input)
```

---

## パフォーマンス最適化

### 描画の最適化

```python
# 変更前: 毎フレーム全体を再描画
def draw(self):
    pyxel.cls(0)
    self._draw_all_elements()

# 変更後: 必要な部分のみ更新
def draw(self):
    if self.needs_redraw:
        pyxel.cls(0)
        self._draw_all_elements()
        self.needs_redraw = False
    else:
        # 動的な部分のみ更新（タイマー表示など）
        self._draw_dynamic_elements()
```

### データベースクエリの最適化

```python
# 変更前: N+1クエリ
for pattern_id in pattern_ids:
    times = get_pattern_times(pattern_id)
    # 処理...

# 変更後: バッチクエリ
cursor.execute("""
    SELECT pattern_id, solve_time
    FROM pattern_solves
    WHERE pattern_id IN ({})
""".format(','.join('?' * len(pattern_ids))), pattern_ids)
all_times = cursor.fetchall()
```

### メモリ使用の最適化

```python
# 変更前: 全データをメモリに読み込み
all_solves = cursor.execute("SELECT * FROM solves").fetchall()

# 変更後: ページングまたはジェネレーター
def get_solves_paginated(page_size=100):
    offset = 0
    while True:
        cursor.execute(
            "SELECT * FROM solves LIMIT ? OFFSET ?",
            (page_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += page_size
```

---

## デバッグのヒント

### Pyxel特有のデバッグ

```python
# フレームカウントでデバッグ
if pyxel.frame_count % 60 == 0:  # 1秒ごと
    print(f"FPS: {pyxel.frame_count / (time.time() - start_time)}")

# 入力のトレース
if pyxel.btnp(pyxel.KEY_SPACE):
    print(f"Space pressed at frame {pyxel.frame_count}")

# 描画領域の可視化
pyxel.rectb(x, y, w, h, 8)  # デバッグ用の矩形
```

### ステートマシンのデバッグ

```python
# state_history を追加
self.state_history = []

def change_state(self, new_state):
    self.state_history.append({
        'from': self.state,
        'to': new_state,
        'frame': pyxel.frame_count,
        'timestamp': datetime.now()
    })
    self.state = new_state
    
    # 履歴を表示
    if len(self.state_history) > 100:
        print("State history:")
        for s in self.state_history[-10:]:
            print(f"  {s}")
```

---

## 追加リソース

- [Pyxel公式ドキュメント](https://github.com/kitao/pyxel)
- [SQLite公式ドキュメント](https://www.sqlite.org/docs.html)
- [gspread公式ドキュメント](https://docs.gspread.org/)
- [プロジェクトロードマップ](roadmap.md)
- [アーキテクチャドキュメント](ARCHITECTURE.md)

質問や問題があれば、GitHubのIssueで相談してください！
