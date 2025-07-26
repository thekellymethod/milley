import argparse
from pathlib import Path
from powerball_suite.io.fetch import fetch_latest_csv
from powerball_suite.io.fetch import clean_df

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Powerball Suite CLI",
        description= "Swiss-army-knife for Powerball data",)
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the Powerball data"
    )
    args = parser.parse_args()
    if args.update:
        path = fetch_latest_csv(Path("data/powerball.csv"))
        if path:
            print(f"Updated Powerball data saved to {path}")
        else:
            print("Failed to update Powerball data.")
    if __name__ == "__main__":
        main()  