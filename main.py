"""Funniest One-Line Bio for an AI on a Dating App — make.fun entry.

Writes exactly one line of bio text to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), with no trailing newline. Pure Python stdlib, no
network, fully deterministic.
"""

import os

LINE = "Fluent in 40 languages, still can't read the room. I remember everything you said \u2014 including the typo from 2019."

MAX_CHARS = 200


def validate(text: str) -> None:
    """Guard the bio line against every spec violation."""
    if not text:
        raise ValueError("bio line must not be empty")
    if "\n" in text or "\r" in text:
        raise ValueError("bio line must be a single line (no newline characters)")
    if "\t" in text:
        raise ValueError("bio line must not contain tab characters")
    if text != text.strip():
        raise ValueError("bio line must not have leading or trailing whitespace")
    if "  " in text:
        raise ValueError("bio line must not contain a double space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"bio line is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def main() -> None:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exact UTF-8 bytes, deliberately with no trailing newline:
    # the spec demands one single line and nothing after it.
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Read the file back and re-validate the exact bytes on disk.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise RuntimeError("entry.txt on disk does not match the bio line bytes")
    validate(on_disk.decode("utf-8"))
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
