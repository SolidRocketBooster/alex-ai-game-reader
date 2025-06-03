import sys, time, tempfile, requests, json, pathlib, io
import mss
from PIL import Image
from PyQt6 import QtCore, QtGui, QtWidgets
from tqdm import tqdm
from overlay import CropDialog
from pydub import AudioSegment
from pydub.playback import play
from pydub import AudioSegment
import simpleaudio as sa

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
        print("Full-screen PNG saved.")
        self.send_and_play(path)

    def play_audio(self, seg: AudioSegment):  # +++
        play_obj = sa.play_buffer(
            seg.raw_data,
            num_channels=seg.channels,
            bytes_per_sample=seg.sample_width,
            sample_rate=seg.frame_rate
        )
        play_obj.wait_done()

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

    def send_and_play(self, png_path: pathlib.Path, lang="pl"):
        with png_path.open("rb") as fh:
            resp = requests.post(
                "http://192.168.0.55:8080/speak",
                files={"img": (png_path.name, fh)},
                data={"lang": lang},
                timeout=120,
            )

        if resp.ok:
            audio = AudioSegment.from_file(io.BytesIO(resp.content), format="wav")
            self.play_audio(audio) 
        else:
            print("TTS error:", resp.text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    win = SowaWindow()
    win.show()

    print("Click window then Ctrl+Shift+R. Close window to quit")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
