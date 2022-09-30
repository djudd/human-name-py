# human-name-py
Python bindings for the Rust crate `human_name`, a library for parsing and comparing human names.

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

Linux, MacOS, and Windows, as of the versions currently supported by GitHub Actions.
x86-64 or Apple Silicon. Python 3.10 or later.

If you have access to another environment which is supported by the Rust compiler,
it should be relatively straightforward to fork the library and add support. You'll need
to build [`human_name`](http://github.com/djudd/human-name), copy the resulting library
from `target/release/` in that repository to `humanname/native/<arch>/` in this one,
and modify `_load_lib` appropriately. If this environment is additionally supported by
GitHub Actions, I'm also happy to accept a PR.

# Alternatives

You might also consider using the pure-Python [nameparser](https://github.com/derek73/python-nameparser).
Parsing performance is just about identical; the advantage we gain from the Rust
implementation we surrender in the overhead of the `ctypes` interface.

`humanname` _does_ offer significantly more sophisticated comparison logic,
which understands how initials relate to names, can in many cases handle
nicknames and transliteration intelligently, etc.
