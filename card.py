#!/usr/bin/env python

from PyQt5.QtGui import (QColor)

from expansion import *

class CardType:
    DEFAULT, COIN, VICTORY, ACTION, REACTION, DURATION, PROJECT, ARTIFACT = range(8)

CardTypeColors = {
    CardType.DEFAULT:QColor(0, 0, 0),
    CardType.COIN:QColor(255, 255, 0),
    CardType.VICTORY:QColor(41,253,47),
    CardType.REACTION:QColor(11,36,251),
    CardType.DURATION:QColor(255,165,0),
    CardType.PROJECT:QColor(234,145,152),
    CardType.ARTIFACT:QColor(216,182,142),
}


class Card:
    def __init__(self, no, name, reading, eng, expansion, cost, potion, debt,
                 cardtypes):
        self.cid = no
        self.japanese_name = name
        self.reading = reading
        self.name = eng
        self.expansion = expansion
        self.cost = cost
        self.potion = potion
        self.debt = debt
        self.cardtypes = cardtypes

def load_card_info(filename, expansions):
    cards = []
    with open(filename) as f:
        for line in f:
            if line[0] == '#':
                # ignore comment line
                continue
            cardtypes = []
            data = line.rstrip().split('\t')
            no = int(data[0])
            name, reading, eng, expansion, cost = data[1:6]
            potion, debt, coin, victory, action, reaction = map(int, data[6:12])
            if len(data) == 13:
                # additional information
                tags = data[12].split(",")
                if "duration" in tags:
                    cardtypes.append(CardType.DURATION)
                if "project" in tags:
                    cardtypes.append(CardType.PROJECT)
                if "artifact" in tags:
                    cardtypes.append(CardType.ARTIFACT)

            # set card type
            if coin == 1: cardtypes.append(CardType.COIN)
            if victory == 1: cardtypes.append(CardType.VICTORY)
            # if action == 1: cardtypes.append(CardType.ACTION)
            if reaction == 1: cardtypes.append(CardType.REACTION)

            card = Card(no, name, reading, eng, expansions[expansion],
                        cost, potion, debt, cardtypes)
            cards.append(card)
    return cards

if __name__ == '__main__':
    expansions = load_expansion_info("data/expansions.txt")
    cards = []
    tmp_cards = load_card_info("data/basic_2nd_cards.txt", expansions)
    cards.extend(tmp_cards)
