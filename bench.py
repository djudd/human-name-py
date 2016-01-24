from __future__ import print_function

from timeit import timeit
from humanname import Name

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


url = "https://raw.githubusercontent.com/djudd/human-name/master/tests/benchmark-names.txt"     # noqa
names = urlopen(url).read().splitlines()


def parse_all():
    for string in names:
        n = Name.parse(string)
        if n is not None:
            n.surname

t = timeit(parse_all, number=25)

print("Parsing %d names 25 times (humanname): %fs" % (len(names), t))


try:
    from nameparser import HumanName
except ImportError:
    exit(0)


def parse_all_nameparser():
    for string in names:
        HumanName(string).last

t = timeit(parse_all, number=25)

print("Parsing %d names 25 times (nameparser): %fs" % (len(names), t))
