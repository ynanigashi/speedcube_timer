"""GUI関連の定数を管理するモジュール"""

class DisplayConfig:
    """画面表示に関する設定"""
    # 色
    DEFAULT_BACKGROUND_COLOR = 1  # 紺色
    DEFAULT_TEXT_COLOR = 7  # 白色
    DEFAULT_WARNING_COLOR = 8  # 赤色（4秒以下警告用）
    DEFAULT_BLINK_COLOR = 7  # 白色（点滅表示用）

    # フォントサイズ
    SMALL_FONT_WIDTH = 4
    SMALL_FONT_HEIGHT = 8
    MIDDLE_FONT_WIDTH = 5
    MIDDLE_FONT_HEIGHT = 10
    LARGE_FONT_WIDTH = 6
    LARGE_FONT_HEIGHT = 12
    
    # フォントパス
    FONT_PATH = "../.venv/Lib/site-packages/pyxel/examples/assets"
    MIDDLE_FONT_FILE = f"{FONT_PATH}/umplus_j10r.bdf"
    LARGE_FONT_FILE = f"{FONT_PATH}/umplus_j12r.bdf"
    
    # レイアウト
    FONT_SPACING_X = 1
    FONT_SPACING_Y = 5
    MARGIN_X = 20
    MARGIN_Y = 10

    # ウィンドウサイズ（フォント幅 * スクランブル最大59文字 + フォントスペース * 58 + 左右マージン20×2）
    WINDOW_WIDTH = MIDDLE_FONT_WIDTH * 59 + FONT_SPACING_X * 58 + MARGIN_X * 2
    WINDOW_HEIGHT = 240
    
    # 縦方向の位置（上マージンを考慮して調整）
    SCRAMBLE_Y = MARGIN_Y
    SCRAMBLE_TEXT_Y = SCRAMBLE_Y + MIDDLE_FONT_HEIGHT + FONT_SPACING_Y
    TIMER_Y = SCRAMBLE_TEXT_Y + MIDDLE_FONT_HEIGHT + MARGIN_Y * 3
    RESULTS_Y = TIMER_Y + LARGE_FONT_HEIGHT + MARGIN_Y * 3
    
    # フレームレート
    FPS = 30
    
    # 点滅表示
    BLINK_CYCLE = FPS
    BLINK_ON_TIME = (FPS // 3) * 2  # 1サイクル中の表示時間

class GameConfig:
    """ゲームロジックに関する定数"""
    # WCAルールに関する定数
    INSPECTION_TIME = 15.0  # WCAルールの15秒
    BUTTON_HOLD_TIME = 1.0  # スペースキー長押しの必要時間
    COUNTDOWN_BEEP_TIMES = [3, 2, 1, 0]  # ビープ音を鳴らすタイミング（残り秒数）
    INSPECTION_GRACE_PERIOD = 2.0  # インスペクション開始後のホールドチェックスキップ時間（秒）

class TextConstants:
    """表示テキストの定数"""
    SCRAMBLE = "SCRAMBLE"
    HOLD_FORMAT = "HOLD: {:.1f}"
    HOLD_INSTRUCTION = "HOLD [SPACE] TO INSPECTION"
    INSPECTION = "INSPECTION TIME"
    PRESS_SPACE = "PRESS [SPACE] TO STOP"
    RECENT = "RECENT"
    AVERAGE = "AVERAGE OF N"
    AO5_FORMAT = "AO5 : {:.2f}"
    AO12_FORMAT = "AO12: {:.2f}"
    AO_EMPTY = "{}: -"
    SOLVE_FORMAT = "#{:02d}:  {:.2f}"  # 例: #01: 12.34
    QUIT = "PRESS [Q] TO QUIT"


class SoundConfig:
    """サウンド関連の定数"""
    BEEP_CHANNEL = 0
    SOUND_CHANNEL = 1
    
    # サウンドインデックス
    COUNTDOWN_SOUND = 0
    START_SOUND = 1
    FINISH_SOUND = 2
    CHANGE_SOUND = 3
    HOLD_SOUND = 4
    SYNC_SOUND = 5