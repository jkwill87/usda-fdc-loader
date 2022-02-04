import time
from contextlib import contextmanager
from datetime import datetime
from functools import cache
from pathlib import Path

from teletype.io import style_print


def mdy_to_ymd(s: str) -> str:
    return datetime.strptime(s, "%m/%d/%Y").strftime("%Y-%m-%d")


@cache
def count_lines(filepath: Path) -> int:
    with open(filepath, "r") as f:
        return sum(1 for _ in f)


@contextmanager
def measure(title: str):
    start = time.monotonic()
    print(title, end=" ", flush=True)
    try:
        yield
        end = time.monotonic()
        style_print(f"({end-start:.2f} secs)", style="green")
    except KeyboardInterrupt:
        style_print("aborted", style="red")
        exit(1)
    except:
        style_print("failed", style="red")
        raise
