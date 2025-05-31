from PyQt6 import QtWidgets, QtGui, QtCore
import sys

class RectOverlay(QtWidgets.QWidget):
    """Transparent full‑screen widget to grab a rectangle."""

    def __init__(self):
        super().__init__(flags=QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.3)
        self.setGeometry(QtWidgets.QApplication.primaryScreen().geometry())
        self.origin = None
        self.rect = QtCore.QRect()
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

    def exec_(self):
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        self.showFullScreen()
        result = app.exec()
        return self._rect_tuple() if result == 0 else None

    def _rect_tuple(self):
        r = self.rect.normalized()
        return (r.x(), r.y(), r.width(), r.height()) if r.width() and r.height() else None

    # Event handlers
    def mousePressEvent(self, ev):
        self.origin = ev.pos()
        self.rect = QtCore.QRect(self.origin, QtCore.QSize())

    def mouseMoveEvent(self, ev):
        if self.origin:
            self.rect = QtCore.QRect(self.origin, ev.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, ev):
        self.close()  # triggers app.exec() exit

    def paintEvent(self, ev):
        if self.rect and self.rect.width() and self.rect.height():
            painter = QtGui.QPainter(self)
            pen = QtGui.QPen(QtGui.QColor("red"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
