import csv
from pathlib import Path

import pytest

TESTDATA_DIR = Path(__file__).resolve().parent.parent / "testdata"


def load_csv(name):
    rows = []
    with open(TESTDATA_DIR / name, newline="", encoding="utf-8-sig") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            if any(str(value or "").strip() for value in row.values()):
                row["tc_id"] = (row["tc_id"] or "").strip() or f"{Path(name).stem}-row{line}"
                rows.append(row)
    return rows


def load_cases(name):
    return [
        pytest.param(
            row,
            id=row["tc_id"],
            marks=[getattr(pytest.mark, m) for m in (row.get("marker") or "regression").split()],
        )
        for row in load_csv(name)
    ]


def parse_items(text, all_items):
    if text.strip().upper() == "ALL":
        return list(all_items)
    return [name.strip() for name in text.split(";") if name.strip()]
