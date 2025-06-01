import sys, time, tempfile, pathlib
import mss
from PIL import Image
from PyQt6 import QtCore, QtGui, QtWidgets

from overlay import CropDialog

OUT_DIR = pathlib.Path(tempfile.gettempdir()) / "alex_reader"
OUT_DIR.mkdir(exist_ok=True)


class SowaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(windowTitle="🦉 Sówka – Screen Grab")
        self.setFixedSize(260, 80)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)

        lab = QtWidgets.QLabel("Focus here →\nCtrl + Shift + R = capture", self)
        lab.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(lab)

        shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+R"), self)
        shortcut.activated.connect(self.capture_full)

    def capture_full(self):
        with mss.mss() as sct:
            raw = sct.grab(sct.monitors[0])
        Image.frombytes("RGB", raw.size, raw.rgb).save(
            OUT_DIR / f"cap-{int(time.time()*1000)}.png" )
        print("🦉  Full-screen PNG zapisany.")

    def capture(self):
        with mss.mss() as sct:
            raw = sct.grab(sct.monitors[0])
        full = Image.frombytes("RGB", raw.size, raw.rgb)

        dlg = CropDialog(full)
        rect = dlg.get_crop_rect()
        if rect is None:
            return

        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        full.crop((x, y, x + w, y + h)).save(
            OUT_DIR / f"cap-{int(time.time()*1000)}.png"
        )
        QtWidgets.QMessageBox.information(
            self, "Sówka",
            f"PNG {w}×{h}px zapisany w:\n{OUT_DIR}",
            QtWidgets.QMessageBox.StandardButton.Ok
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    win = SowaWindow()
    win.show()

    print("🦉  Kliknij okno Sówki, potem Ctrl+Shift+R.  Zamknij okno by wyjść.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
