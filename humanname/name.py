import platform
import os

from ctypes import cdll, c_char_p, c_void_p, c_bool


def _load_lib():
    system = platform.system()
    if system == 'Darwin':
        filename = 'libhuman_name.dylib'
    elif system == 'Linux':
        filename = 'libhuman_name.so'
    elif system == 'Windows':
        filename = 'human_name.dll'
    else:
        raise ImportError("Unsupported system: %s" % system)

    cpu = platform.machine()
    if cpu == 'AMD64':
        cpu = 'x86_64'

    dirname = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(dirname, 'native', cpu, filename)
    if not os.path.exists(fname):
        raise ImportError("Unsupported system: %s-%s" % (system, cpu))

    return cdll.LoadLibrary(fname)

lib = _load_lib()


class _RustString(c_char_p):
    pass


# Unfortunately since "ctypes does not implement original object return" it
# does not appear to be possible to avoid a redundant allocation here (a Rust
# string and then a Python one).
#
# https://docs.python.org/2/library/ctypes.html#ctypes-fundamental-data-types-2
def _rust_to_py_string(rust_string, _func, _args):
    val = rust_string.value
    if val is None:
        return None
    else:
        _free_string(rust_string)
        return val.decode('UTF-8')


def _py_to_rust_string(string):
    if isinstance(string, bytes):
        string.decode('UTF-8')          # Validate encoding
        return string
    else:
        return string.encode('UTF-8')


def _init_name_part(part):
    func = getattr(lib, 'human_name_' + part)
    func.restype = _RustString
    func.argtypes = [c_void_p]
    func.errcheck = _rust_to_py_string
    return func


_free_string = lib.human_name_free_string
_free_string.argtypes = [c_char_p]

_free_name = lib.human_name_free_name
_free_name.argtypes = [c_void_p]

_parse = lib.human_name_parse
_parse.restype = c_void_p
_parse.argtypes = [c_char_p]

_surname = _init_name_part('surname')
_given_name = _init_name_part('given_name')
_initials = _init_name_part('initials')
_first_initial = _init_name_part('first_initial')
_middle_initials = _init_name_part('middle_initials')
_middle_names = _init_name_part('middle_names')
_suffix = _init_name_part('suffix')
_display_first_last = _init_name_part('display_first_last')
_display_full = _init_name_part('display_full')
_display_initial_surname = _init_name_part('display_initial_surname')

_consistent_with = lib.human_name_consistent_with
_consistent_with.restype = c_bool
_consistent_with.argtypes = [c_void_p, c_void_p]

_matches_slug_or_localpart = lib.human_name_matches_slug_or_localpart
_matches_slug_or_localpart.restype = c_bool
_matches_slug_or_localpart.argtypes = [c_void_p, c_char_p]

_goes_by_middle_name = lib.human_name_goes_by_middle_name
_goes_by_middle_name.restype = c_bool
_goes_by_middle_name.argtypes = [c_void_p]

_hash = lib.human_name_hash
_hash.argtypes = [c_void_p]

_byte_len = lib.human_name_byte_len
_byte_len.argtypes = [c_void_p]


class Name(object):

    @staticmethod
    def parse(string):
        string = _py_to_rust_string(string)
        parsed = _parse(string)
        if parsed is None:
            return None
        else:
            return Name(parsed)

    def __init__(self, rust_obj):
        self._rust_obj = rust_obj

    def __del__(self):
        _free_name(self._rust_obj)

    def __eq__(self, other):
        if not isinstance(other, Name):
            return False

        return _consistent_with(self._rust_obj, other._rust_obj)

    def __hash__(self):
        return _hash(self._rust_obj)

    def __repr__(self):
        return "Name(%s)" % self.display_full

    def __str__(self):
        return self.display_full

    @property
    def surname(self):
        return _surname(self._rust_obj)

    @property
    def given_name(self):
        return _given_name(self._rust_obj)

    @property
    def initials(self):
        return _initials(self._rust_obj)

    @property
    def first_initial(self):
        return _first_initial(self._rust_obj)

    @property
    def middle_initials(self):
        return _middle_initials(self._rust_obj)

    @property
    def middle_names(self):
        return _middle_names(self._rust_obj)

    @property
    def suffix(self):
        return _suffix(self._rust_obj)

    @property
    def display_first_last(self):
        return _display_first_last(self._rust_obj)

    @property
    def display_full(self):
        return _display_full(self._rust_obj)

    @property
    def display_initial_surname(self):
        return _display_initial_surname(self._rust_obj)

    @property
    def goes_by_middle_name(self):
        return _goes_by_middle_name(self._rust_obj)

    @property
    def length(self):
        return _byte_len(self._rust_obj)

    def matches_slug_or_localpart(self, string):
        string = _py_to_rust_string(string)
        return _matches_slug_or_localpart(self._rust_obj, string)
