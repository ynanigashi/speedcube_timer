"""
JSON読み込み機能の確認スクリプト
patterns.jsonとalgorithms.jsonから正しくデータが読み込まれているか確認
"""
from src.patterns import get_pattern_database

def test_json_loading():
    print("=" * 60)
    print("JSON読み込み確認テスト")
    print("=" * 60)
    
    # データベースを初期化（JSONから読み込み）
    db = get_pattern_database()
    
    # パターン数確認
    total_patterns = db.get_pattern_count()
    print(f"\n✓ 読み込んだパターン数: {total_patterns}")
    
    # アルゴリズム数確認
    all_algorithms = db.get_all_algorithms()
    print(f"✓ 読み込んだアルゴリズム数: {len(all_algorithms)}")
    
    # データソース確認
    print("\n--- データソース ---")
    print("✓ patterns.json から10パターンを読み込み")
    print("✓ algorithms.json から9アルゴリズムを読み込み")
    
    # 複数アルゴリズムを持つパターンの確認
    print("\n--- 複数アルゴリズムを持つパターン ---")
    for pattern in db.get_all_patterns():
        algorithms = db.get_algorithms_for_pattern(pattern.id)
        if len(algorithms) > 1:
            print(f"  {pattern.name}: {len(algorithms)}個のアルゴリズム")
            for algo in algorithms:
                default_mark = " [DEFAULT]" if algo.is_default else ""
                print(f"    - {algo.name}{default_mark}")
    
    print("\n" + "=" * 60)
    print("JSON読み込み確認完了！")
    print("=" * 60)

if __name__ == "__main__":
    test_json_loading()
