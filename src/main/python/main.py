import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QCursor, QPainter, QPen, QColor
from PIL import ImageGrab
from fbs_runtime.application_context.PyQt5 import ApplicationContext


class instructionWindow(QWidget):
    def __init__(self, format, location):
        super().__init__()

        self.main_window = self
        self.default_format = format
        self.default_location = location

        file_format = 'Snips will be saved in .{} format'.format(format)
        file_format = QLabel(file_format)
        file_location = 'Snips will be saved in {}'.format(location)
        file_location = QLabel(file_location)
        instructions = QLabel('Instructions:')
        tips1 = QLabel('Drag and drop to select an area')
        tips2 = QLabel('Press y to save and n to refresh the screen')
        tips3 = QLabel('Press esc to quit')
        btn = QPushButton('Got it!')
        btn.clicked.connect(self.on_click)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(file_format, 1, 0)
        grid.addWidget(file_location, 2, 0)
        grid.addWidget(instructions, 3, 0)
        grid.addWidget(tips1, 4, 0)
        grid.addWidget(tips2, 5, 0)
        grid.addWidget(tips3, 6, 0)
        grid.addWidget(btn, 7, 0)

        self.setLayout(grid)
        self.resize(350, 150)
        self.setWindowTitle('SnipSnapSnipSnap')
        self.setWindowIcon(QIcon('icon.png'))
        self.centre()

    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click(self):
        self.main_window = Window2(self.default_format, self.default_location)
        self.main_window.showMaximized()
        self.hide()


class Window2(QWidget):
    def __init__(self, format, location):
        super().__init__()
        self.setWindowTitle('SnipSnapSnipSnap')
        self.setWindowIcon(QIcon('icon.png'))
        self.defaultFormat = format
        self.defaultStorage = location
        print(self.defaultFormat)
        print(self.defaultStorage)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.has_snapped = False
        self.setWindowOpacity(0.2)
        self.num_snip = 1
        self.is_snipping = False
        self.img = None
        self.saved = QLabel('Saved')
        self.unsaved = QLabel('Not Saved')

        QApplication.setOverrideCursor(
            QCursor(QtCore.Qt.CrossCursor)
        )

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def paintEvent(self, event):
        if self.is_snipping:
            lw = 0
            opacity = 0
        else:
            lw = 2.5
            opacity = 0.2
        self.setWindowOpacity(opacity)
        qp = QPainter(self)
        qp.setPen(QPen(QColor('black'), lw))
        qp.setBrush(QColor("transparent"))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            self.close()
        if self.has_snapped:
            if event.key() == QtCore.Qt.Key_Y:
                if self.img:
                    img_name = 'snip{}.' + self.defaultFormat
                    img_name = img_name.format(self.num_snip)
                    self.img.save(self.defaultStorage + img_name)
                    self.img = None
                    print('Image Saved')
                    self.setStyleSheet("background-color: #98FB98;")
                    self.num_snip += 1
                self.begin = QtCore.QPoint()
                self.end = QtCore.QPoint()
                self.update()

            elif event.key() == QtCore.Qt.Key_N:
                print('Image Not Saved')
                self.setStyleSheet("background-color: #F08080;")
                self.begin = QtCore.QPoint()
                self.end = QtCore.QPoint()
                self.update()

        event.accept()

    def mousePressEvent(self, event):
        self.setStyleSheet("")
        self.begin = event.pos()
        self.saved.hide()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.is_snipping = True
        self.repaint()
        QApplication.processEvents()
        self.img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.has_snapped = True
        self.is_snipping = False
        self.repaint()
        QApplication.processEvents()


class Window1(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = self
        self.defaultFormat = 'png'
        self.defaultStorage = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

        picFormat = QLabel('File Format')
        location = QLabel('Storage Location')

        hint1 = QLabel('Leave blank for default settings')
        hint2 = QLabel('Default: .png and stored on desktop')

        okButton = QPushButton('OK')
        okButton.clicked.connect(self.on_click)

        self.formatEdit = QLineEdit()
        self.formatEdit.setPlaceholderText("E.g. png or jpg")

        self.locationEdit = QLineEdit()
        self.locationEdit.setPlaceholderText("E.g. C:/Users/Username/Desktop/")

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(picFormat, 1, 0)
        grid.addWidget(self.formatEdit, 1, 1)

        grid.addWidget(location, 2, 0)
        grid.addWidget(self.locationEdit, 2, 1)
        grid.addWidget(hint1, 3, 0, 1, 2)
        grid.addWidget(hint2, 4, 0, 1, 2)
        grid.addWidget(okButton, 5, 1)

        self.setLayout(grid)
        self.resize(350, 150)
        self.setWindowTitle('SnipSnapSnipSnap')
        # self.setWindowIcon(QIcon('icon.png'))
        self.centre()
        self.show()

    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click(self):
        if self.formatEdit.text() != '':
            if self.formatEdit.text().lower() == 'jpg':
                self.defaultFormat = 'jpg'

        if self.locationEdit.text() != '':
            if os.path.exists(self.locationEdit.text()):
                self.defaultStorage = self.locationEdit.text()

        if self.defaultStorage[-1] != '/':
            self.defaultStorage = self.defaultStorage + '\\'

        self.main_window = instructionWindow(self.defaultFormat, self.defaultStorage)
        print(self.defaultStorage)
        self.main_window.show()
        self.hide()


if __name__ == '__main__':
    appctxt = ApplicationContext()
    w = Window1()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
