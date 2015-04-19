import sys
from PySide import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colors')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        # self.drawRectangles(qp)
        self.drawImage(qp)
        qp.end()

    def drawImage(self, qp):
        with open(r"C:\Windows\SysWOW64\calc.exe", "rb") as f:
            data = f.read()
        image = QtGui.QImage(data, 256, len(data) / 1024, QtGui.QImage.Format_RGB32)
        transform = QtGui.QTransform()
        transform.rotate(90)
        image = image.transformed(transform)
        pixmap = QtGui.QPixmap.fromImage(image)
        qp.drawPixmap(0, 0, pixmap)

    def mousePressEvent(self, event):
        print event.x(), event.y()
        x = 200 - event.y()
        y = event.x()
        print x, y
        print ((y * 200) + x) * 4


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()