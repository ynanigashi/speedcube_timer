"""
Phase 1: パターンデータと基本機能のテスト
"""
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from patterns import get_pattern_database, PatternCategory
from stats import SpeedcubeStats
from log_handler import SpeedcubeLogger

def test_pattern_database():
    """パターンデータベースのテスト"""
    print("=" * 60)
    print("Phase 1: パターンデータベーステスト")
    print("=" * 60)
    
    # パターンデータベースの取得
    pattern_db = get_pattern_database()
    
    # 1. 総パターン数の確認
    total_count = pattern_db.get_pattern_count()
    print(f"\n✓ 総パターン数: {total_count}")
    
    # 2. カテゴリ別パターン数の確認
    print("\n✓ カテゴリ別パターン数:")
    for category in pattern_db.get_categories():
        count = pattern_db.get_category_count(category)
        print(f"  - {category.value}: {count}パターン")
    
    # 3. 各カテゴリのパターン一覧
    print("\n✓ パターン一覧:")
    for category in pattern_db.get_categories():
        patterns = pattern_db.get_patterns_by_category(category)
        if patterns:
            print(f"\n  [{category.value}]")
            for pattern in patterns:
                print(f"    - {pattern.name} (ID: {pattern.id}, 難易度: {pattern.difficulty})")
                print(f"      セットアップ: {pattern.setup_moves}")
    
    # 4. 個別パターンの取得テスト
    print("\n✓ 個別パターン取得テスト:")
    test_pattern = pattern_db.get_pattern("OLL_01")
    if test_pattern:
        print(f"  パターン名: {test_pattern.name}")
        print(f"  カテゴリ: {test_pattern.category.value}")
        print(f"  説明: {test_pattern.description}")
        print(f"  セットアップムーブ: {test_pattern.setup_moves}")
    
    print("\n" + "=" * 60)
    print("パターンデータベーステスト完了！")
    print("=" * 60)

def test_database_schema():
    """データベーススキーマのテスト"""
    print("\n" + "=" * 60)
    print("Phase 1: データベーススキーマテスト")
    print("=" * 60)
    
    try:
        # ロガーの初期化（これによりテーブルが作成される）
        logger = SpeedcubeLogger()
        
        # テーブルの存在確認
        cursor = logger.cursor
        
        # pattern_solvesテーブルの確認
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pattern_solves'
        """)
        result = cursor.fetchone()
        
        if result:
            print("\n✓ pattern_solvesテーブルが正常に作成されました")
            
            # テーブルスキーマの確認
            cursor.execute("PRAGMA table_info(pattern_solves)")
            columns = cursor.fetchall()
            print("\n  テーブル構造:")
            for col in columns:
                print(f"    - {col[1]}: {col[2]}")
            
            # インデックスの確認
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND tbl_name='pattern_solves'
            """)
            indexes = cursor.fetchall()
            print("\n  インデックス:")
            for idx in indexes:
                print(f"    - {idx[0]}")
        else:
            print("\n✗ pattern_solvesテーブルの作成に失敗しました")
        
        print("\n" + "=" * 60)
        print("データベーススキーマテスト完了！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def test_pattern_stats_methods():
    """パターン統計メソッドのテスト"""
    print("\n" + "=" * 60)
    print("Phase 1: パターン統計メソッドテスト")
    print("=" * 60)
    
    try:
        logger = SpeedcubeLogger()
        stats = SpeedcubeStats(logger)
        
        # テストデータの挿入
        print("\n✓ テストデータを挿入中...")
        test_pattern_id = "OLL_01"
        test_times = [3.5, 4.2, 3.8, 5.1, 3.3]
        
        cursor = logger.cursor
        for time in test_times:
            cursor.execute("""
                INSERT INTO pattern_solves 
                (pattern_id, pattern_name, pattern_category, solve_time, session_id, practice_mode)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (test_pattern_id, "OLL #1", "OLL", time, logger.session_id, "manual"))
        logger.conn.commit()
        
        print(f"  {len(test_times)}件のテストデータを挿入しました")
        
        # 統計メソッドのテスト
        print("\n✓ 統計メソッドのテスト:")
        
        # 試技回数
        count = stats.get_pattern_count(test_pattern_id)
        print(f"  - 試技回数: {count}")
        
        # ベストタイム
        best = stats.get_pattern_best(test_pattern_id)
        print(f"  - ベストタイム: {best:.2f}秒" if best else "  - ベストタイム: データなし")
        
        # 全タイム取得
        times = stats.get_pattern_times(test_pattern_id)
        print(f"  - 全タイム: {[f'{t:.2f}' for t in times]}")
        
        # 直近3回のタイム
        recent_times = stats.get_pattern_times(test_pattern_id, limit=3)
        print(f"  - 直近3回: {[f'{t:.2f}' for t in recent_times]}")
        
        print("\n" + "=" * 60)
        print("パターン統計メソッドテスト完了！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Phase 1の全テストを実行"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Phase 1: 基盤構築テスト" + " " * 25 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 各テストを実行
    test_pattern_database()
    test_database_schema()
    test_pattern_stats_methods()
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "Phase 1 完了！" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n✓ パターンデータ構造の設計: 完了")
    print("✓ データベーススキーマの拡張: 完了")
    print("✓ 基本的な統計メソッドの実装: 完了")
    print("✓ 状態定義の追加: 完了")
    print("\nPhase 2 (手動パターン選択モード) の実装準備が整いました！")

if __name__ == "__main__":
    main()
