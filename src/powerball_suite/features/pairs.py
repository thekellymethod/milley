from collections import Counter
from typing import List, Tuple
from ..io.clean import tidy

def most_common_pairs(top_k: int = 20) -> List[Tuple[Tuple[int, int], int]]:
    counter: Counter = Counter()
    for row in tidy():
        combo = sorted(row.balls)
        # All 10 distinct 2-ball combinations
        for i in range(5):
            for j in range(i + 1, 5):
                counter[(combo[i], combo[j])] += 1
    return counter.most_common(top_k)
