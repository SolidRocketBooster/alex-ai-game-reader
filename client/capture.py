import time, tempfile, pathlib, keyboard
import dxcam
from PIL import Image
from overlay import RectOverlay

HOTKEY = "ctrl+shift+r"
OUTPUT_DIR = pathlib.Path(tempfile.gettempdir()) / "alex_reader"
OUTPUT_DIR.mkdir(exist_ok=True)
cam = dxcam.create(output_idx=0, output_color="BGRA")

def capture_rect():
    overlay = RectOverlay()
    rect = overlay.exec_()
    if rect is None:
        return
    x, y, w, h = rect
    frame = cam.grab(region=(x, y, x + w, y + h))
    if frame is None:
        print("[capture] No frame")
        return
    # BGRA numpy -> RGB PIL
    img = Image.fromarray(frame[..., :3][..., ::-1])
    ts = int(time.time() * 1000)
    path = OUTPUT_DIR / f"cap-{ts}.png"
    img.save(path)
    print(f"[capture] Saved {path}")

keyboard.add_hotkey(HOTKEY, capture_rect)
print(f"[capture] Ready. Press {HOTKEY}. Esc to quit.")
keyboard.wait("esc")
