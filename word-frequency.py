#!/usr/bin/env python3
# https://code.activestate.com/recipes/576699-python-word-frequency-count-using-sets-and-lists/#c4

import re
import sys

from collections import Counter

wordre = re.compile(r'\w+')

def words(f):
    for line in f:
        for word in wordre.findall(line):
            yield word

with open(sys.argv[1]) as f:
    c = Counter(words(f))

[print(w) for w in c.most_common(20)]
