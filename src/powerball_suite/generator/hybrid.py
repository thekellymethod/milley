"""
Hybrid sampler = 70 % ‘hot’ pool + 30 % ‘cold’ pool (very naive baseline).
"""
import random
from typing import List
from ..features.pairs import most_common_pairs
from .rules import sample_without_repeats, apply_filters

def hot_pool(top_n: int = 20) -> List[int]:
    pairs = most_common_pairs(top_n)
    flat = {n for pair, _ in pairs for n in pair}
    return sorted(flat)

def cold_pool() -> List[int]:
    from ..io.clean import tidy
    seen = {n for r in tidy() for n in r.balls}
    return [n for n in range(1, 70) if n not in seen]

def hybrid_sample() -> List[int]:
    h, c = hot_pool(), cold_pool()
    nums = []
    # Weighted pick
    while len(nums) < 5:
        pool = h if random.random() < 0.7 else c
        pick = random.choice(pool)
        if pick not in nums:
            nums.append(pick)
    nums.sort()
    return nums if apply_filters(nums) else hybrid_sample()
