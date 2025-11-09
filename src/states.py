"""タイマーの状態を管理するための列挙型"""
from enum import Enum, auto

class TimerState(Enum):
    """タイマーの状態を表す列挙型"""
    READY = auto()       # 準備完了状態
    COUNTDOWN = auto()   # インスペクション/カウントダウン状態
    RUNNING = auto()     # 計測中状態
    SYNCING = auto()     # 同期中状態
    STATS = auto()       # 統計画面状態
    
    # パターン習得モード用の状態（Phase 2）
    PATTERN_LIST_SELECT = auto()      # パターン一覧選択画面
    PATTERN_ALGORITHM_SELECT = auto()  # アルゴリズム選択画面
    PATTERN_READY = auto()            # パターン表示・準備状態
    PATTERN_FINISH = auto()           # パターン完了・評価画面