"""Healthcheck for Docker: the process is alive if it has updated the heartbeat file recently."""

import os
import sys
import time
from pathlib import Path

HEARTBEAT = Path(os.environ.get("HEARTBEAT_FILE", "/tmp/heartbeat"))
MAX_AGE = int(os.environ.get("HEALTH_MAX_AGE", "900"))  # longer than the longest card processing


def beat() -> None:
    HEARTBEAT.touch()


def main() -> int:
    try:
        age = time.time() - HEARTBEAT.stat().st_mtime
    except FileNotFoundError:
        print("no heartbeat")
        return 1
    if age > MAX_AGE:
        print(f"heartbeat was {age:.0f} s ago")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())