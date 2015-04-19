import sys
from PySide import QtGui, QtCore
import bitstring
import threading
import operator


class BitView(QtGui.QWidget):
    COLOR_ON = QtGui.QColor(120, 120, 255, 255)
    COLOR_OFF = QtGui.QColor(255, 255, 255, 255)

    def __init__(self, *args, **kwargs):
        super(BitView, self).__init__(*args, **kwargs)

        self._size = 10
        self._width = 32
        self._bits = None
        self._image_data = None

        self.initUI()

    def initUI(self):
        self.imageLabel = QtGui.QLabel()
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidget(self.imageLabel)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.scrollArea, 0, 0)
        self.setLayout(layout)

    def paintEvent(self, e):
        if self._image_data is None:
            return

        image = QtGui.QImage(self._image_data,
                             self._width,
                             len(self._bits) / (self._width * 4),
                             QtGui.QImage.Format_RGB32).copy()

        transform = QtGui.QTransform()
        transform.scale(self._size, self._size)
        image = image.transformed(transform)

        self.imageLabel.setGeometry(0, 0, image.width(), image.height())

        pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
        self.imageLabel.setPixmap(pixmap)

    def set_data(self, data):
        self._bits = bitstring.Bits(bytes=data)
        self._image_data = bytearray(len(self._bits) * 4)

        for i, bit in enumerate(self._bits):
            color = self.COLOR_ON if bit else self.COLOR_OFF
            i *= 4
            self._image_data[i + 0] = color.blue()
            self._image_data[i + 1] = color.green()
            self._image_data[i + 2] = color.red()
            self._image_data[i + 3] = color.alpha()

        self.update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.update()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.update()



class Test(QtGui.QWidget):
    def __init__(self):
        super(Test, self).__init__()

        data = "".join(map(lambda x: chr(x) * 8, xrange(255))) * 10

        bv = BitView(self)

        bv.set_data(data)
        layout = QtGui.QGridLayout()
        layout.addWidget(bv, 0, 0)
        self.setLayout(layout)
        self.show()


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

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
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(40, 40, 40))
        self.setPalette(palette)

        self.bitViewer = BitView(self)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.bitViewer, 0, 0, 2, 1)
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

        self.bitViewer.set_data(data[:0x10000])
        self.update()

    def changeSize(self, value):
        self.bitViewer.size = value
        self.update()

    def changeValue(self, value):
        self.bitViewer.width = value // 4
        self.lbl.setText(str(value // 4))
        self.lbl.adjustSize()
        self.update()


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