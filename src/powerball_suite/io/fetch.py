"""
Download the latest Powerball data from the official website.
Run with python -m powerball_suite.io.fetch"""
import io
import pandas as pd
import requests
from .schema import DrawRow, DATA_HOME

SOURCE_URL = (
    "https://www.powerball.com/lottery/powerball-draw-results",
    "https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Results/Powerball_results.html"
)

def fetch_raw() -> pd.DataFrame:
    """
    Fetches the latest Powerball draw data from the official website.
    Returns a DataFrame with the raw data.
    """
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()
    csv_bytes = io.BytesIO(r.content)
    df = pd.read_csv(csv_bytes, header=None)
    return df 

def main() -> None:
    raw = fetch_raw
    out = DATA_HOME / "output.csv"
    raw.to_csv(out, index=False)
    print(f"Saved -> {out}")

    if __name__ == "__main__":
        main()