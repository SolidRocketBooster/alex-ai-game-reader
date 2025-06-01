import sys, time, tempfile, requests, json, pathlib
import mss
from PIL import Image
from PyQt6 import QtCore, QtGui, QtWidgets
from tqdm import tqdm
from overlay import CropDialog

OUT_DIR = pathlib.Path(tempfile.gettempdir()) / "alex_reader"
OUT_DIR.mkdir(exist_ok=True)


class SowaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(windowTitle="Alex AI Reader")
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
        path = OUT_DIR / f"cap-{int(time.time()*1000)}.png"
        Image.frombytes("RGB", raw.size, raw.rgb).save(path)
        print("🦉  Full-screen PNG saved.")
        self.send_to_api(path)

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
            self, "alex-ai-reader",
            f"PNG {w}×{h}px saced:\n{OUT_DIR}",
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    def send_to_api(self, png: pathlib.Path):
        """Sends PNG to http://192.168.0.55:8080/read and return OCR."""
        url = "http://192.168.0.55:8080/read"
        try:
            with png.open("rb") as fh:
                files = {"img": (png.name, fh, "image/png")}
                with requests.post(url, files=files, stream=True) as resp:
                    resp.raise_for_status()
                    # jeśli odpowiedź jest spora, pokaż progress bar
                    total = int(resp.headers.get("Content-Length", 0))
                    data = resp.iter_content(chunk_size=8192)
                    body = b"".join(tqdm(data, total=total//8192 or None, unit="chunk"))
            result = json.loads(body)
            print("\n——— OCR result ———")
            for r in result.get("results", []):
                print(f"{r['text']!r}  (p={r['prob']:.2f})")
        except requests.RequestException as e:
            print("[!] HTTP error:", e)
        except json.JSONDecodeError:
            print("[!] Wrong JSON from server:", body[:200])

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)   # zamknięcie okna → koniec

    win = SowaWindow()
    win.show()

    print("Click window then Ctrl+Shift+R. Close window to quit")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
