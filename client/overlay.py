from PyQt6 import QtCore, QtGui, QtWidgets
from PIL.ImageQt import ImageQt
from PIL import Image


class CropDialog(QtWidgets.QDialog):

    def __init__(self, screenshot: Image.Image):
        super().__init__(flags=QtCore.Qt.WindowType.FramelessWindowHint)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.setModal(True)
        self.setWindowState(QtCore.Qt.WindowState.WindowActive)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(QtWidgets.QApplication.primaryScreen().geometry())

        # tło = zamrożony screenshot
        self.bg = QtGui.QPixmap.fromImage(ImageQt(screenshot))
        self.band = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Shape.Rectangle, self)
        self.origin = QtCore.QPoint()

    # -- events -------------------------------------------------------------
    def paintEvent(self, _):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.bg)

    def mousePressEvent(self, ev):
        self.origin = ev.pos()
        self.band.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.band.show()

    def mouseMoveEvent(self, ev):
        if self.band.isVisible():
            self.band.setGeometry(QtCore.QRect(self.origin, ev.pos()).normalized())

    def mouseReleaseEvent(self, ev):
        self.accept()

    # -- public -------------------------------------------------------------
    def get_crop_rect(self) -> QtCore.QRect | None:
        if self.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            r = self.band.geometry()
            if r.width() >= 10 and r.height() >= 10:
                return r.normalized()
        return None
