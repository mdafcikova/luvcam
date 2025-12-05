from typing import Dict, Iterable, List, Optional, Sequence, Union

def _checksum(line: str) -> int:
    """Return NORAD checksum (mod‑10) for first 68 chars of *line*."""
    s = 0
    for ch in line[:68]:
        if ch.isdigit():
            s += int(ch)
        elif ch == "-":
            s += 1
    return s % 10

def _clean_tle_line(line: str) -> str:
    """Strip extraneous chars and repair checksum to 69‑char TLE."""
    line = line.rstrip().rstrip(",")  # remove trailing comma if present
    if len(line) < 69:
        line = line.ljust(69)
    return line[:68] + str(_checksum(line))


def _sanitize_tle(tle: Iterable[str]) -> tuple[str, str, str]:
    """Return name, line1, line2 with valid checksums."""
    name, l1, l2 = tle
    return name.strip(), _clean_tle_line(l1), _clean_tle_line(l2)
