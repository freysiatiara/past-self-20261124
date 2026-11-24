#!/usr/bin/env python3
"""Two Lines to Your Past Self.

Writes a two-line warning to the writer's past self to entry.txt.
Standard library only.
"""

import os
import sys

ENTRY_TEXT = (
    "Don't tell Ana she's overreacting in the school car park "
    "on the last day of term.\n"
    "Those five words ended a ten-year friendship in a minute, "
    "and listening that afternoon would have kept her beside you "
    "at your dad's funeral.\n"
)


def resolve_output_path():
    """Resolve the output path in priority order.

    1. ENTRY_OUTPUT environment variable.
    2. OUTPUT_DIR or MAKEFUN_OUTPUT_DIR joined with "entry.txt".
    3. /output/entry.txt
    """
    entry_output = os.environ.get("ENTRY_OUTPUT")
    if entry_output:
        return entry_output
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def main():
    text = ENTRY_TEXT

    # Validate: non-empty, 1..280 characters total, exactly two lines.
    if not text:
        print("error: entry text is empty", file=sys.stderr)
        return 1
    if len(text) > 280:
        print(
            "error: entry text is %d characters, over the 280 limit"
            % len(text),
            file=sys.stderr,
        )
        return 1
    lines = text.splitlines()
    if len(lines) != 2:
        print(
            "error: entry must have exactly two lines, found %d"
            % len(lines),
            file=sys.stderr,
        )
        return 1
    if any(not line.strip() for line in lines):
        print("error: entry lines must not be blank", file=sys.stderr)
        return 1

    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
        if not os.access(parent, os.W_OK):
            print(
                "error: output directory %s is not writable" % parent,
                file=sys.stderr,
            )
            return 1

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.chmod(path, 0o644)

    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        print("error: file content differs from entry text", file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
