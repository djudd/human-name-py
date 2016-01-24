# human-name-py
Python bindings for the Rust crate `human_name`, a library for parsing and comparing human names.

[![Build Status](https://travis-ci.org/djudd/human-name-py.svg?branch=master)](https://travis-ci.org/djudd/human-name-py)

See the [`human_name` docs](http://djudd.github.io/human-name) for details.

# Examples

```python
  from humanname import Name

  doe_jane = Name.parse("Doe, Jane")
  doe_jane.surname
  => u"Doe"
  doe_jane.given_name
  => u"Jane"
  doe_jane.initials
  => u"J"

  j_doe = Name.parse("J. Doe")
  j_doe.surname
  => u"Doe"
  j_doe.given_name
  => None
  j_doe.initials
  => u"J"

  j_doe == doe_jane
  => True
  j_doe == Name.parse("John Doe")
  => True
  doe_jane == Name.parse("John Doe")
  => False
```

# Supported environments

Without modification, 64-bit Linux or OS X 10.9+. Depends on a `.so` or `.dylib`
dynamic library built on Travis' container infrastructure, which means Ubuntu 12.04
or OS X 10.9.5.

In theory, anywhere where the nightly Rust compiler will run. First, build your
own `libhuman_name.so` (or `libhuman_name.dylib` on OS X):
```bash
curl -s https://static.rust-lang.org/rustup.sh | sh -s -- --channel=nightly
git clone git@github.com:djudd/human-name.git
cd human-name
cargo build --release
```

Then, fork this repo (`djudd/human-name-py`), replace `libhuman_name.so` with
the file from `human-name/target/release`, and run `py.test` or `tox` to ensure
the tests are passing.

# Alternatives

You might also consider using the pure-Python [nameparser](https://github.com/derek73/python-nameparser).
Parsing performance is just about identical; the advantage we gain from the Rust
implementation we surrender in the overhead of the ctypes interface.

`humanname` _does_ offer significantly more sophisticated comparison logic,
which understands how initials relate to names, can in many cases handle
nicknames and transliteration intelligently, etc.
