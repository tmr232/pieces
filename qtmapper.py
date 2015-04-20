import sys
from PySide import QtGui, QtCore
import bitstring
import threading
import operator
import pieces.bits


def get_bit8(byte, bit):
    return ((byte & 0xFF) >> (7 - bit)) & 1

def map_byte_to_pixels(color_on, color_off):
    print color_on
    pixel_on = str(bytearray([color_on.blue(), color_on.green(), color_on.red(), color_on.alpha()]))
    pixel_off = str(bytearray([color_off.blue(), color_off.green(), color_off.red(), color_off.alpha()]))


    map = [
        "".join(pixel_on if get_bit8(byte, bit) else pixel_off
                for bit in xrange(8))
        for byte in xrange(256)
    ]

    return map


class BitView(QtGui.QWidget):
    COLOR_ON = QtGui.QColor(120, 120, 255, 255)
    COLOR_OFF = QtGui.QColor(255, 255, 255, 255)
    BYTE_TO_PIXELS = map_byte_to_pixels(COLOR_ON, COLOR_OFF)

    def __init__(self, *args, **kwargs):
        super(BitView, self).__init__(*args, **kwargs)

        self._size = 10
        self._width = 32
        self._image_data = None

        self.initUI()

    def byte_to_pixels(self, byte):
        return self.BYTE_TO_PIXELS[byte]

    def initUI(self):
        self.imageLabel = QtGui.QLabel()
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidget(self.imageLabel)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.scrollArea, 0, 0)
        self.setLayout(layout)

    def make_extra_pixels(self, n):
        return bytearray(4 * n)

    def paintEvent(self, e):
        if self._image_data is None:
            return

        width = self._width

        image_data = self._image_data[:]

        if (len(self._image_data) / 4) % width:
            image_data += self.make_extra_pixels(width)

        number_of_pixels = len(image_data) / 4

        height = (number_of_pixels / width)

        image = QtGui.QImage(image_data,
                             width,
                             height,
                             QtGui.QImage.Format_ARGB32).copy()

        transform = QtGui.QTransform()
        transform.scale(self._size, self._size)
        image = image.transformed(transform)
        self.imageLabel.setGeometry(0, 0, image.width(), image.height())

        pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
        self.imageLabel.setPixmap(pixmap)

    def set_data(self, data):
        self._image_data = "".join(self.byte_to_pixels(ord(byte)) for byte in data)

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


class MutatorUI(QtGui.QWidget):
    """
    +---------------------------------+
    |    Title                        |
    | <----#---------------->  Value  |
    +---------------------------------+
    """
    def __init__(self, *args, **kwargs):
        super(MutatorUI, self).__init__(*args, **kwargs)

        self.initUI()

    def initUI(self):
        title = QtGui.QLabel("ROL8", self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        slider.setRange(0, 7)
        slider.setValue(0)
        slider.valueChanged[int].connect(self.sliderEvent)

        value = QtGui.QLineEdit(self)
        value.setText(str(slider.value()))

        self.title = title
        self.value = value
        self.slider = slider

        layout = QtGui.QGridLayout()
        layout.addWidget(self.title, 0, 0)
        layout.addWidget(self.slider, 1, 0)
        layout.addWidget(self.value, 1, 1)
        self.setLayout(layout)


    def sliderEvent(self, value):
        self.value.setText(str(value))


class Test(QtGui.QWidget):
    def __init__(self):
        super(Test, self).__init__()

        data = "".join(map(lambda x: chr(x) * 8, xrange(255))) * 10

        bv = BitView(self)

        bv.set_data(data)
        layout = QtGui.QGridLayout()
        mutator = MutatorUI(self)
        layout.addWidget(bv, 0, 0)
        layout.addWidget(mutator, 0, 1)
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

        rol_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        rol_slider.setRange(-7, 700)
        rol_slider.setValue(0)
        rol_slider.valueChanged[int].connect(self.RolChanged)

        btn = QtGui.QPushButton("Open", self)
        btn.move(700, 0)
        btn.clicked.connect(self.openFile)

        self.image = QtGui.QLabel()

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(40, 40, 40))
        self.setPalette(palette)

        self.bitViewer = BitView(self)
        self._data = ("\0" * 32 + "\xff" + "\0" + "\x01") * (0x1000 / 32)
        self.bitViewer.set_data(self._data)
        # self.bitViewer.set_data("\x55" * (0x1000 ))
        layout = QtGui.QGridLayout()
        layout.addWidget(self.bitViewer, 0, 0, 2, 1)
        layout.addWidget(btn, 0, 1)
        layout.addWidget(sld1, 0, 2)
        layout.addWidget(sld2, 0, 3)
        layout.addWidget(self.lbl, 1, 2)
        layout.addWidget(rol_slider, 2, 0)
        self.setLayout(layout)

        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colors')
        self.show()


    def RolChanged(self, value):
        data = bytearray(self._data)
        for index, byte in enumerate(data):
            data[index] = pieces.bits.ROL8(byte, value)
        self.bitViewer.set_data(str(data))

    def openFile(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", "")
        with open(fname, "rb") as f:
            data = f.read()
        self._data = data[:0x1000]
        self.bitViewer.set_data(self._data)
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