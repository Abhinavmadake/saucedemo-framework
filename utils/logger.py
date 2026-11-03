import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "reports" / "logs"

_log = logging.getLogger("saucedemo")
_current_test = "-"


class _TestName(logging.Filter):
    def filter(self, record):
        record.test = _current_test
        if not hasattr(record, "kind"):
            record.kind = "INFO"
        return True


def setup_logging():
    if _log.handlers:
        return
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_DIR / f"run_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(test)s | %(kind)-6s | %(message)s", "%Y-%m-%d %H:%M:%S"))
    handler.addFilter(_TestName())
    _log.addHandler(handler)
    _log.setLevel(logging.INFO)


def set_test(name):
    global _current_test
    _current_test = name


def step(message):
    _log.info(message, extra={"kind": "STEP"})


def status(message):
    _log.info(message, extra={"kind": "STATUS"})
