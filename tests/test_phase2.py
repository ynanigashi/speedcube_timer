"""
Phase 2: パターン習得モード（手動選択モード）のテスト
"""
import sys
import os

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.patterns import PatternDatabase
from src.stats import SpeedcubeStats
from src.log_handler import SpeedcubeLogger


def test_pattern_database():
    """パターンデータベースのテスト"""
    print("=" * 50)
    print("Test: パターンデータベース")
    print("=" * 50)
    
    db = PatternDatabase()
    
    # パターン数の確認
    patterns = db.patterns
    print(f"✓ Total patterns: {len(patterns)}")
    assert len(patterns) == 10, "Should have 10 patterns"
    
    # アルゴリズム数の確認
    algorithms = db.algorithms
    print(f"✓ Total algorithms: {len(algorithms)}")
    assert len(algorithms) == 9, "Should have 9 algorithms"
    
    # 複数アルゴリズムを持つパターンの確認
    pll_ua = db.get_pattern("PLL_Ua")
    assert pll_ua is not None, "PLL_Ua should exist"
    ua_algorithms = db.get_algorithms_for_pattern("PLL_Ua")
    print(f"✓ PLL_Ua has {len(ua_algorithms)} algorithms")
    assert len(ua_algorithms) >= 2, "PLL_Ua should have multiple algorithms"
    
    # デフォルトアルゴリズムの確認
    default_algo = db.get_default_algorithm("PLL_Ua")
    assert default_algo is not None, "Should have default algorithm"
    assert default_algo.is_default, "Default algorithm should be marked"
    print(f"✓ Default algorithm for PLL_Ua: {default_algo.name}")
    
    print("\n✅ All pattern database tests passed!\n")


def test_user_preferences():
    """ユーザー設定の保存・読み込みテスト"""
    print("=" * 50)
    print("Test: ユーザー設定管理")
    print("=" * 50)
    
    logger = SpeedcubeLogger()
    stats = SpeedcubeStats(logger)
    
    # アルゴリズム選択の保存
    pattern_id = "PLL_Ua"
    algorithm_id = "PLL_Ua_alternative"
    
    result = stats.set_user_selected_algorithm(pattern_id, algorithm_id)
    assert result, "Should save user preference successfully"
    print(f"✓ Saved preference: {pattern_id} -> {algorithm_id}")
    
    # アルゴリズム選択の読み込み
    saved_algo_id = stats.get_user_selected_algorithm(pattern_id)
    assert saved_algo_id == algorithm_id, "Should retrieve saved preference"
    print(f"✓ Retrieved preference: {saved_algo_id}")
    
    # 評価の保存
    rating = 4
    notes = "とてもやりやすい"
    result = stats.set_algorithm_rating(algorithm_id, rating, notes)
    assert result, "Should save rating successfully"
    print(f"✓ Saved rating: {rating}/5 - {notes}")
    
    # 評価の読み込み
    saved_rating, saved_notes = stats.get_algorithm_rating(algorithm_id)
    assert saved_rating == rating, "Should retrieve saved rating"
    assert saved_notes == notes, "Should retrieve saved notes"
    print(f"✓ Retrieved rating: {saved_rating}/5 - {saved_notes}")
    
    print("\n✅ All user preference tests passed!\n")


def test_pattern_solve_recording():
    """パターン解法記録のテスト"""
    print("=" * 50)
    print("Test: パターン解法記録")
    print("=" * 50)
    
    logger = SpeedcubeLogger()
    stats = SpeedcubeStats(logger)
    db = PatternDatabase()
    
    # テスト用パターンとアルゴリズムを取得
    pattern = db.get_pattern("OLL_21")
    algorithm = db.get_default_algorithm("OLL_21")
    
    # 解法記録を保存
    solve_time = 2.45
    cursor = logger.cursor
    cursor.execute(
        """
        INSERT INTO pattern_solves 
        (pattern_id, pattern_name, pattern_category, solve_time, 
         session_id, practice_mode, algorithm_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            pattern.id,
            pattern.name,
            pattern.category.value,
            solve_time,
            logger.session_id,
            'manual',
            algorithm.id if algorithm else None
        )
    )
    logger.conn.commit()
    print(f"✓ Recorded solve: {pattern.name} - {solve_time}s")
    
    # 記録の取得
    best_time = stats.get_pattern_best(pattern.id)
    assert best_time is not None, "Should have best time"
    print(f"✓ Best time for {pattern.name}: {best_time}s")
    
    count = stats.get_pattern_count(pattern.id)
    assert count >= 1, "Should have at least one solve"
    print(f"✓ Solve count for {pattern.name}: {count}")
    
    # アルゴリズム別統計
    if algorithm:
        algo_best = stats.get_algorithm_best(algorithm.id)
        assert algo_best is not None, "Should have algorithm best time"
        print(f"✓ Best time for {algorithm.name}: {algo_best}s")
        
        algo_count = stats.get_algorithm_count(algorithm.id)
        assert algo_count >= 1, "Should have at least one solve"
        print(f"✓ Solve count for {algorithm.name}: {algo_count}")
    
    print("\n✅ All pattern solve recording tests passed!\n")


def test_database_tables():
    """データベーステーブルの存在確認"""
    print("=" * 50)
    print("Test: データベーステーブル")
    print("=" * 50)
    
    logger = SpeedcubeLogger()
    cursor = logger.cursor
    
    # user_pattern_preferencesテーブルの確認
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='user_pattern_preferences'"
    )
    result = cursor.fetchone()
    assert result is not None, "user_pattern_preferences table should exist"
    print("✓ user_pattern_preferences table exists")
    
    # user_algorithm_ratingsテーブルの確認
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='user_algorithm_ratings'"
    )
    result = cursor.fetchone()
    assert result is not None, "user_algorithm_ratings table should exist"
    print("✓ user_algorithm_ratings table exists")
    
    # pattern_solvesテーブルの確認
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='pattern_solves'"
    )
    result = cursor.fetchone()
    assert result is not None, "pattern_solves table should exist"
    print("✓ pattern_solves table exists")
    
    print("\n✅ All database table tests passed!\n")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Phase 2 実装テスト開始")
    print("=" * 50 + "\n")
    
    try:
        test_database_tables()
        test_pattern_database()
        test_user_preferences()
        test_pattern_solve_recording()
        
        print("=" * 50)
        print("🎉 Phase 2: すべてのテストが成功しました！")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
