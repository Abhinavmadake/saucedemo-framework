import csv
from pathlib import Path

TESTDATA_DIR = Path(__file__).resolve().parent.parent / "testdata"


def load_csv(name):
    with open(TESTDATA_DIR / name, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))
