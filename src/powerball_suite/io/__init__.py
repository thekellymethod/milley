"""
Lightweight I/O module for the Powerball suite.
Keeps the codebase clean and organized."""
from pathlib import Path

#Default data directory (~powerball_suite/data)

DATA_HOME = Path.home() / "powerball_suite" / "data"
DATA_HOME.mkdir(exist_ok=True)
