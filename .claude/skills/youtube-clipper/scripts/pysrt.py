"""A minimal subset of the ``pysrt`` API used by the lesson scripts.

This fallback keeps the lesson runnable in offline sandboxes where the
third-party ``pysrt`` package cannot be installed.
"""

from __future__ import annotations

from dataclasses import dataclass
import builtins
import re
from typing import Iterable


@dataclass
class SubRipTime:
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0

    def __post_init__(self) -> None:
        total = (
            ((self.hours * 60 + self.minutes) * 60 + self.seconds) * 1000
            + self.milliseconds
        )
        self.hours = total // 3_600_000
        total %= 3_600_000
        self.minutes = total // 60_000
        total %= 60_000
        self.seconds = total // 1_000
        self.milliseconds = total % 1_000

    @property
    def ordinal(self) -> int:
        return (
            ((self.hours * 60 + self.minutes) * 60 + self.seconds) * 1000
            + self.milliseconds
        )

    def __str__(self) -> str:
        return (
            f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},"
            f"{self.milliseconds:03d}"
        )

    @classmethod
    def from_string(cls, value: str) -> "SubRipTime":
        match = re.fullmatch(r"(\d+):(\d{2}):(\d{2}),(\d{3})", value.strip())
        if not match:
            raise ValueError(f"Invalid SRT time: {value}")
        return cls(
            hours=int(match.group(1)),
            minutes=int(match.group(2)),
            seconds=int(match.group(3)),
            milliseconds=int(match.group(4)),
        )


@dataclass
class SubRipItem:
    index: int
    start: SubRipTime
    end: SubRipTime
    text: str

    def __post_init__(self) -> None:
        if isinstance(self.start, str):
            self.start = SubRipTime.from_string(self.start)
        if isinstance(self.end, str):
            self.end = SubRipTime.from_string(self.end)


class SubRipFile(list):
    def save(self, path: str, encoding: str = "utf-8") -> None:
        with builtins.open(path, "w", encoding=encoding) as fh:
            for item in self:
                fh.write(f"{item.index}\n")
                fh.write(f"{item.start} --> {item.end}\n")
                fh.write(f"{item.text}\n\n")


def _parse_blocks(content: str) -> Iterable[SubRipItem]:
    for raw_block in re.split(r"\n\s*\n", content.strip()):
        lines = [line.rstrip("\r") for line in raw_block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0].strip())
            start_raw, end_raw = [part.strip() for part in lines[1].split("-->", 1)]
        except (ValueError, IndexError):
            continue
        yield SubRipItem(
            index=index,
            start=SubRipTime.from_string(start_raw),
            end=SubRipTime.from_string(end_raw),
            text="\n".join(lines[2:]),
        )


def open(path: str, encoding: str = "utf-8") -> SubRipFile:
    with builtins.open(path, "r", encoding=encoding) as fh:
        content = fh.read()
    subs = SubRipFile()
    subs.extend(_parse_blocks(content))
    return subs
