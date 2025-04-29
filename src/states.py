"""タイマーの状態を管理するための列挙型"""
from enum import Enum, auto

class TimerState(Enum):
    """タイマーの状態を表す列挙型"""
    READY = auto()       # 準備完了状態
    COUNTDOWN = auto()   # インスペクション/カウントダウン状態
    RUNNING = auto()     # 計測中状態
    SYNCING = auto()      # 同期中状態