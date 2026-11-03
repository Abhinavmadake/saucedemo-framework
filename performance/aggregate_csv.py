import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
stats = json.loads((HERE / "html_report" / "statistics.json").read_text())

with open(HERE / "results" / "aggregate.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Label", "# Samples", "Average", "Median", "90% Line", "95% Line", "99% Line",
                "Min", "Max", "Error %", "Throughput", "Received KB/sec", "Sent KB/sec"])
    for key in sorted(stats, key=lambda k: (k == "Total", k)):
        s = stats[key]
        w.writerow([
            "TOTAL" if key == "Total" else key,
            s["sampleCount"],
            round(s["meanResTime"]),
            round(s["medianResTime"]),
            round(s["pct1ResTime"]),
            round(s["pct2ResTime"]),
            round(s["pct3ResTime"]),
            round(s["minResTime"]),
            round(s["maxResTime"]),
            f'{s["errorPct"]:.2f}%',
            f'{s["throughput"]:.2f}',
            f'{s["receivedKBytesPerSec"]:.2f}',
            f'{s["sentKBytesPerSec"]:.2f}',
        ])
