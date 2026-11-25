#!/usr/bin/env python3
"""Pigeon Pitch, One Line -- make.fun entry.

Writes the winning elevator pitch to /output/entry.txt.

Tournament (specificity / surprise / freshness, 1-5 each):
  1. Seed round literally seeds -- 4/4/3 = 11 (seed pun is flooded)
  2. TAM is every breadcrumb in Manhattan since 1974 -- 5/5/4 = 14
  3. Pooped on 40 Teslas, brand loyalty -- 5/5/5 = 15 (WINNER)
  4. Pivot: delivery fleet to statue-cleaning sub -- 5/5/4 = 14
  5. Churn zero, nobody ever evicted a pigeon -- 5/4/4 = 13
  6. First round from a guy feeding me, term sheet -- 5/5/5 = 15
  7. Moat is 4,000 years of being unremovable -- 5/5/4 = 14
Tie at 15 between #3 and #6: #3 wins because pooping on cars is
unmistakably pigeon behaviour, the concrete number (40 Teslas) and the
"brand loyalty you can't buy" twist land in one breath, and it closes
as a real pitch ("I'm raising at a $12M cap").
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "I pooped on 40 Teslas last quarter and not one owner sued. "
    "That's brand loyalty you can't buy. I'm raising at a $12M cap."
)

GATE_MIN = 1
GATE_MAX = 200


TOURNAMENT = [
    ("Seed round literally seeds", 4, 4, 3),
    ("TAM is every breadcrumb in Manhattan since 1974", 5, 5, 4),
    ("Pooped on 40 Teslas, brand loyalty", 5, 5, 5),
    ("Pivot: delivery fleet to statue-cleaning sub", 5, 5, 4),
    ("Churn zero, nobody ever evicted a pigeon", 5, 4, 4),
    ("First round from a guy feeding me, term sheet", 5, 5, 5),
    ("Moat is 4,000 years of being unremovable", 5, 5, 4),
]


def print_tournament() -> None:
    for i, (label, spec, surp, fresh) in enumerate(TOURNAMENT, 1):
        print(f"{i}. {label} -- {spec}/{surp}/{fresh} = {spec + surp + fresh}")


def gate_ok(text: str) -> bool:
    """Gate: UTF-8 text of 1-200 chars, not only whitespace."""
    return GATE_MIN <= len(text) <= GATE_MAX and text.strip() != ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the pigeon pitch.")
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="path to write entry.txt to (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the gate and print the entry, without writing",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp path and verify a byte-identical round trip",
    )
    parser.add_argument(
        "--tournament",
        action="store_true",
        help="print the candidate tournament scores and exit",
    )
    args = parser.parse_args(argv)

    if args.tournament:
        print_tournament()
        return 0

    if not gate_ok(ENTRY):
        print(f"gate FAIL: {len(ENTRY)} chars", file=sys.stderr)
        return 1

    if args.check:
        print(f"gate OK: {len(ENTRY)} chars, {len(ENTRY.encode('utf-8'))} bytes")
        print(ENTRY)
        return 0

    if args.self_test:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "entry.txt"
            probe.write_text(ENTRY, encoding="utf-8")
            back = probe.read_text(encoding="utf-8")
            assert back == ENTRY, "round trip mismatch"
            print(f"self-test OK: {len(ENTRY)} chars, byte-identical")
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {out} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
