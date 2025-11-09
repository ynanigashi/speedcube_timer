"""
パターン習得モード用のパターン定義
OLL、PLL、F2L、Crossなどのパターンデータを管理する
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json
import os


class PatternCategory(Enum):
    """パターンカテゴリ"""
    OLL = "OLL"
    PLL = "PLL"
    F2L = "F2L"
    CROSS = "Cross"


@dataclass
class Algorithm:
    """アルゴリズムデータクラス（マスターデータ）"""
    id: str                    # アルゴリズムID（例："PLL_Ua_standard", "PLL_Ua_rud"）
    pattern_id: str            # 関連するパターンID
    name: str                  # アルゴリズム名（例："Standard", "RUD", "Two-gen"）
    moves: str                 # ムーブ記法
    finger_tricks: str = ""    # フィンガートリックの説明（オプション）
    is_default: bool = False   # デフォルトで使用するか
    notes: str = ""            # メモ（オプション）
    
    # 注: ユーザー個別の評価（speed_rating, ergonomics_rating）は
    # user_algorithm_ratingsテーブルで管理し、stats.pyで取得
    
    def __str__(self) -> str:
        return f"{self.name}: {self.moves}"


@dataclass
class Pattern:
    """パターンデータクラス"""
    id: str                    # パターンID（例："OLL_01", "PLL_Aa"）
    name: str                  # パターン名（例："OLL #1", "PLL Aa"）
    category: PatternCategory  # カテゴリ
    setup_moves: str          # セットアップムーブ（パターンを作るためのムーブ）
    description: str          # パターンの説明
    difficulty: int           # 難易度（1-5）
    
    def __str__(self) -> str:
        return f"{self.name} ({self.category.value})"


class PatternDatabase:
    """パターンマスターデータベース"""
    
    def __init__(self):
        """パターンデータの初期化"""
        self._patterns: Dict[str, Pattern] = {}
        self._algorithms: Dict[str, Algorithm] = {}
        self._load_from_json()
    
    @property
    def patterns(self) -> List[Pattern]:
        """全パターンをリストで取得"""
        return list(self._patterns.values())
    
    @property
    def algorithms(self) -> List[Algorithm]:
        """全アルゴリズムをリストで取得"""
        return list(self._algorithms.values())
    
    def _load_from_json(self):
        """JSONファイルからパターンとアルゴリズムをロード"""
        # プロジェクトルートのdataディレクトリからロード
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        patterns_path = os.path.join(project_root, 'data', 'patterns.json')
        algorithms_path = os.path.join(project_root, 'data', 'algorithms.json')
        
        # パターンのロード
        try:
            with open(patterns_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                patterns_data = data.get('patterns', [])
                for pattern_dict in patterns_data:
                    pattern = Pattern(
                        id=pattern_dict['id'],
                        name=pattern_dict['name'],
                        category=PatternCategory[pattern_dict['category']],
                        setup_moves=pattern_dict['setup_moves'],
                        description=pattern_dict['description'],
                        difficulty=pattern_dict['difficulty']
                    )
                    self._patterns[pattern.id] = pattern
        except FileNotFoundError:
            print(f"Warning: {patterns_path} not found. Using fallback patterns.")
            self._initialize_patterns_fallback()
        except json.JSONDecodeError as e:
            print(f"Error decoding {patterns_path}: {e}. Using fallback patterns.")
            self._initialize_patterns_fallback()
        
        # アルゴリズムのロード
        try:
            with open(algorithms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                algorithms_data = data.get('algorithms', [])
                for algo_dict in algorithms_data:
                    algorithm = Algorithm(
                        id=algo_dict['id'],
                        pattern_id=algo_dict['pattern_id'],
                        name=algo_dict['name'],
                        moves=algo_dict['moves'],
                        finger_tricks=algo_dict.get('finger_tricks', ''),
                        is_default=algo_dict.get('is_default', False),
                        notes=algo_dict.get('notes', '')
                    )
                    self._algorithms[algorithm.id] = algorithm
        except FileNotFoundError:
            print(f"Warning: {algorithms_path} not found. Using fallback algorithms.")
            self._initialize_algorithms_fallback()
        except json.JSONDecodeError as e:
            print(f"Error decoding {algorithms_path}: {e}. Using fallback algorithms.")
            self._initialize_algorithms_fallback()
    
    def _initialize_patterns_fallback(self):
        """パターンマスターデータの初期化（フォールバック用）"""
        # OLLパターン（検証用に5つ）
        oll_patterns = [
            Pattern(
                id="OLL_01",
                name="OLL #1",
                category=PatternCategory.OLL,
                setup_moves="R U2 R2 F R F' U2 R' F R F'",
                description="Cross on top, all corners oriented",
                difficulty=2
            ),
            Pattern(
                id="OLL_02",
                name="OLL #2",
                category=PatternCategory.OLL,
                setup_moves="F R U R' U' F' f R U R' U' f'",
                description="T-shape",
                difficulty=3
            ),
            Pattern(
                id="OLL_03",
                name="OLL #3",
                category=PatternCategory.OLL,
                setup_moves="f R U R' U' f' U' F R U R' U' F'",
                description="Small L-shape",
                difficulty=3
            ),
            Pattern(
                id="OLL_04",
                name="OLL #4",
                category=PatternCategory.OLL,
                setup_moves="f R U R' U' f' U F R U R' U' F'",
                description="Small L-shape (mirror)",
                difficulty=3
            ),
            Pattern(
                id="OLL_21",
                name="OLL #21",
                category=PatternCategory.OLL,
                setup_moves="R U2 R' U' R U R' U' R U' R'",
                description="Anti-Sune",
                difficulty=1
            ),
        ]
        
        # PLLパターン（検証用に3つ）
        pll_patterns = [
            Pattern(
                id="PLL_Aa",
                name="PLL Aa",
                category=PatternCategory.PLL,
                setup_moves="x R' U R' D2 R U' R' D2 R2 x'",
                description="Adjacent corners swap (clockwise)",
                difficulty=2
            ),
            Pattern(
                id="PLL_Ua",
                name="PLL Ua",
                category=PatternCategory.PLL,
                setup_moves="R U' R U R U R U' R' U' R2",
                description="3 edges clockwise",
                difficulty=1
            ),
            Pattern(
                id="PLL_H",
                name="PLL H",
                category=PatternCategory.PLL,
                setup_moves="M2 U M2 U2 M2 U M2",
                description="Opposite edges swap (2 pairs)",
                difficulty=2
            ),
        ]
        
        # F2Lパターン（検証用に2つ）
        f2l_patterns = [
            Pattern(
                id="F2L_01",
                name="F2L #1",
                category=PatternCategory.F2L,
                setup_moves="U R U' R'",
                description="Easy insert - corner and edge paired",
                difficulty=1
            ),
            Pattern(
                id="F2L_02",
                name="F2L #2",
                category=PatternCategory.F2L,
                setup_moves="R U R' U' R U R'",
                description="Corner on top, edge in slot",
                difficulty=2
            ),
        ]
        
        # 全パターンを辞書に登録
        all_patterns = oll_patterns + pll_patterns + f2l_patterns
        for pattern in all_patterns:
            self._patterns[pattern.id] = pattern
    
    def _initialize_algorithms_fallback(self):
        """アルゴリズムマスターデータの初期化（フォールバック用）"""
        # PLL Uaの複数アルゴリズム例
        pll_ua_algorithms = [
            Algorithm(
                id="PLL_Ua_standard",
                pattern_id="PLL_Ua",
                name="Standard",
                moves="R U' R U R U R U' R' U' R2",
                is_default=True,
                notes="最も一般的なアルゴリズム"
            ),
            Algorithm(
                id="PLL_Ua_alternative",
                pattern_id="PLL_Ua",
                name="Alternative",
                moves="M2 U M U2 M' U M2",
                notes="M回転を使用するバージョン"
            ),
            Algorithm(
                id="PLL_Ua_rud",
                pattern_id="PLL_Ua",
                name="RUD",
                moves="R U R' U R' U' R2 U' R' U R' U R",
                notes="R, U, Dのみを使用"
            ),
        ]
        
        # PLL Aaの複数アルゴリズム例
        pll_aa_algorithms = [
            Algorithm(
                id="PLL_Aa_standard",
                pattern_id="PLL_Aa",
                name="Standard",
                moves="x R' U R' D2 R U' R' D2 R2 x'",
                is_default=True,
                notes="標準的なアルゴリズム"
            ),
            Algorithm(
                id="PLL_Aa_alternative",
                pattern_id="PLL_Aa",
                name="Alternative",
                moves="l' U R' D2 R U' R' D2 R2",
                notes="x回転を避けるバージョン"
            ),
        ]
        
        # PLL Hの複数アルゴリズム例
        pll_h_algorithms = [
            Algorithm(
                id="PLL_H_standard",
                pattern_id="PLL_H",
                name="Standard",
                moves="M2 U M2 U2 M2 U M2",
                is_default=True,
                notes="最も一般的"
            ),
            Algorithm(
                id="PLL_H_alternative",
                pattern_id="PLL_H",
                name="Alternative",
                moves="R2 U2 R U2 R2 U2 R2 U2 R U2 R2",
                notes="M回転を使わないバージョン"
            ),
        ]
        
        # OLL #21の複数アルゴリズム例
        oll_21_algorithms = [
            Algorithm(
                id="OLL_21_standard",
                pattern_id="OLL_21",
                name="Standard",
                moves="R U2 R' U' R U R' U' R U' R'",
                is_default=True,
                notes="Anti-Sune（最も一般的）"
            ),
            Algorithm(
                id="OLL_21_alternative",
                pattern_id="OLL_21",
                name="Alternative",
                moves="y' R' U2 R U R' U' R U R' U R",
                notes="向きを変えて実行"
            ),
        ]
        
        # 全アルゴリズムを辞書に登録
        all_algorithms = (pll_ua_algorithms + pll_aa_algorithms + 
                         pll_h_algorithms + oll_21_algorithms)
        for algorithm in all_algorithms:
            self._algorithms[algorithm.id] = algorithm
    
    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """パターンIDからパターンを取得"""
        return self._patterns.get(pattern_id)
    
    def get_all_patterns(self) -> List[Pattern]:
        """全パターンを取得"""
        return list(self._patterns.values())
    
    def get_patterns_by_category(self, category: PatternCategory) -> List[Pattern]:
        """カテゴリ別にパターンを取得"""
        return [p for p in self._patterns.values() if p.category == category]
    
    def get_pattern_ids_by_category(self, category: PatternCategory) -> List[str]:
        """カテゴリ別にパターンIDを取得"""
        return [p.id for p in self._patterns.values() if p.category == category]
    
    def get_categories(self) -> List[PatternCategory]:
        """利用可能なカテゴリ一覧を取得"""
        return list(PatternCategory)
    
    def get_available_categories(self) -> List[PatternCategory]:
        """実際にデータが存在するカテゴリ一覧を取得"""
        categories = set()
        for pattern in self._patterns.values():
            categories.add(pattern.category)
        # カテゴリの定義順にソート（OLL, PLL, F2L, CROSS）
        all_categories = list(PatternCategory)
        return [cat for cat in all_categories if cat in categories]
    
    def get_pattern_count(self) -> int:
        """総パターン数を取得"""
        return len(self._patterns)
    
    def get_category_count(self, category: PatternCategory) -> int:
        """カテゴリ別パターン数を取得"""
        return len(self.get_patterns_by_category(category))
    
    # ========================================
    # アルゴリズム管理メソッド
    # ========================================
    
    def get_algorithm(self, algorithm_id: str) -> Optional[Algorithm]:
        """アルゴリズムIDからアルゴリズムを取得"""
        return self._algorithms.get(algorithm_id)
    
    def get_algorithms_for_pattern(self, pattern_id: str) -> List[Algorithm]:
        """特定パターンの全アルゴリズムを取得"""
        return [alg for alg in self._algorithms.values() if alg.pattern_id == pattern_id]
    
    def get_default_algorithm(self, pattern_id: str) -> Optional[Algorithm]:
        """特定パターンのデフォルトアルゴリズムを取得"""
        algorithms = self.get_algorithms_for_pattern(pattern_id)
        for alg in algorithms:
            if alg.is_default:
                return alg
        # デフォルトが設定されていない場合は最初のアルゴリズムを返す
        return algorithms[0] if algorithms else None
    
    def get_all_algorithms(self) -> List[Algorithm]:
        """全アルゴリズムを取得"""
        return list(self._algorithms.values())
    
    def has_multiple_algorithms(self, pattern_id: str) -> bool:
        """パターンが複数のアルゴリズムを持つかチェック"""
        return len(self.get_algorithms_for_pattern(pattern_id)) > 1
    
    # ========================================
    # ランダム選択メソッド（Phase 3）
    # ========================================
    
    def get_random_pattern(self, category: str = "ALL", exclude_ids: List[str] = None) -> Optional[Pattern]:
        """
        カテゴリ別にランダムなパターンを取得
        
        Args:
            category: "OLL", "PLL", "ALL" のいずれか
            exclude_ids: 除外するパターンIDのリスト（重複回避用）
        
        Returns:
            ランダムに選択されたパターン、選択できない場合はNone
        """
        import random
        
        exclude_ids = exclude_ids or []
        
        # カテゴリに応じてパターンを取得
        if category == "ALL":
            candidates = self.get_all_patterns()
        elif category == "OLL":
            candidates = self.get_patterns_by_category(PatternCategory.OLL)
        elif category == "PLL":
            candidates = self.get_patterns_by_category(PatternCategory.PLL)
        else:
            return None
        
        # 除外IDを適用
        available_patterns = [p for p in candidates if p.id not in exclude_ids]
        
        if not available_patterns:
            # 除外後に候補がない場合は除外なしで再試行
            available_patterns = candidates
        
        if not available_patterns:
            return None
        
        return random.choice(available_patterns)


# グローバルインスタンス
_pattern_db_instance: Optional[PatternDatabase] = None


def get_pattern_database() -> PatternDatabase:
    """パターンデータベースのシングルトンインスタンスを取得"""
    global _pattern_db_instance
    if _pattern_db_instance is None:
        _pattern_db_instance = PatternDatabase()
    return _pattern_db_instance
