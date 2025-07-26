import pandas as pd
from typing import Dict
from ..io.clean import tidy

def rolling_counts(window: int = 100) -> Dict[int, pd.Series]:
    """
    Return a dict {ball → rolling count} with window size `window`.
    """
    rows = tidy()
    df = pd.DataFrame([r.balls for r in rows],
                      index=[r.draw_date for r in rows])
    counts = {}
    for col in range(5):
        s = df[col].explode().value_counts()
        counts[col] = s.rolling(window, min_periods=1).sum()
    return counts
