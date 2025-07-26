import random
from typing import List, Sequence

ALL_BALLS = list(range(1, 70))

def sample_without_repeats(k: int = 5) -> List[int]:
    return sorted(random.sample(ALL_BALLS, k))

def apply_filters(nums: Sequence[int]) -> bool:
    """Return True if `nums` passes *all* filters; extend as needed."""
    # Example: forbid 5-odd or 5-even sets
    odd = sum(n % 2 for n in nums)
    return not (odd == 0 or odd == 5)
