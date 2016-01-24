# encoding: UTF-8

from humanname import Name


def test_simple_name():
    n = Name.parse("Jane Doe")
    assert n.given_name == 'Jane'
    assert n.surname == 'Doe'
    assert n.middle_names is None
    assert n.suffix is None
    assert n.display_full == 'Jane Doe'
    assert n.display_first_last == 'Jane Doe'
    assert n.display_initial_surname == 'J. Doe'
    assert n.goes_by_middle_name is False
    assert n.length == 8


def test_complex_name():
    n = Name.parse("JOHN ALLEN Q DE LA MACDONALD JR")
    assert n.given_name == 'John'
    assert n.surname == 'de la MacDonald'
    assert n.suffix == 'Jr.'
    assert n.display_full == 'John Allen Q. de la MacDonald, Jr.'
    assert n.display_first_last == 'John de la MacDonald'
    assert n.display_initial_surname == 'J. de la MacDonald'
    assert n.length == len('John Allen Q. de la MacDonald, Jr.')


def test_failure():
    assert Name.parse('nope') is None


def test_non_utf8():
    string = u"Björn O'Malley-Muñoz".encode("ISO-8859-1").decode("ISO-8859-1")

    n = Name.parse(string)
    assert n.given_name == u"Björn"             # Normalized NFKD
    assert n.surname == u"O'Malley-Muñoz"       # Normalized NFKD


def test_equality_identical():
    assert Name.parse("Jane Doe") == Name.parse("Jane Doe")


def test_equality_consistent():
    assert Name.parse("Jane Doe") == Name.parse("J. Doe")


def test_equality_inconsistent():
    assert Name.parse("Jane Doe") != Name.parse("John Doe")


def test_hash_identical():
    assert hash(Name.parse("Jane Doe")) == hash(Name.parse("Jane Doe"))


def test_hash_consistent():
    assert hash(Name.parse("Jane Doe")) == hash(Name.parse("J. Doe"))


def test_hash_different_surnames():
    assert hash(Name.parse("Jane Doe")) != hash(Name.parse("Jane Dee"))


def test_matches_slug_or_localpart_matching():
    assert Name.parse("Jane Doe").matches_slug_or_localpart('janexdoe')


def test_matches_slug_or_localpart_nonmatching():
    assert not Name.parse("Jane Doe").matches_slug_or_localpart('johnxdoe')


def test_no_memory_leak():
    import gc
    import os

    def rss():
        gc.collect()
        out = os.popen("ps -o rss= -p %d" % os.getpid()).read()
        return int(out.strip())

    before = rss()

    for _ in range(100000):
        n = Name.parse("John Doe")
        n.given_name
        n.surname

    after = rss()

    assert after < 1.1 * before
