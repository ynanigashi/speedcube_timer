from enum import Enum, auto

class TimerState(Enum):
    READY = auto()
    COUNTDOWN = auto()
    RUNNING = auto()
    FINISHED = auto()  # 追加