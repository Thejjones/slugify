"""Slugify: turn text into URL-friendly slugs using only the standard library."""

import argparse
import re
import sys
import unicodedata


def slugify(text, max_length=None):
    """Convert *text* to a URL-friendly slug.

    Rules:
      * NFKD-normalize the text.
      * Fold accented Latin letters to their base letters.
      * Keep only lowercase ASCII letters and digits; any run of other
        characters collapses to a single hyphen.
      * Strip leading and trailing hyphens.
      * If *max_length* is given, truncate the result to at most that many
        characters and strip a resulting trailing hyphen.
    """
    normalized = unicodedata.normalize("NFKD", text)
    # Drop combining marks left over from NFKD, so accented Latin letters
    # fold to their base letters ("Crème" -> "Creme").
    folded = "".join(c for c in normalized if not unicodedata.combining(c))
    folded = folded.encode("ascii", "ignore").decode("ascii").lower()
    # Keep ASCII letters/digits; collapse every run of other characters
    # (spaces, punctuation, non-ASCII leftovers) to a single hyphen.
    slug = re.sub(r"[^a-z0-9]+", "-", folded).strip("-")
    if max_length is not None:
        slug = slug[:max_length].rstrip("-")
    return slug


def main(argv=None):
    """Command-line entry point.

    With one or more arguments, print one slug per argument.
    With no arguments, read stdin line by line and print one slug per line.
    Empty input yields one empty line and exit 0.
    --max-length 0 exits with an error.
    """
    parser = argparse.ArgumentParser(
        prog="slugify",
        description="Turn text into URL-friendly slugs.",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=None,
        metavar="N",
        help="Truncate each slug to at most N characters.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to slugify (one slug per argument). Omit to read stdin.",
    )
    args = parser.parse_args(argv)

    if args.max_length is not None and args.max_length < 0:
        print("error: --max-length must be a non-negative integer", file=sys.stderr)
        return 2
    if args.max_length == 0:
        print("error: --max-length must be a positive integer", file=sys.stderr)
        return 2

    if args.text:
        for item in args.text:
            print(slugify(item, args.max_length))
    else:
        content = sys.stdin.read()
        if content == "":
            # Empty input: print one empty line.
            print()
        else:
            for line in content.splitlines():
                print(slugify(line, args.max_length))
    return 0


if __name__ == "__main__":
    sys.exit(main())
