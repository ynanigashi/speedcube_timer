"""
Phase 1拡張: 複数アルゴリズム対応のテスト
"""
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from patterns import get_pattern_database, PatternCategory

def test_multiple_algorithms():
    """複数アルゴリズム機能のテスト"""
    print("=" * 60)
    print("複数アルゴリズム機能テスト")
    print("=" * 60)
    
    pattern_db = get_pattern_database()
    
    # 1. PLL Uaの複数アルゴリズムをテスト
    print("\n✓ PLL Uaのアルゴリズム一覧:")
    pll_ua_algs = pattern_db.get_algorithms_for_pattern("PLL_Ua")
    for alg in pll_ua_algs:
        default_mark = " [DEFAULT]" if alg.is_default else ""
        print(f"  - {alg.name}{default_mark}")
        print(f"    ID: {alg.id}")
        print(f"    Moves: {alg.moves}")
        if alg.notes:
            print(f"    Notes: {alg.notes}")
        print()
    
    # 2. デフォルトアルゴリズムの取得
    print("✓ デフォルトアルゴリズムの取得:")
    default_alg = pattern_db.get_default_algorithm("PLL_Ua")
    if default_alg:
        print(f"  PLL Ua のデフォルト: {default_alg.name}")
        print(f"  Moves: {default_alg.moves}")
    
    # 3. 全パターンの複数アルゴリズム対応状況
    print("\n✓ 複数アルゴリズムを持つパターン:")
    for pattern in pattern_db.get_all_patterns():
        if pattern_db.has_multiple_algorithms(pattern.id):
            alg_count = len(pattern_db.get_algorithms_for_pattern(pattern.id))
            print(f"  - {pattern.name}: {alg_count}個のアルゴリズム")
    
    # 4. 各カテゴリのアルゴリズム統計
    print("\n✓ カテゴリ別アルゴリズム統計:")
    all_algorithms = pattern_db.get_all_algorithms()
    print(f"  総アルゴリズム数: {len(all_algorithms)}")
    
    for category in pattern_db.get_categories():
        patterns = pattern_db.get_patterns_by_category(category)
        alg_count = 0
        for pattern in patterns:
            alg_count += len(pattern_db.get_algorithms_for_pattern(pattern.id))
        if alg_count > 0:
            print(f"  {category.value}: {alg_count}個のアルゴリズム")
    
    # 5. PLL Aaのアルゴリズム詳細
    print("\n✓ PLL Aaのアルゴリズム:")
    pll_aa_algs = pattern_db.get_algorithms_for_pattern("PLL_Aa")
    for alg in pll_aa_algs:
        print(f"  [{alg.name}]")
        print(f"    {alg.moves}")
        if alg.notes:
            print(f"    → {alg.notes}")
    
    # 6. OLL #21のアルゴリズム
    print("\n✓ OLL #21のアルゴリズム:")
    oll_21_algs = pattern_db.get_algorithms_for_pattern("OLL_21")
    for alg in oll_21_algs:
        print(f"  [{alg.name}]")
        print(f"    {alg.moves}")
        if alg.notes:
            print(f"    → {alg.notes}")
    
    print("\n" + "=" * 60)
    print("複数アルゴリズム機能テスト完了！")
    print("=" * 60)

def test_algorithm_selection():
    """アルゴリズム選択機能のテスト"""
    print("\n" + "=" * 60)
    print("アルゴリズム選択シミュレーション")
    print("=" * 60)
    
    pattern_db = get_pattern_database()
    
    # シナリオ: ユーザーがPLL Uaを練習する
    pattern_id = "PLL_Ua"
    pattern = pattern_db.get_pattern(pattern_id)
    
    print(f"\n練習パターン: {pattern.name}")
    print(f"説明: {pattern.description}")
    print(f"\n利用可能なアルゴリズム:")
    
    algorithms = pattern_db.get_algorithms_for_pattern(pattern_id)
    for i, alg in enumerate(algorithms, 1):
        default_mark = " ★" if alg.is_default else ""
        print(f"  {i}. {alg.name}{default_mark}")
        print(f"     {alg.moves}")
    
    # デフォルトアルゴリズムの使用
    default_alg = pattern_db.get_default_algorithm(pattern_id)
    print(f"\n→ デフォルトアルゴリズムを使用: {default_alg.name}")
    print(f"  ムーブ: {default_alg.moves}")
    
    print("\n" + "=" * 60)
    print("アルゴリズム選択シミュレーション完了！")
    print("=" * 60)

def main():
    """全テストを実行"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Phase 1拡張: 複数アルゴリズム対応" + " " * 14 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_multiple_algorithms()
    test_algorithm_selection()
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "テスト完了！" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n✓ 複数アルゴリズムのデータ構造: 完了")
    print("✓ アルゴリズム管理メソッド: 完了")
    print("✓ デフォルトアルゴリズム選択: 完了")
    print("✓ アルゴリズム別統計メソッド: 完了")
    print("\nユーザーは好みのアルゴリズムを選択して練習できます！")

if __name__ == "__main__":
    main()
