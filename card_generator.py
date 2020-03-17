#!/usr/bin/env python

import random

from PyQt5.QtPrintSupport import (QPrinter)
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QPen, QBrush, QColor, QPainter, QIntValidator, QImage)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

from expansion import *
from card import *


class CardGenerator(QGraphicsItem):
    def __init__(self, width=420, height=594, size=42):
        super(CardGenerator, self).__init__()
        self.width = width
        self.height = height
        self.size = size
        self.xsize = 2*size
        self.ysize = size
        self.NH = self.height//self.ysize
        self.NW = int(self.width//self.xsize)
        self.board = []
        for y in range(self.NH):
            self.board.append([0] * self.NW)
        self.load()
        self.reset()

    def load(self):
        self.expansions = load_expansion_info("data/expansions.txt")
        self.DefalutCard = Card(0, "", "", "default", self.expansions["default"], 0, 0, 0, [])
        self.cards = []
        basic2_cards = load_card_info("data/basic_2nd_cards.txt", self.expansions)
        intrigue2_cards = load_card_info("data/intrigue_2nd_cards.txt", self.expansions)
        renaissance_cards = load_card_info("data/renaissance_cards.txt", self.expansions)
        self.cards.extend(renaissance_cards)
        self.cards.append(self.DefalutCard)
        self.cards.extend(renaissance_cards)
        # self.cards.extend(basic2_cards)
        # self.cards.extend(intrigue2_cards)
        # self.cards.append(self.DefalutCard)
        # self.cards.extend(basic2_cards)
        # self.cards.extend(intrigue2_cards)

    def reset(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = self.DefalutCard
        for i, card in enumerate(self.cards):
            x, y = i%self.NW, i//self.NW
            self.board[y][x] = card
        self.update()

    def randomInit(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = self.DefalutCard
        for x in range(self.NW):
            random_number = random.randint(0, 20)
            if random_number < len(self.cards):
                self.board[0][x] = self.cards[random_number]
        self.update()

    def paint(self, painter, option, widget):
        # draw card
        for y in range(self.NH):
            for x in range(self.NW):
                card = self.board[y][x]
                self.drawCard(painter, card, x, y)

        # draw grid line
        pen = QPen(Qt.white, 0.5, Qt.SolidLine)
        painter.setPen(pen)
        for y in range(self.NH+1):
            painter.drawLine(0, y*self.ysize, self.NW*self.xsize, y*self.ysize)
        for x in range(self.NW+1):
            painter.drawLine(x*self.xsize, 0, x*self.xsize, self.NH*self.ysize)


    def drawCard(self, painter, card, x, y):
        if card.expansion.name == "default":
            return

        # draw outer frame
        painter.setBrush(Qt.black)
        painter.drawRect(self.xsize*x, self.ysize*y, self.xsize, self.ysize)
        # draw inner frame
        self.contour_thickness = 0.08*self.size
        contour_thickness = self.contour_thickness
        painter.setBrush(Qt.white)
        painter.drawRect(self.xsize*x+contour_thickness, self.ysize*y+contour_thickness,
                         self.xsize-2*contour_thickness, self.ysize-2*contour_thickness)

        ## draw card informations
        self.drawExpansion(painter, card, x, y)
        self.drawCenterLine(painter, x, y)
        self.drawCardName(painter, card, x, y)
        self.drawCoin(painter, card, x, y)
        self.drawCardType(painter, card, x, y)


    def drawExpansion(self, painter, card, x, y):
        font = painter.font()
        font.setPointSize(5)
        painter.setFont(font)
        # expansion information
        pen = QPen(Qt.black, 0, Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(card.expansion.color)
        painter.drawRect(self.xsize*x+self.contour_thickness, self.ysize*y+self.contour_thickness,
                         0.08*self.xsize, self.ysize-2*self.contour_thickness)
        painter.save()
        painter.translate(self.xsize*(x)+self.contour_thickness, self.ysize*(y+0.9))
        painter.rotate(270)
        rect = QRectF(0, 0,
                      self.ysize * 0.5, self.contour_thickness*2)
        painter.drawText(rect, Qt.AlignLeft, card.expansion.japanese_name)
        painter.restore()

    def drawCenterLine(self, painter, x, y):
        # draw center line
        pen_thickness = 1
        pen = QPen(Qt.black, pen_thickness, Qt.SolidLine)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.drawLine(self.xsize*x+pen_thickness, self.ysize*(y+0.5), self.xsize*(x+1), self.ysize*(y+0.5))
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)

    def drawCardName(self, painter, card, x, y):
        # card name
        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)
        rect = QRectF(self.xsize*(x+0.22)+self.contour_thickness, self.ysize*(y+0.57),
                      self.xsize, self.ysize * 0.25)
        painter.drawText(rect, Qt.AlignLeft, card.name)
        # painter.drawText(self.xsize*(x+0.2)+2*self.contour_thickness, self.ysize*(y+0.7), card.name)

        painter.save()
        painter.translate(self.xsize*(x+0.9)-2*self.contour_thickness, self.ysize*(y+0.3))
        painter.rotate(180)
        painter.drawText(0, 0,
                         # self.xsize*(x+1), self.ysize*(y+1),
                         card.name)
        painter.restore()

        painter.setFont(font)

    def drawCoin(self, painter, card, x, y):
        r = self.ysize * 0.25
        # coin
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        pen = QPen(Qt.black, 0, Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QColor(222, 150, 65))
        rect = QRectF(self.xsize*(x+0.08)+self.contour_thickness, self.ysize*(y+0.57),
                      r, r)
        painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, str(card.cost))
        painter.save()
        painter.translate(self.xsize*(x+1)-self.contour_thickness, self.ysize*(y+0.43))
        painter.rotate(180)
        rect = QRectF(0, 0, r, r)
        painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, str(card.cost))
        painter.restore()

    def drawCardType(self, painter, card, x, y):
        # TODO: len > 1の時複数色draw
        if len(card.cardtypes) != 1:
            return
        color =  CardTypeColors[card.cardtypes[0]]
        painter.setBrush(color)
        rect = QRectF(self.xsize*(x+0.8), self.ysize*(y+0.46),
                      self.xsize*0.2-self.contour_thickness, self.ysize*0.08)
        painter.drawRect(rect)


    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 420, 594)
        self.graphicsView.setScene(scene)
        self.cardGenerator = CardGenerator(420, 594)
        scene.addItem(self.cardGenerator)
        self.scene = scene

        self.resetButton = QPushButton("&Reset")
        self.resetButton.clicked.connect(self.reset)
        self.randomInitButton = QPushButton("&Random init")
        self.randomInitButton.clicked.connect(self.randomInit)
        self.saveButton = QPushButton("&Save")
        self.saveButton.clicked.connect(self.saveImage)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addWidget(self.randomInitButton)
        buttonLayout.addWidget(self.saveButton)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(buttonLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Card Generator")
        self.timer = None

    def reset(self):
        self.cardGenerator.reset()

    def randomInit(self):
        self.cardGenerator.randomInit()

    def saveImage(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFileName("tmp.pdf")
        printer.setOutputFormat(QPrinter.PdfFormat)
        scene = self.scene
        scene.clearSelection()

        painter = QPainter(printer)
        scene.render(painter)
        painter.end()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
