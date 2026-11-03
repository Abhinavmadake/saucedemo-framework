# Performance Findings

Run: 3 Nov 2026, 21:32:52 to 21:35:52 IST, JMeter 5.6.3 in non-GUI mode, client: MacBook (macOS)
Profile: 20 users, 60 s ramp-up, 180 s duration, 0-500 ms think time (Uniform Random Timer)

| NFR | Metric | Threshold | Measured | Result |
|---|---|---|---|---|
| NFR-01 | Login Page P95 | < 3.0 s | 0.044 s | PASS |
| NFR-02 | Products Page P95 | < 4.0 s | 0.044 s | PASS |
| NFR-03 | Overall error rate | < 2 % | 0.60 % (63 of 10,434) | PASS |

Total samples: 10,434, throughput: 58.02 req/s

| Page | Samples | Average | Median | 90% | 95% | 99% | Max | Error % |
|---|---|---|---|---|---|---|---|---|
| Login Page | 5,223 | 38 ms | 35 ms | 42 ms | 44 ms | 84 ms | 10,144 ms | 0.54 % |
| Products Page | 5,211 | 37 ms | 35 ms | 42 ms | 44 ms | 61 ms | 18,057 ms | 0.67 % |

Notes:
- Login in SauceDemo happens in the browser; no login request reaches a server. NFR-01/02 measure page delivery from GitHub Pages.
- Products Page uses /?/inventory.html because /inventory.html returns HTTP 404 on GitHub Pages.
- All 63 errors are connection-level failures, not error responses: 47 "Connection reset", 15 "Broken pipe", 1 "Operation timed out". Every response that arrived had status 200 and contained "Swag Labs". They happened between 63 s and 135 s, after all 20 users were active.
- Only 7 of 10,434 samples took over 1 s: six spent about 10 s opening the connection and then returned 200, and the 18.1 s one is the "Operation timed out" error. They do not affect P95.
- aggregate.csv is written by `python performance/aggregate_csv.py` from JMeter's own dashboard statistics (html_report/statistics.json).

Run it again (from the repo root, delete old results first):

```
jmeter -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report
python performance/aggregate_csv.py
```
