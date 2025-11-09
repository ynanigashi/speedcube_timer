# Speedcube Timer フロー図

このドキュメントでは、Speedcube Timerの画面遷移とフローをMermaid図で示します。

## 目次
- [現在の実装状態（Phase 1-3完了）](#現在の実装状態phase-1-3完了)
- [通常タイマーモード](#通常タイマーモード)
- [パターン練習モード - 手動選択](#パターン練習モード---手動選択)
- [パターン練習モード - ランダム](#パターン練習モード---ランダム)
- [将来の計画（Phase 4-6）](#将来の計画phase-4-6)

---

## 現在の実装状態（Phase 1-3完了）

### 全体の状態遷移

```mermaid
stateDiagram-v2
    [*] --> READY
    
    READY --> STATS: 右矢印キー
    STATS --> READY: 左矢印キー
    READY --> SYNCING: Sキー長押し
    SYNCING --> READY: 同期結果表示後
    
    READY --> PATTERN_LIST_SELECT: Pキー
    PATTERN_LIST_SELECT --> READY: ESCキー
    
    READY --> COUNTDOWN: SPACE長押し
    COUNTDOWN --> RUNNING: SPACE長押しor15秒経過
    COUNTDOWN --> READY: ESCキー(スクランブル再生成)
    RUNNING --> READY: SPACE押下(記録保存)
    RUNNING --> READY: ESCキー(計測中断)
    
    note right of READY
        メインメニュー
        - 通常タイマー
        - パターン練習
        - 統計表示
        - 手動同期（Sキー長押し）
        - 背景色切り替え（Cキー）
    end note
```

---

## 通常タイマーモード

```mermaid
flowchart TD
    Start([起動]) --> Ready[READY<br/>スクランブル表示]
    
    Ready -->|右矢印| Stats[STATS<br/>統計表示画面]
    Stats -->|左矢印| Ready
    Ready -->|S長押し| Sync[SYNCING<br/>手動同期結果表示]
    Sync --> Ready
    Ready -->|C| Color[背景色切替]
    Color --> Ready
    
    Ready -->|SPACE長押し| Countdown[COUNTDOWN<br/>インスペクション<br/>15秒カウントダウン]
    
    Countdown -->|SPACE長押し| Running[RUNNING<br/>タイマー計測中]
    Countdown -->|15秒経過| Running
    Countdown -->|ESC| CancelCountdown[スクランブル再生成]
    CancelCountdown --> Ready
    
    Running -->|SPACE押下| SaveRecord[記録保存<br/>スクランブル再生成]
    SaveRecord --> Ready
    Running -->|ESC| CancelRunning[計測中断<br/>記録なし<br/>スクランブル再生成]
    CancelRunning --> Ready
    
    Ready -->|ESC| NewScramble[新しいスクランブル生成]
    NewScramble --> Ready
    
    Ready -->|Q| Exit([終了])
    
    style Ready fill:#e1f5ff
    style Countdown fill:#fff4e1
    style Running fill:#fff9e1
    style SaveRecord fill:#e1ffe1
    style CancelCountdown fill:#ffe1e1
    style CancelRunning fill:#ffe1e1
    style Sync fill:#e1ffe1
    style Color fill:#fff4e1
```

---

## パターン練習モード - 手動選択

```mermaid
flowchart TD
    Ready[READY] -->|Pキー| PatternList[PATTERN_LIST_SELECT<br/>パターン選択画面<br/>RAND/PLL/OLLタブ]
    
    PatternList -->|TAB| TabSwitch{タブ切り替え}
    TabSwitch -->|順次| PatternList
    
    PatternList -->|PLL/OLLタブ<br/>選択中| ManualMode{手動選択モード}
    
    ManualMode -->|上下キー| CursorMove[カーソル移動<br/>循環ナビゲーション]
    CursorMove --> ManualMode
    
    ManualMode -->|左右キー| PageMove[ページ送り<br/>5件単位・循環]
    PageMove --> ManualMode
    
    ManualMode -->|Aキー<br/>複数アルゴリズム有| AlgoSelect[PATTERN_ALGORITHM_SELECT<br/>アルゴリズム選択]
    
    AlgoSelect -->|上下キー| AlgoCursor[カーソル移動]
    AlgoCursor --> AlgoSelect
    
    AlgoSelect -->|ENTER| SaveAlgo[アルゴリズム選択保存]
    SaveAlgo --> PatternReady
    
    AlgoSelect -->|ESC| PatternList
    
    ManualMode -->|ENTER| PatternReady[PATTERN_READY<br/>パターン準備画面<br/>アルゴリズム表示]
    
    PatternReady -->|SPACE長押し| PatternRun[RUNNING<br/>タイマー計測]
    
    PatternRun -->|SPACE押下| SavePatternRecord[記録保存<br/>DB格納]
    SavePatternRecord --> PatternFinish[PATTERN_FINISH<br/>結果表示・評価入力]
    
    PatternRun -->|ESC| BackToList[パターン一覧に戻る]
    BackToList --> PatternList
    
    PatternFinish -->|1-5キー| Rating[評価設定<br/>1-5]
    Rating --> PatternFinish
    
    PatternFinish -->|Rキー| PatternReady
    PatternFinish -->|SPACE/ENTER| SaveAndBack[評価自動保存]
    SaveAndBack --> PatternList
    
    PatternFinish -->|ESC| ClearState[状態クリア]
    ClearState --> PatternList
    
    PatternReady -->|ESC| PatternList
    PatternList -->|ESC| ClearAll[パターンモード終了<br/>状態クリア]
    ClearAll --> Ready
    
    style PatternList fill:#ffe1f5
    style PatternReady fill:#e1f5ff
    style PatternRun fill:#fff9e1
    style SavePatternRecord fill:#e1ffe1
    style PatternFinish fill:#e1ffe1
    style BackToList fill:#ffe1e1
```

---

## パターン練習モード - ランダム

```mermaid
flowchart TD
    Ready[READY] -->|Pキー| PatternList[PATTERN_LIST_SELECT<br/>パターン選択画面]
    
    PatternList -->|TAB→RANDタブ| RandTab[RANDタブ選択]
    
    RandTab --> RandUI[ランダムカテゴリ選択UI<br/>OLL / PLL / ALL]
    
    RandUI -->|上下キー| CategorySelect[カテゴリ選択]
    CategorySelect --> RandUI
    
    RandUI -->|ENTER| RandomPick[ランダムパターン抽出<br/>重複回避:直近5件除外]
    
    RandomPick --> SetMode[random_mode = True<br/>履歴に追加]
    
    SetMode --> RandReady[PATTERN_READY<br/>ランダムモード<br/>パターン&アルゴリズム表示]
    
    RandReady -->|SPACE長押し| RandRun[RUNNING<br/>タイマー計測]
    
    RandRun -->|SPACE押下| SaveRandRecord[記録保存<br/>DB格納]
    SaveRandRecord --> RandFinish[PATTERN_FINISH<br/>ランダムモード<br/>結果表示・評価入力]
    
    RandRun -->|ESC| ExitRand2[random_mode = False]
    ExitRand2 --> PatternList
    
    RandFinish -->|1-5キー| RandRating[評価設定]
    RandRating --> RandFinish
    
    RandFinish -->|Rキー| RandReady
    
    RandFinish -->|SPACE/ENTER| NextRandom[次のランダムパターン抽出<br/>重複回避適用]
    NextRandom --> UpdateHistory[履歴更新<br/>最大5件保持]
    UpdateHistory --> RandReady
    
    RandFinish -->|ESC| ExitRand[random_mode = False<br/>状態クリア]
    ExitRand --> PatternList
    
    RandReady -->|ESC| PatternList
    PatternList -->|ESC| ClearAll[パターンモード終了]
    ClearAll --> Ready
    
    style RandTab fill:#fff4e1
    style RandReady fill:#e1f5ff
    style RandRun fill:#fff9e1
    style SaveRandRecord fill:#e1ffe1
    style RandFinish fill:#e1ffe1
    style NextRandom fill:#ffe1e1
    style ExitRand2 fill:#ffe1e1
```

### ランダムモードの重複回避ロジック

```mermaid
flowchart LR
    Start([ランダム抽出開始]) --> GetCategory[カテゴリ取得<br/>OLL/PLL/ALL]
    
    GetCategory --> GetHistory[履歴取得<br/>recent_random_patterns<br/>最大5件]
    
    GetHistory --> FilterPatterns[候補パターン抽出<br/>履歴IDを除外]
    
    FilterPatterns --> CheckEmpty{候補が空?}
    
    CheckEmpty -->|Yes| UseAll[履歴無視<br/>全パターンから選択]
    CheckEmpty -->|No| RandomSelect[候補からランダム選択]
    
    UseAll --> RandomSelect
    RandomSelect --> AddHistory[履歴に追加]
    
    AddHistory --> CheckLimit{履歴が5件超?}
    CheckLimit -->|Yes| RemoveOldest[最古の履歴削除]
    CheckLimit -->|No| Done([完了])
    
    RemoveOldest --> Done
    
    style FilterPatterns fill:#e1f5ff
    style RandomSelect fill:#ffe1e1
```

---

## 将来の計画（Phase 4-6）

### Phase 4: プリセット連続実行モード（未実装）

```mermaid
flowchart TD
    PatternList[PATTERN_LIST_SELECT] -->|新機能| PresetMode[プリセットモード選択]
    
    PresetMode --> CategorySelect[カテゴリ選択<br/>OLL全57/PLL全21]
    
    CategorySelect -->|ENTER| LoadSet[セット読み込み<br/>全パターンリスト作成]
    
    LoadSet --> SetIndex[進捗管理<br/>current_index = 0]
    
    SetIndex --> PresetReady[PATTERN_READY<br/>1/57表示<br/>進捗バー]
    
    PresetReady -->|SPACE長押し| PresetRun[RUNNING]
    
    PresetRun -->|SPACE| PresetFinish[PATTERN_FINISH<br/>進捗表示]
    
    PresetFinish -->|SPACE/ENTER| NextCheck{次のパターン有?}
    
    NextCheck -->|Yes| IncrementIndex[index++]
    IncrementIndex --> PresetReady
    
    NextCheck -->|No| Complete[セット完了画面<br/>統計サマリー]
    
    Complete -->|SPACE/ENTER| PatternList
    
    PresetFinish -->|ESC| PatternList
    
    style PresetMode fill:#e1e1ff
    style Complete fill:#e1ffe1
```

### Phase 5: カスタムセット機能（未実装）

```mermaid
flowchart TD
    PatternList[PATTERN_LIST_SELECT] -->|新機能| CustomMode[カスタムセット選択]
    
    CustomMode --> SetList[保存済みセット一覧]
    
    SetList -->|ENTER| LoadCustom[セット読み込み]
    LoadCustom --> CustomReady[連続実行開始]
    
    SetList -->|Nキー| CreateNew[新規セット作成]
    
    CreateNew --> EditMode[PATTERN_CUSTOM_SET_EDIT<br/>セット編集画面]
    
    EditMode --> AddPattern[パターン追加UI<br/>カテゴリ→パターン選択]
    
    AddPattern -->|ENTER| AddToSet[セットに追加]
    AddToSet --> EditMode
    
    EditMode -->|上下キー| Reorder[パターン並び替え]
    Reorder --> EditMode
    
    EditMode -->|DEL| RemovePattern[パターン削除]
    RemovePattern --> EditMode
    
    EditMode -->|Sキー| SaveSet[セット保存<br/>DB格納]
    SaveSet --> SetList
    
    EditMode -->|ESC| SetList
    
    CustomReady --> CustomRun[RUNNING]
    CustomRun --> CustomFinish[PATTERN_FINISH]
    CustomFinish -->|次へ| CustomReady
    
    style CustomMode fill:#ffe1f5
    style EditMode fill:#e1e1ff
```

### Phase 6: 統計画面拡張（未実装）

```mermaid
flowchart TD
    Stats[STATS画面] -->|新機能| DetailMode[詳細統計モード]
    
    DetailMode --> PatternStats[パターン別統計<br/>タブ切り替え]
    
    PatternStats --> CategoryView[カテゴリ別表示<br/>OLL/PLL]
    
    CategoryView --> PatternDetail[個別パターン詳細<br/>- 試技回数<br/>- ベスト/平均/AO5/AO12<br/>- タイム履歴グラフ<br/>- 使用アルゴリズム]
    
    DetailMode --> AlgoStats[アルゴリズム別統計]
    
    AlgoStats --> AlgoDetail[アルゴリズム詳細<br/>- 使用回数<br/>- ベスト/平均<br/>- 評価履歴]
    
    DetailMode --> WeakPattern[苦手パターン分析<br/>- 平均が遅いパターン<br/>- 未練習パターン<br/>- 練習推奨リスト]
    
    style DetailMode fill:#e1ffe1
    style WeakPattern fill:#ffe1e1
```

---

## データフロー

### パターン解法記録のデータフロー

```mermaid
flowchart LR
    User([ユーザー操作]) -->|計測完了| Timer[タイマー停止]
    
    Timer --> SaveSolve[pattern_solves<br/>テーブルに記録]
    
    SaveSolve --> Data[保存データ]
    
    Data -->|含む| PatternID[pattern_id]
    Data -->|含む| Time[solve_time]
    Data -->|含む| AlgoID[algorithm_id]
    Data -->|含む| Mode[practice_mode<br/>manual/random]
    
    SaveSolve --> UpdateStats[統計更新]
    
    UpdateStats --> Best[ベストタイム更新]
    UpdateStats --> Count[試技回数カウント]
    UpdateStats --> History[履歴記録]
    
    Best --> Display[画面表示]
    Count --> Display
    History --> Display
    
    style SaveSolve fill:#e1f5ff
    style UpdateStats fill:#ffe1e1
```

### ユーザー設定のデータフロー

```mermaid
flowchart LR
    User([ユーザー操作]) -->|アルゴリズム選択| AlgoSelect[アルゴリズム選択画面]
    
    AlgoSelect -->|ENTER| SavePref[user_pattern_preferences<br/>selected_algorithm_id保存]
    
    SavePref --> Persist[永続化]
    
    User -->|評価入力| RatingInput[1-5キー押下]
    
    RatingInput -->|完了画面で保存| SaveRating[user_algorithm_ratings<br/>評価保存]
    
    SaveRating --> Persist
    
    Persist --> NextTime[次回起動時]
    
    NextTime --> Restore[設定復元]
    
    Restore --> ShowAlgo[選択済みアルゴリズム表示]
    Restore --> ShowRating[評価表示]
    
    style SavePref fill:#e1f5ff
    style SaveRating fill:#ffe1e1
    style Restore fill:#e1ffe1
```

---

## 凡例

```mermaid
flowchart LR
    A[状態<br/>State] --> B[状態<br/>State]
    B -->|条件| C[処理<br/>Process]
    C --> D{判定<br/>Decision}
    D -->|Yes| E([終了<br/>End])
    D -->|No| A
    
    style A fill:#e1f5ff
    style C fill:#ffe1e1
    style E fill:#e1ffe1
```

- 青色: 状態（State）
- 赤色: 処理・アクション
- 緑色: 完了・終了状態
- 紫色: 特別な状態（編集モードなど）
