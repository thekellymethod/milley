"""
Read raw -> dupes, coerce dtypes, return tidy pd.DataFrame"""
from typing import List
import pandas as pd
from datetime import datetime
from .schema import DrawRow, DATA_HOME

_COLS = ["game", "month", "day", "year", "n1", "n2", "n2", "n4", "n5", "pb", "pp" ]

def load_raw() -> pd.DataFrame:
    src = DATA_HOME / "powerball_raw.csv"
    df = pd.read_csv(src, names=_COLS)
    return df

def tidy() -> List[DrawRow]:
    """
    Convert raw Powerball data to a list of DrawRow objects.
    """
    df = load_raw()
    df["draw_date"] = pd.to_datetime(df[["year", "month", "day"]])
    df[["year", "month", "day"]].astype(str).agg("-".join, axis=1)
    
    df = df[df["game"].str.contains("Powerball", na=False)]

    balls = df[["n1", "n2", "n3", "n4", "n5"]].astype(int).values.tolist()
    rows = [
        DrawRow(draw_date=row.draw_date(), balls=b)
        for row, b in zip(df.itertuples(), balls)
    ]
    return rows