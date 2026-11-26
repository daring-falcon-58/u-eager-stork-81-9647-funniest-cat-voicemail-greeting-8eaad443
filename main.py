#!/usr/bin/env python3
"""Funniest Cat Voicemail Greeting — make.fun entry.

Writes the tournament-winning voicemail greeting to /output/entry.txt.
Winner (112 chars, chosen from 38 candidates by a scored head-to-head
tournament against the judge persona's criteria, in order):
  "Hi, you've reached Miso. I'm sitting on the book you're reading.
   Leave a message - the ending was boring anyway."
"""

import os

WINNING_LINE = (
    "Hi, you've reached Miso. I'm sitting on the book you're reading. "
    "Leave a message - the ending was boring anyway."
)


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(WINNING_LINE)
    # Read-back verification: the gate requires 1-120 UTF-8 chars, not
    # only whitespace, and the file must hold exactly the winning line.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == WINNING_LINE, "entry.txt does not match the winning line"
    assert 1 <= len(written) <= 120, f"entry.txt is {len(written)} chars (gate: 1-120)"
    assert written.strip(), "entry.txt is only whitespace"


if __name__ == "__main__":
    main()
