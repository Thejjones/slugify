"""Tests for the slugify CLI and function (subprocess-based)."""

import subprocess
import sys
import unittest


def run_slugify(args=None, stdin=None):
    """Run python -m slugify with the given args, return CompletedProcess."""
    cmd = [sys.executable, "-m", "slugify"]
    if args:
        cmd.extend(args)
    return subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
    )


class TestSlugifyCLI(unittest.TestCase):
    def test_hello_world(self):
        result = run_slugify(["Hello, World!"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "hello-world")

    def test_accented_letters(self):
        result = run_slugify(["Crème Brûlée"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "creme-brulee")

    def test_already_slugged(self):
        result = run_slugify(["  --Already--slugged--  "])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "already-slugged")

    def test_max_length_5(self):
        result = run_slugify(["--max-length", "5", "Hello World"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "hello")

    def test_max_length_0_exits_nonzero(self):
        result = run_slugify(["--max-length", "0", "x"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_empty_stdin_yields_empty_line(self):
        result = run_slugify(stdin="")
        self.assertEqual(result.returncode, 0)
        # One empty line
        self.assertEqual(result.stdout, "\n")

    def test_multiple_args(self):
        result = run_slugify(["a", "b"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "a\nb")


class TestSlugifyFunction(unittest.TestCase):
    def setUp(self):
        from slugify import slugify as fn
        self.fn = fn

    def test_basic(self):
        self.assertEqual(self.fn("Hello, World!"), "hello-world")

    def test_accented(self):
        self.assertEqual(self.fn("Crème Brûlée"), "creme-brulee")

    def test_trailing_leading_hyphens_stripped(self):
        self.assertEqual(self.fn("  --Already--slugged--  "), "already-slugged")

    def test_max_length_truncates(self):
        self.assertEqual(self.fn("Hello World", max_length=5), "hello")

    def test_max_length_strips_trailing_hyphen(self):
        # "Hello World" -> "hello-world"; max_length=6 -> "hello-" -> "hello"
        self.assertEqual(self.fn("Hello World", max_length=6), "hello")

    def test_no_max_length(self):
        self.assertEqual(self.fn("foo bar"), "foo-bar")

    def test_digits_kept(self):
        self.assertEqual(self.fn("foo123bar"), "foo123bar")

    def test_empty_string(self):
        self.assertEqual(self.fn(""), "")

    def test_only_special_chars(self):
        self.assertEqual(self.fn("!!!"), "")


if __name__ == "__main__":
    unittest.main()
