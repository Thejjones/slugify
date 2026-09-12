# slugify

A command-line tool that turns text into URL-friendly slugs. Python 3, standard library only — no third-party packages, accounts, or network access.

## Usage

```
python -m slugify TEXT...
```

Prints one slug per argument, one per line:

```console
$ python -m slugify "Hello, World!"
hello-world

$ python -m slugify "Crème Brûlée"
creme-brulee

$ python -m slugify "  --Already--slugged--  "
already-slugged

$ python -m slugify "a" "b"
a
b
```

### Reading from standard input

With no arguments, slugify reads standard input line by line and prints one slug per line:

```console
$ echo "Hello World" | python -m slugify
hello-world
```

Empty input (nothing at all on stdin) prints a single empty line and exits with status 0.

### `--max-length N`

Truncates each slug to at most `N` characters and strips any resulting trailing hyphen:

```console
$ python -m slugify --max-length 5 "Hello World"
hello
```

`--max-length 0` is rejected: the tool exits with a non-zero status (exit code 2) and prints an error message to standard error (stderr):

```console
$ python -m slugify --max-length 0 "x"
error: --max-length must be a positive integer
```

(A negative value is also rejected with `error: --max-length must be a non-negative integer` and exit code 2.)

## Slug transformation rules

For each input string, in order:

1. **Normalize** with Unicode NFKD.
2. **Fold** accented Latin letters to their base letters by dropping the combining marks left over from NFKD (`Crème` → `Creme`).
3. **ASCII-fold and lowercase**: drop any remaining non-ASCII characters and lowercase the rest, so only ASCII letters and digits survive this stage.
4. **Hyphen-collapse**: replace any run of one or more characters that are not lowercase ASCII letters or digits with a single hyphen.
5. **Trim** leading and trailing hyphens.
6. **Truncate** (only when `--max-length N` is given): cut the result to at most `N` characters, then strip a trailing hyphen if the cut left one.

Result: a slug made of lowercase ASCII letters, digits, and single hyphens, with no leading or trailing hyphens.

## Testing

The test suite is Python `unittest`, run against the project's configured check. The runner discovers every `test*.py` file under `tests/` (currently `tests/test_slugify.py`, 16 tests) using `python:3.12-slim`. The CLI tests invoke the module as a subprocess (`python -m slugify`), so they exercise the shipped command-line interface directly.

From the project root you can run the same discovery the check uses:

```console
$ python -m unittest discover -s tests -p 'test*.py'
```

Expected: 16 tests, all passing. The registered `tests` check passes with a non-zero test count.

## Layout

```
slugify/
  __init__.py      # re-exports slugify()
  __main__.py      # python -m slugify entry point
  slugify.py       # slugify(text, max_length=None) and main()
tests/
  test_slugify.py  # subprocess CLI tests + direct-function tests
```
