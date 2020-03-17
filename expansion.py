#!/usr/bin/env python

from PyQt5.QtGui import (QColor)

class ExpansionType:
    none, basic, intrigue = range(3)

class Expansion:
    def __init__(self, eng, jpn, c):
        self.name = eng
        self.japanese_name = jpn
        self.color = c

def load_expansion_info(filename):
    expansions = dict()
    with open(filename) as f:
        for line in f:
            if line[0] == '#':
                # ignore comment line
                continue
            data = line.rstrip().split('\t')
            eng, jpn, r, g, b = data[0], data[1], int(data[2]), int(data[3]), int(data[4])
            expansions[eng] = Expansion(eng, jpn, QColor(r, g, b))
            # print(eng, jpn, r, g, b)
    return expansions

if __name__ == '__main__':
    import sys
    load_expansion_info("data/expansions.txt")
