# Changelog

本プロジェクトのすべての重要な変更はこのファイルに記録されます。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [Unreleased]

### Phase 4 - プリセット連続実行モード（予定）
- プリセットセット機能（全OLL・全PLLを連続練習）
- セット進捗管理機能
- スキップ・中断機能

### Phase 5 - カスタムセット機能（予定）
- カスタムセット作成・編集・削除
- 苦手パターン識別機能
- セット管理UI

### Phase 6 - 統計表示と最適化（予定）
- パターン統計画面の拡張
- ソート・フィルタ機能
- パフォーマンス最適化

## [0.3.0] - 2025-11-09

### Phase 3 - ランダムモード完了

#### Added
- RANDタブの追加（RAND/PLL/OLLの順）
- カテゴリ別ランダム選択機能（OLL/PLL/ALL）
- 重複回避機能（最近5パターンを除外）
- 連続ランダム練習機能（SPACE連打で次々と練習）
- ランダムモード終了時の状態クリア処理

#### Fixed
- パターン練習後に通常タイマーに戻った際、パターン状態が残る不具合を修正
- ESCキーでパターン一覧に戻る際、全てのパターン関連状態をクリアするように修正

#### Changed
- タブ順序を使いやすさ優先に変更（OLL/PLL/RAND → RAND/PLL/OLL）

## [0.2.0] - 2025-11-08

### Phase 2 - 手動パターン選択モード完了

#### Added
- パターン選択画面の実装（カテゴリタブ、ページ送り、循環ナビゲーション）
- アルゴリズム選択画面の実装
- パターン準備画面の実装
- パターン結果画面の実装（評価入力機能付き）
- 78パターン対応（OLL: 57種、PLL: 21種）
- ユーザー設定テーブル（`user_pattern_preferences`, `user_algorithm_ratings`）
- アルゴリズム評価機能（1-5段階評価）
- 選択アルゴリズムの自動復元機能
- パターン・アルゴリズム別統計機能

#### Changed
- カテゴリタブによるパターン切り替え（TABキー）
- ページ送り機能（左右キー、5件単位）
- 循環ナビゲーション（末尾→先頭）

### Phase 1.5 - 複数アルゴリズム対応完了

#### Added
- `Algorithm`クラスの実装
- JSONファイルによるマスターデータ管理
  - `data/patterns.json` - パターン定義
  - `data/algorithms.json` - アルゴリズム定義
- アルゴリズム管理メソッド群の実装
- アルゴリズム別統計メソッドの実装
- デフォルトアルゴリズム管理機能

#### Changed
- `pattern_solves`テーブルに`algorithm_id`カラムを追加
- パターンとアルゴリズムを別々に管理する設計に変更

## [0.1.0] - 2025-11-05

### Phase 1 - 基盤構築完了

#### Added
- パターンデータ構造の設計・実装（`Pattern`クラス）
- データベーススキーマの拡張
  - `pattern_solves`テーブル作成
  - インデックス作成（3つ）
- 基本統計メソッドの実装
  - `get_pattern_times(pattern_id)`
  - `get_pattern_best(pattern_id)`
  - `get_pattern_count(pattern_id)`
- 状態定義の追加（`PATTERN_READY`）
- テストスクリプトの作成

#### テスト
- パターンデータの読み込みテスト
- DBテーブル作成の確認
- 統計メソッドの単体テスト

## [0.0.1] - 2025-10-31

### Initial Release - 基本タイマー機能

#### Added
- WCAルール準拠のタイマー機能
  - インスペクションタイム（15秒）
  - スペースキー長押しでスタート/ストップ
- 音声フィードバック機能
  - インスペクション開始音
  - カウントダウンビープ（8秒、12秒、15秒）
  - タイマー開始・終了音
- スクランブル生成機能
- SQLiteによるローカルデータベース
  - セッション単位での記録管理
  - `solves`テーブル、`sessions`テーブル
- Google Sheets連携機能
  - プログラム終了時の自動同期
- 統計表示機能
  - 最新5回の記録表示
  - AO5（直近5回の平均）
  - AO12（直近12回の平均）
  - 試技回数カウント
- 統計画面（STATS）
  - 月次統計表示
  - ESCキーで終了せず、LEFT矢印キーでREADYに戻る仕様

#### プロジェクト構造
- PyxelベースのGUIアプリケーション
- 状態マシンによる画面遷移管理（READY, COUNTDOWN, RUNNING, STATS）
- モジュール分割設計（app, renderer, states, state_handlers, stats, scramble, log_handler）

---

[Unreleased]: https://github.com/ynanigashi/speedcube_timer/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/ynanigashi/speedcube_timer/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ynanigashi/speedcube_timer/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ynanigashi/speedcube_timer/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/ynanigashi/speedcube_timer/releases/tag/v0.0.1
