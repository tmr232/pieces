import sys
from PySide import QtGui, QtCore
import bitstring
import threading
import operator


class BitView(QtGui.QWidget):
    def __init__(self):
        super(BitView, self).__init__()

        self.size = 4
        self.width = 32

        self.initUI()

    def initUI(self):
        self.imageLabel = QtGui.QLabel()
        self.scrollArea = QtGui.QScrollArea(self)


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        filename = r"C:\Windows\SysWOW64\calc.exe"
        # filename = __file__
        with open(filename, "rb") as f:
            data = f.read()
        # bits = bitstring.Bits(bytes=data[:0x10000])
        bits = bitstring.Bits(bytes="".join(map(lambda x:chr(x)*8, xrange(255))))*10
        print len(bits)
        bit_on = QtGui.QColor(120, 120, 255, 255)
        bit_off = QtGui.QColor(240, 240, 240, 255)
        color = lambda bit: bit_on if bit else bit_off
        bit_str = lambda bit: chr(color(bit).blue()) + chr(color(bit).green()) + chr(color(bit).red()) + "\xFF"
        self.data = "".join([bit_str(x) for x in bits])
        # self.data = "\0\xFF\xFF\xFF"*63000
        self.width = 10
        self.size = 1
        self.initUI()

    def initUI(self):

        self.lbl = QtGui.QLabel(self)
        self.lbl.move(600, 0)

        sld1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        sld1.setGeometry(600, 40, 12, 400)
        sld1.setRange(4, 400)
        sld1.valueChanged[int].connect(self.changeValue)

        sld2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
        sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        sld2.setGeometry(650, 40, 12, 400)
        sld2.setRange(1, 10)
        sld2.valueChanged[int].connect(self.changeSize)

        btn = QtGui.QPushButton("Open", self)
        btn.move(700, 0)
        btn.clicked.connect(self.openFile)

        self.image = QtGui.QLabel()

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(40,40,40))
        self.setPalette(palette)

        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(self.image)
        scrollArea.setGeometry(0, 0, 400, 700)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        layout = QtGui.QGridLayout()
        layout.addWidget(scrollArea, 0, 0, 2, 1)
        layout.addWidget(btn, 0, 1)
        layout.addWidget(sld1, 0, 2)
        layout.addWidget(sld2, 0, 3)
        layout.addWidget(self.lbl, 1, 2)
        self.setLayout(layout)

        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colors')
        self.show()

    def openFile(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", "")
        with open(fname, "rb") as f:
            data = f.read()
        bits = bitstring.Bits(bytes=data[:0x10000])

        self.data = "".join([chr(x*255)*3 + '\xff' for x in bits])
        # self.data = "\xFF" * len(self.data)
        print "opened"
        # print "loaded"
        # self.repaint()
        self.update()
        # self.show()

    def changeSize(self, value):
        print "yay"
        self.size = value
        # self.show()
        self.update()

    def changeValue(self, value):
        self.width = value // 4
        self.lbl.setText(str(value // 4))
        self.lbl.adjustSize()
        # self.show()
        self.update()

    def paintEvent(self, e):
        self.drawImage()

    def drawImage(self):
        print "ThreadId", threading.currentThread()
        data = self.data
        print "a"
        print len(data)
        # print data
        image = QtGui.QImage(self.data, self.width, len(data) / (self.width * 4), QtGui.QImage.Format_RGB32)
        image = image.copy()
        print "bla"
        transform = QtGui.QTransform()
        # transform.rotate(90)
        print "size", self.size
        transform.scale(self.size, self.size)
        image = image.transformed(transform)
        print  image.width(), image.height()
        self.image.setGeometry(0, 0, image.width(), image.height())
        pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
        print "pixmap", pixmap.isNull()
        print pixmap
        self.image.clear()
        self.image.setPixmap(pixmap)

    def mousePressEvent(self, event):
        print event.x(), event.y()
        x = 200 - event.y()
        y = event.x()
        print x, y
        print ((y * 200) + x) * 4

def main():
    try:
        app = QtGui.QApplication(sys.argv)
        ex = Example()
        app.exec_()
    except:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()